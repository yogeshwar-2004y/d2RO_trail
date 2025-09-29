<template>
  <div class="template-dashboard">
    <div class="header">
      <div class="header-left">
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
      </div>
      <div class="header-center">
        <div class="page-title">
          <svg class="title-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          <span class="title-text">TEMPLATE DASHBOARD</span>
        </div>
      </div>
      <div class="header-right">
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search Templates" class="search-input">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading templates...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <div class="error-message">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        <h3>Error Loading Templates</h3>
        <p>{{ error }}</p>
        <button @click="loadTemplates" class="retry-button">Retry</button>
      </div>
    </div>
    
    <div v-else class="template-grid">
      <div 
        v-for="template in filteredTemplates" 
        :key="template.name" 
        class="template-card" 
        @click="viewTemplate(template)"
      >
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
        </div>
        <span class="card-title">{{ template.displayName }}</span>
        <span class="card-description">{{ template.description }}</span>
      </div>
      
      <div v-if="filteredTemplates.length === 0" class="no-templates">
        <div class="no-templates-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <h3>No Templates Found</h3>
        <p>No templates match your current search.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TemplateDashboard',
  data() {
    return {
      searchQuery: '',
      templates: [],
      loading: true,
      error: null,
    };
  },
  computed: {
    filteredTemplates() {
      if (!this.searchQuery) {
        return this.templates;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.templates.filter(template => 
        template.displayName.toLowerCase().includes(query) ||
        template.description.toLowerCase().includes(query)
      );
    },
  },
  mounted() {
    this.loadTemplates();
  },
  methods: {
    loadTemplates() {
      try {
        this.loading = true;
        this.error = null;
        
        // Define available templates
        this.templates = [
          {
            name: 'ObservationReport',
            displayName: 'Observation Report',
            description: 'Template for creating observation reports with detailed analysis',
            component: 'ObservationReport'
          }
        ];
        
        this.loading = false;
      } catch (error) {
        console.error('Error loading templates:', error);
        this.error = error.message;
        this.loading = false;
      }
    },
    
    viewTemplate(template) {
      // Navigate to template viewer
      this.$router.push({
        name: 'TemplateViewer',
        params: {
          templateName: template.name,
          templateDisplayName: template.displayName
        }
      });
    }
  }
};
</script>

<style scoped>
.template-dashboard {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
}

.logo {
  width: 150px;
}

.header-center {
  display: flex;
  align-items: center;
  flex-grow: 1;
  justify-content: center;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  color: #555;
  width: 32px;
  height: 32px;
}

.title-text {
  font-size: 1.5em;
  font-weight: bold;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-box {
  position: relative;
}

.search-input {
  width: 250px;
  padding: 10px 15px;
  padding-left: 40px;
  border: 1px solid #ccc;
  border-radius: 25px;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 25px;
  padding: 30px;
}

.template-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 200px;
  text-align: center;
  border: 2px solid transparent;
}

.template-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  border-color: #667eea;
}

.card-icon {
  margin-bottom: 15px;
}

.card-icon svg {
  color: #667eea;
  width: 48px;
  height: 48px;
}

.card-title {
  font-size: 1.1em;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.card-description {
  font-size: 0.9em;
  color: #666;
  line-height: 1.4;
}

/* Loading, Error, and No Templates States */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.error-message {
  text-align: center;
  max-width: 400px;
}

.error-message svg {
  color: #e74c3c;
  margin-bottom: 20px;
}

.error-message h3 {
  color: #e74c3c;
  margin-bottom: 10px;
}

.error-message p {
  color: #666;
  margin-bottom: 20px;
}

.retry-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.retry-button:hover {
  background-color: #2980b9;
}

.no-templates {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  grid-column: 1 / -1;
}

.no-templates-icon {
  margin-bottom: 20px;
}

.no-templates-icon svg {
  color: #bdc3c7;
}

.no-templates h3 {
  color: #7f8c8d;
  margin-bottom: 10px;
}

.no-templates p {
  color: #95a5a6;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 20px;
    padding: 15px 20px;
  }
  
  .header-right {
    flex-direction: column;
    gap: 15px;
    width: 100%;
  }
  
  .search-box {
    width: 100%;
  }
  
  .search-input {
    width: 100%;
  }
  
  .template-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    padding: 20px;
  }
  
  .template-card {
    height: 180px;
    padding: 20px;
  }
}
</style>
