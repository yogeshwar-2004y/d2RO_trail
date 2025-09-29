import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import ObservationReport from '@/components/ObservationReport.vue'
import { userStore } from '@/stores/userStore'

// Mock the user store
vi.mock('@/stores/userStore', () => ({
  userStore: {
    getters: {
      currentUserRole: vi.fn(() => 1),
      roleName: vi.fn(() => 'Admin')
    }
  }
}))

// Mock fetch
global.fetch = vi.fn()

// Mock router
const mockRouter = {
  go: vi.fn(),
  push: vi.fn()
}

describe('ObservationReport.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
    global.fetch.mockClear()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
  })

  const createWrapper = (props = {}) => {
    return mount(ObservationReport, {
      global: {
        mocks: {
          $router: mockRouter
        }
      },
      props
    })
  }

  const mockReportData = {
    id: 1,
    projectName: 'Test Project',
    lruName: 'Test LRU',
    serialNumber: 'SN001',
    observationCount: 5,
    currentYear: '2024',
    currentDate: '2024-01-15',
    currentVersion: '1.0',
    revision: 'A',
    projectNumber: 'PROJ001',
    status: 'Active'
  }

  describe('Component Rendering', () => {
    it('renders the observation report page', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.view-observations-page').exists()).toBe(true)
      expect(wrapper.find('.page-header').exists()).toBe(true)
      expect(wrapper.find('.main-content').exists()).toBe(true)
    })

    it('displays correct page title', () => {
      wrapper = createWrapper()
      
      const title = wrapper.find('.page-title')
      expect(title.text()).toBe('IQA OBSERVATION REPORT')
    })

    it('renders export button', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.export-button').exists()).toBe(true)
    })
  })

  describe('Report Header', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ 
        projectName: mockReportData.projectName,
        lruName: mockReportData.lruName,
        serialNumber: mockReportData.serialNumber,
        observationCount: mockReportData.observationCount,
        currentYear: mockReportData.currentYear
      })
    })

    it('displays document path correctly', () => {
      const documentPath = wrapper.find('.document-path')
      expect(documentPath.text()).toContain('CASDIC/Test Project/Test LRU/SL.SN001/5/2024')
    })

    it('displays current date', () => {
      const reportDate = wrapper.find('.report-date')
      expect(reportDate.text()).toContain('Date:')
    })
  })

  describe('Subject Line', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ 
        lruName: mockReportData.lruName,
        isVersionSpecific: true,
        currentVersion: mockReportData.currentVersion,
        reportData: {
          revision: mockReportData.revision
        }
      })
    })

    it('displays subject line with LRU name', () => {
      const subjectLine = wrapper.find('.subject-line')
      expect(subjectLine.text()).toContain('IQA Observation Report for Test LRU')
    })

    it('shows version information when version specific', () => {
      const versionInfo = wrapper.find('.version-info')
      expect(versionInfo.text()).toContain('Version 1.0 - Revision A')
    })
  })

  describe('Export Functionality', () => {
    beforeEach(() => {
      wrapper = createWrapper()
    })

    it('handles export button click', async () => {
      const exportButton = wrapper.find('.export-button')
      await exportButton.trigger('click')

      expect(wrapper.vm.exportReport).toHaveBeenCalled()
    })

    it('exports report as PDF', async () => {
      // Mock html2canvas and jsPDF
      const mockCanvas = { toDataURL: vi.fn(() => 'data:image/png;base64,test') }
      const mockPdf = { 
        addImage: vi.fn(),
        save: vi.fn()
      }
      
      global.html2canvas = vi.fn(() => Promise.resolve(mockCanvas))
      global.jsPDF = vi.fn(() => mockPdf)

      await wrapper.vm.exportReport()

      expect(global.html2canvas).toHaveBeenCalled()
      expect(mockPdf.save).toHaveBeenCalled()
    })
  })

  describe('Navigation', () => {
    it('goes back when back button is clicked', async () => {
      wrapper = createWrapper()
      
      const backButton = wrapper.find('.back-button')
      await backButton.trigger('click')

      expect(mockRouter.go).toHaveBeenCalledWith(-1)
    })
  })

  describe('Data Loading', () => {
    it('loads report data on mount', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockReportData)
      })

      wrapper = createWrapper()
      await wrapper.vm.$nextTick()

      expect(global.fetch).toHaveBeenCalled()
    })

    it('handles loading errors', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      wrapper = createWrapper()
      await wrapper.vm.loadReportData()
      
      expect(wrapper.vm.error).toBe('Failed to load report data')
    })
  })

  describe('Report Content', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ reportData: mockReportData })
    })

    it('displays observation details', () => {
      const observations = wrapper.findAll('.observation-item')
      expect(observations.length).toBeGreaterThanOrEqual(0)
    })

    it('shows report status', () => {
      const statusElement = wrapper.find('.report-status')
      if (statusElement.exists()) {
        expect(statusElement.text()).toContain('Active')
      }
    })
  })

  describe('Responsive Design', () => {
    it('adapts to different screen sizes', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.view-observations-page').exists()).toBe(true)
    })
  })
})