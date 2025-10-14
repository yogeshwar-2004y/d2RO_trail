<template>
  <div class="test-group-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <span class="page-title">ESS - ENVIRONMENTAL STRESS SCREENING</span>
    </div>

    <div class="test-config-card">
      <div class="data-summary">
        <p>
          <strong>Test Group:</strong> ESS (Environmental Stress Screening) | 
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
  name: "ESSTestGroup",
  data() {
    return {
      subTests: [
        { id: 1, number: 1, name: "Pre-ESS Functional Test" },
        { id: 2, number: 2, name: "Power Burn-in / Burn-in Test" },
        { id: 3, number: 3, name: "Pre Thermal Vibration Test (RV1)" },
        { id: 4, number: 4, name: "Thermal Cycling" },
        { id: 5, number: 5, name: "Post Thermal Vibration Test (RV2)" },
        { id: 6, number: 6, name: "Final Functional Test" }
      ],
      bulletins: [
        // Pre-ESS Functional Test
        // { id: 1, subTestId: 1, name: 'Pre-ESS Functional Test' },
        {},
        // Power Burn-in / Burn-in Test
        // { id: 2, subTestId: 2, name: 'Power Burn-in / Burn-in Test' },
        {},
        // Pre Thermal Vibration Test (RV1)
        { id: 3, subTestId: 3, name: 'Pre-Vibration Visual Inspection' },
        { id: 4, subTestId: 3, name: 'Pre-Vibration Functional Test' },
        { id: 5, subTestId: 3, name: 'INSITU Functional Check' },
        { id: 6, subTestId: 3, name: 'Post Vibration Functional Check' },
        
        // Thermal Cycling
        { id: 7, subTestId: 4, name: 'Pre Thermal Visual Inspection' },
        { id: 8, subTestId: 4, name: 'Pre-Thermal Functional Test' },
        { id: 9, subTestId: 4, name: 'INSITU Functional Check', parentBulletinId: null },
        { id: 10, subTestId: 4, name: '10 Cycles – High Temperature', parentBulletinId: 9 },
        { id: 11, subTestId: 4, name: '10 Cycles – Low Temperature', parentBulletinId: 9 },
        { id: 12, subTestId: 4, name: 'Post Thermal Functional Check' },
        { id: 13, subTestId: 4, name: 'Post Thermal Visual Inspection' },
        
        // Post Thermal Vibration Test (RV2)
        { id: 15, subTestId: 5, name: 'Visual Inspection' },
        { id: 16, subTestId: 5, name: 'Pre-Vibration Functional Test' },
        { id: 17, subTestId: 5, name: 'INSITU Functional Check' },
        { id: 18, subTestId: 5, name: 'Post Vibration Functional Check' },
        
        // Final Functional Test
        { id: 19, subTestId: 6, name: 'Visual Inspection' },
        { id: 20, subTestId: 6, name: 'Dimensional Check' },
        { id: 21, subTestId: 6, name: 'Functional Check' }
      ],
      showSubTestModal: false,
      showBulletinModal: false,
      editingSubTest: null,
      editingBulletin: null,
      subTestForm: { name: '' },
      bulletinForm: { name: '', subTestId: null },
      nextSubTestId: 7,
      nextBulletinId: 22
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

