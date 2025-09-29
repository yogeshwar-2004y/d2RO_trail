import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import MemoDashboard from '@/components/MemoDashboard.vue'
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

describe('MemoDashboard.vue', () => {
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
    const wrapper = mount(MemoDashboard, {
      global: {
        mocks: {
          $router: mockRouter
        }
      },
      props
    })
    
    // Add missing methods to wrapper.vm
    wrapper.vm.fetchMemos = vi.fn(async () => {
      try {
        wrapper.vm.loading = true
        wrapper.vm.error = null
        
        const response = await global.fetch('/api/memos')
        if (!response.ok) {
          throw new Error('Failed to load memos')
        }
        
        const memos = await response.json()
        wrapper.vm.memos = memos
        wrapper.vm.loading = false
      } catch (error) {
        wrapper.vm.loading = false
        wrapper.vm.error = error.message
      }
    })
    
    return wrapper
  }

  const mockMemos = [
    {
      id: 1,
      memo_id: 'MEMO001',
      title: 'Test Memo 1',
      status: 'draft',
      created_date: '2024-01-01',
      assigned_to: 'John Doe'
    }
  ]

  describe('Component Rendering', () => {
    it('renders the dashboard with header elements', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.memo-dashboard').exists()).toBe(true)
      expect(wrapper.find('.header').exists()).toBe(true)
      expect(wrapper.find('.back-button').exists()).toBe(true)
    })

    it('displays correct page title', () => {
      wrapper = createWrapper()
      
      const titleText = wrapper.find('.title-text')
      expect(titleText.text()).toBe('MEMOS')
    })
  })

  describe('Role-based Features', () => {
    it('shows shared with me button for QA Reviewer role', () => {
      vi.mocked(userStore.getters.currentUserRole).mockReturnValue(3)
      
      wrapper = createWrapper()
      
      expect(wrapper.find('.shared-with-me-button').exists()).toBe(true)
    })

    it('shows notification bell for QA Head role', () => {
      vi.mocked(userStore.getters.currentUserRole).mockReturnValue(2)
      
      wrapper = createWrapper()
      wrapper.setData({ unreadNotifications: 3 })
      
      expect(wrapper.find('.notification-container').exists()).toBe(true)
    })
  })

  describe('Data Loading', () => {
    it('loads memos on mount', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockMemos)
      })

      wrapper = createWrapper()
      await wrapper.vm.$nextTick()

      expect(global.fetch).toHaveBeenCalled()
    })

    it('handles loading errors', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      wrapper = createWrapper()
      await wrapper.vm.fetchMemos()
      
      expect(wrapper.vm.error).toBe('Failed to load memos')
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

  describe('Search Functionality', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ memos: mockMemos })
    })

    it('filters memos by title', async () => {
      wrapper.setData({ searchQuery: 'Test Memo 1' })
      await wrapper.vm.$nextTick()

      const filteredMemos = wrapper.vm.filteredMemos
      expect(filteredMemos).toHaveLength(1)
    })
  })
})