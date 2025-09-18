import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ProjectsDashboard from '@/components/ProjectsDashboard.vue'
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

// Mock router
const mockRouter = {
  push: vi.fn()
}

// Mock fetch globally
global.fetch = vi.fn()

describe('ProjectsDashboard.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
    
    // Mock successful API response
    fetch.mockResolvedValue({
      json: () => Promise.resolve({
        success: true,
        projects: [
          { id: 1, name: 'Project Alpha' },
          { id: 2, name: 'Project Beta' },
          { id: 3, name: 'Project Gamma' }
        ]
      })
    })

    wrapper = mount(ProjectsDashboard, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
  })

  it('renders correctly with project data', async () => {
    // Wait for component to mount and fetch data
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 10))

    expect(wrapper.find('.projects-dashboard').exists()).toBe(true)
    expect(wrapper.find('.page-title h1').text()).toBe('Project Dashboard')
  })

  it('displays loading state initially', () => {
    expect(wrapper.vm.loading).toBe(true)
  })

  it('fetches projects on mount', () => {
    expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/projects')
  })

  it('filters projects based on search query', async () => {
    // Set up projects data
    await wrapper.setData({
      projects: [
        { id: 1, name: 'Project Alpha' },
        { id: 2, name: 'Project Beta' },
        { id: 3, name: 'Project Gamma' }
      ],
      loading: false
    })

    // Test search functionality
    await wrapper.setData({ searchQuery: '1' })
    expect(wrapper.vm.filteredProjects).toHaveLength(1)
    expect(wrapper.vm.filteredProjects[0].id).toBe(1)
  })

  it('navigates to LRU dashboard when viewing a project', async () => {
    const testProject = { id: 1, name: 'Test Project' }
    
    await wrapper.vm.viewProject(testProject)
    
    expect(mockRouter.push).toHaveBeenCalledWith({
      name: 'LruDashboard',
      params: { projectId: 1, projectName: 'Test Project' }
    })
  })

  it('handles API errors gracefully', async () => {
    fetch.mockRejectedValue(new Error('Network error'))
    
    const wrapper2 = mount(ProjectsDashboard, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })

    await wrapper2.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 10))

    expect(wrapper2.vm.error).toContain('Failed to connect to server')
    expect(wrapper2.vm.loading).toBe(false)
  })

  it('handles API response errors', async () => {
    fetch.mockResolvedValue({
      json: () => Promise.resolve({
        success: false,
        message: 'Server error'
      })
    })

    const wrapper2 = mount(ProjectsDashboard, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })

    await wrapper2.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 10))

    expect(wrapper2.vm.error).toBe('Server error')
  })

  it('computes user role correctly', () => {
    expect(wrapper.vm.currentUserRole).toBe(1)
    expect(wrapper.vm.roleName).toBe('Admin')
  })

  it('returns all projects when search query is empty', async () => {
    const projects = [
      { id: 1, name: 'Project Alpha' },
      { id: 2, name: 'Project Beta' }
    ]
    
    await wrapper.setData({ projects, searchQuery: '' })
    
    expect(wrapper.vm.filteredProjects).toEqual(projects)
  })
})
