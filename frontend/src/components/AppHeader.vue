<template>
  <header class="app-header">
    <div class="header-content">
      <!-- Left Logo - DRDO -->
      <div class="logo-left">
        <!-- Add DRDO logo image path here -->
        <img 
          src="" 
          alt="DRDO Logo" 
          class="logo-image"
        />
      </div>
      
      <!-- Center Title/Brand -->
      <div class="header-center">
        <!-- Add Aviatrax logo image here -->
        <img 
          src="@/assets/images/aviatrax-logo.png" 
          alt="Aviatrax Logo" 
          class="aviatrax-logo"
        />
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
  padding: 15px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  height: 80px; /* Increased from 60px */
  width: auto;
  object-fit: contain; /* Ensures complete image fits within container */
  max-width: 100%; /* Prevents image from overflowing */
}

.header-center {
  flex: 1;
  text-align: center;
  margin: 0 20px;
}

.aviatrax-logo {
  height: 100px; /* Increased from 80px */
  width: auto;
  object-fit: contain; /* Ensures complete image fits within container */
  max-width: 100%; /* Prevents image from overflowing */
  margin-bottom: 5px;
}

.subtitle {
  font-size: 0.8rem; /* Reduced from 1rem */
  color: #000;
  margin: 5px 0 0 0;
  font-family: Arial, sans-serif;
}

/* Responsive design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  
  .aviatrax-logo {
    height: 80px; /* Reduced for mobile but still larger than before */
  }
  
  .subtitle {
    font-size: 0.7rem; /* Further reduced for mobile */
  }
  
  .logo-image {
    height: 60px; /* Reduced for mobile but still larger than before */
  }
}
</style>
