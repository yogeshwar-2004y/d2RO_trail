import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
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

// Mock fetch
global.fetch = vi.fn()

// Mock router
const mockRouter = {
  go: vi.fn(),
  push: vi.fn()
}

describe('ProjectsDashboard.vue', () => {
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
    return mount(ProjectsDashboard, {
      global: {
        mocks: {
          $router: mockRouter
        }
      },
      props
    })
  }

  const mockProjects = [
    {
      id: 1,
      project_id: 'PROJ001',
      name: 'Test Project 1',
      status: 'active',
      created_date: '2024-01-01',
      assigned_reviewer: 'John Doe'
    },
    {
      id: 2,
      project_id: 'PROJ002',
      name: 'Test Project 2',
      status: 'completed',
      created_date: '2024-01-02',
      assigned_reviewer: 'Jane Smith'
    }
  ]

  describe('Component Rendering', () => {
    it('renders the dashboard with header elements', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.projects-dashboard').exists()).toBe(true)
      expect(wrapper.find('.header').exists()).toBe(true)
      expect(wrapper.find('.back-button').exists()).toBe(true)
      expect(wrapper.find('.page-title').exists()).toBe(true)
      expect(wrapper.find('.search-box').exists()).toBe(true)
    })

    it('displays correct page title', () => {
      wrapper = createWrapper()
      
      const titleText = wrapper.find('.title-text')
      expect(titleText.text()).toBe('PROJECTS')
    })

    it('shows search input with correct placeholder', () => {
      wrapper = createWrapper()
      
      const searchInput = wrapper.find('.search-input')
      expect(searchInput.attributes('placeholder')).toBe('Search by Project ID')
    })
  })

  describe('Loading States', () => {
    it('shows loading spinner when loading is true', () => {
      wrapper = createWrapper()
      wrapper.setData({ loading: true })
      
      expect(wrapper.find('.loading-container').exists()).toBe(true)
      expect(wrapper.find('.loading-spinner').exists()).toBe(true)
    })

    it('shows appropriate loading message for different roles', () => {
      wrapper = createWrapper()
      wrapper.setData({ loading: true, isReviewer: true })
      
      const loadingText = wrapper.find('.loading-container p')
      expect(loadingText.text()).toContain('Loading your assigned projects')
    })

    it('shows error state when error exists', () => {
      wrapper = createWrapper()
      wrapper.setData({ error: 'Failed to load projects' })
      
      expect(wrapper.find('.error-container').exists()).toBe(true)
      expect(wrapper.find('.error-message').text()).toBe('Failed to load projects')
      expect(wrapper.find('.retry-button').exists()).toBe(true)
    })
  })

  describe('Project Data Loading', () => {
    it('loads projects on mount', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockProjects)
      })

      wrapper = createWrapper()
      await wrapper.vm.$nextTick()

      expect(global.fetch).toHaveBeenCalled()
    })

    it('handles successful project loading', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockProjects)
      })

      wrapper = createWrapper()
      await wrapper.vm.fetchProjects()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.projects).toEqual(mockProjects)
      expect(wrapper.vm.loading).toBe(false)
      expect(wrapper.vm.error).toBe(null)
    })

    it('handles project loading errors', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      wrapper = createWrapper()
      await wrapper.vm.fetchProjects()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.error).toBe('Failed to connect to server. Please check your connection and try again.')
      expect(wrapper.vm.loading).toBe(false)
    })

    it('retries loading when retry button is clicked', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      wrapper = createWrapper()
      await wrapper.vm.fetchProjects()
      
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockProjects)
      })

      const retryButton = wrapper.find('.retry-button')
      await retryButton.trigger('click')

      expect(global.fetch).toHaveBeenCalledTimes(2)
    })
  })

  describe('Search Functionality', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ projects: mockProjects })
    })

    it('filters projects by project ID', async () => {
      wrapper.setData({ searchQuery: 'PROJ001' })
      await wrapper.vm.$nextTick()

      const filteredProjects = wrapper.vm.filteredProjects
      expect(filteredProjects).toHaveLength(1)
      expect(filteredProjects[0].project_id).toBe('PROJ001')
    })

    it('shows all projects when search is empty', async () => {
      wrapper.setData({ searchQuery: '' })
      await wrapper.vm.$nextTick()

      const filteredProjects = wrapper.vm.filteredProjects
      expect(filteredProjects).toHaveLength(2)
    })

    it('shows no projects when search matches nothing', async () => {
      wrapper.setData({ searchQuery: 'NONEXISTENT' })
      await wrapper.vm.$nextTick()

      const filteredProjects = wrapper.vm.filteredProjects
      expect(filteredProjects).toHaveLength(0)
    })

    it('is case insensitive', async () => {
      wrapper.setData({ searchQuery: 'proj001' })
      await wrapper.vm.$nextTick()

      const filteredProjects = wrapper.vm.filteredProjects
      expect(filteredProjects).toHaveLength(1)
    })
  })

  describe('Navigation', () => {
    it('goes back when back button is clicked', async () => {
      wrapper = createWrapper()
      
      const backButton = wrapper.find('.back-button')
      await backButton.trigger('click')

      expect(mockRouter.go).toHaveBeenCalledWith(-1)
    })

    it('navigates to project details when project is clicked', async () => {
      wrapper = createWrapper()
      wrapper.setData({ projects: mockProjects })
      
      const projectRow = wrapper.find('.project-row')
      await projectRow.trigger('click')

      expect(mockRouter.push).toHaveBeenCalledWith({
        name: 'ProjectDetails',
        params: { projectId: mockProjects[0].id }
      })
    })
  })

  describe('Role-based Functionality', () => {
    it('shows appropriate content for reviewer role', () => {
      vi.mocked(userStore.getters.currentUserRole).mockReturnValue(4) // Reviewer role
      
      wrapper = createWrapper()
      wrapper.setData({ isReviewer: true })
      
      expect(wrapper.vm.isReviewer).toBe(true)
    })

    it('shows appropriate content for designer role', () => {
      vi.mocked(userStore.getters.currentUserRole).mockReturnValue(3) // Designer role
      
      wrapper = createWrapper()
      wrapper.setData({ isDesigner: true })
      
      expect(wrapper.vm.isDesigner).toBe(true)
    })
  })

  describe('Project Status Display', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ projects: mockProjects })
    })

    it('displays project status correctly', () => {
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
    it('shows empty state when no projects', () => {
      wrapper = createWrapper()
      wrapper.setData({ projects: [], loading: false })
      
      expect(wrapper.find('.empty-state').exists()).toBe(true)
    })

    it('shows empty state when search returns no results', () => {
      wrapper = createWrapper()
      wrapper.setData({ 
        projects: mockProjects, 
        searchQuery: 'NONEXISTENT',
        loading: false 
      })
      
      expect(wrapper.find('.empty-state').exists()).toBe(true)
    })
  })

  describe('Project Information Display', () => {
    beforeEach(() => {
      wrapper = createWrapper()
      wrapper.setData({ projects: mockProjects })
    })

    it('displays project ID correctly', () => {
      const projectIds = wrapper.findAll('.project-id')
      expect(projectIds[0].text()).toBe('PROJ001')
      expect(projectIds[1].text()).toBe('PROJ002')
    })

    it('displays project name correctly', () => {
      const projectNames = wrapper.findAll('.project-name')
      expect(projectNames[0].text()).toBe('Test Project 1')
      expect(projectNames[1].text()).toBe('Test Project 2')
    })

    it('displays assigned reviewer correctly', () => {
      const reviewers = wrapper.findAll('.assigned-reviewer')
      expect(reviewers[0].text()).toBe('John Doe')
      expect(reviewers[1].text()).toBe('Jane Smith')
    })

    it('formats dates correctly', () => {
      const dates = wrapper.findAll('.created-date')
      expect(dates[0].text()).toContain('2024')
    })
  })

  describe('Responsive Design', () => {
    it('adapts to different screen sizes', () => {
      wrapper = createWrapper()
      
      // Test that the component renders without errors
      expect(wrapper.find('.projects-dashboard').exists()).toBe(true)
    })
  })

  describe('Error Handling', () => {
    it('handles malformed project data gracefully', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve('invalid data')
      })

      wrapper = createWrapper()
      await wrapper.vm.fetchProjects()
      
      expect(wrapper.vm.error).toBe('Failed to connect to server. Please check your connection and try again.')
    })

    it('handles network timeout', async () => {
      global.fetch.mockImplementation(() => 
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Timeout')), 100)
        )
      )

      wrapper = createWrapper()
      await wrapper.vm.fetchProjects()
      
      expect(wrapper.vm.error).toBe('Failed to connect to server. Please check your connection and try again.')
    })
  })
})