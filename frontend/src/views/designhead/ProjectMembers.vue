<template>
  <div class="project-members-page">
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
      <span class="page-title">ASSIGN PROJECT</span>
      <span class="project-id">{{ projectId }}</span>
      <button class="add-member-button" @click="addMember">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="8.5" cy="7" r="4"></circle>
          <line x1="20" y1="8" x2="20" y2="14"></line>
          <line x1="23" y1="11" x2="17" y2="11"></line>
        </svg>
        Add Member
      </button>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>SL NO</th>
            <th>USER ID</th>
            <th>USER NAME</th>
            <th>ACTIONS</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(member, index) in members" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ member.userId }}</td>
            <td>{{ member.userName }}</td>
            <td class="actions">
              <button class="action-button" @click="removeMember(index)">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 6h18"></path>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProjectMembers',
  data() {
    return {
      projectId: this.$route.params.projectId,
      members: [
        { userId: 'EMP0000', userName: 'XYZ' },
        { userId: 'EMP0001', userName: 'ABC' },
      ],
    };
  },
  methods: {
    addMember() {
    //   alert(`Adding a new member to project ${this.projectId}`);
        this.$router.push({ name: 'AddMember', params: { projectId: this.projectId } });
    },
    removeMember(index) {
      if (confirm(`Are you sure you want to remove ${this.members[index].userName} from this project?`)) {
        this.members.splice(index, 1);
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
th, td {
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
</style>