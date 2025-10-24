<template>
  <div class="tech-support-page">
    <div class="main-content">
      <div class="form-container">
        <div class="form-header">
          <h1>Technical Support</h1>
          <p>
            Please fill out the form below to report any technical issues you're
            experiencing.
          </p>

          <!-- Offline Indicator -->
          <div v-if="!isOnline" class="offline-indicator">
            <span class="offline-icon">⚠️</span>
            <span class="offline-text"
              >You're currently offline. Your request will be saved locally and
              submitted when connection is restored.</span
            >
          </div>
        </div>

        <!-- Success Message -->
        <div v-if="showSuccessMessage" class="success-message">
          <div class="success-content">
            <span class="success-icon">✓</span>
            <span class="success-text">{{ successMessage }}</span>
            <button @click="hideSuccessMessage" class="close-btn">
              &times;
            </button>
          </div>
        </div>

        <form @submit.prevent="submitForm" class="support-form">
          <div class="form-group">
            <label for="username">Username *</label>
            <input
              type="text"
              id="username"
              v-model="formData.username"
              placeholder="Enter your username"
              required
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="userId">User ID *</label>
            <input
              type="number"
              id="userId"
              v-model="formData.userId"
              placeholder="Enter your user ID"
              required
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="date">Date *</label>
            <input
              type="date"
              id="date"
              v-model="formData.date"
              required
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="issue">Issue Faced *</label>
            <textarea
              id="issue"
              v-model="formData.issue"
              placeholder="Please describe the issue you're facing in detail..."
              required
              rows="6"
              class="form-textarea"
            ></textarea>
          </div>

          <div class="form-actions">
            <button type="button" @click="goBack" class="btn-secondary">
              Back to Login
            </button>
            <button type="submit" class="btn-primary" :disabled="isSubmitting">
              {{ isSubmitting ? "Submitting..." : "Submit" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import techSupportSync from "@/services/techSupportSync.js";

export default {
  name: "TechSupportPage",
  data() {
    return {
      formData: {
        username: "",
        userId: "",
        date: new Date().toISOString().split("T")[0], // Today's date as default
        issue: "",
      },
      isSubmitting: false,
      showSuccessMessage: false,
      successMessage: "",
      isOnline: navigator.onLine,
    };
  },
  mounted() {
    // Trigger sync when page loads (in case we just came back online)
    if (navigator.onLine) {
      techSupportSync.syncOfflineRequests();
    }

    // Listen for online/offline events
    window.addEventListener("online", this.handleOnline);
    window.addEventListener("offline", this.handleOffline);
  },

  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener("online", this.handleOnline);
    window.removeEventListener("offline", this.handleOffline);
  },
  methods: {
    async submitForm() {
      if (!this.validateForm()) {
        return;
      }

      this.isSubmitting = true;

      try {
        // Try to submit to backend first
        const response = await fetch("http://127.0.0.1:5000/api/tech-support", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.formData),
          mode: "cors",
        });

        const data = await response.json();

        if (data.success) {
          if (data.duplicate) {
            this.showSuccessMessage(`This request already exists (ID: ${data.existing_request_id}). Current status: ${data.existing_status.toUpperCase()}`);
          } else {
            this.showSuccessMessage("Your technical support request has been submitted successfully. We will get back to you soon.");
          }
          this.resetForm();
          setTimeout(() => this.goBack(), 2000);
        } else {
          throw new Error(data.message || "Backend submission failed");
        }
      } catch (error) {
        console.log("Backend unavailable, storing locally:", error.message);

        // Backend is down - store locally and show success
        this.storeLocally();
        this.showSuccessMessage(
          "Your technical support request has been saved locally and will be submitted when the system is back online. We will get back to you soon."
        );
        this.resetForm();
        setTimeout(() => this.goBack(), 2000);
      } finally {
        this.isSubmitting = false;
      }
    },

    validateForm() {
      if (!this.formData.username.trim()) {
        alert("Please enter your username.");
        return false;
      }
      if (!this.formData.userId || this.formData.userId <= 0) {
        alert("Please enter a valid user ID (positive number).");
        return false;
      }
      if (!this.formData.date) {
        alert("Please select a date.");
        return false;
      }
      if (!this.formData.issue.trim()) {
        alert("Please describe the issue you're facing.");
        return false;
      }
      return true;
    },

    resetForm() {
      this.formData = {
        username: "",
        userId: "",
        date: new Date().toISOString().split("T")[0],
        issue: "",
      };
    },

    goBack() {
      this.$router.push({ name: "login" });
    },

    storeLocally() {
      // Create a unique ID for this request
      const requestId =
        "tech_support_" +
        Date.now() +
        "_" +
        Math.random().toString(36).substr(2, 9);

      // Prepare the request data
      const requestData = {
        id: requestId,
        username: this.formData.username,
        userId: parseInt(this.formData.userId),
        date: this.formData.date,
        issue: this.formData.issue,
        status: "pending",
        created_at: new Date().toISOString(),
        stored_locally: true,
        submission_attempts: 0,
      };

      // Get existing local requests
      const existingRequests = JSON.parse(
        localStorage.getItem("tech_support_offline") || "[]"
      );

      // Add new request
      existingRequests.push(requestData);

      // Save back to localStorage
      localStorage.setItem(
        "tech_support_offline",
        JSON.stringify(existingRequests)
      );

      console.log("Tech support request stored locally:", requestData);
    },

    showSuccessMessage(message) {
      this.successMessage = message;
      this.showSuccessMessage = true;

      // Auto-hide after 5 seconds
      setTimeout(() => {
        this.hideSuccessMessage();
      }, 8000);
    },

    hideSuccessMessage() {
      this.showSuccessMessage = false;
      this.successMessage = "";
    },

    handleOnline() {
      this.isOnline = true;
      console.log("Back online - syncing offline requests");
      techSupportSync.syncOfflineRequests();
    },

    handleOffline() {
      this.isOnline = false;
      console.log("Gone offline");
    },
  },
};
</script>

<style scoped>
.tech-support-page {
  min-height: calc(
    100vh - 310px
  ); /* Account for header, breadcrumb, news ticker, and footer */
  background-color: #f0f8ff;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  font-family: Arial, sans-serif;
}

.main-content {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.form-container {
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  padding: 40px;
  margin: 20px 0;
}

.form-header {
  text-align: center;
  margin-bottom: 30px;
}

.form-header h1 {
  color: #162845;
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: bold;
}

.form-header p {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
}

/* Success Message Styles */
.success-message {
  margin-bottom: 20px;
  animation: slideDown 0.3s ease-out;
}

.success-content {
  background: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 8px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.success-icon {
  background: #28a745;
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  flex-shrink: 0;
}

.success-text {
  color: #155724;
  font-weight: 500;
  flex: 1;
}

.close-btn {
  background: none;
  border: none;
  color: #155724;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.close-btn:hover {
  background-color: rgba(21, 87, 36, 0.1);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Offline Indicator Styles */
.offline-indicator {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 12px 16px;
  margin-top: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: slideDown 0.3s ease-out;
}

.offline-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.offline-text {
  color: #856404;
  font-weight: 500;
  font-size: 0.95rem;
}

.support-form {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  color: #162845;
  margin-bottom: 8px;
  font-size: 1rem;
}

.form-input,
.form-textarea {
  padding: 12px 15px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s ease;
  font-family: Arial, sans-serif;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #162845;
  box-shadow: 0 0 0 3px rgba(22, 40, 69, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 20px;
}

.btn-primary,
.btn-secondary {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 150px;
}

.btn-primary {
  background-color: #162845;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #51759a;
  transform: translateY(-2px);
}

.btn-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .tech-support-page {
    padding: 10px;
    min-height: calc(100vh - 350px);
  }

  .form-container {
    padding: 20px;
    margin: 10px 0;
  }

  .form-header h1 {
    font-size: 2rem;
  }

  .form-header p {
    font-size: 1rem;
  }

  .form-actions {
    flex-direction: column;
    align-items: center;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .form-container {
    padding: 15px;
  }

  .form-header h1 {
    font-size: 1.8rem;
  }

  .form-input,
  .form-textarea {
    padding: 10px 12px;
    font-size: 0.9rem;
  }
}
</style>
