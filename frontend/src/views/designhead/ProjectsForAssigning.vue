<template>
  <div class="projects-assign-dashboard">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
      <span class="page-title">ASSIGN PROJECT</span>
    </div>
    <div class="card-grid">
      <div v-for="project in projects" :key="project.id" class="project-card" @click="viewProjectMembers(project.id)">
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
  name: 'ProjectsForAssigning',
  data() {
    return {
      projects: [
        { id: 'PRJ001', name: 'PRJ001' },
        { id: 'PRJ002', name: 'PRJ002' },
        { id: 'PRJ003', name: 'PRJ003' },
      ],
    };
  },
  methods: {
    viewProjectMembers(projectId) {
      this.$router.push({ name: 'ProjectMembers', params: { projectId } });
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
</style>