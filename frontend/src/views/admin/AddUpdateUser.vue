<template>
  <div class="add-update-user-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
      <span class="page-title">ADD USER</span>
      <div class="header-buttons">
        <button class="header-button" @click="goToManageUsers">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          Manage Users
        </button>
        <button class="header-button" @click="goToUpdateUser">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path>
          </svg>
          Update existing user
        </button>
      </div>
    </div>

    <div class="form-container">
      <div class="form-row">
        <label for="userName">USER NAME</label>
        <input type="text" id="userName" v-model="user.name" class="form-input">
      </div>
      <div class="form-row">
        <label for="userId">USER ID</label>
        <input type="text" id="userId" v-model="user.id" class="form-input">
      </div>
      <div class="form-row">
        <label for="userMailId">USER MAIL ID</label>
        <input type="email" id="userMailId" v-model="user.email" class="form-input">
      </div>
      <div class="form-row">
        <label for="password">PASSWORD</label>
        <input type="password" id="password" v-model="user.password" class="form-input">
      </div>
      <div class="form-row">
        <label for="role">ROLE</label>
        <select id="role" v-model="user.role" class="form-input">
          <option value="" disabled>Select a role</option>
          <option v-for="role in roles" :key="role" :value="role">{{ role }}</option>
        </select>
      </div>

      <button class="add-button" @click="addUser">ADD USER</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddUpdateUser',
  data() {
    return {
      user: {
        name: '',
        id: '',
        email: '',
        password: '',
        role: '',
      },
      roles: ['Admin', 'QA Head', 'QA Reviewer', 'Design Head', 'Design Member'],
    };
  },
  methods: {
    addUser() {
      // Logic to send user data to the backend
      console.log('Adding user:', this.user);
      alert('User added!');
    },
    goToManageUsers() {
      // alert('Navigating to Manage Users page.');
      this.$router.push({ name: 'ManageUsers' });
    },
    goToUpdateUser() {
      alert('Navigating to Update existing user page.');
    },
  },
};
</script>

<style scoped>
.add-update-user-page {
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
  justify-content: space-between;
  width: 100%;
  max-width: 900px;
  margin-bottom: 30px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
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

.header-buttons {
  display: flex;
  gap: 15px;
}

.header-button {
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 20px;
  padding: 10px 15px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-button svg {
  color: #000;
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

.add-button {
  width: 50%;
  padding: 15px;
  border: none;
  border-radius: 25px;
  font-size: 1.1em;
  color: #fff;
  background: linear-gradient(to right, #ccc, #888);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 30px;
}

.add-button:hover {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}
</style>