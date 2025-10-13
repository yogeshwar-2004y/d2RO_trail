<template>
  <header class="app-header">
    <div class="header-content">
      <!-- Left Logo - DRDO -->
      <div class="logo-left">

        <img 
          src="/Users/avanthika/Documents/vista/Aviatrax/frontend/src/assets/images/DRDO.png" 
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
          src="@/assets/images/vista_logo.png" 
          alt="VISTA Logo" 
          class="logo-image"
        />
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader'
}
</script>

<style scoped>
.app-header {
  background-color: #DDEFFD; /* Light blue background */
  width: 100%;
  padding: 10px 10px; /* Reduced from 15px */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
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

.header-center {
  flex: 1;
  text-align: center;
  margin: 0 30x;
}

.logo-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin-bottom: 1px; /* Reduced spacing */
}

.aviatrax-logo {
  height: 120px; /* Increased from 70px */
  width: auto;
  object-fit: contain; /* Ensures complete image fits within container */
  max-width: 100%; /* Prevents image from overflowing */
}

.version-text {
  font-size: 1.5rem;
  font-weight: normal; /* Remove bold */
  color: #000;
  font-family: Arial, sans-serif;
}

.subtitle {
  font-size: 1.5rem; /* Increased from 0.8rem */
  font-weight: bold; /* Made bold */
  color: #000;
  margin: 1px 0 0 0; /* Reduced margin */
  font-family: Arial, sans-serif;
  width: 100%; /* Cover more horizontal area */
  max-width: 1000px; /* Allow wider subtitle */
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
}
</style>
