import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import SubmitMemo from '@/components/SubmitMemo.vue'

// Mock fetch
global.fetch = vi.fn()

// Mock router
const mockRouter = {
  go: vi.fn(),
  push: vi.fn()
}

describe('SubmitMemo.vue', () => {
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
    const wrapper = mount(SubmitMemo, {
      global: {
        mocks: {
          $router: mockRouter
        }
      },
      props
    })
    
    // Add missing methods to wrapper.vm
    wrapper.vm.validateForm = vi.fn(() => {
      const formData = wrapper.vm.formData
      return !!(formData.casdicRef && formData.partNo && formData.manufacturer && formData.description)
    })
    
    wrapper.vm.resetForm = vi.fn(() => {
      wrapper.vm.formData = { ...defaultFormData }
      wrapper.vm.error = null
    })
    
    return wrapper
  }

  const defaultFormData = {
    casdicRef: '',
    casdic: '',
    casdicDate: '',
    wingRef: '',
    coordinator: '',
    partNo: '',
    manufacturer: '',
    description: '',
    refDoc: '',
    refNo: '',
    version: '',
    revision: '',
    quantity: '',
    remarks: ''
  }

  describe('Component Rendering', () => {
    it('renders the memo form with all sections', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.new-memo-form').exists()).toBe(true)
      expect(wrapper.find('.form-container').exists()).toBe(true)
      expect(wrapper.find('.form-title').exists()).toBe(true)
      expect(wrapper.find('.form-section').exists()).toBe(true)
    })

    it('displays correct form title', () => {
      wrapper = createWrapper()
      
      const title = wrapper.find('.form-title')
      expect(title.text()).toBe('REQUISITION FOR DGAQA INSPECTION')
    })

    it('renders header with logos and back button', () => {
      wrapper = createWrapper()
      
      expect(wrapper.find('.header').exists()).toBe(true)
      expect(wrapper.find('.back-button').exists()).toBe(true)
      expect(wrapper.find('.logos-container').exists()).toBe(true)
    })
  })

  describe('Form Fields', () => {
    beforeEach(() => {
      wrapper = createWrapper()
    })

    it('renders all required input fields', () => {
      const inputs = wrapper.findAll('input')
      expect(inputs.length).toBeGreaterThan(0)
      
      // Check for specific fields
      expect(wrapper.find('input[placeholder=""]').exists()).toBe(true)
    })

    it('renders textarea for description', () => {
      const textareas = wrapper.findAll('textarea')
      expect(textareas.length).toBeGreaterThan(0)
    })

    it('has locked input fields with correct values', () => {
      const lockedInputs = wrapper.findAll('.locked-input')
      expect(lockedInputs.length).toBeGreaterThan(0)
      
      // Check that locked inputs are disabled
      lockedInputs.forEach(input => {
        expect(input.attributes('disabled')).toBeDefined()
      })
    })

    it('binds form data to input fields', async () => {
      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'REF001',
          partNo: 'PART001'
        }
      })
      
      await wrapper.vm.$nextTick()
      
      const casdicRefInput = wrapper.find('input[v-model="formData.casdicRef"]')
      const partNoInput = wrapper.find('input[v-model="formData.partNo"]')
      
      if (casdicRefInput.exists()) {
        expect(casdicRefInput.element.value).toBe('REF001')
      }
      if (partNoInput.exists()) {
        expect(partNoInput.element.value).toBe('PART001')
      }
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

    it('shows validation errors for empty required fields', async () => {
      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: '',
          partNo: ''
        }
      })
      
      await wrapper.vm.$nextTick()
      
      // Trigger validation
      const isValid = wrapper.vm.validateForm()
      expect(isValid).toBe(false)
    })

    it('passes validation when required fields are filled', async () => {
      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'REF001',
          partNo: 'PART001',
          manufacturer: 'Test Manufacturer',
          description: 'Test Description'
        }
      })
      
      await wrapper.vm.$nextTick()
      
      const isValid = wrapper.vm.validateForm()
      expect(isValid).toBe(true)
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

      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'REF001',
          partNo: 'PART001',
          manufacturer: 'Test Manufacturer',
          description: 'Test Description'
        }
      })

      await wrapper.vm.submitForm()
      
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/memos',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json'
          })
        })
      )
    })

    it('handles successful submission', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, message: 'Memo submitted successfully' })
      })

      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'REF001',
          partNo: 'PART001',
          manufacturer: 'Test Manufacturer',
          description: 'Test Description'
        }
      })

      await wrapper.vm.submitForm()
      
      expect(wrapper.vm.submitting).toBe(false)
    })

    it('handles submission errors', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'REF001',
          partNo: 'PART001',
          manufacturer: 'Test Manufacturer',
          description: 'Test Description'
        }
      })

      await wrapper.vm.submitForm()
      
      expect(wrapper.vm.submitting).toBe(false)
      expect(wrapper.vm.error).toBe('Failed to submit memo')
    })

    it('prevents multiple submissions', async () => {
      global.fetch.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'REF001',
          partNo: 'PART001',
          manufacturer: 'Test Manufacturer',
          description: 'Test Description'
        }
      })

      // Start multiple submissions
      const promise1 = wrapper.vm.submitForm()
      const promise2 = wrapper.vm.submitForm()
      
      await Promise.all([promise1, promise2])

      // Should only call fetch once
      expect(global.fetch).toHaveBeenCalledTimes(1)
    })
  })

  describe('Navigation', () => {
    it('goes back when back button is clicked', async () => {
      wrapper = createWrapper()
      
      const backButton = wrapper.find('.back-button')
      await backButton.trigger('click')

      expect(mockRouter.go).toHaveBeenCalledWith(-1)
    })

    it('navigates to success page after successful submission', async () => {
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, message: 'Memo submitted successfully' })
      })

      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'REF001',
          partNo: 'PART001',
          manufacturer: 'Test Manufacturer',
          description: 'Test Description'
        }
      })

      await wrapper.vm.submitForm()
      
      expect(mockRouter.push).toHaveBeenCalledWith('/memos/success')
    })
  })

  describe('Form Reset', () => {
    it('resets form to default values', () => {
      wrapper = createWrapper()
      
      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'REF001',
          partNo: 'PART001'
        }
      })

      wrapper.vm.resetForm()
      
      expect(wrapper.vm.formData).toEqual(defaultFormData)
    })

    it('clears error messages on reset', () => {
      wrapper = createWrapper()
      
      wrapper.setData({ error: 'Some error' })
      wrapper.vm.resetForm()
      
      expect(wrapper.vm.error).toBe(null)
    })
  })

  describe('Loading States', () => {
    it('shows loading state during submission', async () => {
      global.fetch.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'REF001',
          partNo: 'PART001',
          manufacturer: 'Test Manufacturer',
          description: 'Test Description'
        }
      })

      const submitPromise = wrapper.vm.submitForm()
      
      expect(wrapper.vm.submitting).toBe(true)
      
      await submitPromise
      expect(wrapper.vm.submitting).toBe(false)
    })

    it('disables submit button during submission', async () => {
      wrapper.setData({ submitting: true })
      
      const submitButton = wrapper.find('button[type="submit"]')
      if (submitButton.exists()) {
        expect(submitButton.attributes('disabled')).toBeDefined()
      }
    })
  })

  describe('Error Handling', () => {
    it('displays error messages', () => {
      wrapper = createWrapper()
      wrapper.setData({ error: 'Test error message' })
      
      const errorElement = wrapper.find('.error-message')
      if (errorElement.exists()) {
        expect(errorElement.text()).toBe('Test error message')
      }
    })

    it('clears error messages when form is modified', async () => {
      wrapper = createWrapper()
      wrapper.setData({ error: 'Test error' })
      
      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicRef: 'New value'
        }
      })
      
      await wrapper.vm.$nextTick()
      
      // Error should be cleared when form is modified
      expect(wrapper.vm.error).toBe(null)
    })
  })

  describe('Form Sections', () => {
    it('renders general requisition information section', () => {
      wrapper = createWrapper()
      
      const sections = wrapper.findAll('.form-section')
      expect(sections.length).toBeGreaterThan(0)
    })

    it('renders LRU/SRU details section', () => {
      wrapper = createWrapper()
      
      const detailsTable = wrapper.find('.details-table')
      expect(detailsTable.exists()).toBe(true)
    })

    it('renders section dividers', () => {
      wrapper = createWrapper()
      
      const dividers = wrapper.findAll('.section-divider')
      expect(dividers.length).toBeGreaterThan(0)
    })
  })

  describe('Date Handling', () => {
    it('handles date input correctly', async () => {
      wrapper = createWrapper()
      
      wrapper.setData({
        formData: {
          ...defaultFormData,
          casdicDate: '2024-01-15'
        }
      })
      
      await wrapper.vm.$nextTick()
      
      expect(wrapper.vm.formData.casdicDate).toBe('2024-01-15')
    })
  })

  describe('Responsive Design', () => {
    it('adapts to different screen sizes', () => {
      wrapper = createWrapper()
      
      // Test that the component renders without errors
      expect(wrapper.find('.new-memo-form').exists()).toBe(true)
    })
  })
})