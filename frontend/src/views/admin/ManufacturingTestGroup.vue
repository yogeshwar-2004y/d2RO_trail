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
      <span class="page-title">MANUFACTURING</span>
    </div>

    <div class="test-config-card">
      <div class="data-summary">
        <p>
          <strong>Test Group:</strong> Manufacturing | 
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
  name: "ManufacturingTestGroup",
  data() {
    return {
      subTests: [
        { id: 1, number: 1, name: "Raw Material Inspection" },
        { id: 2, number: 2, name: "Machined Part Inspection" },
        { id: 3, number: 3, name: "Assembly Inspection" },
        { id: 4, number: 4, name: "Kit of Part Inspection" },
        { id: 5, number: 5, name: "Bare PCB Inspection" },
        { id: 6, number: 6, name: "Assembled PCB Inspection" },
        { id: 7, number: 7, name: "SRU Level Testing" },
        { id: 8, number: 8, name: "SRU with Mechanical Assembly" },
        { id: 9, number: 9, name: "LRU Level Assembly Inspection" }
      ],
      columns: [
        { id: 'visual', name: 'Visual Inspection' },
        { id: 'dimensional', name: 'Dimensional Check' },
        { id: 'functional', name: 'Functional Check' },
        { id: 'tensile', name: 'Tensile Strength' },
        { id: 'ultrasonic', name: 'Ultrasonic Test' },
        { id: 'die_penetration', name: 'Die Penetration Test' },
        { id: 'chemical', name: 'Chemical Composition' }
      ],
      items: [
        // Raw Material Inspection
        { id: 1, subTestId: 1, columnId: 'tensile', name: 'Tensile Strength' },
        { id: 2, subTestId: 1, columnId: 'ultrasonic', name: 'Ultrasonic Test' },
        { id: 3, subTestId: 1, columnId: 'die_penetration', name: 'Die Penetration Test' },
        { id: 4, subTestId: 1, columnId: 'chemical', name: 'Chemical Composition' },
        
        // Machined Part Inspection
        { id: 5, subTestId: 2, columnId: 'visual', name: 'Visual Inspection' },
        { id: 6, subTestId: 2, columnId: 'dimensional', name: 'Dimensional Check' },
        
        // Assembly Inspection
        { id: 7, subTestId: 3, columnId: 'visual', name: 'Visual Inspection' },
        { id: 8, subTestId: 3, columnId: 'dimensional', name: 'Dimensional Check' },
        
        // Kit of Part Inspection
        { id: 9, subTestId: 4, columnId: 'visual', name: 'Kit of Part Inspection' },
        
        // Bare PCB Inspection
        { id: 10, subTestId: 5, columnId: 'visual', name: 'Bare PCB Inspection' },
        
        // Assembled PCB Inspection
        { id: 11, subTestId: 6, columnId: 'visual', name: 'Assembled PCB Inspection' },
        
        // SRU Level Testing
        { id: 12, subTestId: 7, columnId: 'functional', name: 'SRU Level Testing' },
        
        // SRU with Mechanical Assembly
        { id: 13, subTestId: 8, columnId: 'visual', name: 'Visual Inspection' },
        { id: 14, subTestId: 8, columnId: 'dimensional', name: 'Dimensional Check' },
        { id: 15, subTestId: 8, columnId: 'functional', name: 'Functional Check' },
        
        // LRU Level Assembly Inspection
        { id: 16, subTestId: 9, columnId: 'visual', name: 'Visual Inspection' },
        { id: 17, subTestId: 9, columnId: 'dimensional', name: 'Dimensional Check' },
        { id: 18, subTestId: 9, columnId: 'functional', name: 'Functional Check' }
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
