import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import PlanDocsTestComponent from '@/components/PlanDocsTestComponent.vue'
import { userStore } from '@/stores/userStore'

// Mock the user store
vi.mock('@/stores/userStore', () => ({
  userStore: {
    getters: {
      isLoggedIn: vi.fn(() => true),
      currentUser: vi.fn(() => ({ id: 1, name: 'Test User', email: 'test@example.com' })),
      currentUserRole: vi.fn(() => 2),
      roleName: vi.fn(() => 'Design Head')
    },
    actions: {
      hasRole: vi.fn((roleId) => roleId === 2),
      hasRoleName: vi.fn((roleName) => roleName === 'Design Head'),
      login: vi.fn(),
      logout: vi.fn()
    }
  }
}))

// Mock router
const mockRouter = {
  push: vi.fn()
}

describe('PlanDocsTestComponent.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
    
    wrapper = mount(PlanDocsTestComponent, {
      global: {
        mocks: {
          $router: mockRouter,
          $forceUpdate: vi.fn()
        }
      }
    })
  })

  it('renders correctly', () => {
    expect(wrapper.find('.plan-docs-test').exists()).toBe(true)
    expect(wrapper.find('h2').text()).toContain('Plan Documents Global User Store Test')
  })

  it('displays user store integration status', () => {
    expect(wrapper.find('.test-section').exists()).toBe(true)
    expect(wrapper.text()).toContain('global user store is working correctly')
  })

  it('computes login status from store', () => {
    expect(wrapper.vm.isLoggedIn).toBe(true)
  })

  it('computes current user from store', () => {
    const user = wrapper.vm.currentUser
    expect(user).toEqual({
      id: 1,
      name: 'Test User',
      email: 'test@example.com'
    })
  })

  it('computes current user role from store', () => {
    expect(wrapper.vm.currentUserRole).toBe(2)
  })

  it('computes role name from store', () => {
    expect(wrapper.vm.roleName).toBe('Design Head')
  })

  it('computes canUpload correctly for Design Head', () => {
    expect(wrapper.vm.canUpload).toBe(true)
  })

  it('computes canUpload correctly for Designer', () => {
    userStore.getters.roleName.mockReturnValue('Designer')
    
    const wrapper2 = mount(PlanDocsTestComponent, {
      global: {
        mocks: {
          $router: mockRouter,
          $forceUpdate: vi.fn()
        }
      }
    })
    
    expect(wrapper2.vm.canUpload).toBe(true)
  })

  it('computes canUpload correctly for other roles', () => {
    userStore.getters.roleName.mockReturnValue('Reviewer')
    
    const wrapper2 = mount(PlanDocsTestComponent, {
      global: {
        mocks: {
          $router: mockRouter,
          $forceUpdate: vi.fn()
        }
      }
    })
    
    expect(wrapper2.vm.canUpload).toBe(false)
  })

  it('computes isQAHead correctly', () => {
    userStore.getters.roleName.mockReturnValue('QA Head')
    
    const wrapper2 = mount(PlanDocsTestComponent, {
      global: {
        mocks: {
          $router: mockRouter,
          $forceUpdate: vi.fn()
        }
      }
    })
    
    expect(wrapper2.vm.isQAHead).toBe(true)
  })

  it('computes isDesignHead correctly', () => {
    expect(wrapper.vm.isDesignHead).toBe(true)
  })

  it('computes isDesigner correctly', () => {
    userStore.getters.roleName.mockReturnValue('Designer')
    
    const wrapper2 = mount(PlanDocsTestComponent, {
      global: {
        mocks: {
          $router: mockRouter,
          $forceUpdate: vi.fn()
        }
      }
    })
    
    expect(wrapper2.vm.isDesigner).toBe(true)
  })

  it('computes isAdmin correctly', () => {
    userStore.getters.roleName.mockReturnValue('Admin')
    
    const wrapper2 = mount(PlanDocsTestComponent, {
      global: {
        mocks: {
          $router: mockRouter,
          $forceUpdate: vi.fn()
        }
      }
    })
    
    expect(wrapper2.vm.isAdmin).toBe(true)
  })

  it('refreshes data when refreshData is called', async () => {
    const forceUpdateSpy = vi.spyOn(wrapper.vm, '$forceUpdate')
    
    await wrapper.vm.refreshData()
    
    expect(forceUpdateSpy).toHaveBeenCalled()
  })

  it('navigates to projects dashboard', async () => {
    await wrapper.vm.goToProjects()
    
    expect(mockRouter.push).toHaveBeenCalledWith({ name: 'ProjectsDashboard' })
  })

  it('navigates to LRU dashboard with parameters', async () => {
    await wrapper.vm.goToLRUs()
    
    expect(mockRouter.push).toHaveBeenCalledWith({
      name: 'LruDashboard',
      params: {
        projectId: 1,
        projectName: 'Test Project'
      }
    })
  })

  it('displays action buttons', () => {
    const buttons = wrapper.findAll('.btn')
    expect(buttons).toHaveLength(3)
    
    const buttonTexts = buttons.map(btn => btn.text())
    expect(buttonTexts).toContain('Refresh Data')
    expect(buttonTexts).toContain('Go to Projects Dashboard')
    expect(buttonTexts).toContain('Go to LRU Dashboard')
  })

  it('handles click events on buttons', async () => {
    const refreshSpy = vi.spyOn(wrapper.vm, 'refreshData')
    const projectsSpy = vi.spyOn(wrapper.vm, 'goToProjects')
    const lruSpy = vi.spyOn(wrapper.vm, 'goToLRUs')
    
    const buttons = wrapper.findAll('.btn')
    
    await buttons[0].trigger('click') // Refresh Data
    expect(refreshSpy).toHaveBeenCalled()
    
    await buttons[1].trigger('click') // Go to Projects Dashboard
    expect(projectsSpy).toHaveBeenCalled()
    
    await buttons[2].trigger('click') // Go to LRU Dashboard
    expect(lruSpy).toHaveBeenCalled()
  })

  it('displays user information correctly', () => {
    const userInfo = wrapper.find('.user-info')
    expect(userInfo.exists()).toBe(true)
    
    // Check if user data is displayed
    expect(wrapper.text()).toContain('Test User')
    expect(wrapper.text()).toContain('Design Head')
  })

  it('shows role-based permissions correctly', () => {
    expect(wrapper.text()).toContain('Can Upload')
    expect(wrapper.text()).toContain('Design Head')
  })

  it('handles store updates reactively', async () => {
    // Change user role in store
    userStore.getters.roleName.mockReturnValue('QA Head')
    userStore.getters.currentUserRole.mockReturnValue(3)
    
    // Force component update
    await wrapper.vm.refreshData()
    await wrapper.vm.$nextTick()
    
    // Should reflect new role
    expect(wrapper.vm.roleName).toBe('QA Head')
    expect(wrapper.vm.currentUserRole).toBe(3)
  })

  it('maintains component name correctly', () => {
    expect(wrapper.vm.$options.name).toBe('PlanDocsTestComponent')
  })

  it('demonstrates global store integration', () => {
    // This component specifically tests that global user store works
    expect(wrapper.vm.isLoggedIn).toBeDefined()
    expect(wrapper.vm.currentUser).toBeDefined()
    expect(wrapper.vm.currentUserRole).toBeDefined()
    expect(wrapper.vm.roleName).toBeDefined()
    
    // All these values should come from the global store
    expect(userStore.getters.isLoggedIn).toHaveBeenCalled()
    expect(userStore.getters.currentUser).toHaveBeenCalled()
    expect(userStore.getters.currentUserRole).toHaveBeenCalled()
    expect(userStore.getters.roleName).toHaveBeenCalled()
  })
})
