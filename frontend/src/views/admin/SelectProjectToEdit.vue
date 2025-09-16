<template>
  <div class="select-project-page">
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
      <span class="page-title">SELECT PROJECT TO EDIT</span>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>PROJECT ID</th>
            <th>PROJECT NAME</th>
            <th>DATE CREATED</th>
            <th>LRUs COUNT</th>
            <th>ACTION</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr>
              <td colspan="5" class="loading-cell">Loading projects...</td>
            </tr>
          </template>
          <template v-else-if="projects.length === 0">
            <tr>
              <td colspan="5" class="no-data-cell">No projects found</td>
            </tr>
          </template>
          <template v-else>
            <tr
              v-for="project in projects"
              :key="project.project_id"
              class="project-row"
            >
              <td>{{ project.project_id }}</td>
              <td>{{ project.project_name }}</td>
              <td>{{ formatDate(project.created_at) }}</td>
              <td>{{ project.lrus ? project.lrus.length : 0 }}</td>
              <td>
                <button class="edit-button" @click="editProject(project)">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"
                    ></path>
                  </svg>
                  Edit
                </button>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "SelectProjectToEdit",
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
    editProject(project) {
      // Navigate to edit project form with project data
      this.$router.push({
        name: "EditProject",
        params: { projectId: project.project_id },
        query: {
          name: project.project_name,
          created_at: project.created_at,
          lrusData: JSON.stringify(project.lrus || []),
        },
      });
    },
    formatDate(dateString) {
      if (!dateString) return "N/A";
      return new Date(dateString).toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.select-project-page {
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
  max-width: 1200px;
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
  max-width: 1200px;
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

.project-row:nth-child(even) {
  background-color: #f9f9f9;
}

.project-row:hover {
  background-color: #f0f0f0;
}

td {
  vertical-align: middle;
}

.edit-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.9em;
  transition: background-color 0.3s ease;
}

.edit-button:hover {
  background-color: #0056b3;
}

.edit-button svg {
  stroke: white;
}
</style>
