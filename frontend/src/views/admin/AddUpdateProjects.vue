<template>
  <div class="AddUpdateProjects">
    <!-- Header -->
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

      <div class="header-actions">
        <button class="action-btn" @click="goToManageProjects">
          Manage Projects
        </button>
        <button class="action-btn" @click="goToUpdateProject">
          Update existing project
        </button>
      </div>
    </div>

    <!-- Card -->
    <div class="form-card">
      <h2 class="title">CREATE PROJECT</h2>
      <form @submit.prevent="createProject">
        <div class="form-group">
          <label>PROJECT NAME</label>
          <input
            type="text"
            v-model="project.name"
            placeholder="Enter Project Name"
          />
        </div>

        <div class="form-group">
          <label>PROJECT NUMBER</label>
          <input
            type="text"
            v-model="project.number"
            placeholder="Enter Project Number"
          />
        </div>

        <div class="form-group">
          <label>PROJECT DATE</label>
          <input type="date" v-model="project.date" />
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
              <h4>LRU {{ index + 1 }}</h4>
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
                v-model="lru.name"
                placeholder="Enter LRU Name"
              />
            </div>

            <div class="form-group">
              <label>Serial Number Quantity</label>
              <select v-model="lru.serialQuantity">
                <option disabled value="">Select Quantity</option>
                <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
              </select>
            </div>
          </div>
        </div>

        <button type="submit" class="create-btn">CREATE PROJECT</button>
      </form>
    </div>
  </div>
</template>

<script>
import { userStore } from "@/stores/userStore";

export default {
  name: "AddUpdateProjects",
  data() {
    return {
      project: {
        name: "",
        number: "",
        date: "",
        lrus: [
          {
            name: "",
            serialQuantity: "",
          },
        ],
      },
    };
  },
  computed: {
    // Get current user from global store
    currentUser() {
      return userStore.getters.currentUser();
    },
    isLoggedIn() {
      return userStore.getters.isLoggedIn();
    },
  },
  methods: {
    addLru() {
      this.project.lrus.push({
        name: "",
        serialQuantity: "",
      });
    },
    removeLru(index) {
      if (this.project.lrus.length > 1) {
        this.project.lrus.splice(index, 1);
      }
    },

    validateProject() {
      if (!this.project.name || !this.project.number || !this.project.date) {
        alert("Please fill in all project details.");
        return false;
      }

      for (let i = 0; i < this.project.lrus.length; i++) {
        const lru = this.project.lrus[i];
        if (!lru.name) {
          alert(`Please enter a name for LRU ${i + 1}.`);
          return false;
        }

        if (!lru.serialQuantity) {
          alert(
            `Please select a serial number quantity for LRU "${lru.name}".`
          );
          return false;
        }
      }

      return true;
    },
    async createProject() {
      if (!this.validateProject()) {
        return;
      }

      // Check if user is logged in using global store
      if (!this.isLoggedIn || !this.currentUser?.id) {
        alert("User session expired. Please login again.");
        this.$router.push({ name: "login" });
        return;
      }

      try {
        const projectData = {
          ...this.project,
          createdBy: this.currentUser.id,
        };

        const response = await fetch("http://localhost:8000/api/projects", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(projectData),
        });

        const data = await response.json();

        if (data.success) {
          alert("Project created successfully!");
          // Reset form
          this.project = {
            name: "",
            number: "",
            date: "",
            lrus: [
              {
                name: "",
                serialQuantity: "",
              },
            ],
          };
        } else {
          alert("Error creating project: " + data.message);
        }
      } catch (error) {
        console.error("Error creating project:", error);
        alert(
          "Error creating project. Please check if the backend is running."
        );
      }
    },
    goToManageProjects() {
      this.$router.push({ name: "ManageProjects" });
    },
    goToUpdateProject() {
      this.$router.push({ name: "SelectProjectToEdit" });
    },
  },
};
</script>

<style scoped>
.add-update-projects {
  font-family: Arial, sans-serif;
  background-color: #e5e5e5;
  min-height: 100vh;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  padding: 10px 20px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 15px;
}
</style>

