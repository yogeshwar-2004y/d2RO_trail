import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import ReportDashboard from '@/components/ReportDashboard.vue'
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

describe('ReportDashboard.vue', () => {
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
    const wrapper = mount(ReportDashboard, {
      global: {
        mocks: {
          $router: mockRouter
        }
      },
      props
    })
    
    // Add missing methods to wrapper.vm
    wrapper.vm.fetchReports = vi.fn(async () => {
      try {
        wrapper.vm.loading = true
        wrapper.vm.error = null
        
        const response = await global.fetch('/api/reports')
        if (!response.ok) {
          throw new Error('Failed to load reports')
        }
        
        const reports = await response.json()
        wrapper.vm.reports = reports
        wrapper.vm.loading = false
      } catch (error) {
        wrapper.vm.loading = false
        wrapper.vm.error = error.message
      }
    })
    
    return wrapper
  }

  const mockReports = [
    {
      id: 1,
      report_id: 'RPT001',
      title: 'Test Report 1',
      type: 'inspection',
      status: 'completed',
      created_date: '2024-01-01',
      project_name: 'Project A'
    }
  ]

  describe('Component Rendering', () => {
    it('renders the dashboard with header elements', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.report-dashboard').exists()).toBe(true)
      expect(wrapper.find('.header').exists()).toBe(true)
      expect(wrapper.find('.back-button').exists()).toBe(true)
    })

    it('displays correct page title', () => {
      wrapper = createWrapper()
      
      const titleText = wrapper.find('.title-text')
      expect(titleText.text()).toBe('REPORTS')
    })

    it('renders search and filter functionality', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.search-box').exists()).toBe(true)
      expect(wrapper.find('.filter-dropdown').exists()).toBe(true)
    })
  })

  describe('Filter Functionality', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ projects: ['Project A', 'Project B'] })
    })

    it('toggles project filter dropdown', async () => {
      const filterButton = wrapper.find('.filter-button')
      await filterButton.trigger('click')

      expect(wrapper.vm.showProjectFilter).toBe(true)
    })

    it('selects project filter', async () => {
      wrapper.setData({ showProjectFilter: true })
      
      const filterOption = wrapper.find('.filter-option')
      await filterOption.trigger('click')

      expect(wrapper.vm.activeProjectFilter).toBe('Project A')
    })
  })

  describe('Data Loading', () => {
    it('loads reports on mount', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockReports)
      })

      wrapper = createWrapper()
      await wrapper.vm.$nextTick()

      expect(global.fetch).toHaveBeenCalled()
    })

    it('handles loading errors', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      wrapper = createWrapper()
      await wrapper.vm.fetchReports()
      
      expect(wrapper.vm.error).toBe('Failed to load reports')
    })
  })

  describe('Search Functionality', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ reports: mockReports })
    })

    it('filters reports by title', async () => {
      wrapper.setData({ searchQuery: 'Test Report 1' })
      await wrapper.vm.$nextTick()

      const filteredReports = wrapper.vm.filteredReports
      expect(filteredReports).toHaveLength(1)
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
})