<template>
  <div class="edit-user-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <div class="logos-container">
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
        <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
      </div>
      <span class="page-title">EDIT USER</span>
    </div>

    <div class="form-container">
      <div class="user-info">
        <h3>Editing User ID: {{ userId }}</h3>
      </div>
      
      <div class="form-row">
        <label for="userName">USER NAME</label>
        <input type="text" id="userName" v-model="user.name" class="form-input">
      </div>
      
      <div class="form-row">
        <label for="userMailId">USER MAIL ID</label>
        <input type="email" id="userMailId" v-model="user.email" class="form-input">
      </div>
      
      <div class="form-row">
        <label for="password">NEW PASSWORD</label>
        <input type="password" id="password" v-model="user.password" class="form-input" placeholder="Leave blank to keep current password">
      </div>
      
      <div class="form-row">
        <label for="role">ROLE</label>
        <select id="role" v-model="user.roleId" class="form-input">
          <option value="" disabled>Select a role</option>
          <option v-for="role in roles" :key="role.id" :value="role.id" :selected="role.name === user.currentRole">
            {{ role.name }}
          </option>
        </select>
      </div>

      <div class="button-group">
        <button class="cancel-button" @click="cancelEdit">
          CANCEL
        </button>
        <button class="update-button" @click="updateUser" :disabled="loading">
          {{ loading ? 'UPDATING USER...' : 'UPDATE USER' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditUser',
  data() {
    return {
      userId: this.$route.params.userId,
      user: {
        name: '',
        email: '',
        password: '',
        roleId: '',
        currentRole: ''
      },
      roles: [],
      loading: false,
      originalData: {}
    };
  },
  async mounted() {
    await this.loadUserData();
    await this.fetchRoles();
  },
  methods: {
    loadUserData() {
      // Get user data from query parameters passed from the previous page
      const query = this.$route.query;
      this.user.name = query.name || '';
      this.user.email = query.email || '';
      this.user.currentRole = query.role || '';
      
      // Store original data for comparison
      this.originalData = {
        name: this.user.name,
        email: this.user.email,
        role: this.user.currentRole
      };
    },
    
    async fetchRoles() {
      try {
        this.loading = true;
        const response = await fetch('http://localhost:5000/api/roles');
        const data = await response.json();
        
        if (data.success) {
          this.roles = data.roles;
          // Set the current role as selected
          const currentRole = this.roles.find(role => role.name === this.user.currentRole);
          if (currentRole) {
            this.user.roleId = currentRole.id;
          }
        } else {
          alert('Error fetching roles: ' + data.message);
        }
      } catch (error) {
        console.error('Error fetching roles:', error);
        alert('Error fetching roles. Please check if the backend is running.');
      } finally {
        this.loading = false;
      }
    },
    
    validateUser() {
      if (!this.user.name || !this.user.email || !this.user.roleId) {
        alert('Please fill in all required fields (Name, Email, Role).');
        return false;
      }
      
      // Basic email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.user.email)) {
        alert('Please enter a valid email address.');
        return false;
      }
      
      return true;
    },
    
    async updateUser() {
      if (!this.validateUser()) {
        return;
      }
      
      try {
        this.loading = true;
        
        // Prepare update data - only include fields that have changed
        const updateData = {
          user_id: this.userId
        };
        
        if (this.user.name !== this.originalData.name) {
          updateData.name = this.user.name;
        }
        
        if (this.user.email !== this.originalData.email) {
          updateData.email = this.user.email;
        }
        
        if (this.user.password && this.user.password.trim() !== '') {
          updateData.password = this.user.password;
        }
        
        // Always include role update if roleId is set
        if (this.user.roleId) {
          updateData.roleId = this.user.roleId;
        }
        
        const response = await fetch(`http://localhost:5000/api/users/${this.userId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updateData)
        });
        
        const data = await response.json();
        
        if (data.success) {
          alert('User updated successfully!');
          this.$router.push({ name: 'SelectUserToEdit' });
        } else {
          alert('Error updating user: ' + data.message);
        }
      } catch (error) {
        console.error('Error updating user:', error);
        alert('Error updating user. Please check if the backend is running.');
      } finally {
        this.loading = false;
      }
    },
    
    cancelEdit() {
      if (confirm('Are you sure you want to cancel? All changes will be lost.')) {
        this.$router.push({ name: 'SelectUserToEdit' });
      }
    }
  }
};
</script>

<style scoped>
.edit-user-page {
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

.form-container {
  width: 100%;
  max-width: 700px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 50px 70px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-info {
  width: 100%;
  margin-bottom: 30px;
  text-align: center;
}

.user-info h3 {
  color: #333;
  font-size: 1.2em;
  margin: 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #007bff;
}

.form-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 25px;
}

.form-row label {
  font-weight: bold;
  font-size: 1.1em;
  flex: 1;
  text-align: left;
}

.form-input {
  flex: 2;
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 15px;
  font-size: 1em;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05), 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.button-group {
  display: flex;
  gap: 20px;
  width: 100%;
  justify-content: center;
  margin-top: 30px;
}

.cancel-button, .update-button {
  padding: 15px 30px;
  border: none;
  border-radius: 25px;
  font-size: 1.1em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 150px;
}

.cancel-button {
  background-color: #6c757d;
  color: white;
}

.cancel-button:hover {
  background-color: #5a6268;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.update-button {
  background: linear-gradient(to right, #28a745, #20c997);
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.update-button:hover:not(:disabled) {
  background: linear-gradient(to right, #218838, #1ea085);
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
}

.update-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
</style>
