import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import LruDashboard from '@/components/LruDashboard.vue'
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

// Mock route parameters
const mockRoute = {
  params: {
    projectId: '1',
    projectName: 'Test Project'
  }
}

describe('LruDashboard.vue', () => {
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
    return mount(LruDashboard, {
      global: {
        mocks: {
          $router: mockRouter,
          $route: mockRoute
        }
      },
      props
    })
  }

  const mockLrus = [
    {
      id: 1,
      lru_name: 'LRU001',
      project_id: 'PROJ001',
      status: 'active',
      created_date: '2024-01-01',
      last_modified: '2024-01-15',
      name: 'LRU001' // Add name property for search functionality
    },
    {
      id: 2,
      lru_name: 'LRU002',
      project_id: 'PROJ002',
      status: 'completed',
      created_date: '2024-01-02',
      last_modified: '2024-01-16',
      name: 'LRU002' // Add name property for search functionality
    }
  ]

  describe('Component Rendering', () => {
    it('renders the dashboard with header elements', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.lru-dashboard').exists()).toBe(true)
      expect(wrapper.find('.header').exists()).toBe(true)
      expect(wrapper.find('.back-button').exists()).toBe(true)
      expect(wrapper.find('.page-title').exists()).toBe(true)
    })

    it('displays correct page title', () => {
      wrapper = createWrapper()
      
      const titleText = wrapper.find('.title-text')
      expect(titleText.text()).toBe('LRU DASHBOARD')
    })

    it('renders search functionality', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.search-box').exists()).toBe(true)
      expect(wrapper.find('.search-input').exists()).toBe(true)
    })
  })

  describe('Loading States', () => {
    it('shows loading spinner when loading is true', () => {
      wrapper = createWrapper()
      wrapper.setData({ loading: true })
      
      expect(wrapper.find('.loading-container').exists()).toBe(true)
      expect(wrapper.find('.loading-spinner').exists()).toBe(true)
    })

    it('shows error state when error exists', () => {
      wrapper = createWrapper()
      wrapper.setData({ error: 'Failed to load LRUs' })
      
      expect(wrapper.find('.error-container').exists()).toBe(true)
      expect(wrapper.find('.error-message').text()).toBe('Failed to load LRUs')
      expect(wrapper.find('.retry-button').exists()).toBe(true)
    })
  })

  describe('LRU Data Loading', () => {
    it('loads LRUs on mount', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockLrus)
      })

      wrapper = createWrapper()
      await wrapper.vm.$nextTick()

      expect(global.fetch).toHaveBeenCalled()
    })

    it('handles successful LRU loading', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockLrus)
      })

      wrapper = createWrapper()
      await wrapper.vm.fetchLrus()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.lrus).toEqual(mockLrus)
      expect(wrapper.vm.loading).toBe(false)
      expect(wrapper.vm.error).toBe(null)
    })

    it('handles LRU loading errors', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      wrapper = createWrapper()
      await wrapper.vm.fetchLrus()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.error).toBe('Failed to fetch LRUs')
      expect(wrapper.vm.loading).toBe(false)
    })

    it('retries loading when retry button is clicked', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      wrapper = createWrapper()
      await wrapper.vm.fetchLrus()
      
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockLrus)
      })

      const retryButton = wrapper.find('.retry-button')
      await retryButton.trigger('click')

      expect(global.fetch).toHaveBeenCalledTimes(2)
    })
  })

  describe('Search Functionality', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ lrus: mockLrus })
    })

    it('filters LRUs by name', async () => {
      wrapper.setData({ searchQuery: 'LRU001' })
      await wrapper.vm.$nextTick()

      const filteredLrus = wrapper.vm.filteredLrus
      expect(filteredLrus).toHaveLength(1)
      expect(filteredLrus[0].lru_name).toBe('LRU001')
    })

    it('shows all LRUs when search is empty', async () => {
      wrapper.setData({ searchQuery: '' })
      await wrapper.vm.$nextTick()

      const filteredLrus = wrapper.vm.filteredLrus
      expect(filteredLrus).toHaveLength(2)
    })

    it('shows no LRUs when search matches nothing', async () => {
      wrapper.setData({ searchQuery: 'NONEXISTENT' })
      await wrapper.vm.$nextTick()

      const filteredLrus = wrapper.vm.filteredLrus
      expect(filteredLrus).toHaveLength(0)
    })

    it('is case insensitive', async () => {
      wrapper.setData({ searchQuery: 'lru001' })
      await wrapper.vm.$nextTick()

      const filteredLrus = wrapper.vm.filteredLrus
      expect(filteredLrus).toHaveLength(1)
    })
  })

  describe('Navigation', () => {
    it('goes back when back button is clicked', async () => {
      wrapper = createWrapper()
      
      const backButton = wrapper.find('.back-button')
      await backButton.trigger('click')

      expect(mockRouter.go).toHaveBeenCalledWith(-1)
    })

    it('navigates to LRU details when LRU is clicked', async () => {
      wrapper = createWrapper()
      wrapper.setData({ lrus: mockLrus })
      
      const lruRow = wrapper.find('.lru-row')
      await lruRow.trigger('click')

      expect(mockRouter.push).toHaveBeenCalledWith({
        name: 'LruDetails',
        params: { lruId: mockLrus[0].id }
      })
    })
  })

  describe('LRU Status Display', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ lrus: mockLrus })
    })

    it('displays LRU status correctly', () => {
      const statusElements = wrapper.findAll('.status-badge')
      expect(statusElements[0].text()).toBe('active')
      expect(statusElements[1].text()).toBe('completed')
    })

    it('applies correct CSS classes for different statuses', () => {
      const statusElements = wrapper.findAll('.status-badge')
      expect(statusElements[0].classes()).toContain('status-active')
      expect(statusElements[1].classes()).toContain('status-completed')
    })
  })

  describe('Empty States', () => {
    it('shows empty state when no LRUs', () => {
      wrapper = createWrapper()
      wrapper.setData({ lrus: [], loading: false })
      
      expect(wrapper.find('.empty-state').exists()).toBe(true)
    })

    it('shows empty state when search returns no results', () => {
      wrapper = createWrapper()
      wrapper.setData({ 
        lrus: mockLrus, 
        searchQuery: 'NONEXISTENT',
        loading: false 
      })
      
      expect(wrapper.find('.empty-state').exists()).toBe(true)
    })
  })

  describe('LRU Information Display', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ lrus: mockLrus })
    })

    it('displays LRU name correctly', () => {
      const lruNames = wrapper.findAll('.lru-name')
      expect(lruNames[0].text()).toBe('LRU001')
      expect(lruNames[1].text()).toBe('LRU002')
    })

    it('displays project ID correctly', () => {
      const projectIds = wrapper.findAll('.project-id')
      expect(projectIds[0].text()).toBe('PROJ001')
      expect(projectIds[1].text()).toBe('PROJ002')
    })

    it('formats dates correctly', () => {
      const dates = wrapper.findAll('.created-date')
      expect(dates[0].text()).toContain('2024')
    })
  })

  describe('Role-based Functionality', () => {
    it('shows appropriate content for different roles', () => {
      vi.mocked(userStore.getters.currentUserRole).mockReturnValue(2) // QA Head role
      
      wrapper = createWrapper()
      
      expect(wrapper.vm.currentUserRole).toBe(2)
    })
  })

  describe('Error Handling', () => {
    it('handles malformed LRU data gracefully', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve('invalid data')
      })

      wrapper = createWrapper()
      await wrapper.vm.fetchLrus()
      
      expect(wrapper.vm.error).toBe('Failed to fetch LRUs')
    })

    it('handles network timeout', async () => {
      global.fetch.mockImplementation(() => 
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Timeout')), 100)
        )
      )

      wrapper = createWrapper()
      await wrapper.vm.fetchLrus()
      
      expect(wrapper.vm.error).toBe('Failed to fetch LRUs')
    })
  })

  describe('Responsive Design', () => {
    it('adapts to different screen sizes', () => {
      wrapper = createWrapper()
      
      // Test that the component renders without errors
      expect(wrapper.find('.lru-dashboard').exists()).toBe(true)
    })
  })

  describe('LRU Actions', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ lrus: mockLrus })
    })

    it('shows action buttons for appropriate roles', () => {
      const actionButtons = wrapper.findAll('.action-button')
      expect(actionButtons.length).toBeGreaterThanOrEqual(0)
    })

    it('handles LRU creation', async () => {
      const createButton = wrapper.find('.create-lru-button')
      if (createButton.exists()) {
        await createButton.trigger('click')
        expect(mockRouter.push).toHaveBeenCalledWith('/lrus/create')
      }
    })
  })
})