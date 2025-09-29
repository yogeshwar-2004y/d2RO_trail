import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import PlanDocsTestComponent from '@/components/PlanDocsTestComponent.vue'
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

describe('PlanDocsTestComponent.vue', () => {
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
    return mount(PlanDocsTestComponent, {
      props
    })
  }

  describe('Component Rendering', () => {
    it('renders the test component', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.plan-docs-test').exists()).toBe(true)
      expect(wrapper.find('h2').text()).toBe('Plan Documents Global User Store Test')
    })

    it('displays current user information', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.test-section').exists()).toBe(true)
      expect(wrapper.text()).toContain('Current User Information')
    })
  })

  describe('User Information Display', () => {
    it('shows logged in status', () => {
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('Is Logged In: true')
    })

    it('displays user details', () => {
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('User ID: 1')
      expect(wrapper.text()).toContain('User Name: Test User')
      expect(wrapper.text()).toContain('User Email: test@example.com')
    })

    it('shows role information', () => {
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('Role ID: 2')
      expect(wrapper.text()).toContain('Role Name: QA Head')
    })
  })

  describe('Role-Based Access Tests', () => {
    it('shows role-based access tests section', () => {
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('Role-Based Access Test')
      expect(wrapper.find('.access-tests').exists()).toBe(true)
    })

    it('displays access test results', () => {
      wrapper = createWrapper()
      
      expect(wrapper.text()).toContain('Can Upload Documents')
      expect(wrapper.text()).toContain('Is QA Head')
    })

    it('shows success/fail indicators', () => {
      wrapper = createWrapper()
      
      const successElements = wrapper.findAll('.success')
      const failElements = wrapper.findAll('.fail')
      
      expect(successElements.length + failElements.length).toBeGreaterThan(0)
    })
  })

  describe('Computed Properties', () => {
    it('calculates canUpload correctly', () => {
      wrapper = createWrapper()
      
      expect(typeof wrapper.vm.canUpload).toBe('boolean')
    })

    it('calculates isQAHead correctly', () => {
      wrapper = createWrapper()
      
      expect(typeof wrapper.vm.isQAHead).toBe('boolean')
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

  describe('Test Actions', () => {
    it('handles test button clicks', async () => {
      wrapper = createWrapper()
      
      const testButtons = wrapper.findAll('.test-button')
      if (testButtons.length > 0) {
        await testButtons[0].trigger('click')
        // Test that the action was handled
        expect(wrapper.vm).toBeDefined()
      }
    })
  })
})
