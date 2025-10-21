<template>
  <div class="user-activities-page">
    <button class="back-button" @click="$router.go(-1)">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
    <div class="card-container">
      <div class="card" @click="goToPage('AddUpdateProjects')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <span class="card-title">ADD / UPDATE PROJECTS</span>
      </div>
      <div class="card" @click="goToPage('AddUpdateUsers')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="8.5" cy="7" r="4"></circle>
            <line x1="20" y1="8" x2="20" y2="14"></line>
            <line x1="23" y1="11" x2="17" y2="11"></line>
          </svg>
        </div>
        <span class="card-title">ADD / UPDATE USERS</span>
      </div>
      <div class="card" @click="goToPage('ActivityLogs')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="12" y1="1" x2="12" y2="23"></line>
          <path d="M12 12h-3"></path>
          <path d="M12 16h-2"></path>
          </svg>
        </div>
        <span class="card-title">ACTIVITY LOGS</span>
      </div>
      <div class="card" @click="goToPage('Tests')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 11 12 14 22 4"></polyline>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
          </svg>
        </div>
        <span class="card-title">TESTS</span>
      </div>
      <div class="card" @click="goToPage('NewsUpdates')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2z"></path>
            <path d="M6 12h8"></path>
            <path d="M6 16h8"></path>
            <path d="M6 8h8"></path>
          </svg>
        </div>
        <span class="card-title">NEWS UPDATES</span>
      </div>
      <div class="card" @click="goToPage('CustomiseBackground')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="9" cy="9" r="2"></circle>
            <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
          </svg>
        </div>
        <span class="card-title">CUSTOMISE BACKGROUND</span>
      </div>
      <div class="card" @click="goToPage('TechSupport')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 12l2 2 4-4"></path>
            <path d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"></path>
            <path d="M3 12v6c0 .552.448 1 1 1h16c.552 0 1-.448 1-1v-6"></path>
          </svg>
        </div>
        <span class="card-title">TECH SUPPORT</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserActivities",
  methods: {
    goToPage(pageName) {
      if (pageName === "AddUpdateProjects") {
        this.$router.push({ name: "AddUpdateProjects" });
      } else if (pageName === "AddUpdateUsers") {
        this.$router.push({ name: "AddUpdateUser" });
      } else if (pageName === "ActivityLogs") {
        this.$router.push({ name: "ActivityLogs" });
      } else if (pageName === "Tests") {
        this.$router.push({ name: "MajorTestGroups" });
      } else if (pageName === "NewsUpdates") {
        this.$router.push({ name: "NewsUpdates" });
      } else if (pageName === "CustomiseBackground") {
        this.$router.push({ name: "CustomiseBackground" });
      } else if (pageName === "TechSupport") {
        this.$router.push({ name: "TechSupportManagement" });
      }
    },
  },
};
</script>

<style scoped>
.user-activities-page {
  background-color: #f0f0f0;
  min-height: calc(100vh - 240px);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 40px 20px;
  margin: 0;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  justify-items: center;
  align-items: start;
}

.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 250px;
  height: 200px;
  padding: 20px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Center the last 3 cards in the bottom row */
.card:nth-child(n+5) {
  grid-column: span 1;
}

/* Center the bottom row with 3 cards */
.card:nth-child(5) {
  grid-column: 1;
}

.card:nth-child(6) {
  grid-column: 2;
}

.card:nth-child(7) {
  grid-column: 3;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-icon {
  color: #000;
  margin-bottom: 15px;
}

.card-title {
  font-size: 0.85em;
  font-weight: bold;
  text-align: center;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  line-height: 1.2;
  margin-top: 10px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  position: absolute;
  left: 90px;
  top: 180px;
}
.back-button:hover {
  color: #0056b3;
  background-color: #e9ecef;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .card-container {
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
  }
  
  .card {
    max-width: 220px;
    height: 180px;
  }
  
  /* Adjust for 3-3-1 layout on medium screens */
  .card:nth-child(5) {
    grid-column: 1;
  }
  
  .card:nth-child(6) {
    grid-column: 2;
  }
  
  .card:nth-child(7) {
    grid-column: 3;
  }
}

@media (max-width: 768px) {
  .card-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    padding: 0 10px;
  }
  
  .card {
    max-width: 200px;
    height: 180px;
    padding: 15px;
  }
  
  .card-title {
    font-size: 0.75em;
  }
  
  /* Reset grid positioning for mobile */
  .card:nth-child(n+5) {
    grid-column: auto;
  }
}

@media (max-width: 480px) {
  .card-container {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .card {
    width: 100%;
    max-width: 280px;
    height: 160px;
  }
}
</style>

