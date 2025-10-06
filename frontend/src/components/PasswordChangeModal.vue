<template>
  <div class="modal-overlay" v-if="isOpen" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>{{ modalTitle }}</h3>
        <button class="close-btn" @click="closeModal">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label for="oldPassword">Current Password</label>
            <div class="input-wrapper">
              <input
                :type="showOldPassword ? 'text' : 'password'"
                id="oldPassword"
                v-model="formData.oldPassword"
                placeholder="Enter current password"
                required
                :disabled="loading"
              />
              <button type="button" class="toggle-password" @click="toggleOldPassword">
                <svg v-if="!showOldPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="newPassword">New Password</label>
            <div class="input-wrapper">
              <input
                :type="showNewPassword ? 'text' : 'password'"
                id="newPassword"
                v-model="formData.newPassword"
                placeholder="Enter new password"
                required
                :disabled="loading"
              />
              <button type="button" class="toggle-password" @click="toggleNewPassword">
                <svg v-if="!showNewPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">Confirm New Password</label>
            <div class="input-wrapper">
              <input
                :type="showConfirmPassword ? 'text' : 'password'"
                id="confirmPassword"
                v-model="formData.confirmPassword"
                placeholder="Re-enter new password"
                required
                :disabled="loading"
              />
              <button type="button" class="toggle-password" @click="toggleConfirmPassword">
                <svg v-if="!showConfirmPassword" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              </button>
            </div>
          </div>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
          
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
        </form>
      </div>
      
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" @click="closeModal" :disabled="loading">
          Cancel
        </button>
        <button type="button" class="btn btn-primary" @click="submitForm" :disabled="loading || !isFormValid">
          <span v-if="loading" class="loading-spinner"></span>
          {{ loading ? 'Updating...' : 'Update Password' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'PasswordChangeModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    passwordType: {
      type: String,
      default: 'login', // 'login' or 'signature'
      validator: value => ['login', 'signature'].includes(value)
    }
  },
  data() {
    return {
      formData: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      showOldPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      loading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  computed: {
    modalTitle() {
      return this.passwordType === 'login' 
        ? 'Change Login Password' 
        : 'Change Signature Password'
    },
    isFormValid() {
      return this.formData.oldPassword && 
             this.formData.newPassword && 
             this.formData.confirmPassword &&
             this.formData.newPassword === this.formData.confirmPassword
    }
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.resetForm()
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    toggleOldPassword() {
      this.showOldPassword = !this.showOldPassword
    },
    toggleNewPassword() {
      this.showNewPassword = !this.showNewPassword
    },
    toggleConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword
    },
    resetForm() {
      this.formData = {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
      this.showOldPassword = false
      this.showNewPassword = false
      this.showConfirmPassword = false
      this.errorMessage = ''
      this.successMessage = ''
      this.loading = false
    },
    async submitForm() {
      if (!this.isFormValid) {
        this.errorMessage = 'Please fill in all fields and ensure passwords match'
        return
      }
      
      if (this.formData.newPassword.length < 6) {
        this.errorMessage = 'New password must be at least 6 characters long'
        return
      }
      
      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''
      
      try {
        const currentUser = userStore.getters.currentUser()
        if (!currentUser) {
          throw new Error('User not found')
        }
        
        const response = await fetch(`http://127.0.0.1:8000/api/users/change-${this.passwordType}-password`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: currentUser.id,
            current_password: this.formData.oldPassword,
            new_password: this.formData.newPassword
          })
        })
        
        const data = await response.json()
        
        if (data.success) {
          this.successMessage = data.message
          setTimeout(() => {
            this.closeModal()
          }, 2000)
        } else {
          this.errorMessage = data.message || 'Failed to update password'
        }
      } catch (error) {
        console.error('Error updating password:', error)
        this.errorMessage = 'An error occurred while updating password'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 2000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 24px 0 24px;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  color: #6b7280;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #f3f4f6;
  color: #374151;
}

.modal-body {
  padding: 0 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper input {
  width: 100%;
  padding: 12px 16px;
  padding-right: 48px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  background-color: #fff;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input-wrapper input:disabled {
  background-color: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

.toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #6b7280;
  transition: color 0.2s ease;
}

.toggle-password:hover {
  color: #374151;
}

.error-message {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.875rem;
  margin-top: 16px;
}

.success-message {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #16a34a;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.875rem;
  margin-top: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid #e5e7eb;
  margin-top: 24px;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e5e7eb;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive design */
@media (max-width: 480px) {
  .modal-content {
    margin: 0 10px;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding-left: 16px;
    padding-right: 16px;
  }
}
</style>
