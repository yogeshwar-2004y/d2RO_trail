<template>
  <div class="projects-dashboard">
    <div class="header">
      <div class="header-left">
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
          <input type="text" v-model="searchQuery" placeholder="Search Projects" class="search-input">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
      </div>
    </div>
    <div class="card-grid">
      <div v-for="project in filteredProjects" :key="project.id" class="project-card" @click="viewProject(project.name)">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <span class="card-title">{{ project.name }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QAHeadProjectsDashboard',
  data() {
    return {
      searchQuery: '',
      projects: [
        { id: 1, name: 'PRJ-2025-018' },
        { id: 2, name: 'PRJ002' },
        { id: 3, name: 'PRJ003' },
        { id: 4, name: 'PRJ004' },
        { id: 5, name: 'PRJ005' },
        { id: 6, name: 'PRJ006' },
        { id: 7, name: 'PRJ007' },
        { id: 8, name: 'PRJ008' },
        { id: 9, name: 'PRJ009' },
        { id: 10, name: 'PRJ010' },
        { id: 11, name: 'PRJ011' },
        { id: 12, name: 'PRJ012' },
        { id: 13, name: 'PRJ013' },
        { id: 14, name: 'PRJ014' },
        { id: 15, name: 'PRJ015' },
        { id: 16, name: 'PRJ016' },
        { id: 17, name: 'PRJ017' },
        { id: 18, name: 'PRJ018' },
        { id: 19, name: 'PRJ019' },
        { id: 20, name: 'PRJ020' },
        { id: 21, name: 'PRJ021' },
        { id: 22, name: 'PRJ022' },
        { id: 23, name: 'PRJ023' },
        { id: 24, name: 'PRJ024' },
      ],
    };
  },
  computed: {
    filteredProjects() {
      if (!this.searchQuery) {
        return this.projects;
      }
      const query = this.searchQuery.toLowerCase();
      return this.projects.filter(project =>
        project.name.toLowerCase().includes(query)
      );
    },
  },
  methods: {
    viewProject(projectName) {
      // Navigate to the QA Head LRU Dashboard, passing the project name as a parameter
      this.$router.push({ name: 'QAHeadLruDashboard', params: { projectName } });
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
</style>
