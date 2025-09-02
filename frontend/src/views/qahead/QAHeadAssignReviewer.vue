<template>
  <div class="assign-reviewer-overlay" @click="closeOverlay">
    <div class="assign-reviewer-modal" @click.stop>
      <!-- Header -->
      <div class="modal-header">
        <div class="header-content">
          <div class="header-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <h2 class="modal-title">ASSIGN REVIEWER</h2>
        </div>
        <button class="close-button" @click="closeOverlay">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Form Content -->
      <div class="modal-content">
        <form @submit.prevent="assignReviewer" class="assign-form">
          <!-- Project Details (Auto-filled) -->
          <div class="form-section">
            <h3 class="section-title">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
              Project Details
            </h3>
            <div class="form-row">
              <div class="form-group">
                <label>PROJECT NAME</label>
                <input type="text" v-model="formData.projectName" readonly class="readonly-input">
              </div>
              <div class="form-group">
                <label>PROJECT NUMBER</label>
                <input type="text" v-model="formData.projectNumber" readonly class="readonly-input">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>PROJECT DATE</label>
                <input type="text" v-model="formData.projectDate" readonly class="readonly-input">
              </div>
              <div class="form-group">
                <label>VERSION</label>
                <input type="text" v-model="formData.version" readonly class="readonly-input">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>REVISION</label>
                <input type="text" v-model="formData.revision" readonly class="readonly-input">
              </div>
            </div>
          </div>

          <!-- Reviewer Assignment -->
          <div class="form-section">
            <h3 class="section-title">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
              Reviewer Assignment
            </h3>
            <div class="form-row">
              <div class="form-group">
                <label>REVIEWER ID *</label>
                <div class="dropdown-container">
                  <select v-model="formData.reviewerId" @change="onReviewerChange" required class="form-select">
                    <option value="">Select Reviewer</option>
                    <option 
                      v-for="reviewer in availableReviewers" 
                      :key="reviewer.id" 
                      :value="reviewer.id"
                      :disabled="!reviewer.available"
                      :class="{ 'disabled-option': !reviewer.available }"
                    >
                      {{ reviewer.id }} {{ !reviewer.available ? '(Not Available)' : '' }}
                    </option>
                  </select>
                  <div class="dropdown-arrow">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="6,9 12,15 18,9"></polyline>
                    </svg>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label>REVIEWER NAME</label>
                <input type="text" v-model="formData.reviewerName" readonly class="readonly-input">
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="form-actions">
            <button type="button" @click="closeOverlay" class="btn btn-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="!formData.reviewerId">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
              ASSIGN REVIEWER
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Success Overlay -->
    <div v-if="showSuccessOverlay" class="success-overlay" @click="closeSuccessOverlay">
      <div class="success-modal" @click.stop>
        <div class="success-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        </div>
        <h3>Reviewer Assigned Successfully!</h3>
        <p>Reviewer {{ formData.reviewerName }} has been assigned to {{ formData.projectName }}</p>
        <button @click="closeSuccessOverlay" class="btn btn-success">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20,6 9,17 4,12"></polyline>
          </svg>
          OK
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QAHeadAssignReviewer',
  props: {
    lruName: {
      type: String,
      required: true
    },
    projectName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      formData: {
        projectName: '',
        projectNumber: '',
        projectDate: '',
        version: '',
        revision: '',
        reviewerId: '',
        reviewerName: ''
      },
      availableReviewers: [
        { id: 'EMP1234', name: 'John Smith', available: true },
        { id: 'EMP1235', name: 'Sarah Johnson', available: false },
        { id: 'EMP1236', name: 'Michael Brown', available: true },
        { id: 'EMP1237', name: 'Emily Davis', available: true },
        { id: 'EMP1238', name: 'David Wilson', available: false }
      ],
      showSuccessOverlay: false
    };
  },
  mounted() {
    this.initializeForm();
  },
  methods: {
    initializeForm() {
      // Auto-fill project details
      this.formData.projectName = this.projectName;
      this.formData.projectNumber = 'PRJ-2025-078'; // Sample data
      this.formData.projectDate = '2025-07-01'; // Sample data
      this.formData.version = '1.0'; // Sample data
      this.formData.revision = '0'; // Sample data
    },
    
    onReviewerChange() {
      if (this.formData.reviewerId) {
        const selectedReviewer = this.availableReviewers.find(r => r.id === this.formData.reviewerId);
        if (selectedReviewer) {
          this.formData.reviewerName = selectedReviewer.name;
        }
      } else {
        this.formData.reviewerName = '';
      }
    },
    
    assignReviewer() {
      if (!this.formData.reviewerId) {
        alert('Please select a reviewer');
        return;
      }
      
      // Here you would typically make an API call to assign the reviewer
      console.log('Assigning reviewer:', this.formData);
      
      // Show success overlay
      this.showSuccessOverlay = true;
    },
    
    closeOverlay() {
      this.$emit('close');
    },
    
    closeSuccessOverlay() {
      this.showSuccessOverlay = false;
      this.closeOverlay();
    }
  }
};
</script>

<style scoped>
.assign-reviewer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
  backdrop-filter: blur(5px);
}

.assign-reviewer-modal {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30px 40px;
  background: #2d3748;
  border-radius: 20px 20px 0 0;
  position: relative;
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-icon {
  background: rgba(255, 255, 255, 0.1);
  padding: 12px;
  border-radius: 12px;
  color: white;
}

.modal-title {
  margin: 0;
  font-size: 2em;
  font-weight: 700;
  color: white;
  text-align: center;
  letter-spacing: 1px;
}

.close-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: white;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.modal-content {
  padding: 40px;
}

.form-section {
  margin-bottom: 40px;
}

.section-title {
  color: #2d3748;
  border-bottom: 3px solid #4a5568;
  padding-bottom: 15px;
  margin-bottom: 25px;
  font-size: 1.4em;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-title svg {
  color: #4a5568;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  margin-bottom: 25px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 10px;
  font-size: 0.9em;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input,
.form-group select {
  padding: 15px 18px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1em;
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4a5568;
  box-shadow: 0 0 0 4px rgba(74, 85, 104, 0.1);
  transform: translateY(-2px);
}

.readonly-input {
  background: #f7fafc;
  color: #718096;
  cursor: not-allowed;
  border-color: #cbd5e0;
}

.dropdown-container {
  position: relative;
}

.form-select {
  width: 100%;
  appearance: none;
  padding-right: 50px;
  cursor: pointer;
}

.dropdown-arrow {
  position: absolute;
  right: 18px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: #4a5568;
}

.disabled-option {
  color: #a0aec0;
  background-color: #f7fafc;
}

.form-actions {
  display: flex;
  gap: 20px;
  justify-content: flex-end;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 2px solid #e2e8f0;
}

.btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1em;
  letter-spacing: 0.5px;
}

.btn-primary {
  background: #2d3748;
  color: white;
  box-shadow: 0 4px 15px rgba(45, 55, 72, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(45, 55, 72, 0.4);
}

.btn-primary:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-secondary {
  background: #718096;
  color: white;
  box-shadow: 0 4px 15px rgba(113, 128, 150, 0.3);
}

.btn-secondary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(113, 128, 150, 0.4);
}

.btn-success {
  background: #4a5568;
  color: white;
  padding: 15px 35px;
  box-shadow: 0 4px 15px rgba(74, 85, 104, 0.3);
}

.btn-success:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(74, 85, 104, 0.4);
}

/* Success Overlay */
.success-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  backdrop-filter: blur(8px);
}

.success-modal {
  background: white;
  border-radius: 20px;
  padding: 50px;
  text-align: center;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
  max-width: 450px;
  width: 90%;
  animation: successSlideIn 0.4s ease-out;
}

@keyframes successSlideIn {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.success-icon {
  margin-bottom: 25px;
  color: #4a5568;
  animation: successBounce 0.6s ease-out 0.2s both;
}

@keyframes successBounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0,0,0);
  }
  40%, 43% {
    transform: translate3d(0,-20px,0);
  }
  70% {
    transform: translate3d(0,-10px,0);
  }
  90% {
    transform: translate3d(0,-4px,0);
  }
}

.success-modal h3 {
  color: #2d3748;
  margin-bottom: 20px;
  font-size: 1.6em;
  font-weight: 700;
}

.success-modal p {
  color: #718096;
  margin-bottom: 30px;
  line-height: 1.6;
  font-size: 1.1em;
}

/* Responsive Design */
@media (max-width: 768px) {
  .assign-reviewer-modal {
    margin: 10px;
    max-height: 95vh;
  }
  
  .modal-header {
    padding: 20px 25px;
  }
  
  .modal-content {
    padding: 25px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .success-modal {
    padding: 30px 25px;
  }
}
</style>
