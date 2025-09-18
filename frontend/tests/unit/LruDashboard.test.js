import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import LruDashboard from '@/components/LruDashboard.vue'
import { userStore } from '@/stores/userStore'

// Mock the user store
vi.mock('@/stores/userStore', () => ({
  userStore: {
    getters: {
      currentUserRole: vi.fn(() => 2),
      roleName: vi.fn(() => 'QA Head')
    }
  }
}))

// Mock router
const mockRoute = {
  params: {
    projectId: '1',
    projectName: 'Test Project'
  }
}

// Mock fetch globally
global.fetch = vi.fn()

describe('LruDashboard.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
    
    // Mock successful API response
    fetch.mockResolvedValue({
      json: () => Promise.resolve({
        success: true,
        lrus: [
          { id: 1, name: 'LRU Alpha', status: 'CLEARED' },
          { id: 2, name: 'LRU Beta', status: 'DISAPPROVED' },
          { id: 3, name: 'LRU Gamma', status: 'NOT CLEARED' }
        ]
      })
    })

    wrapper = mount(LruDashboard, {
      global: {
        mocks: {
          $route: mockRoute
        }
      }
    })
  })

  it('renders correctly with LRU data', async () => {
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.lru-dashboard').exists()).toBe(true)
    expect(wrapper.find('.page-title h1').text()).toBe('Test Project')
  })

  it('initializes with route parameters', () => {
    expect(wrapper.vm.projectId).toBe(1)
    expect(wrapper.vm.projectName).toBe('Test Project')
  })

  it('displays all predefined statuses', () => {
    const expectedStatuses = ['CLEARED', 'DISAPPROVED', 'ASSIGNED & RETURNED', 'MOVED TO NEXT STAGE', 'NOT CLEARED']
    const componentStatuses = wrapper.vm.statuses.map(s => s.name)
    
    expectedStatuses.forEach(status => {
      expect(componentStatuses).toContain(status)
    })
  })

  it('filters LRUs by status', async () => {
    await wrapper.setData({
      lrus: [
        { id: 1, name: 'LRU Alpha', status: 'CLEARED' },
        { id: 2, name: 'LRU Beta', status: 'DISAPPROVED' },
        { id: 3, name: 'LRU Gamma', status: 'CLEARED' }
      ],
      loading: false
    })

    // Filter by CLEARED status
    await wrapper.setData({ activeStatusFilter: 'CLEARED' })
    
    expect(wrapper.vm.filteredLrus).toHaveLength(2)
    expect(wrapper.vm.filteredLrus.every(lru => lru.status === 'CLEARED')).toBe(true)
  })

  it('filters LRUs by search query', async () => {
    await wrapper.setData({
      lrus: [
        { id: 1, name: 'LRU Alpha', status: 'CLEARED' },
        { id: 2, name: 'LRU Beta', status: 'DISAPPROVED' },
        { id: 3, name: 'LRU Gamma', status: 'NOT CLEARED' }
      ],
      loading: false
    })

    // Search for 'Alpha'
    await wrapper.setData({ searchQuery: 'Alpha' })
    
    expect(wrapper.vm.filteredLrus).toHaveLength(1)
    expect(wrapper.vm.filteredLrus[0].name).toBe('LRU Alpha')
  })

  it('combines status and search filters', async () => {
    await wrapper.setData({
      lrus: [
        { id: 1, name: 'Alpha Test', status: 'CLEARED' },
        { id: 2, name: 'Beta Test', status: 'CLEARED' },
        { id: 3, name: 'Alpha Unit', status: 'DISAPPROVED' }
      ],
      loading: false
    })

    // Filter by status and search
    await wrapper.setData({ 
      activeStatusFilter: 'CLEARED',
      searchQuery: 'Alpha'
    })
    
    expect(wrapper.vm.filteredLrus).toHaveLength(1)
    expect(wrapper.vm.filteredLrus[0]).toEqual({
      id: 1, 
      name: 'Alpha Test', 
      status: 'CLEARED'
    })
  })

  it('handles missing project ID gracefully', () => {
    const wrapperNoProject = mount(LruDashboard, {
      global: {
        mocks: {
          $route: { params: {} }
        }
      }
    })

    expect(wrapperNoProject.vm.error).toBe('Project ID not found')
    expect(wrapperNoProject.vm.loading).toBe(false)
  })

  it('toggles status filter visibility', async () => {
    expect(wrapper.vm.showStatusFilter).toBe(false)
    
    // Simulate toggle
    await wrapper.setData({ showStatusFilter: true })
    expect(wrapper.vm.showStatusFilter).toBe(true)
  })

  it('computes user role from store', () => {
    expect(wrapper.vm.currentUserRole).toBe(2)
    expect(wrapper.vm.roleName).toBe('QA Head')
  })

  it('handles API errors when fetching LRUs', async () => {
    fetch.mockRejectedValue(new Error('Network error'))
    
    const errorWrapper = mount(LruDashboard, {
      global: {
        mocks: {
          $route: mockRoute
        }
      }
    })

    await errorWrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 10))

    expect(errorWrapper.vm.error).toContain('Failed to fetch LRUs')
    expect(errorWrapper.vm.loading).toBe(false)
  })

  it('returns all LRUs when no filters applied', async () => {
    const lrus = [
      { id: 1, name: 'LRU Alpha', status: 'CLEARED' },
      { id: 2, name: 'LRU Beta', status: 'DISAPPROVED' }
    ]
    
    await wrapper.setData({ 
      lrus,
      activeStatusFilter: null,
      searchQuery: ''
    })
    
    expect(wrapper.vm.filteredLrus).toEqual(lrus)
  })
})
