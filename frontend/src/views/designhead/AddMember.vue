<template>
  <div class="add-member-page">
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
      <span class="page-title">ASSIGN PROJECT</span>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading project data...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="loadInitialData" class="retry-button">Retry</button>
    </div>

    <!-- Form -->
    <div v-else class="form-container">
      <div class="form-row">
        <label for="projectName">PROJECT NAME</label>
        <input
          type="text"
          id="projectName"
          v-model="project.name"
          class="form-input"
          readonly
        />
      </div>
      <div class="form-row">
        <label for="projectNumber">PROJECT ID</label>
        <input
          type="text"
          id="projectNumber"
          v-model="project.id"
          class="form-input"
          readonly
        />
      </div>
      <div class="form-row">
        <label for="projectDate">PROJECT DATE</label>
        <input
          type="date"
          id="projectDate"
          v-model="project.date"
          class="form-input"
          readonly
        />
      </div>
      <div class="form-row">
        <label for="userName">USER NAME</label>
        <select
          id="userName"
          v-model="selectedUserId"
          class="form-input"
          @change="updateUserName"
        >
          <option value="" disabled>Select User</option>
          <option
            v-for="designer in availableDesigners"
            :key="designer.user_id"
            :value="designer.user_id"
          >
            {{ designer.name }}
          </option>
        </select>
      </div>
      <div class="form-row">
        <label for="displayUserId">USER ID</label>
        <input
          type="text"
          id="displayUserId"
          v-model="displayUserId"
          class="form-input"
          readonly
        />
      </div>

      <button
        class="assign-button"
        @click="assignMember"
        :disabled="!selectedUserId || assigning"
      >
        {{ assigning ? "ASSIGNING..." : "ASSIGN PROJECT" }}
      </button>
    </div>
  </div>
</template>

<script>
import { userStore } from "@/stores/userStore";

export default {
  name: "AddMember",
  data() {
    return {
      projectId: this.$route.params.projectId,
      project: {
        id: "",
        name: "",
        date: "",
      },
      selectedUserId: "",
      displayUserId: "",
      availableDesigners: [],
      loading: true,
      error: null,
      assigning: false,
    };
  },
  computed: {
    currentUser() {
      return userStore.getters.currentUser();
    },
  },
  async mounted() {
    await this.loadInitialData();
  },
  methods: {
    async loadInitialData() {
      try {
        this.loading = true;
        this.error = null;

        // Load project details and designers in parallel
        const [projectResponse, designersResponse] = await Promise.all([
          fetch(`http://localhost:5000/api/projects/${this.projectId}/details`),
          fetch("http://localhost:5000/api/available-designers"),
        ]);

        const projectData = await projectResponse.json();
        const designersData = await designersResponse.json();

        if (!projectData.success) {
          throw new Error(
            projectData.message || "Failed to load project details"
          );
        }

        if (!designersData.success) {
          throw new Error(
            designersData.message || "Failed to load available designers"
          );
        }

        // Set project data
        this.project = {
          id: projectData.project.project_id,
          name: projectData.project.project_name,
          date: projectData.project.project_date,
        };

        // Set available designers
        this.availableDesigners = designersData.designers;
      } catch (err) {
        console.error("Error loading initial data:", err);
        this.error = err.message || "Failed to load data. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    updateUserName() {
      // This method is called when user selection changes
      // Auto-fetch and display the user ID when a user is selected
      if (this.selectedUserId) {
        const selectedDesigner = this.availableDesigners.find(
          (designer) => designer.user_id === this.selectedUserId
        );
        this.displayUserId = selectedDesigner ? selectedDesigner.user_id : "";
      } else {
        this.displayUserId = "";
      }
    },

    async assignMember() {
      if (!this.selectedUserId) {
        alert("Please select a user to assign to the project.");
        return;
      }

      try {
        this.assigning = true;

        const response = await fetch(
          `http://localhost:5000/api/projects/${this.projectId}/members`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              user_id: this.selectedUserId,
              assigned_by: this.currentUser?.id || null,
            }),
          }
        );

        const data = await response.json();

        if (data.success) {
          const selectedDesigner = this.availableDesigners.find(
            (d) => d.user_id === this.selectedUserId
          );
          alert(
            `${selectedDesigner.name} has been successfully assigned to project ${this.project.name}`
          );

          // Navigate back to project members page
          this.$router.push({
            name: "ProjectMembers",
            params: { projectId: this.projectId },
          });
        } else {
          alert(`Error: ${data.message}`);
        }
      } catch (err) {
        console.error("Error assigning member:", err);
        alert("Failed to assign member. Please try again.");
      } finally {
        this.assigning = false;
      }
    },
  },
};
</script>

<style scoped>
.add-member-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  max-width: 900px;
  margin-bottom: 30px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
}

.logo {
  width: 120px;
  margin-left: 20px;
}

.page-title {
  font-size: 1.5em;
  font-weight: bold;
  flex-grow: 1;
  text-align: center;
}

.form-container {
  width: 100%;
  max-width: 700px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 50px 70px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 25px;
}

.form-row label {
  font-weight: bold;
  font-size: 1.1em;
  flex: 1;
  text-align: left;
}

.form-input {
  flex: 2;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 15px;
  font-size: 1em;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.form-input[readonly] {
  background-color: #f8f8f8;
  color: #555;
}

.assign-button {
  width: 50%;
  padding: 15px;
  border: none;
  border-radius: 25px;
  font-size: 1.1em;
  color: #fff;
  background: linear-gradient(to right, #ccc, #888);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 30px;
}

.assign-button:hover {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}
.assign-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
.assign-button:disabled:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  transform: none;
}
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  max-width: 700px;
}
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  max-width: 700px;
}
.error-message {
  color: #ff4d4f;
  font-size: 1.1em;
  margin-bottom: 20px;
  text-align: center;
}
.retry-button {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 1em;
}
.retry-button:hover {
  background: #0056b3;
}
</style>
