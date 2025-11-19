<template>
  <div class="document-types-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <span class="page-title">DOCUMENT TYPES</span>
    </div>

    <div class="content-container">
      <div class="action-bar">
        <button class="add-type-button" @click="openAddModal">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Type
        </button>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading document types...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="error-container">
        <p class="error-message">{{ error }}</p>
        <button @click="fetchDocumentTypes" class="retry-button">Retry</button>
      </div>

      <!-- Document Types List -->
      <div v-else class="types-list">
        <div v-if="documentTypes.length === 0" class="empty-state">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="64"
            height="64"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
          <p>No document types found. Click "Type" to add one.</p>
        </div>

        <div v-else class="types-grid">
          <div
            v-for="docType in documentTypes"
            :key="docType.type_id"
            class="type-card"
          >
            <div class="type-card-header">
              <h3 class="type-name">{{ docType.type_name }}</h3>
              <div class="type-actions">
                <button
                  class="edit-button"
                  @click="openEditModal(docType)"
                  title="Edit"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                    ></path>
                    <path
                      d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                    ></path>
                  </svg>
                </button>
                <button
                  class="delete-button"
                  @click="deleteDocumentType(docType.type_id)"
                  title="Delete"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path
                      d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                    ></path>
                  </svg>
                </button>
              </div>
            </div>
            <p v-if="docType.description" class="type-description">
              {{ docType.description }}
            </p>
            <p v-else class="type-description empty">No description</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal Overlay -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingType ? 'Edit Document Type' : 'Add Document Type' }}</h3>
          <button class="close-button" @click="closeModal">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label for="typeName">Type Name *</label>
            <input
              id="typeName"
              v-model="formData.type_name"
              type="text"
              placeholder="Enter document type name"
              class="form-input"
              :class="{ error: errors.type_name }"
            />
            <span v-if="errors.type_name" class="error-message">{{
              errors.type_name
            }}</span>
          </div>

          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="formData.description"
              placeholder="Enter description (optional)"
              class="form-textarea"
              rows="4"
            ></textarea>
          </div>
        </div>

        <div class="modal-footer">
          <button class="cancel-button" @click="closeModal">Cancel</button>
          <button
            class="save-button"
            @click="saveDocumentType"
            :disabled="saving"
          >
            {{ saving ? 'Saving...' : editingType ? 'Update' : 'Add' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DocumentTypes',
  data() {
    return {
      documentTypes: [],
      loading: false,
      error: null,
      showModal: false,
      editingType: null,
      saving: false,
      formData: {
        type_name: '',
        description: ''
      },
      errors: {}
    };
  },
  mounted() {
    this.fetchDocumentTypes();
  },
  methods: {
    async fetchDocumentTypes() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch('http://localhost:5000/api/document-types');
        const data = await response.json();

        if (data.success) {
          this.documentTypes = data.document_types;
        } else {
          this.error = data.message || 'Failed to fetch document types';
        }
      } catch (err) {
        console.error('Error fetching document types:', err);
        this.error = 'Failed to fetch document types. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    openAddModal() {
      this.editingType = null;
      this.formData = {
        type_name: '',
        description: ''
      };
      this.errors = {};
      this.showModal = true;
    },

    openEditModal(docType) {
      this.editingType = docType;
      this.formData = {
        type_name: docType.type_name,
        description: docType.description || ''
      };
      this.errors = {};
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.editingType = null;
      this.formData = {
        type_name: '',
        description: ''
      };
      this.errors = {};
    },

    validateForm() {
      this.errors = {};
      if (!this.formData.type_name.trim()) {
        this.errors.type_name = 'Type name is required';
        return false;
      }
      return true;
    },

    async saveDocumentType() {
      if (!this.validateForm()) {
        return;
      }

      this.saving = true;
      try {
        const url = this.editingType
          ? `http://localhost:5000/api/document-types/${this.editingType.type_id}`
          : 'http://localhost:5000/api/document-types';
        const method = this.editingType ? 'PUT' : 'POST';

        const response = await fetch(url, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            type_name: this.formData.type_name.trim(),
            description: this.formData.description.trim() || null
          })
        });

        const data = await response.json();

        if (data.success) {
          this.closeModal();
          await this.fetchDocumentTypes();
          alert(
            this.editingType
              ? 'Document type updated successfully'
              : 'Document type added successfully'
          );
        } else {
          alert(data.message || 'Failed to save document type');
        }
      } catch (err) {
        console.error('Error saving document type:', err);
        alert('Failed to save document type. Please try again.');
      } finally {
        this.saving = false;
      }
    },

    async deleteDocumentType(typeId) {
      if (!confirm('Are you sure you want to delete this document type?')) {
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:5000/api/document-types/${typeId}`,
          {
            method: 'DELETE'
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.fetchDocumentTypes();
          alert('Document type deleted successfully');
        } else {
          alert(data.message || 'Failed to delete document type');
        }
      } catch (err) {
        console.error('Error deleting document type:', err);
        alert('Failed to delete document type. Please try again.');
      }
    }
  }
};
</script>

<style scoped>
.document-types-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 20px;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  transition: color 0.2s;
}

.back-button:hover {
  color: #007bff;
}

.page-title {
  font-size: 1.8em;
  font-weight: bold;
  color: #2c3e50;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.action-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 30px;
}

.add-type-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-type-button:hover {
  background-color: #0056b3;
}

.loading-container,
.error-container {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-message {
  color: #dc3545;
  margin-bottom: 20px;
}

.retry-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.types-list {
  min-height: 200px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.empty-state svg {
  margin-bottom: 20px;
  color: #adb5bd;
}

.types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.type-card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  transition: box-shadow 0.2s, transform 0.2s;
}

.type-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.type-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.type-name {
  margin: 0;
  font-size: 1.2em;
  font-weight: 600;
  color: #2c3e50;
  flex: 1;
}

.type-actions {
  display: flex;
  gap: 8px;
}

.edit-button,
.delete-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.edit-button {
  color: #007bff;
}

.edit-button:hover {
  background-color: #e7f3ff;
}

.delete-button {
  color: #dc3545;
}

.delete-button:hover {
  background-color: #ffe7e7;
}

.type-description {
  margin: 0;
  color: #6c757d;
  font-size: 0.9em;
  line-height: 1.5;
}

.type-description.empty {
  font-style: italic;
  color: #adb5bd;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5em;
  color: #2c3e50;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #6c757d;
  transition: color 0.2s;
}

.close-button:hover {
  color: #2c3e50;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #007bff;
}

.form-input.error {
  border-color: #dc3545;
}

.form-textarea {
  resize: vertical;
}

.error-message {
  display: block;
  color: #dc3545;
  font-size: 0.875em;
  margin-top: 4px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px;
  border-top: 1px solid #dee2e6;
}

.cancel-button,
.save-button {
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.cancel-button {
  background-color: #6c757d;
  color: white;
}

.cancel-button:hover {
  background-color: #5a6268;
}

.save-button {
  background-color: #007bff;
  color: white;
}

.save-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

