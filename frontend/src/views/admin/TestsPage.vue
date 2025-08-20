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
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>TESTS</th>
              <th v-for="(stage, index) in stages" :key="index">
                Stage {{ index + 1 }}
                <button @click="removeStage(index)" class="remove-stage-button">+</button>
              </th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(test, testIndex) in tests" :key="testIndex">
              <td>
                <span class="test-name">{{ test.name }}</span>
                <button @click="removeTest(testIndex)" class="remove-test-button">+</button>
              </td>
              <td v-for="(stage, stageIndex) in stages" :key="stageIndex">
                <select v-model="test.stages[stageIndex]" class="stage-select">
                  <option v-for="type in stageTypes" :key="type" :value="type">{{ type }}</option>
                </select>
              </td>
              <td>
                <button @click="addStage(testIndex)" class="add-stage-button">+</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="control-buttons">
        <button class="add-button" @click="addTest">+ Add tests</button>
        <button class="add-button" @click="addStage">+ Add Stage</button>
      </div>
      
      <button class="save-button" @click="saveChanges">SAVE CHANGES</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestsPage',
  data() {
    return {
      stages: [{}, {}, {}, {}], // Represents Stage 1, 2, 3, 4
      stageTypes: ['TYPE-1', 'TYPE-2', 'TYPE-3', 'TYPE-4'],
      tests: [
        { name: 'SOFT', stages: ['TYPE-1', 'TYPE-2', 'TYPE-3', 'TYPE-4'] },
        { name: 'QT', stages: ['TYPE-1', 'TYPE-2', 'TYPE-3', 'TYPE-4'] },
        { name: 'AT', stages: ['TYPE-1', 'TYPE-2', 'TYPE-3', 'TYPE-4'] },
        { name: 'DT', stages: ['TYPE-1', 'TYPE-2', 'TYPE-3', 'TYPE-4'] },
        { name: 'TS', stages: ['TYPE-1', 'TYPE-2', 'TYPE-3', 'TYPE-4'] },
        { name: 'ESS', stages: ['TYPE-1', 'TYPE-2', 'TYPE-3', 'TYPE-4'] },
      ],
    };
  },
  methods: {
    addTest() {
      // Logic to add a new test row
      const newStages = this.stages.map(() => '');
      const newTestName = prompt('Enter new test name:');
      if (newTestName) {
        this.tests.push({ name: newTestName, stages: newStages });
      }
    },
    removeTest(index) {
      // Logic to remove a test row
      if (confirm(`Are you sure you want to remove test ${this.tests[index].name}?`)) {
        this.tests.splice(index, 1);
      }
    },
    addStage() {
      // Logic to add a new stage column
      this.stages.push({});
      this.tests.forEach(test => test.stages.push(''));
    },
    removeStage(index) {
      // Logic to remove a stage column
      if (confirm(`Are you sure you want to remove Stage ${index + 1}?`)) {
        this.stages.splice(index, 1);
        this.tests.forEach(test => test.stages.splice(index, 1));
      }
    },
    saveChanges() {
      // Logic to save all changes to the backend
      console.log('Saving changes:', this.tests);
      alert('Changes saved successfully!');
    },
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

.save-button:hover {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}
</style>