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

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>SUB-TEST TYPES</th>
              <th v-for="column in columns" :key="column.id">
                {{ column.name }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="subTest in subTests" :key="subTest.id">
              <td class="sub-test-name">
                {{ subTest.number }}. {{ subTest.name }}
              </td>
              <td v-for="column in columns" :key="column.id">
                <div v-if="getItemsForSubTestAndColumn(subTest.id, column.id).length > 0" class="items-container">
                  <div v-for="item in getItemsForSubTestAndColumn(subTest.id, column.id)" :key="item.id" class="item">
                    {{ item.name }}
                  </div>
                </div>
                <div v-else class="empty-cell">
                  -
                </div>
              </td>
            </tr>
          </tbody>
        </table>
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
      columns: [
        { id: 'visual', name: 'Visual Inspection' },
        { id: 'functional', name: 'Functional Check' },
        { id: 'dimensional', name: 'Dimensional Check' },
        { id: 'insitu', name: 'INSITU Functional Check' },
        { id: 'post_ht', name: 'Post HT Functional Check' },
        { id: 'post_lt', name: 'Post LT Functional Check' },
        { id: 'initial_resonance', name: 'Initial Resonance test' },
        { id: 'x_axis', name: 'X Axis' },
        { id: 'y_axis', name: 'Y Axis' },
        { id: 'z_axis', name: 'Z Axis' },
        { id: 'final_resonance', name: 'Final Resonance Research' },
        { id: 'post_rv', name: 'Post RV Functional Check' },
        { id: 'radiated_emission', name: 'Radiated Emission Test' },
        { id: 'conducted_emission', name: 'Conducted Emission Test' },
        { id: 'radiated_susceptibility', name: 'Radiated Susceptibility Test' },
        { id: 'conducted_susceptibility', name: 'Conducted Susceptibility Test' },
        { id: 'dc_test', name: 'DC Test (LDC)' },
        { id: 'single_phase_ac', name: 'Single Phase AC (SAC)' },
        { id: 'three_phase_ac', name: 'Three Phase AC (TAC)' },
        { id: 'altitude', name: 'Altitude' },
        { id: 'low_temp', name: 'Low temperature' },
        { id: 'high_temp', name: 'High temperature' },
        { id: 'humidity', name: 'Humidity' },
        { id: 'post_humidity', name: 'Post Humidity Functional Check' },
        { id: 'endurance_vibration', name: 'Endurance Vibration Test' },
        { id: 'acceleration', name: 'Acceleration Test' },
        { id: 'shock_crash', name: 'Shock Crash Hazard' },
        { id: 'rapid_decomposition', name: 'Rapid Decomposition Test' },
        { id: 'explosive_atmosphere', name: 'Explosive Atmosphere Test' },
        { id: 'humidity_test', name: 'Humidity Test' },
        { id: 'cath', name: 'CATH Test' }
      ],
      items: [
        // Pre-SoFT Functional Test
        { id: 1, subTestId: 1, columnId: 'visual', name: 'Visual Inspection' },
        { id: 2, subTestId: 1, columnId: 'dimensional', name: 'Dimensional Check' },
        { id: 3, subTestId: 1, columnId: 'functional', name: 'Functional Check' },
        
        // Low Pressure (Altitude Test)
        { id: 4, subTestId: 2, columnId: 'altitude', name: 'Low Pressure (Altitude Test)' },
        
        // High Temperature Test
        { id: 5, subTestId: 3, columnId: 'high_temp', name: 'High Temperature Test' },
        { id: 6, subTestId: 3, columnId: 'insitu', name: 'INSITU Functional Check' },
        { id: 7, subTestId: 3, columnId: 'post_ht', name: 'Post HT Functional Check' },
        
        // Low Temperature Test
        { id: 8, subTestId: 4, columnId: 'low_temp', name: 'Low Temperature Test' },
        { id: 9, subTestId: 4, columnId: 'insitu', name: 'INSITU Functional Check' },
        { id: 10, subTestId: 4, columnId: 'post_lt', name: 'Post LT Functional Check' },
        
        // Endurance Vibration Test
        { id: 11, subTestId: 5, columnId: 'endurance_vibration', name: 'Endurance Vibration Test' },
        { id: 12, subTestId: 5, columnId: 'initial_resonance', name: 'Initial Resonance test' },
        { id: 13, subTestId: 5, columnId: 'insitu', name: 'INSITU Functional Check' },
        { id: 14, subTestId: 5, columnId: 'x_axis', name: 'X Axis' },
        { id: 15, subTestId: 5, columnId: 'y_axis', name: 'Y Axis' },
        { id: 16, subTestId: 5, columnId: 'z_axis', name: 'Z Axis' },
        { id: 17, subTestId: 5, columnId: 'final_resonance', name: 'Final Resonance Research' },
        { id: 18, subTestId: 5, columnId: 'post_rv', name: 'Post RV Functional Check' },
        { id: 19, subTestId: 5, columnId: 'visual', name: 'Visual Inspection' },
        { id: 20, subTestId: 5, columnId: 'dimensional', name: 'Dimensional Check' },
        { id: 21, subTestId: 5, columnId: 'functional', name: 'Functional Check' },
        
        // EMI / EMC
        { id: 22, subTestId: 6, columnId: 'radiated_emission', name: 'Radiated Emission Test' },
        { id: 23, subTestId: 6, columnId: 'conducted_emission', name: 'Conducted Emission Test' },
        { id: 24, subTestId: 6, columnId: 'radiated_susceptibility', name: 'Radiated Susceptibility Test' },
        { id: 25, subTestId: 6, columnId: 'conducted_susceptibility', name: 'Conducted Susceptibility Test' },
        
        // POWER SUPPLY TEST
        { id: 26, subTestId: 7, columnId: 'dc_test', name: 'DC Test (LDC)' },
        { id: 27, subTestId: 7, columnId: 'single_phase_ac', name: 'Single Phase AC (SAC)' },
        { id: 28, subTestId: 7, columnId: 'three_phase_ac', name: 'Three Phase AC (TAC)' },
        
        // CATH Test
        { id: 29, subTestId: 8, columnId: 'cath', name: 'CATH (Combined Altitude Temperature Humidity Test)' },
        { id: 30, subTestId: 8, columnId: 'altitude', name: 'Altitude' },
        { id: 31, subTestId: 8, columnId: 'low_temp', name: 'Low temperature' },
        { id: 32, subTestId: 8, columnId: 'high_temp', name: 'High temperature' },
        { id: 33, subTestId: 8, columnId: 'humidity', name: 'Humidity' },
        
        // Acceleration Test
        { id: 34, subTestId: 9, columnId: 'acceleration', name: 'Acceleration Test' },
        
        // Shock Crash Hazard
        { id: 35, subTestId: 10, columnId: 'shock_crash', name: 'Shock Crash Hazard' },
        
        // Rapid Decomposition Test
        { id: 36, subTestId: 11, columnId: 'rapid_decomposition', name: 'Rapid Decomposition Test' },
        
        // Explosive Atmosphere Test
        { id: 37, subTestId: 12, columnId: 'explosive_atmosphere', name: 'Explosive Atmosphere Test' },
        
        // Humidity Test
        { id: 38, subTestId: 13, columnId: 'humidity_test', name: 'Humidity Test' },
        { id: 39, subTestId: 13, columnId: 'insitu', name: 'INSITU Functional Check' },
        { id: 40, subTestId: 13, columnId: 'post_humidity', name: 'Post Humidity Functional Check' },
        
        // Post-SoFT Functional Test
        { id: 41, subTestId: 14, columnId: 'visual', name: 'Visual Inspection' },
        { id: 42, subTestId: 14, columnId: 'dimensional', name: 'Dimensional Check' },
        { id: 43, subTestId: 14, columnId: 'functional', name: 'Functional Check' }
      ]
    };
  },
  computed: {
    totalItems() {
      return this.items.length;
    }
  },
  methods: {
    getItemsForSubTestAndColumn(subTestId, columnId) {
      return this.items.filter(item => 
        item.subTestId === subTestId && item.columnId === columnId
      );
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

.table-container {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th,
td {
  border: 1px solid #ccc;
  padding: 12px;
  text-align: center;
  vertical-align: top;
}

th {
  background-color: #f8f8f8;
  font-weight: bold;
  color: #2c3e50;
}

.sub-test-name {
  font-weight: bold;
  text-align: left;
  background-color: #f8f9fa;
  color: #2c3e50;
  min-width: 200px;
}

.items-container {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.item {
  background-color: #e8f4fd;
  border: 1px solid #b3d9ff;
  border-radius: 4px;
  padding: 6px 8px;
  font-size: 0.9em;
  color: #2c3e50;
}

.empty-cell {
  color: #6c757d;
  font-style: italic;
  background: #f8f9fa;
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

/* Responsive design */
@media (max-width: 768px) {
  .test-group-page {
    padding: 15px;
  }
  
  .test-config-card {
    padding: 20px;
  }
  
  .sub-test-name {
    min-width: 150px;
    font-size: 0.9em;
  }
  
  .item {
    font-size: 0.8em;
    padding: 4px 6px;
  }
}
</style>
