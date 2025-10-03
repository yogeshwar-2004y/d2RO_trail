import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import RoleTestComponent from '@/components/RoleTestComponent.vue'
import { userStore } from '@/stores/userStore'

// Mock the user store
vi.mock('@/stores/userStore', () => ({
  userStore: {
    getters: {
      isLoggedIn: vi.fn(() => true),
      currentUser: vi.fn(() => ({
        id: 1,
        name: 'Test User',
        email: 'test@example.com'
      })),
      currentUserRole: vi.fn(() => 2),
      roleName: vi.fn(() => 'QA Head')
    }
  }
}))

describe('RoleTestComponent.vue', () => {
  let wrapper

  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
  })

  const createWrapper = (props = {}) => {
    return mount(RoleTestComponent, {
      props
    })
  }

  describe('Component Rendering', () => {
    it('renders the role test component', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.role-test-component').exists()).toBe(true)
      expect(wrapper.find('h2').text()).toBe('Global Role System Test')
    })

    it('displays user information when logged in', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.user-info').exists()).toBe(true)
      expect(wrapper.text()).toContain('Current User Information')
    })
  })

  describe('User Information Display', () => {
    it('shows user details', () => {
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('Name: Test User')
      expect(wrapper.text()).toContain('Email: test@example.com')
      expect(wrapper.text()).toContain('Role ID: 2')
      expect(wrapper.text()).toContain('Role Name: QA Head')
    })
  })

  describe('Role-based Access Checks', () => {
    it('shows role checks section', () => {
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('Role-based Access Checks')
      expect(wrapper.find('.role-checks').exists()).toBe(true)
    })

    it('displays role check items', () => {
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('Admin (Role ID: 1)')
      expect(wrapper.text()).toContain('QA Head (Role ID: 2)')
      expect(wrapper.text()).toContain('QA Reviewer (Role ID: 3)')
    })

    it('shows access results', () => {
      wrapper = createWrapper()
      
      const accessResults = wrapper.findAll('.check-result')
      expect(accessResults.length).toBeGreaterThan(0)
      
      accessResults.forEach(result => {
        expect(result.text()).toMatch(/✅ Access|❌ No Access/)
      })
    })
  })

  describe('hasRole Method', () => {
    it('checks role access correctly', () => {
      wrapper = createWrapper()
      
      expect(typeof wrapper.vm.hasRole(1)).toBe('boolean')
      expect(typeof wrapper.vm.hasRole(2)).toBe('boolean')
      expect(typeof wrapper.vm.hasRole(3)).toBe('boolean')
    })

    it('returns true for current user role', () => {
      wrapper = createWrapper()
      
      expect(wrapper.vm.hasRole(2)).toBe(true)
    })
  })

  describe('Computed Properties', () => {
    it('calculates isLoggedIn correctly', () => {
      wrapper = createWrapper()
      
      expect(wrapper.vm.isLoggedIn).toBe(true)
    })

    it('gets current user data', () => {
      wrapper = createWrapper()
      
      expect(wrapper.vm.currentUser).toEqual({
        id: 1,
        name: 'Test User',
        email: 'test@example.com'
      })
    })

    it('gets current user role', () => {
      wrapper = createWrapper()
      
      expect(wrapper.vm.currentUserRole).toBe(2)
    })

    it('gets role name', () => {
      wrapper = createWrapper()
      
      expect(wrapper.vm.roleName).toBe('QA Head')
    })
  })

  describe('User Store Integration', () => {
    it('uses user store getters', () => {
      wrapper = createWrapper()
      
      expect(userStore.getters.isLoggedIn).toHaveBeenCalled()
      expect(userStore.getters.currentUser).toHaveBeenCalled()
      expect(userStore.getters.currentUserRole).toHaveBeenCalled()
      expect(userStore.getters.roleName).toHaveBeenCalled()
    })
  })

  describe('Role Check Items', () => {
    it('applies correct CSS classes based on access', () => {
      wrapper = createWrapper()
      
      const checkItems = wrapper.findAll('.check-item')
      checkItems.forEach(item => {
        expect(item.classes()).toContain('has-access')
      })
    })
  })

  describe('Edge Cases', () => {
    it('handles undefined user data', () => {
      vi.mocked(userStore.getters.currentUser).mockReturnValue(undefined)
      
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('Name: N/A')
      expect(wrapper.text()).toContain('Email: N/A')
    })

    it('handles null role data', () => {
      vi.mocked(userStore.getters.currentUserRole).mockReturnValue(null)
      
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('Role ID: N/A')
    })
  })
})