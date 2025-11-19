<template>
  <div class="manage-projects-page">
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
      <span class="page-title">PROJECTS</span>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>PROJECT ID</th>
            <th>PROJECT NAME</th>
            <th>PROJECT DIRECTOR</th>
            <th>DEPUTY PROJECT DIRECTOR</th>
            <th>QA MANAGER</th>
            <th>LRU NAME</th>
            <th>LRU PART NUMBER</th>
            <th>TOTAL SERIAL NUMBERS</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr>
              <td colspan="8" class="loading-cell">Loading projects...</td>
            </tr>
          </template>
          <template v-else-if="projects.length === 0">
            <tr>
              <td colspan="8" class="no-data-cell">No projects found</td>
            </tr>
          </template>
          <template v-else>
            <template v-for="project in projects" :key="project.project_id">
              <template v-if="project.lrus.length === 0">
                <tr>
                  <td>{{ project.project_id }}</td>
                  <td>{{ project.project_name }}</td>
                  <td>{{ project.project_director || '-' }}</td>
                  <td>{{ project.deputy_project_director || '-' }}</td>
                  <td>{{ project.qa_manager || '-' }}</td>
                  <td class="no-data">No LRUs</td>
                  <td class="no-data">-</td>
                  <td class="no-data">0</td>
                </tr>
              </template>
              <template v-else>
                <tr v-for="(lru, lruIndex) in project.lrus" :key="lru.lru_id">
                  <td v-if="lruIndex === 0" :rowspan="project.lrus.length">
                    {{ project.project_id }}
                  </td>
                  <td v-if="lruIndex === 0" :rowspan="project.lrus.length">
                    {{ project.project_name }}
                  </td>
                  <td v-if="lruIndex === 0" :rowspan="project.lrus.length">
                    {{ project.project_director || '-' }}
                  </td>
                  <td v-if="lruIndex === 0" :rowspan="project.lrus.length">
                    {{ project.deputy_project_director || '-' }}
                  </td>
                  <td v-if="lruIndex === 0" :rowspan="project.lrus.length">
                    {{ project.qa_manager || '-' }}
                  </td>
                  <td>{{ lru.lru_name }}</td>
                  <td>{{ lru.lru_part_number || '-' }}</td>
                  <td>{{ lru.serial_numbers.length }}</td>
                </tr>
              </template>
            </template>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "ManageProjects",
  data() {
    return {
      projects: [],
      loading: false,
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

        const response = await fetch(
          "http://localhost:8000/api/projects/manage"
        );
        const data = await response.json();

        if (data.success) {
          this.projects = data.projects;
        } else {
          this.error = data.message || "Failed to fetch projects";
          alert("Error fetching projects: " + this.error);
        }
      } catch (err) {
        console.error("Error fetching projects:", err);
        this.error =
          "Failed to connect to server. Please check if the backend is running.";
        alert(this.error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.manage-projects-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #ebf7fd;
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

th,
td {
  border: 1px solid #ccc;
  padding: 15px;
  text-align: left;
}

th {
  background-color: #f8f8f8;
  font-weight: bold;
}

.loading-cell {
  text-align: center;
  font-style: italic;
  color: #666;
  padding: 30px;
}

.no-data-cell {
  text-align: center;
  color: #999;
  padding: 30px;
}

.no-data {
  color: #999;
  font-style: italic;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f0f0f0;
}

td {
  vertical-align: top;
}

/* Styling for merged cells */
td[rowspan] {
  background-color: #f8f8f8;
  font-weight: 500;
}
</style>
