<template>
  <div class="documents-page">
    <!-- Header -->
    <header class="header">
      <div class="header-left">
        <div class="back-arrow" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </div>
        <img src="@/assets/images/aviatrax-logo.png" alt="AVIATRAX Logo" class="logo">
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
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search Projects" 
            class="search-input"
          >
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="projects-grid">
        <div 
          v-for="project in filteredProjects" 
          :key="project.id" 
          class="project-card"
          @click="selectProject(project)"
        >
          <div class="project-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
          </div>
          <div class="project-id">{{ project.id }}</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "DocumentsPage",
  data() {
    return {
      searchQuery: '',
      projects: [
        { id: 'PRJ001' },
        { id: 'PRJ003' },
        { id: 'PRJ006' },
        { id: 'PRJ007' },
        { id: 'PRJ008' },
        { id: 'PRJ012' },
        { id: 'PRJ013' },
        { id: 'PRJ014' },
        { id: 'PRJ016' },
        { id: 'PRJ018' },
        { id: 'PRJ020' },
        { id: 'PRJ022' }
      ]
    };
  },
  computed: {
    filteredProjects() {
      if (!this.searchQuery) return this.projects;
      return this.projects.filter(project => 
        project.id.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    selectProject(project) {
      console.log('Selected project:', project.id);
      // Navigate to plan documents page
      this.$router.push({ name: 'DesignerPlanDocuments', params: { projectId: project.id } });
    }
  }
};
</script>

<style scoped>
.documents-page {
  font-family: Arial, sans-serif;
  padding: 20px;
  background-color: #f0f0f0;
  min-height: 100vh;
}

/* Header Styles */
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

.back-arrow {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.back-arrow:hover {
  background: #f8f8f8;
  transform: scale(1.05);
}

.back-arrow svg {
  color: #555;
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

.header-right {
  display: flex;
  align-items: center;
}

.search-box {
  position: relative;
  width: 250px;
}

.search-input {
  width: 100%;
  padding: 10px 15px;
  padding-right: 40px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 1em;
  outline: none;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

/* Main Content Styles */
.main-content {
  padding: 20px 0;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

/* Project Card Styles */
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

.project-icon {
  margin-bottom: 10px;
}

.project-icon svg {
  color: #555;
  width: 48px;
  height: 48px;
}

.project-id {
  font-size: 1em;
  font-weight: bold;
  color: #333;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .projects-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 25px;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 20px;
    align-items: flex-start;
  }
  
  .header-left {
    order: 1;
  }
  
  .header-right {
    order: 2;
    align-self: stretch;
  }
  
  .search-box {
    width: 100%;
  }
  
  .projects-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 20px;
  }
  
  .project-card {
    padding: 15px;
    height: 160px;
  }
}

@media (max-width: 480px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .project-card {
    height: 140px;
    padding: 10px;
  }
}
</style>
