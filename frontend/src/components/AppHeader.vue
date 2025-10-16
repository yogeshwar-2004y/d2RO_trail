<template>
  <header class="app-header" :class="{ 'compact-header': !isLoginOrDashboard() }">
    <div class="header-content">
      <!-- Left Logo - DRDO -->
      <div class="logo-left">

        <img 
          src="@/assets/images/DRDO.png" 
          alt="DRDO Logo" 
          class="logo-image"
        />
      </div>
      
      <!-- Center Title/Brand -->
      <div class="header-center">
        <!-- Add Aviatrax logo image here -->
        <div class="logo-title-container">
          <img 
            src="@/assets/images/aviatrax-logo.png" 
            alt="Aviatrax Logo" 
            class="aviatrax-logo"
          />
          <span class="version-text">R1.25</span>
        </div>
        <p class="subtitle">ERP Software for QA Automation and Compliance Management</p>
      </div>
      
      <!-- Right Logo - VISTA -->
      <div class="logo-right">
        <img 

          src="@/assets/images/VISTA_5 Gradient_Sharp Edges.png"
          alt="VISTA Logo" 
          class="logo-image"
        />
      </div>
    </div>
  </header>
</template>

<script>
import { useRoute } from 'vue-router'

export default {
  name: 'AppHeader',
  setup() {
    const route = useRoute()
    
    // Check if current route is login or dashboard pages
    const isLoginOrDashboard = () => {
      const routeName = route.name
      return routeName === 'login' || 
             routeName === 'HomePageAdmin' || 
             routeName === 'HomePageDesigner' || 
             routeName === 'HomePageQAHead' || 
             routeName === 'HomePageReviewer' || 
             routeName === 'HomePageDesignHead'
    }
    
    return {
      isLoginOrDashboard
    }
  }
}
</script>

<style scoped>
.app-header {
  background-color: #DDEFFD; /* Light blue background */
  width: 100%;
  padding: 5px 5px; /* Reduced from 15px */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 0;
}

/* Compact header for non-login and non-dashboard pages */
.app-header.compact-header {
  height: 2.5cm; /* Set header height to exactly 2.5cm */
  padding: 3px 5px; /* Further reduced padding to fit within 2.5cm */
  display: flex;
  align-items: center; /* Center content vertically within the 2.5cm height */
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1350px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo-left,
.logo-right {
  flex: 0 0 auto;
}

.logo-image {
  height: 110px; /* Reduced from 120px */
  width: auto;
  object-fit: contain; /* Ensures complete image fits within container */
  max-width: 100%; /* Prevents image from overflowing */
}

/* Compact header logo sizes */
.app-header.compact-header .logo-image {
  height: 80px; /* Further reduced to fit better within 2.5cm header */
  padding: 0 200px;
}

.header-center {
  flex: 1;
  text-align: center;
  margin: 0 10px;
}

.logo-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1px;
  margin-bottom: 0px; /* Eliminated spacing */
}

.aviatrax-logo {
  height: 120px; /* Increased from 70px */
  width: auto;
  object-fit: contain; /* Ensures complete image fits within container */
  max-width: 1500px; /* Prevents image from overflowing */
}

/* Compact header Aviatrax logo */
.app-header.compact-header .aviatrax-logo {
  height: 90px; /* Further reduced to fit better within 2.5cm header */
}

.version-text {
  font-size: 0.7rem;
  font-weight: normal; /* Remove bold */
  color: #000;
  font-family: Arial, sans-serif;
}

/* Compact header version text */
.app-header.compact-header .version-text {
  font-size: 11px;
  font-style: italic; /* Reduced to fit within 2.5cm header */
}

.subtitle {
  font-size: 1.5rem; /* Increased from 0.8rem */
  font-weight: bold; /* Made bold */
  color: #000;
  margin: 0 0 0 0; /* Eliminated margin */
  font-family: Arial, sans-serif;
  width: 100%; /* Cover more horizontal area */
  max-width: 1100px; /* Allow wider subtitle */
}

/* Compact header subtitle */
.app-header.compact-header .subtitle {
  font-size: 0.8rem; /* Further reduced to fit better within 2.5cm header */
  margin-top: -12px;
  width: 100%;
  max-width: 1000px; /* Move subtitle up a little */
  white-space: nowrap; /* Prevent line wrapping */
  overflow: hidden; /* Hide overflow text */
  text-overflow: ellipsis; /* Show ellipsis if text is too long */
}



/* Responsive design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 10px;
  }
  
  .aviatrax-logo {
    height: 50px; /* Reduced for mobile */
  }
  
  .version-text {
    font-size: 1rem;
  }
  
  .subtitle {
    font-size: 0.5rem; /* Further reduced for mobile */
  }
  
  .logo-image {
    height: 40px; /* Reduced for mobile */
  }
  
  /* Compact header mobile styles */
  .app-header.compact-header .aviatrax-logo {
    height: 30px; /* Further reduced for mobile compact header */
  }
  
  .app-header.compact-header .version-text {
    font-size: 0.6rem; /* Reduced for mobile compact header */
  }
  
  .app-header.compact-header .subtitle {
    font-size: 0.35rem; /* Further reduced for mobile compact header */
  }
  
  .app-header.compact-header .logo-image {
    height: 20px; /* Further reduced for mobile compact header */
  }
}
</style>
