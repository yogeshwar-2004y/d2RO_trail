<template>
  <div class="select-user-page">
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
      <span class="page-title">SELECT USER TO EDIT</span>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>USER ID</th>
            <th>USER MAIL</th>
            <th>USER NAME</th>
            <th>ROLE</th>
            <th>ACTION</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="loading">
            <tr>
              <td colspan="5" class="loading-cell">Loading users...</td>
            </tr>
          </template>
          <template v-else-if="users.length === 0">
            <tr>
              <td colspan="5" class="no-data-cell">No users found</td>
            </tr>
          </template>
          <template v-else>
            <tr v-for="user in users" :key="user.user_id" class="user-row">
              <td>{{ user.user_id }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.name }}</td>
              <td :class="{ 'no-role': user.role === 'No Role Assigned' }">
                {{ user.role }}
              </td>
              <td>
                <button class="edit-button" @click="editUser(user)">
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
  name: "SelectUserToEdit",
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

        const response = await fetch("http://localhost:8000/api/users/manage");
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
    editUser(user) {
      // Navigate to edit user form with user data
      this.$router.push({
        name: "EditUser",
        params: { userId: user.user_id },
        query: {
          name: user.name,
          email: user.email,
          role: user.role,
        },
      });
    },
  },
};
</script>

<style scoped>
.select-user-page {
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
  max-width: 1000px;
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
  max-width: 1000px;
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

.no-role {
  color: #ff6b6b;
  font-style: italic;
}

.user-row:nth-child(even) {
  background-color: #f9f9f9;
}

.user-row:hover {
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
