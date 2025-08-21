<template>
  <div class="manage-users-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
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
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in users" :key="index">
            <td>{{ user.userId }}</td>
            <td>{{ user.userMail }}</td>
            <td>{{ user.userName }}</td>
            <td>{{ user.role }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManageUsers',
  data() {
    return {
      users: [
        { userId: 1, userMail: 'user1@email.com', userName: 'User One', role: 'Admin' },
        { userId: 2, userMail: 'user2@email.com', userName: 'User Two', role: 'QA Head' },
        { userId: 3, userMail: 'user3@email.com', userName: 'User Three', role: 'Design Head' },
        { userId: 4, userMail: 'user4@email.com', userName: 'User Four', role: 'QA Reviewer' },
        { userId: 5, userMail: 'user5@email.com', userName: 'User Five', role: 'Design Member' },
      ],
    };
  },
};
</script>

<style scoped>
.manage-users-page {
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