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
        <button class="action-btn" @click="goToManageProjects">Manage Projects</button>
        <button class="action-btn" @click="goToUpdateProject">Update existing project</button>
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

        <!-- LRUs Section -->
        <div class="lrus-section">
          <div class="section-header">
            <label>LRUs</label>
            <button type="button" class="add-lru-btn" @click="addLru">+ Add LRU</button>
          </div>
          
          <div v-if="project.lrus.length === 0" class="no-lrus-message">
            No LRUs added yet. Click "Add LRU" to start.
          </div>
          
          <div v-for="(lru, index) in project.lrus" :key="index" class="lru-item">
            <div class="lru-header">
              <h4>LRU {{ index + 1 }}</h4>
              <button type="button" class="remove-lru-btn" @click="removeLru(index)" v-if="project.lrus.length > 1">×</button>
            </div>
            
            <div class="form-group">
              <label>LRU Name</label>
              <input type="text" v-model="lru.name" placeholder="Enter LRU Name" />
            </div>
            
            <div class="form-group">
              <label>Serial Number Quantity</label>
              <select v-model="lru.serialQuantity">
                <option disabled value="">Select Quantity</option>
                <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
              </select>
            </div>
          </div>
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
        lrus: [
          {
            name: "",
            serialQuantity: ""
          }
        ]
      }
    };
  },
  methods: {
    addLru() {
      this.project.lrus.push({
        name: "",
        serialQuantity: ""
      });
    },
    removeLru(index) {
      if (this.project.lrus.length > 1) {
        this.project.lrus.splice(index, 1);
      }
    },

    validateProject() {
      if (!this.project.name || !this.project.number || !this.project.date) {
        alert("Please fill in all project details.");
        return false;
      }
      
      for (let i = 0; i < this.project.lrus.length; i++) {
        const lru = this.project.lrus[i];
        if (!lru.name) {
          alert(`Please enter a name for LRU ${i + 1}.`);
          return false;
        }
        
        if (!lru.serialQuantity) {
          alert(`Please select a serial number quantity for LRU "${lru.name}".`);
          return false;
        }
      }
      
      return true;
    },
    async createProject() {
      if (!this.validateProject()) {
        return;
      }
      
      // Get current user from localStorage
      const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
      if (!currentUser.id) {
        alert('User session expired. Please login again.');
        this.$router.push({ name: 'login' });
        return;
      }
      
      try {
        const projectData = {
          ...this.project,
          createdBy: currentUser.id
        };
        
        const response = await fetch('http://localhost:5000/api/projects', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(projectData)
        });
        
        const data = await response.json();
        
        if (data.success) {
          alert("Project created successfully!");
          // Reset form
          this.project = {
            name: "",
            number: "",
            date: "",
            lrus: [
              {
                name: "",
                serialQuantity: ""
              }
            ]
          };
        } else {
          alert("Error creating project: " + data.message);
        }
      } catch (error) {
        console.error('Error creating project:', error);
        alert("Error creating project. Please check if the backend is running.");
      }
    },
    goToManageProjects() {
      this.$router.push({ name: 'ManageProjects' });
    },
    goToUpdateProject() {
      alert('Navigating to Update existing project page.');
      // this.$router.push({ name: 'UpdateProject' });
    },
  },
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

/* LRU Section Styles */
.lrus-section {
  margin-bottom: 25px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header label {
  font-weight: bold;
  font-size: 1.1em;
}

.add-lru-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
  transition: background 0.2s;
}

.add-lru-btn:hover {
  background: #45a049;
}

.lru-item {
  background: #e8e8e8;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 15px;
}

.lru-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.lru-header h4 {
  margin: 0;
  color: #333;
  font-weight: bold;
}

.remove-lru-btn {
  background: #f44336;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.remove-lru-btn:hover {
  background: #da190b;
}

.no-lrus-message {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px dashed #ccc;
}
</style>