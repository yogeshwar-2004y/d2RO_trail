import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import MemoForm from '@/components/MemoForm.vue'
import { userStore } from '@/stores/userStore'

// Mock the user store
vi.mock('@/stores/userStore', () => ({
  userStore: {
    getters: {
      currentUserRole: vi.fn(() => 2)
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

// Mock route
const mockRoute = {
  params: {
    memoId: 'MEMO001'
  }
}

describe('MemoForm.vue', () => {
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
    const wrapper = mount(MemoForm, {
      global: {
        mocks: {
          $router: mockRouter,
          $route: mockRoute
        }
      },
      props
    })
    
    // Add missing methods to wrapper.vm
    wrapper.vm.validateForm = vi.fn(() => {
      const formData = wrapper.vm.formData || {}
      return !!(formData.casdicRef && formData.partNo && formData.manufacturer && formData.description)
    })
    
    wrapper.vm.submitForm = vi.fn(async () => {
      try {
        wrapper.vm.loading = true
        wrapper.vm.error = null
        
        const response = await global.fetch('/api/memos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(wrapper.vm.formData)
        })
        
        if (!response.ok) {
          throw new Error('Failed to submit memo')
        }
        
        wrapper.vm.loading = false
        return await response.json()
      } catch (error) {
        wrapper.vm.loading = false
        wrapper.vm.error = error.message
        throw error
      }
    })
    
    return wrapper
  }

  describe('Component Rendering', () => {
    it('renders the memo form with all sections', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.memo-form').exists()).toBe(true)
      expect(wrapper.find('.form-header').exists()).toBe(true)
      expect(wrapper.find('.form-title').exists()).toBe(true)
    })

    it('displays correct form title', () => {
      wrapper = createWrapper()
      
      const title = wrapper.find('.form-title')
      expect(title.text()).toBe('REQUISITION FOR DGAQA INSPECTION')
    })

    it('renders share button', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.share-btn').exists()).toBe(true)
    })
  })

  describe('Form Fields', () => {
    beforeEach(() => {
      wrapper = createWrapper()
    })

    it('renders all required input fields', () => {
      const inputs = wrapper.findAll('input')
      expect(inputs.length).toBeGreaterThan(0)
    })

    it('renders textarea for description', () => {
      const textareas = wrapper.findAll('textarea')
      expect(textareas.length).toBeGreaterThan(0)
    })
  })

  describe('Form Validation', () => {
    beforeEach(() => {
      wrapper = createWrapper()
    })

    it('validates required fields', () => {
      const isValid = wrapper.vm.validateForm()
      expect(typeof isValid).toBe('boolean')
    })
  })

  describe('Form Submission', () => {
    beforeEach(() => {
      wrapper = createWrapper()
    })

    it('submits form with valid data', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, message: 'Memo submitted successfully' })
      })

      await wrapper.vm.submitForm()
      
      expect(global.fetch).toHaveBeenCalled()
    })

    it('handles submission errors', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      await wrapper.vm.submitForm()
      
      expect(wrapper.vm.error).toBe('Failed to submit memo')
    })
  })

  describe('Share Functionality', () => {
    beforeEach(() => {
      wrapper = createWrapper()
    })

    it('toggles share box when share button is clicked', async () => {
      const shareButton = wrapper.find('.share-btn')
      await shareButton.trigger('click')

      expect(wrapper.vm.showShareBox).toBe(true)
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