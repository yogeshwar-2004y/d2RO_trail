<template>
  <div class="designer-home">
    <!-- Header -->
    <header class="header">
      <div class="brand">
        <img src="@/assets/images/aviatrax-logo.png" alt="AVIATRAX Logo" class="logo-image">
      </div>
      <div class="logout-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="cards-container">
        <!-- Documents Card -->
        <div class="nav-card" @click="navigateToDocuments">
          <div class="card-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <line x1="10" y1="9" x2="8" y2="9"></line>
            </svg>
          </div>
          <div class="card-label">DOCUMENTS</div>
        </div>

        <!-- Memo Card -->
        <div class="nav-card" @click="navigateToMemo">
          <div class="card-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 20h9"></path>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
            </svg>
          </div>
          <div class="card-label">MEMO</div>
        </div>

        <!-- Test Reports Card -->
        <div class="nav-card" @click="navigateToTestReports">
          <div class="card-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 3v18h18"></path>
              <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path>
            </svg>
          </div>
          <div class="card-label">TEST REPORTS</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "HomePageDesigner",
  methods: {
    navigateToDocuments() {
      // Navigate to documents section
      this.$router.push({ name: 'ProjectsDashboard' });
    },
    navigateToMemo() {
      // Navigate to memo section
      console.log('Navigating to Memo');
      this.$router.push({ name: 'MemoDashboard' });
    },
    navigateToTestReports() {
      // Navigate to the test reports page
      this.$router.push({ name: 'ReportDashboard' });
    }
  }
};
</script>

<style scoped>
.designer-home {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* Header Styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0 20px;
  margin-bottom: 40px;
}

.brand {
  display: flex;
  align-items: center;
}

.logo-image {
  width: 150px;
}

.logout-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #000;
  padding: 10px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.logout-btn svg {
  transform: rotate(180deg);
  width: 30px;
  height: 30px;
}

/* Main Content Styles */
.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  padding: 20px;
}

.cards-container {
  display: flex;
  gap: 40px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

/* Navigation Card Styles */
.nav-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  width: 250px;
  height: 250px;
  padding: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.nav-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  border-color: rgba(0, 0, 0, 0.1);
}

.card-icon {
  color: #000;
  margin-bottom: 20px;
}

.card-label {
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
  color: #333;
  line-height: 1.3;
}

/* Responsive Design */
@media (max-width: 768px) {
  .cards-container {
    flex-direction: column;
    gap: 30px;
  }
  
  .nav-card {
    width: 220px;
    height: 220px;
  }
}
</style>
