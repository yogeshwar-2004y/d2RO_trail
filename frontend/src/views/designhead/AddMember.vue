<template>
  <div class="add-member-page">
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

    <div class="form-container">
      <div class="form-row">
        <label for="projectName">PROJECT NAME</label>
        <input type="text" id="projectName" v-model="project.name" class="form-input" readonly>
      </div>
      <div class="form-row">
        <label for="projectNumber">PROJECT NUMBER</label>
        <input type="text" id="projectNumber" v-model="project.number" class="form-input" readonly>
      </div>
      <div class="form-row">
        <label for="projectDate">PROJECT DATE</label>
        <input type="date" id="projectDate" v-model="project.date" class="form-input" readonly>
      </div>
      <div class="form-row">
        <label for="version">VERSION</label>
        <input type="text" id="version" v-model="project.version" class="form-input" readonly>
      </div>
      <div class="form-row">
        <label for="revision">REVISION</label>
        <input type="text" id="revision" v-model="project.revision" class="form-input" readonly>
      </div>
      <div class="form-row">
        <label for="userName">USER NAME</label>
        <input type="text" id="userName" v-model="user.name" class="form-input">
      </div>
      <div class="form-row">
        <label for="userId">USER ID</label>
        <select id="userId" v-model="user.id" class="form-input">
          <option value="" disabled>Select User ID</option>
          <option v-for="user in availableUsers" :key="user.id" :value="user.id">{{ user.id }}</option>
        </select>
      </div>

      <button class="assign-button" @click="assignMember">ASSIGN PROJECT</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddMember',
  data() {
    return {
      project: {
        name: 'ERP QA Automation Tool',
        number: 'PRJ-001',
        date: '2025-07-01',
        version: '1.0',
        revision: '0',
      },
      user: {
        name: '',
        id: '',
      },
      availableUsers: [
        { id: 'EMP0002', name: 'User A' },
        { id: 'EMP0003', name: 'User B' },
        { id: 'EMP0004', name: 'User C' },
      ],
    };
  },
  watch: {
    'user.id'(newId) {
      const selectedUser = this.availableUsers.find(user => user.id === newId);
      this.user.name = selectedUser ? selectedUser.name : '';
    },
  },
  methods: {
    assignMember() {
      // Logic to assign the user to the project
      console.log('Assigning user:', this.user.id, 'to project:', this.project.number);
      alert(`User ${this.user.name} assigned to project ${this.project.number}`);
    },
  },
};
</script>

<style scoped>
.add-member-page {
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

.form-input[readonly] {
  background-color: #f8f8f8;
  color: #555;
}

.assign-button {
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

.assign-button:hover {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}
</style>