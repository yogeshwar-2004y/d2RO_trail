<template>
  <div class="tests-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
      <span class="page-title">TESTS</span>
    </div>

    <div class="test-config-card">
      <div v-if="loading" class="loading-message">
        Loading tests and stages...
      </div>
      
            <div v-else>
        <div class="data-summary">
          <p><strong>Tests:</strong> {{ tests.length }} | <strong>Stages:</strong> {{ stages.length }} | <strong>Stage Types:</strong> {{ stageTypes.length }}</p>
        </div>

        <div v-if="tests.length === 0 && stages.length === 0" class="empty-state">
          <p>No tests or stages found. Start by adding some tests and stages to configure your testing matrix.</p>
        </div>

        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th>TESTS</th>
                <th v-if="stages.length === 0" class="no-stages-message">
                  No stages added yet
                </th>
                <th v-for="stage in stages" :key="stage.stage_id">
                  {{ stage.stage_name }}
                  <button @click="removeStage(stage.stage_id)" class="remove-stage-button">×</button>
                </th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="tests.length === 0">
                <td :colspan="stages.length + 2" class="no-tests-message">
                  No tests added yet. Click "+ Add Test" to get started.
                </td>
              </tr>
              <tr v-for="test in tests" :key="test.test_id">
                <td>
                  <span class="test-name">{{ test.test_name }}</span>
                  <button @click="removeTest(test.test_id)" class="remove-test-button">×</button>
                </td>
                <td v-if="stages.length === 0" class="empty-cell">
                  Add stages to configure
                </td>
                <td v-for="stage in stages" :key="stage.stage_id">
                  <select v-model="testStageConfigs[test.test_id + '_' + stage.stage_id]" class="stage-select">
                    <option value="">Select Type</option>
                    <option v-for="type in stageTypes" :key="type.type_id" :value="type.type_id">
                      {{ type.type_name }}
                    </option>
                  </select>
                </td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="control-buttons">
          <button class="add-button" @click="addTest">+ Add Test</button>
          <button class="add-button" @click="addStage">+ Add Stage</button>
        </div>
        
        <button class="save-button" @click="saveChanges" :disabled="saving">
          {{ saving ? 'SAVING...' : 'SAVE CHANGES' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'TestsPage',
  data() {
    return {
      tests: [],
      stages: [],
      stageTypes: [],
      testStageConfigs: {}, // Maps test_id_stage_id to type_id
      loading: false,
      saving: false,
      error: null
    };
  },
  computed: {
    // Get current user from global store
    currentUser() {
      return userStore.getters.currentUser()
    },
    isLoggedIn() {
      return userStore.getters.isLoggedIn()
    }
  },
  async mounted() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      try {
        this.loading = true;
        this.error = null;

        // Fetch complete configuration matrix from the new endpoint
        const response = await fetch('http://localhost:5000/api/tests-configuration');
        const data = await response.json();

        if (data.success) {
          // Set all data from the single response
          this.tests = data.tests || [];
          this.stages = data.stages || [];
          this.stageTypes = data.stage_types || [];

          // Map configurations to the format expected by the UI
          this.testStageConfigs = {};
          if (data.configurations) {
            data.configurations.forEach(config => {
              const key = config.test_id + '_' + config.stage_id;
              this.testStageConfigs[key] = config.type_id;
            });
          }

          console.log('Loaded data:', {
            tests: this.tests.length,
            stages: this.stages.length,
            stageTypes: this.stageTypes.length,
            configurations: Object.keys(this.testStageConfigs).length
          });

        } else {
          this.error = data.message || 'Failed to load data';
          alert('Error loading data: ' + this.error);
        }

      } catch (error) {
        console.error('Error loading data:', error);
        this.error = 'Failed to load data. Please check if the backend is running.';
        alert(this.error);
      } finally {
        this.loading = false;
      }
    },

    async addTest() {
      const newTestName = prompt('Enter new test name:');
      if (!newTestName || newTestName.trim() === '') {
        return;
      }

      try {
        const response = await fetch('http://localhost:5000/api/tests', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ test_name: newTestName.trim() })
        });

        const data = await response.json();

        if (data.success) {
          // Reload data to get the new test
          await this.loadData();
          alert('Test added successfully!');
        } else {
          alert('Error adding test: ' + data.message);
        }
      } catch (error) {
        console.error('Error adding test:', error);
        alert('Error adding test. Please check if the backend is running.');
      }
    },

    async removeTest(testId) {
      const test = this.tests.find(t => t.test_id === testId);
      if (!test) return;

      if (!confirm(`Are you sure you want to remove test "${test.test_name}"?`)) {
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/tests/${testId}`, {
          method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
          // Reload data to reflect the deletion
          await this.loadData();
          alert('Test removed successfully!');
        } else {
          alert('Error removing test: ' + data.message);
        }
      } catch (error) {
        console.error('Error removing test:', error);
        alert('Error removing test. Please check if the backend is running.');
      }
    },

    async addStage() {
      const newStageName = prompt('Enter new stage name:');
      if (!newStageName || newStageName.trim() === '') {
        return;
      }

      try {
        const response = await fetch('http://localhost:5000/api/stages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ stage_name: newStageName.trim() })
        });

        const data = await response.json();

        if (data.success) {
          // Reload data to get the new stage
          await this.loadData();
          alert('Stage added successfully!');
        } else {
          alert('Error adding stage: ' + data.message);
        }
      } catch (error) {
        console.error('Error adding stage:', error);
        alert('Error adding stage. Please check if the backend is running.');
      }
    },

    async removeStage(stageId) {
      const stage = this.stages.find(s => s.stage_id === stageId);
      if (!stage) return;

      if (!confirm(`Are you sure you want to remove stage "${stage.stage_name}"?`)) {
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/stages/${stageId}`, {
          method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
          // Reload data to reflect the deletion
          await this.loadData();
          alert('Stage removed successfully!');
        } else {
          alert('Error removing stage: ' + data.message);
        }
      } catch (error) {
        console.error('Error removing stage:', error);
        alert('Error removing stage. Please check if the backend is running.');
      }
    },

    async saveChanges() {
      try {
        this.saving = true;

        // Build configurations from current UI state
        const configurations = [];
        
        for (const test of this.tests) {
          for (const stage of this.stages) {
            const key = test.test_id + '_' + stage.stage_id;
            const typeId = this.testStageConfigs[key];
            
            if (typeId && typeId !== '') {
              configurations.push({
                test_id: test.test_id,
                stage_id: stage.stage_id,
                type_id: typeId
              });
            }
          }
        }

        const response = await fetch('http://localhost:5000/api/test-stage-types', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            configurations: configurations,
            assigned_by: this.getCurrentUserId()
          })
        });

        const data = await response.json();

        if (data.success) {
      alert('Changes saved successfully!');
          // Reload data to ensure consistency
          await this.loadData();
        } else {
          alert('Error saving changes: ' + data.message);
        }

      } catch (error) {
        console.error('Error saving changes:', error);
        alert('Error saving changes. Please check if the backend is running.');
      } finally {
        this.saving = false;
      }
    },

    getCurrentUserId() {
      // Get current user from global store or return default
      return this.currentUser?.id || 1002; // Default fallback
    }
  },
};
</script>

<style scoped>
.tests-page {
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
  max-width: 1000px;
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

.test-config-card {
  width: 100%;
  max-width: 1000px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.table-container {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
  position: relative;
}

th {
  background-color: #f8f8f8;
  font-weight: bold;
}

.test-name {
  display: block;
  font-weight: bold;
}

.stage-select {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 1em;
}

.remove-test-button, .remove-stage-button {
  position: absolute;
  top: 50%;
  right: -10px;
  transform: translateY(-50%) rotate(45deg);
  background-color: #ff4d4f;
  color: #fff;
  border-radius: 50%;
  border: none;
  width: 20px;
  height: 20px;
  font-size: 1.2em;
  line-height: 1;
  padding: 0;
  cursor: pointer;
}

.control-buttons {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  gap: 15px;
  margin-top: 20px;
}

.add-button {
  background: none;
  border: 1px dashed #ccc;
  border-radius: 10px;
  padding: 10px 15px;
  font-weight: bold;
  cursor: pointer;
  color: #555;
  transition: all 0.3s ease;
}

.add-button:hover {
  background-color: #f0f0f0;
}

.save-button {
  width: 50%;
  padding: 15px;
  border: none;
  border-radius: 25px;
  font-size: 1.1em;
  color: #fff;
  background: linear-gradient(to right, #9fe6a0, #5cb85c);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 30px;
}

.save-button:hover:not(:disabled) {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-message {
  text-align: center;
  font-size: 1.2em;
  color: #666;
  padding: 50px;
  font-style: italic;
}

.data-summary {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  text-align: center;
}

.data-summary p {
  margin: 0;
  color: #495057;
  font-size: 1.1em;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #6c757d;
  font-style: italic;
  background: #f8f9fa;
  border-radius: 10px;
  border: 2px dashed #dee2e6;
  margin-bottom: 20px;
}

.empty-state p {
  margin: 0;
  font-size: 1.1em;
}

.no-stages-message, .no-tests-message {
  color: #6c757d;
  font-style: italic;
  text-align: center;
  padding: 20px;
}

.empty-cell {
  color: #6c757d;
  font-style: italic;
  text-align: center;
  padding: 10px;
  background: #f8f9fa;
}
</style>