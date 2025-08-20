<template>
  <div class="manage-projects-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
      <span class="page-title">PROJECTS</span>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>ROLL</th>
            <th>PROJECT NAME</th>
            <th>LRU NAME</th>
            <th>SERIAL NUMBERS</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(project, index) in projects" :key="index">
            <td>{{ project.roll }}</td>
            <td>{{ project.projectName }}</td>
            <td>{{ project.lruName }}</td>
            <td>{{ project.serialNumbers }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManageProjects',
  data() {
    return {
      projects: [
        { roll: 1, projectName: 'PRJ-2025-078', lruName: 'LRU-A', serialNumbers: 'SNO001' },
        { roll: 2, projectName: 'PRJ002', lruName: 'LRU-B', serialNumbers: 'SNO002' },
        { roll: 3, projectName: 'PRJ003', lruName: 'LRU-C', serialNumbers: 'SNO003' },
        { roll: 4, projectName: 'PRJ004', lruName: 'LRU-D', serialNumbers: 'SNO004' },
      ],
    };
  },
};
</script>

<style scoped>
.manage-projects-page {
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
  margin-right: 20px;
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

.table-container {
  width: 100%;
  max-width: 900px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ccc;
  padding: 15px;
  text-align: left;
}

th {
  background-color: #f8f8f8;
  font-weight: bold;
}
</style>