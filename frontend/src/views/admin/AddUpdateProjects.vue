<template>
  <div class="AddUpdateProjects">
    <!-- Header -->
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" 
             viewBox="0 0 24 24" fill="none" stroke="currentColor" 
             stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">

      <div class="header-actions">
        <button class="action-btn">Manage Projects</button>
        <button class="action-btn">Update existing project</button>
      </div>
    </div>

    <!-- Card -->
    <div class="form-card">
      <h2 class="title">CREATE PROJECT</h2>
      <form @submit.prevent="createProject">
        <div class="form-group">
          <label>PROJECT NAME</label>
          <input type="text" v-model="project.name" placeholder="Enter Project Name" />
        </div>

        <div class="form-group">
          <label>PROJECT NUMBER</label>
          <input type="text" v-model="project.number" placeholder="Enter Project Number" />
        </div>

        <div class="form-group">
          <label>PROJECT DATE</label>
          <input type="date" v-model="project.date" />
        </div>

        <div class="form-group">
          <label>LRU</label>
          <input type="text" v-model="project.lru" placeholder="Enter LRU" />
        </div>

        <div class="form-group">
          <label>SL NOS</label>
          <select v-model="project.slNo">
            <option disabled value="">Select</option>
            <option v-for="n in 10" :key="n" :value="n"> {{ n }} </option>
          </select>
        </div>

        <button type="submit" class="create-btn">CREATE PROJECT</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddUpdateProjects",
  data() {
    return {
      project: {
        name: "",
        number: "",
        date: "",
        lru: "",
        slNo: ""
      }
    };
  },
  methods: {
    createProject() {
      alert("Project Created: " + JSON.stringify(this.project, null, 2));
    }
  }
};
</script>

<style scoped>
.add-update-projects {
  font-family: Arial, sans-serif;
  background-color: #e5e5e5;
  min-height: 100vh;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  padding: 10px 20px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 15px;
}

.logo {
  width: 140px;
  margin-right: auto;
}

.header-actions {
  display: flex;
  gap: 15px;
}

.action-btn {
  border: 1px solid #333;
  background: #fff;
  padding: 8px 15px;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

.action-btn:hover {
  background: #f0f0f0;
}

.form-card {
  margin: 50px auto;
  background: #f8f8f8;
  padding: 30px 40px;
  border-radius: 15px;
  max-width: 600px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.title {
  text-align: center;
  font-weight: bold;
  margin-bottom: 25px;
}

.form-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.form-group label {
  font-weight: bold;
  flex: 1;
}

.form-group input,
.form-group select {
  flex: 2;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  background: #d3d3d3;
}

.create-btn {
  display: block;
  margin: 30px auto 0 auto;
  padding: 12px 30px;
  border: none;
  border-radius: 20px;
  background: linear-gradient(90deg, #f5f5f5, #a1a1a1);
  box-shadow: 0 4px 6px rgba(0,0,0,0.2);
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s ease-in-out;
}

.create-btn:hover {
  transform: translateY(-2px);
}
</style>