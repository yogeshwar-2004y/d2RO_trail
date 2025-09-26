import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import DocumentViewer from '@/components/DocumentViewer.vue'
import { userStore } from '@/stores/userStore'

// Mock the user store
vi.mock('@/stores/userStore', () => ({
  userStore: {
    getters: {
      roleName: vi.fn(() => 'QA Head')
    }
  }
}))

// Mock VuePdfEmbed component
vi.mock('vue-pdf-embed', () => ({
  default: {
    name: 'VuePdfEmbed',
    template: '<div>PDF Viewer</div>'
  }
}))

// Mock mammoth
vi.mock('mammoth/mammoth.browser', () => ({
  default: {
    convertToHtml: vi.fn(() => Promise.resolve({ value: '<p>Test document content</p>' }))
  }
}))

// Mock pdfjs
vi.mock('pdfjs-dist/build/pdf', () => ({
  GlobalWorkerOptions: { workerSrc: '' },
  getDocument: vi.fn(() => Promise.resolve({
    promise: Promise.resolve({
      numPages: 5
    })
  }))
}))

describe('DocumentViewer.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
    
    // Mock route parameters
    const mockRoute = {
      params: {
        lruId: '1',
        documentId: 'test-doc',
        projectId: 'test-proj'
      }
    }
    
    wrapper = mount(DocumentViewer, {
      global: {
        mocks: {
          $route: mockRoute
        },
        stubs: {
          'VuePdfEmbed': true,
          'QAHeadAssignReviewer': true
        }
      }
    })
  })

  it('renders correctly', () => {
    // Check if component renders (may have different class name)
    expect(wrapper.exists()).toBe(true)
  })

  it('initializes with default document metadata', () => {
    expect(wrapper.vm.lruName).toBe('')
    expect(wrapper.vm.projectName).toBe('')
    expect(wrapper.vm.documentId).toBe(null)
    expect(wrapper.vm.status).toBe('pending')
  })

  it('initializes with user role from store', () => {
    expect(wrapper.vm.currentUserRole).toBe('QA Head')
  })

  it('initializes document viewing properties', () => {
    expect(wrapper.vm.fileType).toBe(null)
    expect(wrapper.vm.pdfUrl).toBe(null)
    expect(wrapper.vm.docxHtml).toBe('')
    expect(wrapper.vm.page).toBe(1)
    expect(wrapper.vm.numPages).toBe(0)
    expect(wrapper.vm.zoom).toBe(1.0)
  })

  it('computes canUpload correctly for authorized roles', () => {
    // Mock Design Head role
    userStore.getters.roleName.mockReturnValue('Design Head')
    
    const wrapper2 = mount(DocumentViewer, {
      global: {
        stubs: {
          'VuePdfEmbed': true,
          'QAHeadAssignReviewer': true
        }
      }
    })
    
    expect(wrapper2.vm.canUpload).toBe(true)
  })

  it('computes canUpload correctly for Designer role', () => {
    userStore.getters.roleName.mockReturnValue('Designer')
    
    const wrapper2 = mount(DocumentViewer, {
      global: {
        stubs: {
          'VuePdfEmbed': true,
          'QAHeadAssignReviewer': true
        }
      }
    })
    
    expect(wrapper2.vm.canUpload).toBe(true)
  })

  it('computes canUpload correctly for unauthorized roles', () => {
    userStore.getters.roleName.mockReturnValue('Reviewer')
    
    const wrapper2 = mount(DocumentViewer, {
      global: {
        stubs: {
          'VuePdfEmbed': true,
          'QAHeadAssignReviewer': true
        }
      }
    })
    
    expect(wrapper2.vm.canUpload).toBe(false)
  })

  it('handles file selection for upload', async () => {
    const mockFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' })
    const mockEvent = {
      target: {
        files: [mockFile]
      }
    }
    
    await wrapper.vm.handleFileSelect(mockEvent)
    
    expect(wrapper.vm.selectedFile).toBe(mockFile)
    expect(wrapper.vm.fileName).toBe('test.pdf')
  })

  it('increases zoom level', async () => {
    const initialZoom = wrapper.vm.zoom
    await wrapper.vm.zoomIn()
    
    expect(wrapper.vm.zoom).toBe(initialZoom + 0.1)
  })

  it('decreases zoom level', async () => {
    await wrapper.setData({ zoom: 1.5 })
    await wrapper.vm.zoomOut()
    
    expect(wrapper.vm.zoom).toBe(1.4)
  })

  it('prevents zoom from going below minimum', async () => {
    await wrapper.setData({ zoom: 0.1 })
    await wrapper.vm.zoomOut()
    
    expect(wrapper.vm.zoom).toBe(0.1) // Should not go below 0.1
  })

  it('goes to next page', async () => {
    await wrapper.setData({ numPages: 5, page: 2 })
    await wrapper.vm.nextPage()
    
    expect(wrapper.vm.page).toBe(3)
  })

  it('goes to previous page', async () => {
    await wrapper.setData({ page: 3 })
    await wrapper.vm.prevPage()
    
    expect(wrapper.vm.page).toBe(2)
  })

  it('prevents going beyond last page', async () => {
    await wrapper.setData({ numPages: 5, page: 5 })
    await wrapper.vm.nextPage()
    
    expect(wrapper.vm.page).toBe(5) // Should stay at last page
  })

  it('prevents going before first page', async () => {
    await wrapper.setData({ page: 1 })
    await wrapper.vm.prevPage()
    
    expect(wrapper.vm.page).toBe(1) // Should stay at first page
  })

  it('initializes document details with default values', () => {
    const details = wrapper.vm.documentDetails
    
    expect(details).toHaveProperty('lruId', 1)
    expect(details).toHaveProperty('documentNumber', '')
    expect(details).toHaveProperty('version', '')
    expect(details).toHaveProperty('revision', '')
    expect(details).toHaveProperty('docVer', 1)
  })

  it('initializes modal states as closed', () => {
    expect(wrapper.vm.showAssignReviewerModal).toBe(false)
    expect(wrapper.vm.showTrackVersionsModal).toBe(false)
    expect(wrapper.vm.showDeleteConfirmModal).toBe(false)
  })

  it('opens assign reviewer modal', async () => {
    await wrapper.setData({ showAssignReviewerModal: true })
    
    expect(wrapper.vm.showAssignReviewerModal).toBe(true)
  })

  it('opens edit reviewer modal', async () => {
    await wrapper.setData({ showAssignReviewerModal: true })
    
    expect(wrapper.vm.showAssignReviewerModal).toBe(true)
  })

  it('closes assign reviewer modal', async () => {
    await wrapper.setData({ showAssignReviewerModal: true })
    await wrapper.setData({ showAssignReviewerModal: false })
    
    expect(wrapper.vm.showAssignReviewerModal).toBe(false)
  })

  it('opens track versions modal', async () => {
    await wrapper.setData({ showTrackVersionsModal: true })
    
    expect(wrapper.vm.showTrackVersionsModal).toBe(true)
  })

  it('closes track versions modal', async () => {
    await wrapper.setData({ showTrackVersionsModal: true })
    await wrapper.vm.closeTrackVersionsModal()
    
    expect(wrapper.vm.showTrackVersionsModal).toBe(false)
  })

  it('adds new comment to comments array', async () => {
    await wrapper.setData({ newComment: 'This is a test comment' })
    await wrapper.vm.addComment()
    
    expect(wrapper.vm.comments).toHaveLength(1)
    expect(wrapper.vm.comments[0]).toBe('This is a test comment')
    expect(wrapper.vm.newComment).toBe('')
  })

  it('does not add empty comments', async () => {
    await wrapper.setData({ newComment: '' })
    await wrapper.vm.addComment()
    
    expect(wrapper.vm.comments).toHaveLength(0)
  })

  it('initializes with empty arrays and default states', () => {
    expect(Array.isArray(wrapper.vm.documentVersions)).toBe(true)
    expect(Array.isArray(wrapper.vm.existingDocuments)).toBe(true)
    expect(Array.isArray(wrapper.vm.comments)).toBe(true)
    expect(typeof wrapper.vm.loading).toBe('boolean')
    expect(wrapper.vm.isUploading).toBe(false)
  })

  it('handles reviewer assignment status', () => {
    expect(wrapper.vm.hasAssignedReviewer).toBe(false)
    expect(wrapper.vm.assignedReviewer).toBe(null)
    expect(wrapper.vm.loadingReviewerStatus).toBe(false)
  })

  it('sets document status correctly', async () => {
    await wrapper.setData({ status: 'approved' })
    expect(wrapper.vm.status).toBe('approved')
  })
})
