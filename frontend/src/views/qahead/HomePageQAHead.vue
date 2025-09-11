<template>
  <div class="home-page">
    <header class="app-header">
      <div class="logos-container">
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
        <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
      </div>
      <button class="logout-button" @click="logout">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
      </button>
    </header>
    <div class="card-container">
      <div class="card" @click="goToPage('QAHeadProjectsDashboard')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
        </div>
        <div class="card-title">PLAN DOCUMENTS</div>
      </div>
      <div class="card" @click="goToPage('QAHeadMemoDashboard')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"></path>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
          </svg>
        </div>
        <div class="card-title">MEMO</div>
      </div>
      <div class="card" @click="goToPage('QAHeadReportDashboard')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 3v18h18"></path>
            <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path>
          </svg>
        </div>
        <div class="card-title">REPORTS</div>
      </div>
    </div>
    
    <!-- News Ticker at the bottom -->
    <NewsTicker 
      height="60px" 
      backgroundColor="#34495e" 
      textColor="#ffffff"
      class="dashboard-news-ticker"
    />
  </div>
</template>

<script>
import NewsTicker from '@/components/NewsTicker.vue'

export default {
  name: 'HomePageQAHead',
  components: {
    NewsTicker
  },
  methods: {
    goToPage(pageName) {
      if (pageName === 'QAHeadProjectsDashboard') {
        this.$router.push({ name: 'ProjectsDashboard' }); //QAHeadProjectsDashboard
      } else if (pageName === 'QAHeadMemoDashboard') {
        this.$router.push({ name: 'MemoDashboard' }); //QAHeadMemoDashboard
      } else if (pageName === 'QAHeadReportDashboard') {
        this.$router.push({ name: 'ReportDashboard' }); //QAHeadReportDashboard
      }
    },
    logout() {
      this.$router.push({ name: 'login' });
    }
  }
};
</script>

<style scoped>
.home-page {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0 20px;
  margin-bottom: 40px;
}

.logos-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo {
  width: 150px;
}

.vista-logo {
  width: 120px;
}

.logout-button {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #000;
  padding: 10px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.logout-button svg {
  transform: rotate(180deg);
  width: 30px;
  height: 30px;
}

.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  gap: 40px;
  padding: 20px;
}

.card {
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

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  border-color: rgba(0, 0, 0, 0.1);
}

.card-icon {
  color: #000;
  margin-bottom: 20px;
}

.card-title {
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
  color: #333;
  line-height: 1.3;
}

@media (max-width: 768px) {
  .card-container {
    flex-direction: column;
    gap: 30px;
  }
  
  .card {
    width: 220px;
    height: 220px;
  }
}

.dashboard-news-ticker {
  margin-top: auto;
  position: sticky;
  bottom: 0;
}
</style>
