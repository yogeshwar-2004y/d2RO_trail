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
                  <td class="no-data">
                    <span class="serial-count">0</span>
                  </td>
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
                  <td>
                    <span class="serial-count">{{ lru.serial_numbers.length }}</span>
                  </td>
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
          "/api/projects/manage"
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
  max-width: 1400px;
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
  max-width: 1400px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
  overflow-x: auto;
}

table {
  width: 100%;
  min-width: 1200px;
  border-collapse: collapse;
  font-size: 14px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px 10px;
}

/* Table header base styles */
th {
  background-color: #667eea;
  color: white;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.5px;
  position: sticky;
  top: 0;
  z-index: 10;
}

/* Table data base styles */
td {
  text-align: left;
  vertical-align: middle;
}

/* Column 1: Project ID - Centered */
th:nth-child(1),
td:nth-child(1) {
  width: 80px;
  text-align: center;
  font-weight: 600;
}

/* Column 2: Project Name - Left aligned */
th:nth-child(2),
td:nth-child(2) {
  width: 150px;
  min-width: 150px;
  text-align: left;
}

/* Column 3: Project Director - Left aligned */
th:nth-child(3),
td:nth-child(3) {
  width: 140px;
  min-width: 140px;
  text-align: left;
}

/* Column 4: Deputy Project Director - Left aligned */
th:nth-child(4),
td:nth-child(4) {
  width: 160px;
  min-width: 160px;
  text-align: left;
}

/* Column 5: QA Manager - Left aligned */
th:nth-child(5),
td:nth-child(5) {
  width: 120px;
  min-width: 120px;
  text-align: left;
}

/* Column 6: LRU Name - Left aligned */
th:nth-child(6),
td:nth-child(6) {
  width: 180px;
  min-width: 180px;
  text-align: left;
  vertical-align: middle;
}

/* Column 7: LRU Part Number - Left aligned */
th:nth-child(7),
td:nth-child(7) {
  width: 150px;
  min-width: 150px;
  text-align: left;
  vertical-align: middle;
}

/* Column 8: Total Serial Numbers - Centered */
th:nth-child(8) {
  width: 120px;
  text-align: center;
  vertical-align: middle;
  font-weight: 600;
}

td:nth-child(8) {
  width: 120px;
  text-align: center !important;
  vertical-align: middle;
  font-weight: 600;
  padding: 12px 10px;
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
  color: #95a5a6;
  font-style: italic;
  text-align: center;
}

/* Empty state styling */
.no-data-cell {
  background-color: #f5f7fa;
}

.loading-cell {
  background-color: #f5f7fa;
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 1400px) {
  .table-container {
    padding: 20px;
  }
  
  table {
    font-size: 13px;
  }
  
  th,
  td {
    padding: 10px 8px;
  }
}

tbody tr:nth-child(even) {
  background-color: #f8f9fa;
}

tbody tr:hover {
  background-color: #e3f2fd;
  transform: scale(1.001);
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* Center no-data cells */
td.no-data {
  text-align: center;
}

/* Styling for merged cells */
td[rowspan] {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #2c3e50;
  vertical-align: middle;
}

/* Ensure all cells have consistent padding and alignment */
td {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* Ensure serial count badge is centered - override any conflicting styles */
td:nth-child(8) {
  text-align: center !important;
}

td:nth-child(8) .serial-count {
  display: inline-block;
  text-align: center;
}

/* Management fields styling */
td:nth-child(3),
td:nth-child(4),
td:nth-child(5) {
  color: #34495e;
  font-weight: 500;
}

/* Project name styling */
td:nth-child(2) {
  font-weight: 600;
  color: #2c3e50;
}

/* LRU name styling */
td:nth-child(6) {
  color: #27ae60;
  font-weight: 500;
}

/* Serial count badge */
.serial-count {
  display: inline-block;
  background-color: #e8f5e9;
  color: #2e7d32;
  border-radius: 12px;
  padding: 4px 10px;
  font-weight: 600;
  min-width: 30px;
  text-align: center;
}

td:nth-child(8).no-data .serial-count {
  background-color: #f5f5f5;
  color: #95a5a6;
}
</style>
