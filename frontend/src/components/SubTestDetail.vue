<template>
  <div class="sub-test-detail-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
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
      </div>
      <div class="header-center">
        <h1 class="page-title">{{ subTestName }}</h1>
        <p class="page-subtitle">
          Manage bulletins and sub-bulletins for this sub-test
        </p>
      </div>
      <div class="header-right">
        <button
          class="add-bulletin-btn"
          @click="showAddBulletinFormForTopLevel"
        >
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
          ADD BULLETIN
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Add Bulletin Form -->
      <div v-if="showAddBulletinForm" class="add-bulletin-form">
        <div class="form-header">
          <h3>Add New Bulletin</h3>
          <button @click="showAddBulletinForm = false" class="close-form-btn">
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
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveBulletin">
          <div class="form-group">
            <label for="bulletinName">Bulletin Name *</label>
            <input
              type="text"
              id="bulletinName"
              v-model="bulletinForm.bulletin_name"
              placeholder="Enter bulletin name"
              required
            />
          </div>

          <div class="form-group">
            <label for="bulletinDescription">Description</label>
            <textarea
              id="bulletinDescription"
              v-model="bulletinForm.bulletin_description"
              placeholder="Enter bulletin description"
              rows="3"
            ></textarea>
          </div>

          <div class="form-actions">
            <button
              type="button"
              @click="showAddBulletinForm = false"
              class="cancel-btn"
            >
              Cancel
            </button>
            <button type="submit" class="save-btn" :disabled="saving">
              {{ saving ? "Saving..." : "Create Bulletin" }}
            </button>
          </div>
        </form>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Loading bulletins...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <h3>Error Loading Data</h3>
        <p>{{ error }}</p>
        <button @click="loadBulletins" class="retry-btn">Retry</button>
      </div>

      <!-- Bulletins Section -->
      <div v-else class="bulletins-section">
        <div class="section-header">
          <h2>Bulletins</h2>
          <span class="bulletin-count"
            >{{ bulletins.length }} bulletin{{
              bulletins.length !== 1 ? "s" : ""
            }}</span
          >
        </div>

        <!-- Empty State -->
        <div v-if="bulletins.length === 0" class="empty-bulletins">
          <div class="empty-icon">📋</div>
          <h3>No Bulletins Found</h3>
          <p>Create your first bulletin to get started.</p>
          <button
            @click="showAddBulletinFormForTopLevel"
            class="add-first-bulletin-btn"
          >
            Create First Bulletin
          </button>
        </div>

        <!-- Bulletins List -->
        <div v-else class="bulletins-list">
          <div
            v-for="bulletin in bulletins"
            :key="bulletin.bulletin_id"
            class="bulletin-item"
            :class="{
              'parent-bulletin': !bulletin.parent_bulletin_id,
              'sub-bulletin': bulletin.parent_bulletin_id,
            }"
          >
            <div class="bulletin-content">
              <div class="bulletin-header">
                <h3 class="bulletin-name">{{ bulletin.bulletin_name }}</h3>
                <div class="bulletin-actions">
                  <button
                    v-if="!bulletin.parent_bulletin_id"
                    @click="addSubBulletin(bulletin)"
                    class="add-sub-bulletin-btn"
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
                      <line x1="12" y1="5" x2="12" y2="19"></line>
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    Add Sub-bulletin
                  </button>
                  <button
                    @click="editBulletin(bulletin)"
                    class="action-btn edit-btn"
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
                    @click="deleteBulletin(bulletin)"
                    class="action-btn delete-btn"
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
              <p class="bulletin-description">
                {{
                  bulletin.bulletin_description || "No description available"
                }}
              </p>
              <div class="bulletin-meta">
                <span class="created-date"
                  >Created: {{ formatDate(bulletin.created_at) }}</span
                >
                <span
                  v-if="bulletin.parent_bulletin_id"
                  class="parent-indicator"
                >
                  Sub-bulletin of:
                  {{ getParentBulletinName(bulletin.parent_bulletin_id) }}
                </span>
                <span
                  v-if="!bulletin.parent_bulletin_id"
                  class="sub-bulletin-count"
                >
                  {{ getSubBulletinCount(bulletin.bulletin_id) }} sub-bulletin{{
                    getSubBulletinCount(bulletin.bulletin_id) !== 1 ? "s" : ""
                  }}
                </span>
              </div>
            </div>

            <!-- Sub-bulletins -->
            <div
              v-if="bulletin.sub_bulletins && bulletin.sub_bulletins.length > 0"
              class="sub-bulletins"
            >
              <div
                v-for="subBulletin in bulletin.sub_bulletins"
                :key="subBulletin.bulletin_id"
                class="sub-bulletin-item"
              >
                <div class="sub-bulletin-content">
                  <div class="sub-bulletin-header">
                    <h4 class="sub-bulletin-name">
                      {{ subBulletin.bulletin_name }}
                    </h4>
                    <div class="sub-bulletin-actions">
                      <button
                        @click="editBulletin(subBulletin)"
                        class="action-btn edit-btn"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="14"
                          height="14"
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
                        @click="deleteBulletin(subBulletin)"
                        class="action-btn delete-btn"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="14"
                          height="14"
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
                  <p class="sub-bulletin-description">
                    {{
                      subBulletin.bulletin_description ||
                      "No description available"
                    }}
                  </p>
                  <div class="sub-bulletin-meta">
                    <span class="created-date"
                      >Created: {{ formatDate(subBulletin.created_at) }}</span
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Bulletin Form -->
    <div v-if="showEditBulletinForm" class="edit-bulletin-form">
      <div class="form-header">
        <h3>Edit Bulletin</h3>
        <button @click="closeEditForm" class="close-form-btn">
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
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <form @submit.prevent="updateBulletin">
        <div class="form-group">
          <label for="editBulletinName">Bulletin Name *</label>
          <input
            type="text"
            id="editBulletinName"
            v-model="editingBulletinForm.bulletin_name"
            placeholder="Enter bulletin name"
            required
          />
        </div>

        <div class="form-group">
          <label for="editBulletinDescription">Description</label>
          <textarea
            id="editBulletinDescription"
            v-model="editingBulletinForm.bulletin_description"
            placeholder="Enter bulletin description"
            rows="3"
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="button" @click="closeEditForm" class="cancel-btn">
            Cancel
          </button>
          <button type="submit" class="save-btn" :disabled="saving">
            {{ saving ? "Saving..." : "Update Bulletin" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "SubTestDetail",
  data() {
    return {
      // Data
      bulletins: [],

      // Loading states
      loading: false,
      saving: false,

      // Error handling
      error: null,

      // Form states
      showAddBulletinForm: false,
      showEditBulletinForm: false,

      // Selected items
      editingBulletin: null,

      // Forms
      bulletinForm: {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      },
      editingBulletinForm: {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      },
    };
  },
  computed: {
    groupId() {
      return this.$route.params.groupId;
    },
    groupName() {
      return this.$route.params.groupName;
    },
    subTestId() {
      return this.$route.params.subTestId;
    },
    subTestName() {
      return this.$route.params.subTestName;
    },
  },
  mounted() {
    this.loadBulletins();
  },
  methods: {
    // API Methods
    async loadBulletins() {
      this.loading = true;
      this.error = null;

      try {
        const response = await fetch(
          `http://localhost:5000/api/sub-tests/${this.subTestId}/bulletins`
        );
        const data = await response.json();

        if (data.success) {
          this.bulletins = data.bulletins;
        } else {
          this.error = data.message || "Failed to load bulletins";
        }
      } catch (error) {
        console.error("Error loading bulletins:", error);
        this.error = "Failed to load bulletins. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    async saveBulletin() {
      this.saving = true;

      try {
        const response = await fetch(
          `http://localhost:5000/api/sub-tests/${this.subTestId}/bulletins`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.bulletinForm),
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.loadBulletins();
          this.showAddBulletinForm = false;
          this.resetBulletinForm();
        } else {
          alert(data.message || "Failed to save bulletin");
        }
      } catch (error) {
        console.error("Error saving bulletin:", error);
        alert("Failed to save bulletin. Please try again.");
      } finally {
        this.saving = false;
      }
    },

    async updateBulletin() {
      this.saving = true;

      try {
        const response = await fetch(
          `http://localhost:5000/api/bulletins/${this.editingBulletin.bulletin_id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.editingBulletinForm),
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.loadBulletins();
          this.closeEditForm();
        } else {
          alert(data.message || "Failed to update bulletin");
        }
      } catch (error) {
        console.error("Error updating bulletin:", error);
        alert("Failed to update bulletin. Please try again.");
      } finally {
        this.saving = false;
      }
    },

    async deleteBulletin(bulletin) {
      if (
        !confirm(`Are you sure you want to delete "${bulletin.bulletin_name}"?`)
      ) {
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:5000/api/bulletins/${bulletin.bulletin_id}`,
          {
            method: "DELETE",
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.loadBulletins();
        } else {
          alert(data.message || "Failed to delete bulletin");
        }
      } catch (error) {
        console.error("Error deleting bulletin:", error);
        alert("Failed to delete bulletin. Please try again.");
      }
    },

    // UI Methods
    addSubBulletin(parentBulletin) {
      this.bulletinForm = {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: parentBulletin.bulletin_id,
      };
      this.showAddBulletinForm = true;
    },

    editBulletin(bulletin) {
      this.editingBulletin = bulletin;
      this.editingBulletinForm = {
        bulletin_name: bulletin.bulletin_name,
        bulletin_description: bulletin.bulletin_description || "",
        parent_bulletin_id: bulletin.parent_bulletin_id,
      };
      this.showEditBulletinForm = true;
    },

    closeEditForm() {
      this.showEditBulletinForm = false;
      this.editingBulletin = null;
      this.editingBulletinForm = {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      };
    },

    // Form Management
    resetBulletinForm() {
      this.bulletinForm = {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      };
    },

    // Method to show add bulletin form for top-level bulletins
    showAddBulletinFormForTopLevel() {
      this.bulletinForm = {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      };
      this.showAddBulletinForm = true;
    },

    // Utility Methods
    getParentBulletinName(parentBulletinId) {
      const parentBulletin = this.bulletins.find(
        (b) => b.bulletin_id === parentBulletinId
      );
      return parentBulletin ? parentBulletin.bulletin_name : "Unknown";
    },

    getSubBulletinCount(bulletinId) {
      return this.bulletins.filter((b) => b.parent_bulletin_id === bulletinId)
        .length;
    },

    formatDate(dateString) {
      if (!dateString) return "Unknown";
      return new Date(dateString).toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.sub-test-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
}

/* Header */
.page-header {
  background: #2d3748;
  padding: 20px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: white;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.header-center {
  flex: 1;
  text-align: center;
}

.page-title {
  color: white;
  font-size: 2.2em;
  font-weight: 700;
  margin: 0;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1em;
  margin: 5px 0 0 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.add-bulletin-btn {
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 25px;
  padding: 12px 20px;
  font-weight: 600;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.add-bulletin-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  background: white;
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 30px;
}

/* Add Bulletin Form */
.add-bulletin-form,
.edit-bulletin-form {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 25px;
  margin-bottom: 30px;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e9ecef;
}

.form-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: 1.4em;
  font-weight: 600;
}

.close-form-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: #6c757d;
}

.close-form-btn:hover {
  background: #f8f9fa;
  color: #dc3545;
}

/* Form Styles */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2d3748;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #007bff;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 25px;
}

.cancel-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #5a6268;
}

.save-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover:not(:disabled) {
  background: #0056b3;
}

.save-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
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

/* Error State */
.error-state {
  text-align: center;
  padding: 60px 20px;
}

.error-icon {
  font-size: 4em;
  margin-bottom: 20px;
}

.error-state h3 {
  color: #dc3545;
  font-size: 1.5em;
  margin-bottom: 10px;
}

.error-state p {
  color: #6c757d;
  margin-bottom: 20px;
}

.retry-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.retry-btn:hover {
  background: #0056b3;
}

/* Bulletins Section */
.bulletins-section {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e9ecef;
}

.section-header h2 {
  margin: 0;
  color: #2d3748;
  font-size: 1.8em;
  font-weight: 600;
}

.bulletin-count {
  color: #6c757d;
  font-size: 1em;
  font-weight: 500;
}

/* Empty State */
.empty-bulletins {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 4em;
  margin-bottom: 20px;
  opacity: 0.6;
}

.empty-bulletins h3 {
  color: #6c757d;
  font-size: 1.5em;
  margin-bottom: 10px;
}

.empty-bulletins p {
  color: #6c757d;
  font-size: 1em;
  margin-bottom: 30px;
}

.add-first-bulletin-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 10px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-first-bulletin-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

/* Bulletins List */
.bulletins-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.bulletin-item {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
}

.bulletin-item:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.parent-bulletin {
  border-left: 4px solid #007bff;
}

.sub-bulletin {
  margin-left: 30px;
  background: #f0f8ff;
  border-left: 4px solid #28a745;
}

.bulletin-content {
  flex: 1;
}

.bulletin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.bulletin-name {
  margin: 0;
  color: #2d3748;
  font-size: 1.2em;
  font-weight: 600;
}

.bulletin-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.add-sub-bulletin-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  font-size: 0.8em;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.add-sub-bulletin-btn:hover {
  background: #218838;
}

.action-btn {
  background: none;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  transform: scale(1.1);
}

.edit-btn:hover {
  background: #e3f2fd;
  border-color: #2196f3;
  color: #2196f3;
}

.delete-btn:hover {
  background: #ffebee;
  border-color: #f44336;
  color: #f44336;
}

.bulletin-description {
  color: #6c757d;
  font-size: 0.9em;
  line-height: 1.4;
  margin: 0 0 12px 0;
}

.bulletin-meta {
  display: flex;
  gap: 15px;
  font-size: 0.8em;
  color: #6c757d;
}

.created-date {
  font-style: italic;
}

.parent-indicator {
  color: #007bff !important;
  font-weight: 500;
}

.sub-bulletin-count {
  font-weight: 500;
  color: #28a745;
}

/* Sub-bulletins */
.sub-bulletins {
  margin-top: 15px;
  padding-left: 20px;
  border-left: 2px solid #e9ecef;
}

.sub-bulletin-item {
  background: #f0f8ff;
  border: 1px solid #cce7ff;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
}

.sub-bulletin-content {
  flex: 1;
}

.sub-bulletin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.sub-bulletin-name {
  margin: 0;
  color: #2d3748;
  font-size: 1em;
  font-weight: 600;
}

.sub-bulletin-actions {
  display: flex;
  gap: 6px;
}

.sub-bulletin-description {
  color: #6c757d;
  font-size: 0.85em;
  line-height: 1.4;
  margin: 0 0 8px 0;
}

.sub-bulletin-meta {
  font-size: 0.75em;
  color: #6c757d;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    padding: 15px 20px;
    flex-direction: column;
    gap: 15px;
  }

  .page-title {
    font-size: 1.8em;
  }

  .main-content {
    padding: 0 20px;
    margin: 20px auto;
  }

  .bulletins-list {
    gap: 15px;
  }

  .bulletin-item {
    padding: 15px;
  }

  .sub-bulletin {
    margin-left: 15px;
  }

  .sub-bulletins {
    padding-left: 15px;
  }

  .add-bulletin-form,
  .edit-bulletin-form {
    padding: 20px;
  }

  .bulletins-section {
    padding: 20px;
  }

  .bulletin-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .bulletin-actions {
    justify-content: flex-start;
  }
}
</style>
