<template>
  <div class="edit-project-page">
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
      <span class="page-title">EDIT PROJECT</span>
    </div>

    <div class="form-card">
      <div class="project-info">
        <h3>Editing Project ID: {{ projectId }}</h3>
        <p class="created-date">
          Created: {{ formatDate(originalData.created_at) }}
        </p>
      </div>

      <form @submit.prevent="updateProject">
        <div class="form-group">
          <label>PROJECT NAME</label>
          <input
            type="text"
            v-model="project.name"
            placeholder="Enter Project Name"
          />
        </div>

        <div class="form-group">
          <label>PROJECT DATE</label>
          <input type="date" v-model="project.date" />
        </div>

        <div class="form-group">
          <label>PROJECT DIRECTOR</label>
          <div class="autocomplete-wrapper">
            <input
              type="text"
              v-model="project.director"
              @input="handleDirectorInput"
              @focus="showDirectorDropdown = true"
              @blur="hideDirectorDropdown"
              placeholder="Type to search users or enter name manually"
              class="autocomplete-input"
            />
            <div v-if="showDirectorDropdown && filteredDirectorUsers.length > 0" class="autocomplete-dropdown">
              <div
                v-for="user in filteredDirectorUsers"
                :key="user.user_id"
                @mousedown="selectDirectorUser(user)"
                class="autocomplete-option"
              >
                {{ user.name }} ({{ user.email }})
              </div>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>DEPUTY PROJECT DIRECTOR</label>
          <div class="autocomplete-wrapper">
            <input
              type="text"
              v-model="project.deputyDirector"
              @input="handleDeputyDirectorInput"
              @focus="showDeputyDirectorDropdown = true"
              @blur="hideDeputyDirectorDropdown"
              placeholder="Type to search users or enter name manually"
              class="autocomplete-input"
            />
            <div v-if="showDeputyDirectorDropdown && filteredDeputyDirectorUsers.length > 0" class="autocomplete-dropdown">
              <div
                v-for="user in filteredDeputyDirectorUsers"
                :key="user.user_id"
                @mousedown="selectDeputyDirectorUser(user)"
                class="autocomplete-option"
              >
                {{ user.name }} ({{ user.email }})
              </div>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>QA MANAGER</label>
          <div class="autocomplete-wrapper">
            <input
              type="text"
              v-model="project.qaManager"
              @input="handleQAManagerInput"
              @focus="showQAManagerDropdown = true"
              @blur="hideQAManagerDropdown"
              placeholder="Type to search users or enter name manually"
              class="autocomplete-input"
            />
            <div v-if="showQAManagerDropdown && filteredQAManagerUsers.length > 0" class="autocomplete-dropdown">
              <div
                v-for="user in filteredQAManagerUsers"
                :key="user.user_id"
                @mousedown="selectQAManagerUser(user)"
                class="autocomplete-option"
              >
                {{ user.name }} ({{ user.email }})
              </div>
            </div>
          </div>
        </div>

        <!-- LRUs Section -->
        <div class="lrus-section">
          <div class="section-header">
            <label>LRUs</label>
            <button type="button" class="add-lru-btn" @click="addLru">
              + Add LRU
            </button>
          </div>

          <div v-if="project.lrus.length === 0" class="no-lrus-message">
            No LRUs added yet. Click "Add LRU" to start.
          </div>

          <div
            v-for="(lru, index) in project.lrus"
            :key="index"
            class="lru-item"
          >
            <div class="lru-header">
              <h4>
                {{
                  lru.lru_id
                    ? `LRU ${index + 1} (ID: ${lru.lru_id})`
                    : `New LRU ${index + 1}`
                }}
              </h4>
              <button
                type="button"
                class="remove-lru-btn"
                @click="removeLru(index)"
                v-if="project.lrus.length > 1"
              >
                ×
              </button>
            </div>

            <div class="form-group">
              <label>LRU Name</label>
              <input
                type="text"
                v-model="lru.lru_name"
                placeholder="Enter LRU Name"
              />
            </div>

            <div class="form-group">
              <label>LRU Part Number</label>
              <input
                type="text"
                v-model="lru.lru_part_number"
                placeholder="Enter LRU Part Number (e.g., ABC-123-XYZ)"
              />
            </div>

            <div
              v-if="lru.serial_numbers && lru.serial_numbers.length > 0"
              class="serial-numbers-info"
            >
              <p>
                <strong>Existing Serial Numbers:</strong>
                {{ lru.serial_numbers.length }}
              </p>
              <div class="serial-list">
                <span
                  v-for="serial in getSortedSerialNumbers(lru.serial_numbers)"
                  :key="serial.serial_id"
                  class="serial-number"
                >
                  {{ serial.serial_number }}
                </span>
              </div>
            </div>

            <div class="form-group" v-if="!lru.lru_id">
              <label>Serial Number Quantity (New LRU)</label>
              <div class="quantity-input-container">
                <input
                  type="number"
                  v-model.number="lru.serialQuantity"
                  min="1"
                  :placeholder="'Enter quantity'"
                  class="quantity-input"
                  @input="validateQuantityInput(index, $event)"
                />
                <div class="quantity-buttons-wrapper">
                  <button
                    type="button"
                    class="quantity-btn quantity-btn-up"
                    @click="incrementQuantity(index)"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="12"
                      height="12"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2.5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <line x1="12" y1="5" x2="12" y2="19"></line>
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                  </button>
                  <button
                    type="button"
                    class="quantity-btn quantity-btn-down"
                    @click="decrementQuantity(index)"
                    :disabled="!lru.serialQuantity || lru.serialQuantity <= 1"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="12"
                      height="12"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2.5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="button-group">
          <button type="button" class="cancel-button" @click="cancelEdit">
            CANCEL
          </button>
          <button type="submit" class="update-button" :disabled="loading">
            {{ loading ? "UPDATING PROJECT..." : "UPDATE PROJECT" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "EditProject",
  data() {
    return {
      projectId: this.$route.params.projectId,
      project: {
        name: "",
        date: "",
        director: "",
        directorId: null,
        deputyDirector: "",
        deputyDirectorId: null,
        qaManager: "",
        qaManagerId: null,
        lrus: [],
      },
      loading: false,
      originalData: {},
      users: [],
      showDirectorDropdown: false,
      showDeputyDirectorDropdown: false,
      showQAManagerDropdown: false,
    };
  },
  computed: {
    filteredDirectorUsers() {
      if (!this.project.director) return this.users;
      const search = this.project.director.toLowerCase();
      return this.users.filter(user => 
        user.name.toLowerCase().includes(search) || 
        user.email.toLowerCase().includes(search)
      );
    },
    filteredDeputyDirectorUsers() {
      if (!this.project.deputyDirector) return this.users;
      const search = this.project.deputyDirector.toLowerCase();
      return this.users.filter(user => 
        user.name.toLowerCase().includes(search) || 
        user.email.toLowerCase().includes(search)
      );
    },
    filteredQAManagerUsers() {
      if (!this.project.qaManager) return this.users;
      const search = this.project.qaManager.toLowerCase();
      return this.users.filter(user => 
        user.name.toLowerCase().includes(search) || 
        user.email.toLowerCase().includes(search)
      );
    },
  },
  async mounted() {
    await this.fetchUsers();
    await this.loadProjectData();
  },
  methods: {
    async loadProjectData() {
      try {
        // Get project data from query parameters passed from the previous page
        const query = this.$route.query;
        this.project.name = query.name || "";
        
        // Set values - if user_id exists, get name from users list, otherwise use text
        if (query.directorId) {
          this.project.directorId = parseInt(query.directorId);
          // Find user name from users list
          const user = this.users.find(u => u.user_id === this.project.directorId);
          this.project.director = user ? user.name : query.director || "";
        } else {
          this.project.director = query.director || "";
          this.project.directorId = null;
        }
        
        if (query.deputyDirectorId) {
          this.project.deputyDirectorId = parseInt(query.deputyDirectorId);
          const user = this.users.find(u => u.user_id === this.project.deputyDirectorId);
          this.project.deputyDirector = user ? user.name : query.deputyDirector || "";
        } else {
          this.project.deputyDirector = query.deputyDirector || "";
          this.project.deputyDirectorId = null;
        }
        
        if (query.qaManagerId) {
          this.project.qaManagerId = parseInt(query.qaManagerId);
          const user = this.users.find(u => u.user_id === this.project.qaManagerId);
          this.project.qaManager = user ? user.name : query.qaManager || "";
        } else {
          this.project.qaManager = query.qaManager || "";
          this.project.qaManagerId = null;
        }
        
        this.originalData.created_at = query.created_at;

        // Parse LRUs data
        if (query.lrusData) {
          try {
            const lrusData = JSON.parse(query.lrusData);
            this.project.lrus = lrusData.map((lru) => ({
              lru_id: lru.lru_id,
              lru_name: lru.lru_name,
              lru_part_number: lru.lru_part_number || "",
              serial_numbers: lru.serial_numbers || [],
            }));
          } catch (e) {
            console.error("Error parsing LRUs data:", e);
            this.project.lrus = [];
          }
        }

        // If no LRUs, add a default empty one
        if (this.project.lrus.length === 0) {
          this.project.lrus.push({
            lru_name: "",
            lru_part_number: "",
            serialQuantity: "",
          });
        }

        // Store original data for comparison
        this.originalData = {
          ...this.originalData,
          name: this.project.name,
          lrus: JSON.parse(JSON.stringify(this.project.lrus)),
        };
      } catch (error) {
        console.error("Error loading project data:", error);
        alert("Error loading project data");
      }
    },

    addLru() {
      this.project.lrus.push({
        lru_name: "",
        lru_part_number: "",
        serialQuantity: "",
      });
    },
    getSortedSerialNumbers(serialNumbers) {
      // Sort serial numbers in ascending order
      if (!serialNumbers || serialNumbers.length === 0) {
        return [];
      }
      return [...serialNumbers].sort((a, b) => {
        const numA = Number(a.serial_number);
        const numB = Number(b.serial_number);
        return numA - numB;
      });
    },
    removeLru(index) {
      if (this.project.lrus.length > 1) {
        const lru = this.project.lrus[index];
        if (lru.lru_id && lru.serial_numbers && lru.serial_numbers.length > 0) {
          if (
            !confirm(
              `This LRU has ${lru.serial_numbers.length} serial numbers. Are you sure you want to remove it?`
            )
          ) {
            return;
          }
        }
        this.project.lrus.splice(index, 1);
      }
    },
    incrementQuantity(index) {
      const lru = this.project.lrus[index];
      const currentValue = parseInt(lru.serialQuantity) || 0;
      lru.serialQuantity = currentValue + 1;
    },
    decrementQuantity(index) {
      const lru = this.project.lrus[index];
      const currentValue = parseInt(lru.serialQuantity) || 1;
      if (currentValue > 1) {
        lru.serialQuantity = currentValue - 1;
      }
    },
    validateQuantityInput(index, event) {
      const lru = this.project.lrus[index];
      let value = parseInt(event.target.value);
      
      // If empty or invalid, set to empty string
      if (isNaN(value) || value === '') {
        lru.serialQuantity = '';
        return;
      }
      
      // Ensure minimum value is 1
      if (value < 1) {
        value = 1;
      }
      
      lru.serialQuantity = value;
    },

    validateProject() {
      if (!this.project.name) {
        alert("Please enter a project name.");
        return false;
      }

      for (let i = 0; i < this.project.lrus.length; i++) {
        const lru = this.project.lrus[i];
        if (!lru.lru_name) {
          alert(`Please enter a name for LRU ${i + 1}.`);
          return false;
        }

        // For new LRUs, require serial quantity
        if (!lru.lru_id && (!lru.serialQuantity || lru.serialQuantity < 1)) {
          alert(
            `Please enter a valid serial number quantity (minimum 1) for new LRU "${lru.lru_name}".`
          );
          return false;
        }
      }

      return true;
    },

    async updateProject() {
      if (!this.validateProject()) {
        return;
      }

      try {
        this.loading = true;

        // Prepare update data with user IDs or text names
        const updateData = {
          project_id: this.projectId,
          name: this.project.name,
          date: this.project.date,
          director: this.project.directorId ? null : this.project.director,
          directorId: this.project.directorId,
          deputyDirector: this.project.deputyDirectorId ? null : this.project.deputyDirector,
          deputyDirectorId: this.project.deputyDirectorId,
          qaManager: this.project.qaManagerId ? null : this.project.qaManager,
          qaManagerId: this.project.qaManagerId,
          lrus: this.project.lrus.map((lru) => ({
            lru_id: lru.lru_id,
            lru_name: lru.lru_name,
            lru_part_number: lru.lru_part_number || "",
            serialQuantity: lru.serialQuantity || null,
          })),
        };

        const response = await fetch(
          `http://localhost:8000/api/projects/${this.projectId}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updateData),
          }
        );

        const data = await response.json();

        if (data.success) {
          alert("Project updated successfully!");
          this.$router.push({ name: "SelectProjectToEdit" });
        } else {
          alert("Error updating project: " + data.message);
        }
      } catch (error) {
        console.error("Error updating project:", error);
        alert(
          "Error updating project. Please check if the backend is running."
        );
      } finally {
        this.loading = false;
      }
    },

    cancelEdit() {
      if (
        confirm("Are you sure you want to cancel? All changes will be lost.")
      ) {
        this.$router.push({ name: "SelectProjectToEdit" });
      }
    },

    async fetchUsers() {
      try {
        const response = await fetch("http://localhost:8000/api/users/list");
        const data = await response.json();
        if (data.success) {
          this.users = data.users;
        }
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    handleDirectorInput() {
      this.showDirectorDropdown = true;
      // Check if current input exactly matches a user's name
      const exactMatch = this.users.find(u => u.name === this.project.director);
      if (exactMatch) {
        this.project.directorId = exactMatch.user_id;
      } else {
        // If not exact match, clear user_id (custom text entry)
        this.project.directorId = null;
      }
    },
    handleDeputyDirectorInput() {
      this.showDeputyDirectorDropdown = true;
      const exactMatch = this.users.find(u => u.name === this.project.deputyDirector);
      if (exactMatch) {
        this.project.deputyDirectorId = exactMatch.user_id;
      } else {
        this.project.deputyDirectorId = null;
      }
    },
    handleQAManagerInput() {
      this.showQAManagerDropdown = true;
      const exactMatch = this.users.find(u => u.name === this.project.qaManager);
      if (exactMatch) {
        this.project.qaManagerId = exactMatch.user_id;
      } else {
        this.project.qaManagerId = null;
      }
    },
    selectDirectorUser(user) {
      this.project.director = user.name;
      this.project.directorId = user.user_id;
      this.showDirectorDropdown = false;
    },
    selectDeputyDirectorUser(user) {
      this.project.deputyDirector = user.name;
      this.project.deputyDirectorId = user.user_id;
      this.showDeputyDirectorDropdown = false;
    },
    selectQAManagerUser(user) {
      this.project.qaManager = user.name;
      this.project.qaManagerId = user.user_id;
      this.showQAManagerDropdown = false;
    },
    hideDirectorDropdown() {
      // Delay to allow click event on dropdown option
      setTimeout(() => {
        this.showDirectorDropdown = false;
      }, 200);
    },
    hideDeputyDirectorDropdown() {
      setTimeout(() => {
        this.showDeputyDirectorDropdown = false;
      }, 200);
    },
    hideQAManagerDropdown() {
      setTimeout(() => {
        this.showQAManagerDropdown = false;
      }, 200);
    },
    formatDate(dateString) {
      if (!dateString) return "N/A";
      return new Date(dateString).toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.edit-project-page {
  font-family: Arial, sans-serif;
  background-color: #e5e5e5;
  min-height: 100vh;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background: transparent;
  padding: 10px 20px;
  margin-bottom: 20px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 15px;
}

.logo {
  width: 140px;
  margin-left: 20px;
}

.page-title {
  font-size: 1.5em;
  font-weight: bold;
  flex-grow: 1;
  text-align: center;
}

.form-card {
  margin: 0 auto;
  background: #f8f8f8;
  padding: 30px 40px;
  border-radius: 15px;
  max-width: 700px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.project-info {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f0f8ff;
  border-radius: 10px;
  border-left: 4px solid #007bff;
}

.project-info h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1.2em;
}

.created-date {
  margin: 0;
  color: #666;
  font-style: italic;
}

.form-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.form-group label {
  font-weight: bold;
  flex: 1;
}

.form-group input,
.form-group select {
  flex: 2;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  background: #d3d3d3;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  background: #c8c8c8;
}

.button-group {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 30px;
}

.cancel-button,
.update-button {
  padding: 12px 30px;
  border: none;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 150px;
}

.cancel-button {
  background: #6c757d;
  color: white;
}

.cancel-button:hover {
  background: #5a6268;
  transform: translateY(-2px);
}

.update-button {
  background: linear-gradient(90deg, #28a745, #20c997);
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.update-button:hover:not(:disabled) {
  background: linear-gradient(90deg, #218838, #1ea085);
  transform: translateY(-2px);
}

.update-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* LRU Section Styles */
.lrus-section {
  margin-bottom: 25px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header label {
  font-weight: bold;
  font-size: 1.1em;
}

.add-lru-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
  transition: background 0.2s;
}

.add-lru-btn:hover {
  background: #45a049;
}

.lru-item {
  background: #e8e8e8;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 15px;
}

.lru-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.lru-header h4 {
  margin: 0;
  color: #333;
  font-weight: bold;
}

.remove-lru-btn {
  background: #f44336;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.remove-lru-btn:hover {
  background: #da190b;
}

.no-lrus-message {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px dashed #ccc;
}

.serial-numbers-info {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 15px;
  margin: 10px 0;
}

.serial-numbers-info p {
  margin: 0 0 10px 0;
  color: #856404;
}

.serial-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.serial-number {
  background: #ffeaa7;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  color: #856404;
}

.autocomplete-wrapper {
  position: relative;
  flex: 2;
}

.autocomplete-input {
  width: 100%;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  background: #d3d3d3;
  box-sizing: border-box;
}

.autocomplete-input:focus {
  outline: none;
  background: #c8c8c8;
}

.autocomplete-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 2px;
}

.autocomplete-option {
  padding: 10px 12px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}

.autocomplete-option:hover {
  background-color: #f0f0f0;
}

.autocomplete-option:last-child {
  border-bottom: none;
}

.quantity-input-container {
  position: relative;
  flex: 2;
  width: 100%;
}

.quantity-input {
  width: 100%;
  padding: 8px 50px 8px 12px;
  border: none;
  border-radius: 8px;
  background: #d3d3d3;
  font-size: 14px;
  text-align: left;
  -moz-appearance: textfield;
  box-sizing: border-box;
}

.quantity-input:focus {
  outline: none;
  background: #c8c8c8;
}

.quantity-input::-webkit-outer-spin-button,
.quantity-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.quantity-buttons-wrapper {
  position: absolute;
  right: 2px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 1px;
  border-left: 1px solid #ccc;
  background: #f5f5f5;
  border-radius: 0 6px 6px 0;
}

.quantity-btn {
  width: 24px;
  height: 18px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: #333;
  padding: 0;
  margin: 0;
}

.quantity-btn:hover:not(:disabled) {
  background: #e0e0e0;
  color: #000;
}

.quantity-btn:active:not(:disabled) {
  background: #d0d0d0;
}

.quantity-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.quantity-btn svg {
  stroke-width: 2.5;
}
</style>
