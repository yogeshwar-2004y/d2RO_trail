<template>
  <div class="project-members-page">
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
      <span class="project-id">{{ projectName || projectId }}</span>
      <button class="add-member-button" @click="addMember">
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
          <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="8.5" cy="7" r="4"></circle>
          <line x1="20" y1="8" x2="20" y2="14"></line>
          <line x1="23" y1="11" x2="17" y2="11"></line>
        </svg>
        Add Member
      </button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading project members...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="fetchProjectMembers" class="retry-button">Retry</button>
    </div>

    <!-- Members table -->
    <div v-else class="table-container">
      <table v-if="members.length > 0">
        <thead>
          <tr>
            <th>SL NO</th>
            <th>USER ID</th>
            <th>USER NAME</th>
            <th>ACTIONS</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(member, index) in members" :key="member.user_id">
            <td>{{ index + 1 }}</td>
            <td>{{ member.user_id }}</td>
            <td>{{ member.user_name }}</td>
            <td class="actions">
              <button
                class="action-button"
                @click="removeMember(member, index)"
                :disabled="removing"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M3 6h18"></path>
                  <path
                    d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                  ></path>
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="no-members">
        <p>No members assigned to this project yet.</p>
        <button @click="addMember" class="add-first-member-button">
          Add First Member
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProjectMembers",
  data() {
    return {
      projectId: this.$route.params.projectId,
      projectName: "",
      members: [],
      loading: true,
      error: null,
      removing: false,
    };
  },
  async mounted() {
    await this.fetchProjectMembers();
  },
  methods: {
    async fetchProjectMembers() {
      try {
        this.loading = true;
        this.error = null;

        const response = await fetch(
          `http://localhost:5000/api/projects/${this.projectId}/members`
        );
        const data = await response.json();

        if (data.success) {
          this.members = data.members;
          this.projectName = data.project.project_name;
        } else {
          this.error = data.message || "Failed to fetch project members";
        }
      } catch (err) {
        console.error("Error fetching project members:", err);
        this.error =
          "Failed to connect to server. Please check if the backend is running.";
      } finally {
        this.loading = false;
      }
    },

    addMember() {
      this.$router.push({
        name: "AddMember",
        params: { projectId: this.projectId },
      });
    },

    async removeMember(member, index) {
      if (
        confirm(
          `Are you sure you want to remove ${member.user_name} from this project?`
        )
      ) {
        try {
          this.removing = true;

          const response = await fetch(
            `http://localhost:5000/api/projects/${this.projectId}/members/${member.user_id}`,
            {
              method: "DELETE",
              headers: {
                "Content-Type": "application/json",
              },
            }
          );

          const data = await response.json();

          if (data.success) {
            // Remove from local array
            this.members.splice(index, 1);
            alert("Member removed from project successfully");
          } else {
            alert(`Error: ${data.message}`);
          }
        } catch (err) {
          console.error("Error removing member:", err);
          alert("Failed to remove member. Please try again.");
        } finally {
          this.removing = false;
        }
      }
    },
  },
};
</script>

<style scoped>
.project-members-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
  padding: 30px;
}
.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 20px;
  width: 100%;
  max-width: 900px;
  margin: 0 auto 30px;
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
.project-id {
  font-size: 1.5em;
  font-weight: bold;
  margin-left: auto;
}
.add-member-button {
  display: flex;
  align-items: center;
  gap: 5px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 20px;
  padding: 10px 15px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.table-container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
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
.actions {
  text-align: center;
}
.action-button {
  background: none;
  border: none;
  cursor: pointer;
}
.action-button svg {
  color: #ff4d4f;
}
.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
  max-width: 900px;
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
  max-width: 900px;
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
.no-members {
  text-align: center;
  padding: 50px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  max-width: 900px;
}
.no-members p {
  font-size: 1.2em;
  color: #666;
  margin-bottom: 20px;
}
.add-first-member-button {
  background: #28a745;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 15px 30px;
  font-size: 1.1em;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.add-first-member-button:hover {
  background: #218838;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
