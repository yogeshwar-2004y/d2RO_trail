<template>
  <div class="manage-users-page">
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
      <span class="page-title">USERS</span>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>USER ID</th>
            <th>USER MAIL</th>
            <th>USER NAME</th>
            <th>ROLE</th>
            <th>STATUS</th>
            <th>SIGNATURE</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr>
              <td colspan="6" class="loading-cell">Loading users...</td>
            </tr>
          </template>
          <template v-else-if="users.length === 0">
            <tr>
              <td colspan="6" class="no-data-cell">No users found</td>
            </tr>
          </template>
          <template v-else>
            <tr v-for="user in users" :key="user.user_id">
              <td>{{ user.user_id }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.name }}</td>
              <td :class="{ 'no-role': user.role === 'No Role Assigned' }">
                {{ user.role }}
              </td>
              <td class="status-cell">
                <span :class="user.enabled ? 'status-enabled' : 'status-disabled'">
                  {{ user.enabled ? 'Enabled' : 'Disabled' }}
                </span>
              </td>
              <td class="signature-cell">
                <div v-if="user.has_signature" class="signature-container">
                  <img
                    :src="`http://localhost:5000${user.signature_url}`"
                    alt="User Signature"
                    class="signature-thumbnail"
                    @error="handleImageError"
                  />
                  <span class="signature-status">✓</span>
                </div>
                <div v-else class="no-signature">
                  <span class="signature-status">✗</span>
                  <span class="no-signature-text">No Signature</span>
                </div>
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
  name: "ManageUsers",
  data() {
    return {
      users: [],
      loading: false,
      error: null,
    };
  },
  async mounted() {
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        this.loading = true;
        this.error = null;

        const response = await fetch("http://localhost:5000/api/users/manage");
        const data = await response.json();

        if (data.success) {
          this.users = data.users;
        } else {
          this.error = data.message || "Failed to fetch users";
          alert("Error fetching users: " + this.error);
        }
      } catch (err) {
        console.error("Error fetching users:", err);
        this.error =
          "Failed to connect to server. Please check if the backend is running.";
        alert(this.error);
      } finally {
        this.loading = false;
      }
    },

    handleImageError(event) {
      // Hide image if it fails to load
      event.target.style.display = "none";
      console.error("Failed to load signature image");
    },
  },
};
</script>

<style scoped>
.manage-users-page {
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
}

.signature-cell {
  text-align: center;
  vertical-align: middle;
}

.signature-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.signature-thumbnail {
  width: 60px;
  height: 30px;
  object-fit: contain;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.signature-status {
  font-weight: bold;
  font-size: 14px;
}

.signature-container .signature-status {
  color: #28a745;
}

.no-signature {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  color: #dc3545;
}

.no-signature .signature-status {
  color: #dc3545;
}

.no-signature-text {
  font-size: 12px;
  font-style: italic;
}

.no-data-cell {
  text-align: center;
  color: #999;
  padding: 30px;
}

.no-role {
  color: #ff6b6b;
  font-style: italic;
}

.status-cell {
  text-align: center;
  vertical-align: middle;
}

.status-enabled {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  background-color: #d4edda;
  color: #155724;
  font-weight: 600;
  font-size: 0.9em;
}

.status-disabled {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  background-color: #f8d7da;
  color: #721c24;
  font-weight: 600;
  font-size: 0.9em;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f0f0f0;
}

td {
  vertical-align: middle;
}
</style>
