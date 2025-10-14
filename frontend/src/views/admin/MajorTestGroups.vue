<template>
  <div class="major-test-groups-page">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    </div>

    <div class="page-title">
      <h1>Major Test Groups</h1>
      <p>Select a major test group to view detailed inspection stages</p>
    </div>

    <div class="card-grid">
      <div class="card" @click="goToGroup('Manufacturing')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
        </div>
        <span class="card-title">MANUFACTURING</span>
        <span class="card-subtitle">Raw Material, Machined Parts, Assembly & PCB Inspection</span>
      </div>

      <div class="card" @click="goToGroup('CoTS Screening')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
            <path d="M9 9l3 3 3-3"></path>
          </svg>
        </div>
        <span class="card-title">CoTS SCREENING</span>
        <span class="card-subtitle">Visual Inspection, Functional Check & Power Burn-In</span>
      </div>

      <div class="card" @click="goToGroup('ESS')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
            <line x1="12" y1="22.08" x2="12" y2="12"></line>
          </svg>
        </div>
        <span class="card-title">ESS </span>
        <span class="card-subtitle">Environmental Stress Screening & Thermal Cycling</span>
      </div>

      <div class="card" @click="goToGroup('QT')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 11 12 14 22 4"></polyline>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
        </div>
        <span class="card-title">QT</span>
        <span class="card-subtitle">Qualification Test - Comprehensive Testing Suite</span>
      </div>

      <div class="card" @click="goToGroup('SoFT')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
            <path d="M2 17l10 5 10-5"></path>
            <path d="M2 12l10 5 10-5"></path>
          </svg>
        </div>
        <span class="card-title">SOFT</span>
        <span class="card-subtitle">Safety of Flight Test - Critical Safety Validation</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MajorTestGroups",
  methods: {
    goToGroup(groupName) {
      if (groupName === "Manufacturing") {
        this.$router.push({ name: "ManufacturingTestGroup" });
      } else if (groupName === "CoTS Screening") {
        this.$router.push({ name: "CoTSScreeningTestGroup" });
      } else if (groupName === "ESS") {
        this.$router.push({ name: "ESSTestGroup" });
      } else if (groupName === "QT") {
        this.$router.push({ name: "QTTestGroup" });
      } else if (groupName === "SoFT") {
        this.$router.push({ name: "SoFTTestGroup" });
      }
    },
  },
};
</script>

<style scoped>
.major-test-groups-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f0f0f0;
}

.header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  padding: 20px 30px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 20px;
}
</style>

