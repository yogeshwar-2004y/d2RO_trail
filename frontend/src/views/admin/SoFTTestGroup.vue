<template>
  <div class="test-group-page">
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
      <span class="page-title">SOFT - SAFETY OF FLIGHT TEST</span>
    </div>

    <div class="test-config-card">
      <div class="data-summary">
        <p>
          <strong>Test Group:</strong> SoFT (Safety of Flight Test) | 
          <strong>Sub-Tests:</strong> {{ subTests.length }} | 
          <strong>Total Items:</strong> {{ totalItems }}
        </p>
      </div>

      <div class="sub-tests-container">
        <div v-for="subTest in subTests" :key="subTest.id" class="sub-test-row">
          <div class="sub-test-header">
            <span class="sub-test-number">{{ subTest.number }}.</span>
            <span class="sub-test-name">{{ subTest.name }}</span>
            <div class="sub-test-actions">
              <button @click="editSubTest(subTest)" class="edit-btn">Edit</button>
              <button @click="deleteSubTest(subTest.id)" class="delete-btn">Delete</button>
            </div>
          </div>
          <div v-if="getBulletinsForSubTest(subTest.id).length > 0" class="bulletins-container">
            <div v-for="bulletin in getBulletinsForSubTest(subTest.id)" :key="bulletin.id" class="bulletin-item">
              <span class="bulletin-text">{{ bulletin.name }}</span>
              <div class="bulletin-actions">
                <button @click="editBulletin(bulletin)" class="edit-btn">Edit</button>
                <button @click="deleteBulletin(bulletin.id)" class="delete-btn">Delete</button>
              </div>
              <!-- Sub-bulletins -->
              <div v-if="getSubBulletinsForBulletin(bulletin.id).length > 0" class="sub-bulletins-container">
                <div v-for="subBulletin in getSubBulletinsForBulletin(bulletin.id)" :key="subBulletin.id" class="sub-bulletin-item">
                  <span class="sub-bulletin-text">{{ subBulletin.name }}</span>
                  <div class="sub-bulletin-actions">
                    <button @click="editBulletin(subBulletin)" class="edit-btn">Edit</button>
                    <button @click="deleteBulletin(subBulletin.id)" class="delete-btn">Delete</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="add-bulletin-container">
            <button @click="addBulletin(subTest.id)" class="add-bulletin-btn">+ Add Bulletin</button>
          </div>
        </div>
      </div>

      <div class="add-sub-test-container">
        <button @click="addSubTest" class="add-sub-test-btn">+ Add Sub-Test</button>
      </div>
    </div>

    <!-- Modal for Sub-Test CRUD -->
    <div v-if="showSubTestModal" class="modal-overlay" @click="closeSubTestModal">
      <div class="modal-content" @click.stop>
        <h3>{{ editingSubTest ? 'Edit Sub-Test' : 'Add Sub-Test' }}</h3>
        <input v-model="subTestForm.name" placeholder="Sub-Test Name" class="modal-input">
        <div class="modal-actions">
          <button @click="saveSubTest" class="save-btn">Save</button>
          <button @click="closeSubTestModal" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Modal for Bulletin CRUD -->
    <div v-if="showBulletinModal" class="modal-overlay" @click="closeBulletinModal">
      <div class="modal-content" @click.stop>
        <h3>{{ editingBulletin ? 'Edit Bulletin' : 'Add Bulletin' }}</h3>
        <input v-model="bulletinForm.name" placeholder="Bulletin Name" class="modal-input">
        <div class="modal-actions">
          <button @click="saveBulletin" class="save-btn">Save</button>
          <button @click="closeBulletinModal" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SoFTTestGroup",
  data() {
    return {
      subTests: [
        { id: 1, number: 1, name: "Pre-SoFT Functional Test" },
        { id: 2, number: 2, name: "Low Pressure (Altitude Test)" },
        { id: 3, number: 3, name: "High Temperature Test" },
        { id: 4, number: 4, name: "Low Temperature Test" },
        { id: 5, number: 5, name: "Endurance Vibration Test" },
        { id: 6, number: 6, name: "EMI / EMC" },
        { id: 7, number: 7, name: "POWER SUPPLY TEST" },
        { id: 8, number: 8, name: "CATH (Combined Altitude Temperature Humidity Test)" },
        { id: 9, number: 9, name: "Acceleration Test" },
        { id: 10, number: 10, name: "Shock Crash Hazard" },
        { id: 11, number: 11, name: "Rapid Decomposition Test" },
        { id: 12, number: 12, name: "Explosive Atmosphere Test" },
        { id: 13, number: 13, name: "Humidity Test" },
        { id: 14, number: 14, name: "Post-SoFT Functional Test" }
      ],
      bulletins: [
        // Pre-SoFT Functional Test
        { id: 1, subTestId: 1, name: 'Visual Inspection' },
        { id: 2, subTestId: 1, name: 'Dimensional Check' },
        { id: 3, subTestId: 1, name: 'Functional Check' },
        
        // Low Pressure (Altitude Test) - No bulletins
        
        // High Temperature Test
        { id: 5, subTestId: 3, name: 'High Temperature Test' },
        { id: 6, subTestId: 3, name: 'INSITU Functional Check' },
        { id: 7, subTestId: 3, name: 'Post HT Functional Check' },
        
        // Low Temperature Test
        { id: 8, subTestId: 4, name: 'Low Temperature Test' },
        { id: 9, subTestId: 4, name: 'INSITU Functional Check' },
        { id: 10, subTestId: 4, name: 'Post LT Functional Check' },
        
        // Endurance Vibration Test
        { id: 11, subTestId: 5, name: 'Initial Resonance test' },
        { id: 12, subTestId: 5, name: 'INSITU Functional Check', parentBulletinId: null },
        { id: 13, subTestId: 5, name: 'X Axis', parentBulletinId: 12 },
        { id: 14, subTestId: 5, name: 'Y Axis', parentBulletinId: 12 },
        { id: 15, subTestId: 5, name: 'Z Axis', parentBulletinId: 12 },
        { id: 16, subTestId: 5, name: 'Final Resonance Research' },
        { id: 17, subTestId: 5, name: 'Post RV Functional Check', parentBulletinId: null },
        { id: 18, subTestId: 5, name: 'Visual Inspection', parentBulletinId: 17 },
        { id: 19, subTestId: 5, name: 'Dimensional Check', parentBulletinId: 17 },
        { id: 20, subTestId: 5, name: 'Functional Check', parentBulletinId: 17 },
        
        // EMI / EMC
        { id: 22, subTestId: 6, name: 'Radiated Emission Test' },
        { id: 23, subTestId: 6, name: 'Conducted Emission Test' },
        { id: 24, subTestId: 6, name: 'Radiated Susceptibility Test' },
        { id: 25, subTestId: 6, name: 'Conducted Susceptibility Test' },
        
        // POWER SUPPLY TEST
        { id: 26, subTestId: 7, name: 'DC Test (LDC)' },
        { id: 27, subTestId: 7, name: 'Single Phase AC (SAC)' },
        { id: 28, subTestId: 7, name: 'Three Phase AC (TAC)' },
        
        // CATH Test
        { id: 29, subTestId: 8, name: 'CATH (Combined Altitude Temperature Humidity Test)' },
        { id: 30, subTestId: 8, name: 'Altitude' },
        { id: 31, subTestId: 8, name: 'Low temperature' },
        { id: 32, subTestId: 8, name: 'High temperature' },
        { id: 33, subTestId: 8, name: 'Humidity' },
        
        // Acceleration Test - No bulletins
        
        // Shock Crash Hazard - No bulletins
        
        // Rapid Decomposition Test - No bulletins
        
        // Explosive Atmosphere Test - No bulletins
        
        // Humidity Test
        { id: 39, subTestId: 13, name: 'INSITU Functional Check' },
        { id: 40, subTestId: 13, name: 'Post Humidity Functional Check' },
        
        // Post-SoFT Functional Test
        { id: 41, subTestId: 14, name: 'Visual Inspection' },
        { id: 42, subTestId: 14, name: 'Dimensional Check' },
        { id: 43, subTestId: 14, name: 'Functional Check' }
      ],
      showSubTestModal: false,
      showBulletinModal: false,
      editingSubTest: null,
      editingBulletin: null,
      subTestForm: { name: '' },
      bulletinForm: { name: '', subTestId: null },
      nextSubTestId: 15,
      nextBulletinId: 44
    };
  },
  computed: {
    totalItems() {
      return this.bulletins.length;
    }
  },
  methods: {
    getBulletinsForSubTest(subTestId) {
      return this.bulletins.filter(bulletin => bulletin.subTestId === subTestId && !bulletin.parentBulletinId);
    },
    
    getSubBulletinsForBulletin(parentBulletinId) {
      return this.bulletins.filter(bulletin => bulletin.parentBulletinId === parentBulletinId);
    },
    
    // Sub-Test CRUD Operations
    addSubTest() {
      this.editingSubTest = null;
      this.subTestForm = { name: '' };
      this.showSubTestModal = true;
    },
    
    editSubTest(subTest) {
      this.editingSubTest = subTest;
      this.subTestForm = { name: subTest.name };
      this.showSubTestModal = true;
    },
    
    saveSubTest() {
      if (!this.subTestForm.name.trim()) {
        alert('Please enter a sub-test name');
        return;
      }
      
      if (this.editingSubTest) {
        // Update existing sub-test
        this.editingSubTest.name = this.subTestForm.name.trim();
      } else {
        // Add new sub-test
        const newSubTest = {
          id: this.nextSubTestId++,
          number: this.subTests.length + 1,
          name: this.subTestForm.name.trim()
        };
        this.subTests.push(newSubTest);
      }
      
      this.closeSubTestModal();
    },
    
    deleteSubTest(subTestId) {
      if (confirm('Are you sure you want to delete this sub-test? This will also delete all associated bulletins.')) {
        // Remove bulletins first
        this.bulletins = this.bulletins.filter(bulletin => bulletin.subTestId !== subTestId);
        
        // Remove sub-test
        this.subTests = this.subTests.filter(subTest => subTest.id !== subTestId);
        
        // Renumber remaining sub-tests
        this.subTests.forEach((subTest, index) => {
          subTest.number = index + 1;
        });
      }
    },
    
    closeSubTestModal() {
      this.showSubTestModal = false;
      this.editingSubTest = null;
      this.subTestForm = { name: '' };
    },
    
    // Bulletin CRUD Operations
    addBulletin(subTestId) {
      this.editingBulletin = null;
      this.bulletinForm = { name: '', subTestId: subTestId };
      this.showBulletinModal = true;
    },
    
    editBulletin(bulletin) {
      this.editingBulletin = bulletin;
      this.bulletinForm = { name: bulletin.name, subTestId: bulletin.subTestId };
      this.showBulletinModal = true;
    },
    
    saveBulletin() {
      if (!this.bulletinForm.name.trim()) {
        alert('Please enter a bulletin name');
        return;
      }
      
      if (this.editingBulletin) {
        // Update existing bulletin
        this.editingBulletin.name = this.bulletinForm.name.trim();
      } else {
        // Add new bulletin
        const newBulletin = {
          id: this.nextBulletinId++,
          subTestId: this.bulletinForm.subTestId,
          name: this.bulletinForm.name.trim()
        };
        this.bulletins.push(newBulletin);
      }
      
      this.closeBulletinModal();
    },
    
    deleteBulletin(bulletinId) {
      if (confirm('Are you sure you want to delete this bulletin?')) {
        this.bulletins = this.bulletins.filter(bulletin => bulletin.id !== bulletinId);
      }
    },
    
    closeBulletinModal() {
      this.showBulletinModal = false;
      this.editingBulletin = null;
      this.bulletinForm = { name: '', subTestId: null };
    }
  }
};
</script>

<style scoped>
.test-group-page {
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
  max-width: 1200px;
  margin-bottom: 30px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 20px;
}

.logos-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo {
  width: 120px;
}

.vista-logo {
  width: 100px;
}

.page-title {
  font-size: 1.5em;
  font-weight: bold;
  flex-grow: 1;
  text-align: center;
  color: #2c3e50;
}

.test-config-card {
  width: 100%;
  max-width: 1200px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.data-summary {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  text-align: center;
  width: 100%;
}

.data-summary p {
  margin: 0;
  color: #495057;
  font-size: 1.1em;
}

.sub-tests-container {
  width: 100%;
  margin-bottom: 30px;
}

.sub-test-row {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  margin-bottom: 15px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.sub-test-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.sub-test-number {
  font-weight: bold;
  color: #2c3e50;
  margin-right: 10px;
  font-size: 1.1em;
}

.sub-test-name {
  font-weight: bold;
  color: #2c3e50;
  font-size: 1.2em;
  flex-grow: 1;
}

.sub-test-actions {
  display: flex;
  gap: 10px;
}

.bulletins-container {
  margin-left: 30px;
  margin-bottom: 15px;
}

.bulletin-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 8px;
  background: #f8f9fa;
  border-left: 4px solid #007bff;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.bulletin-text {
  flex-grow: 1;
  color: #495057;
  font-size: 0.95em;
}

.bulletin-actions {
  display: flex;
  gap: 8px;
}

.sub-bulletins-container {
  margin-left: 20px;
  margin-top: 8px;
}

.sub-bulletin-item {
  display: flex;
  align-items: center;
  padding: 6px 10px;
  margin-bottom: 6px;
  background: #e8f4fd;
  border-left: 3px solid #28a745;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.sub-bulletin-text {
  flex-grow: 1;
  color: #2c3e50;
  font-size: 0.9em;
}

.sub-bulletin-actions {
  display: flex;
  gap: 6px;
}

.add-bulletin-container {
  margin-left: 30px;
  margin-top: 10px;
}

.add-sub-test-container {
  text-align: center;
  margin-top: 20px;
}

.edit-btn, .delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85em;
  font-weight: 500;
  transition: all 0.2s ease;
}

.edit-btn {
  background: #28a745;
  color: white;
}

.edit-btn:hover {
  background: #218838;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #c82333;
}

.add-bulletin-btn, .add-sub-test-btn {
  padding: 10px 20px;
  border: 2px dashed #007bff;
  background: transparent;
  color: #007bff;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.add-bulletin-btn:hover, .add-sub-test-btn:hover {
  background: #007bff;
  color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  min-width: 400px;
}

.modal-content h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  text-align: center;
}

.modal-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1em;
  margin-bottom: 20px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.save-btn, .cancel-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
}

.save-btn {
  background: #007bff;
  color: white;
}

.save-btn:hover {
  background: #0056b3;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background: #545b62;
}

/* Responsive design */
@media (max-width: 768px) {
  .test-group-page {
    padding: 15px;
  }
  
  .test-config-card {
    padding: 20px;
  }
  
  .sub-test-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .sub-test-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .bulletins-container {
    margin-left: 15px;
  }
  
  .add-bulletin-container {
    margin-left: 15px;
  }
  
  .modal-content {
    min-width: 300px;
    margin: 20px;
  }
}
</style>