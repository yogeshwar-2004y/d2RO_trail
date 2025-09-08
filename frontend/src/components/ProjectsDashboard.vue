<template>
  <div class="projects-dashboard">
    <div class="header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
        <div class="page-title">
          <svg class="title-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          <span class="title-text">PROJECTS</span>
        </div>
      </div>
      <div class="header-right">
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search by Project ID" class="search-input">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
      </div>
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
      <div v-if="filteredProjects.length === 0" class="no-projects">
        <p>No projects found.</p>
      </div>
      <div v-else v-for="project in filteredProjects" :key="project.id" class="project-card" @click="viewProject(project)">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <span class="card-title">PROJ ID: {{ project.id }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'ProjectsDashboard',
  data() {
    return {
      searchQuery: '',
      projects: [],
      loading: true,
      error: null
    };
  },
  computed: {
    // Get current user role from global store
    currentUserRole() {
      return userStore.getters.currentUserRole()
    },
    roleName() {
      return userStore.getters.roleName()
    },
    filteredProjects() {
      if (!this.searchQuery) {
        return this.projects;
      }
      const query = this.searchQuery.toLowerCase();
      return this.projects.filter(project =>
        project.id.toString().toLowerCase().includes(query)
      );
    },
  },
  async mounted() {
    await this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await fetch('http://localhost:5000/api/projects');
        const data = await response.json();
        
        if (data.success) {
          this.projects = data.projects;
        } else {
          this.error = data.message || 'Failed to fetch projects';
        }
      } catch (err) {
        console.error('Error fetching projects:', err);
        this.error = 'Failed to connect to server. Please check if the backend is running.';
      } finally {
        this.loading = false;
      }
    },
    viewProject(project) {
      // Navigate to the LRU Dashboard, passing the project ID as a parameter
      this.$router.push({ 
        name: 'LruDashboard', 
        params: { projectId: project.id, projectName: project.name } 
      });
    },
  },
};
</script>

<style scoped>
.projects-dashboard {
  font-family: Arial, sans-serif;
  padding: 20px;
  background-color: #f0f0f0;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo {
  width: 150px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  color: #555;
}

.title-text {
  font-size: 1.5em;
  font-weight: bold;
}

.search-box {
  position: relative;
  width: 250px;
}

.search-input {
  width: 80%;
  padding: 10px 15px;
  padding-right: 40px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 1em;
  outline: none;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
  position: relative;
  left: -10px;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  padding: 20px 0;
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

.card-icon {
  margin-bottom: 10px;
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
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

.back-button {
  background: none;
  border: none;
  cursor: pointer;
}
</style>