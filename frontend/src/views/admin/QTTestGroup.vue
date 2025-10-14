<template>
  <div class="test-group-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <span class="page-title">QT - QUALIFICATION TEST</span>
    </div>

    <div class="test-config-card">
      <div class="data-summary">
        <p>
          <strong>Test Group:</strong> QT (Qualification Test) | 
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
  name: "QTTestGroup",
  data() {
    return {
      subTests: [
        { id: 1, number: 1, name: "Pre-QT Functional Test" },
        { id: 2, number: 2, name: "Low Pressure (Altitude Test)" },
        { id: 3, number: 3, name: "High Temperature Test" },
        { id: 4, number: 4, name: "Low Temperature Test" },
        { id: 5, number: 5, name: "Thermal Shock Test (Temperature Shock)" },
        { id: 6, number: 6, name: "Endurance Vibration Test" },
        { id: 7, number: 7, name: "EMI / EMC" },
        { id: 8, number: 8, name: "POWER SUPPLY TEST" },
        { id: 9, number: 9, name: "Fluid Contamination Test" },
        { id: 10, number: 10, name: "Mould Growth (Fungus Test)" },
        { id: 11, number: 11, name: "Salt fog Test" },
        { id: 12, number: 12, name: "Rain Drip test" },
        { id: 13, number: 13, name: "CATH (Combined Altitude Temperature Humidity Test)" },
        { id: 14, number: 14, name: "Acceleration Test" },
        { id: 15, number: 15, name: "Shock Crash Hazard" },
        { id: 16, number: 16, name: "Transit Drop" },
        { id: 17, number: 17, name: "Gunfire Vibration" },
        { id: 18, number: 18, name: "Bench Handling" },
        { id: 19, number: 19, name: "Mechanical Shock Test" },
        { id: 20, number: 20, name: "Lightning Test" },
        { id: 21, number: 21, name: "Icing / Freezing Test" },
        { id: 22, number: 22, name: "Explosive Atmosphere Test" },
        { id: 23, number: 23, name: "Acoustic Noise Test" },
        { id: 24, number: 24, name: "Humidity Test" },
        { id: 25, number: 25, name: "Post-QT Functional Test" }
      ],
      bulletins: [
        // Pre-QT Functional Test
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
        
        // Thermal Shock Test - No bulletins
        
        // Endurance Vibration Test
        { id: 12, subTestId: 6, name: 'Initial Resonance test' },
        { id: 13, subTestId: 6, name: 'INSITU Functional Check', parentBulletinId: null },
        { id: 14, subTestId: 6, name: 'X Axis', parentBulletinId: 13 },
        { id: 15, subTestId: 6, name: 'Y Axis', parentBulletinId: 13 },
        { id: 16, subTestId: 6, name: 'Z Axis', parentBulletinId: 13 },
        { id: 17, subTestId: 6, name: 'Final Resonance Research' },
        { id: 18, subTestId: 6, name: 'Post RV Functional Check', parentBulletinId: null },
        { id: 19, subTestId: 6, name: 'Visual Inspection', parentBulletinId: 18 },
        { id: 20, subTestId: 6, name: 'Dimensional Check', parentBulletinId: 18 },
        { id: 21, subTestId: 6, name: 'Functional Check', parentBulletinId: 18 },
        
        // EMI / EMC
        { id: 23, subTestId: 7, name: 'Radiated Emission Test' },
        { id: 24, subTestId: 7, name: 'Conducted Emission Test' },
        { id: 25, subTestId: 7, name: 'Radiated Susceptibility Test' },
        { id: 26, subTestId: 7, name: 'Conducted Susceptibility Test' },
        
        // POWER SUPPLY TEST
        { id: 27, subTestId: 8, name: 'DC Test (LDC)' },
        { id: 28, subTestId: 8, name: 'Single Phase AC (SAC)' },
        { id: 29, subTestId: 8, name: 'Three Phase AC (TAC)' },
        
        // Fluid Contamination Test - No bulletins
        
        // Mould Growth (Fungus Test) - No bulletins
        
        // Salt fog Test - No bulletins
        
        // Rain Drip test - No bulletins
        
        // CATH Test
        { id: 34, subTestId: 13, name: 'CATH (Combined Altitude Temperature Humidity Test)' },
        { id: 35, subTestId: 13, name: 'Altitude' },
        { id: 36, subTestId: 13, name: 'Low temperature' },
        { id: 37, subTestId: 13, name: 'High temperature' },
        { id: 38, subTestId: 13, name: 'Humidity' },
        
        // Acceleration Test - No bulletins
        
        // Shock Crash Hazard - No bulletins
        
        // Transit Drop - No bulletins
        
        // Gunfire Vibration - No bulletins
        
        // Bench Handling - No bulletins
        
        // Mechanical Shock Test - No bulletins
        
        // Lightning Test - No bulletins
        
        // Icing / Freezing Test - No bulletins
        
        // Explosive Atmosphere Test - No bulletins
        
        // Acoustic Noise Test - No bulletins
        
        // Humidity Test
        { id: 50, subTestId: 24, name: 'INSITU Functional Check' },
        { id: 51, subTestId: 24, name: 'Post Humidity Functional Check' },
        
        // Post-QT Functional Test
        { id: 52, subTestId: 25, name: 'Visual Inspection' },
        { id: 53, subTestId: 25, name: 'Dimensional Check' },
        { id: 54, subTestId: 25, name: 'Functional Check' }
      ],
      showSubTestModal: false,
      showBulletinModal: false,
      editingSubTest: null,
      editingBulletin: null,
      subTestForm: { name: '' },
      bulletinForm: { name: '', subTestId: null },
      nextSubTestId: 26,
      nextBulletinId: 55
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
</style>

