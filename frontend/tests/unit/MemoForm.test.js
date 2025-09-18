import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import MemoForm from '@/components/MemoForm.vue'
import { userStore } from '@/stores/userStore'

// Mock the user store
vi.mock('@/stores/userStore', () => ({
  userStore: {
    getters: {
      currentUserRole: vi.fn(() => 2)
    }
  }
}))

// Mock route
const mockRoute = {
  params: {
    memoId: 'MEMO001'
  }
}

describe('MemoForm.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
    
    wrapper = mount(MemoForm, {
      global: {
        mocks: {
          $route: mockRoute
        }
      }
    })
  })

  it('renders correctly', () => {
    expect(wrapper.find('.qa-head-memo-form').exists()).toBe(true)
  })

  it('initializes with memo ID from route', () => {
    expect(wrapper.vm.memoId).toBe('MEMO001')
  })

  it('initializes with default memo data', () => {
    expect(wrapper.vm.memoData).toHaveProperty('status', 'Not Assigned')
  })

  it('initializes form overlays as hidden', () => {
    expect(wrapper.vm.showAcceptOverlay).toBe(false)
    expect(wrapper.vm.showRejectOverlay).toBe(false)
  })

  it('initializes additional sections as hidden', () => {
    expect(wrapper.vm.showTestReviewSection).toBe(false)
    expect(wrapper.vm.showRejectionSection).toBe(false)
  })

  it('computes canApproveMemo correctly for QA Head', () => {
    expect(wrapper.vm.canApproveMemo).toBe(true)
  })

  it('computes canApproveMemo correctly for non-QA Head', async () => {
    // Mock different user role
    userStore.getters.currentUserRole.mockReturnValue(1)
    
    const wrapper2 = mount(MemoForm, {
      global: {
        mocks: {
          $route: mockRoute
        }
      }
    })
    
    expect(wrapper2.vm.canApproveMemo).toBe(false)
  })

  it('shows accept overlay when showAcceptForm is called', async () => {
    await wrapper.vm.showAcceptForm()
    
    expect(wrapper.vm.showAcceptOverlay).toBe(true)
    expect(wrapper.vm.showTestReviewSection).toBe(true)
  })

  it('hides accept overlay when hideAcceptOverlay is called', async () => {
    await wrapper.setData({ showAcceptOverlay: true })
    await wrapper.vm.hideAcceptOverlay()
    
    expect(wrapper.vm.showAcceptOverlay).toBe(false)
  })

  it('shows reject overlay when showRejectForm is called', async () => {
    await wrapper.vm.showRejectForm()
    
    expect(wrapper.vm.showRejectOverlay).toBe(true)
    expect(wrapper.vm.showRejectionSection).toBe(true)
  })

  it('hides reject overlay when hideRejectOverlay is called', async () => {
    await wrapper.setData({ showRejectOverlay: true })
    await wrapper.vm.hideRejectOverlay()
    
    expect(wrapper.vm.showRejectOverlay).toBe(false)
  })

  it('initializes accept form data with correct structure', () => {
    const acceptForm = wrapper.vm.acceptFormData
    
    expect(acceptForm).toHaveProperty('testDate', '')
    expect(acceptForm).toHaveProperty('testerId', '')
    expect(acceptForm).toHaveProperty('testerName', '')
    expect(acceptForm).toHaveProperty('comments', '')
    expect(acceptForm).toHaveProperty('authentication', '')
    expect(acceptForm).toHaveProperty('attachments')
    expect(Array.isArray(acceptForm.attachments)).toBe(true)
  })

  it('initializes reject form data with correct structure', () => {
    const rejectForm = wrapper.vm.rejectionFormData
    
    expect(rejectForm).toHaveProperty('section', 'comments')
    expect(rejectForm).toHaveProperty('comments', '')
    expect(rejectForm).toHaveProperty('authentication', '')
    expect(rejectForm).toHaveProperty('attachments')
    expect(Array.isArray(rejectForm.attachments)).toBe(true)
  })

  it('initializes comprehensive form data structure', () => {
    const formData = wrapper.vm.formData
    
    // Check key form fields
    expect(formData).toHaveProperty('from', '')
    expect(formData).toHaveProperty('casdicRef', '')
    expect(formData).toHaveProperty('partNo', '')
    expect(formData).toHaveProperty('manufacturer', '')
    expect(formData).toHaveProperty('testStatus', '')
    
    // Check boolean fields
    expect(formData).toHaveProperty('lruReady', false)
    expect(formData).toHaveProperty('unitsNoted', false)
    expect(formData).toHaveProperty('cert1', false)
    expect(formData).toHaveProperty('cert6', false)
  })

  it('handles file attachments for accept form', async () => {
    const mockFile = new File(['test'], 'test.pdf', { type: 'application/pdf' })
    
    await wrapper.vm.handleAcceptAttachment({ target: { files: [mockFile] } })
    
    expect(wrapper.vm.acceptFormData.attachments).toContain(mockFile)
  })

  it('handles file attachments for reject form', async () => {
    const mockFile = new File(['test'], 'test.pdf', { type: 'application/pdf' })
    
    await wrapper.vm.handleRejectAttachment({ target: { files: [mockFile] } })
    
    expect(wrapper.vm.rejectionFormData.attachments).toContain(mockFile)
  })

  it('removes accept form attachments', async () => {
    const mockFile = new File(['test'], 'test.pdf', { type: 'application/pdf' })
    await wrapper.setData({
      acceptFormData: {
        ...wrapper.vm.acceptFormData,
        attachments: [mockFile]
      }
    })
    
    await wrapper.vm.removeAcceptAttachment(0)
    
    expect(wrapper.vm.acceptFormData.attachments).toHaveLength(0)
  })

  it('removes reject form attachments', async () => {
    const mockFile = new File(['test'], 'test.pdf', { type: 'application/pdf' })
    await wrapper.setData({
      rejectionFormData: {
        ...wrapper.vm.rejectionFormData,
        attachments: [mockFile]
      }
    })
    
    await wrapper.vm.removeRejectAttachment(0)
    
    expect(wrapper.vm.rejectionFormData.attachments).toHaveLength(0)
  })

  it('submits accept form with proper data', async () => {
    const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {})
    
    await wrapper.setData({
      acceptFormData: {
        testDate: '2025-01-01',
        testerId: 'T001',
        testerName: 'John Doe',
        comments: 'Test passed',
        authentication: 'AUTH123',
        attachments: []
      }
    })
    
    await wrapper.vm.submitAcceptForm()
    
    expect(consoleSpy).toHaveBeenCalledWith('Accept form submitted:', expect.any(Object))
    
    consoleSpy.mockRestore()
  })

  it('submits reject form with proper data', async () => {
    const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {})
    
    await wrapper.setData({
      rejectionFormData: {
        section: 'quality',
        comments: 'Quality issues found',
        authentication: 'AUTH456',
        attachments: []
      }
    })
    
    await wrapper.vm.submitRejectForm()
    
    expect(consoleSpy).toHaveBeenCalledWith('Reject form submitted:', expect.any(Object))
    
    consoleSpy.mockRestore()
  })

  it('gets current user role from store', () => {
    expect(wrapper.vm.currentUserRole).toBe(2)
  })
})
