<template>
  <div class="projects-assign-dashboard">
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
      <div class="logos-container">
        <img
          src="@/assets/images/aviatrax-logo.png"
          alt="Aviatrax Logo"
          class="logo"
        />
        <img
          src="@/assets/images/vista_logo.png"
          alt="Vista Logo"
          class="logo vista-logo"
        />
      </div>
      <span class="page-title">ASSIGN PROJECT</span>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading projects...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="fetchProjects" class="retry-button">Retry</button>
    </div>

    <!-- Projects grid -->
    <div v-else class="card-grid">
      <div v-if="projects.length === 0" class="no-projects">
        <p>No projects found.</p>
      </div>
      <div
        v-else
        v-for="project in projects"
        :key="project.id"
        class="project-card"
        @click="viewProjectMembers(project.id)"
      >
        <div class="card-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
            ></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <span class="card-title">PROJ ID: {{ project.id }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProjectsForAssigning",
  data() {
    return {
      projects: [],
      loading: true,
      error: null,
    };
  },
  async mounted() {
    await this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
      try {
        this.loading = true;
        this.error = null;

        const response = await fetch("http://localhost:5000/api/projects");
        const data = await response.json();

        if (data.success) {
          this.projects = data.projects;
        } else {
          this.error = data.message || "Failed to fetch projects";
        }
      } catch (err) {
        console.error("Error fetching projects:", err);
        this.error =
          "Failed to connect to server. Please check if the backend is running.";
      } finally {
        this.loading = false;
      }
    },
    viewProjectMembers(projectId) {
      this.$router.push({ name: "ProjectMembers", params: { projectId } });
    },
  },
};
</script>

<style scoped>
.projects-assign-dashboard {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
}
.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;
  width: 100%;
  padding: 20px 30px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.back-button {
  background: none;
  border: none;
  cursor: pointer;
}
.logo {
  width: 120px;
}
.page-title {
  font-size: 1.5em;
  font-weight: bold;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  padding: 30px;
}
.project-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 180px;
  text-align: center;
}
.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}
.card-icon svg {
  color: #555;
  width: 48px;
  height: 48px;
}
.card-title {
  font-size: 1em;
  font-weight: bold;
  color: #333;
}

.card-description {
  font-size: 0.8em;
  color: #666;
  margin-top: 5px;
  text-align: center;
  line-height: 1.2;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #555;
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
  padding: 60px 20px;
  text-align: center;
}

.error-message {
  color: #d32f2f;
  font-size: 1.1em;
  margin-bottom: 20px;
}

.retry-button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.retry-button:hover {
  background-color: #1565c0;
}

.no-projects {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  text-align: center;
  color: #666;
  font-size: 1.1em;
}
</style>
