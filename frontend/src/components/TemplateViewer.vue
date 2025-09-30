<template>
  <div class="template-viewer">
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
          <span class="title-text">{{ templateDisplayName }} - TEMPLATE</span>
        </div>
      </div>
      <div class="header-right">
        <button class="use-template-button" @click="useTemplate">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          USE TEMPLATE
        </button>
      </div>
    </div>
    
    <div class="template-content">
      <div class="template-info">
        <h2>{{ templateDisplayName }}</h2>
        <p class="template-description">
          This is a preview of the {{ templateDisplayName.toLowerCase() }} template. 
          You can use this template to create new reports with consistent formatting and structure.
        </p>
      </div>
      
      <div class="template-preview">
        <div class="preview-header">
          <h3>Template Preview</h3>
          <div class="preview-actions">
            <button class="preview-action-btn" @click="togglePreviewMode">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              {{ previewMode === 'full' ? 'Compact View' : 'Full View' }}
            </button>
          </div>
        </div>
        
        <div class="preview-container" :class="previewMode">
          <!-- Dynamic component rendering based on template -->
          <component 
            v-if="templateComponent" 
            :is="templateComponent" 
            :isTemplatePreview="true"
            class="template-component"
          />
          <div v-else class="no-template">
            <div class="no-template-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
            </div>
            <h3>Template Not Available</h3>
            <p>The requested template could not be loaded.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ObservationReport from '@/templates/ObservationReport.vue'
import MechanicalInspection from '@/templates/MechanicalInspection.vue'
import KitOfPartInsp from '@/templates/KitOfPartInsp.vue'

export default {
  name: 'TemplateViewer',
  components: {
    ObservationReport,
    MechanicalInspection,
    KitOfPartInsp
  },
  data() {
    return {
      templateName: '',
      templateDisplayName: '',
      templateComponent: null,
      previewMode: 'full' // 'full' or 'compact'
    };
  },
  mounted() {
    // Get template parameters from route
    this.templateName = this.$route.params.templateName || '';
    this.templateDisplayName = this.$route.params.templateDisplayName || 'Unknown Template';
    
    // Load the appropriate template component
    this.loadTemplateComponent();
  },
  methods: {
    loadTemplateComponent() {
      try {
        // Map template names to components
        const templateComponents = {
          'ObservationReport': ObservationReport,
          'MechanicalInspection': MechanicalInspection,
          'KitOfPartInsp': KitOfPartInsp
        };
        
        this.templateComponent = templateComponents[this.templateName] || null;
        
        if (!this.templateComponent) {
          console.error(`Template component not found: ${this.templateName}`);
        }
      } catch (error) {
        console.error('Error loading template component:', error);
      }
    },
    
    togglePreviewMode() {
      this.previewMode = this.previewMode === 'full' ? 'compact' : 'full';
    },
    
    useTemplate() {
      // Navigate back to reports dashboard or create new report with this template
      console.log(`Using template: ${this.templateName}`);
      alert(`Template "${this.templateDisplayName}" will be used to create a new report. This functionality will be implemented soon!`);
      
      // TODO: Implement actual template usage
      // this.$router.push({ 
      //   name: 'CreateReport', 
      //   params: { templateName: this.templateName } 
      // });
    }
  }
};
</script>

<style scoped>
.template-viewer {
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

.use-template-button {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

.use-template-button:hover {
  background: linear-gradient(135deg, #218838, #1ea085);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
}

.template-content {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 30px;
}

.template-info {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.template-info h2 {
  color: #2d3748;
  margin-bottom: 15px;
  font-size: 1.8em;
}

.template-description {
  color: #4a5568;
  font-size: 1.1em;
  line-height: 1.6;
  margin: 0;
}

.template-preview {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  background: #f8f9fa;
  border-bottom: 1px solid #e2e8f0;
}

.preview-header h3 {
  color: #2d3748;
  margin: 0;
  font-size: 1.3em;
}

.preview-actions {
  display: flex;
  gap: 10px;
}

.preview-action-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.preview-action-btn:hover {
  background: #5a6fd8;
  transform: translateY(-1px);
}

.preview-container {
  padding: 25px;
  background: white;
}

.preview-container.compact {
  max-height: 400px;
  overflow-y: auto;
}

.preview-container.full {
  max-height: none;
}

.template-component {
  /* Styles for the template component */
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.no-template {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.no-template-icon {
  margin-bottom: 20px;
}

.no-template-icon svg {
  color: #bdc3c7;
}

.no-template h3 {
  color: #7f8c8d;
  margin-bottom: 10px;
}

.no-template p {
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
  
  .use-template-button {
    width: 100%;
    justify-content: center;
  }
  
  .template-content {
    padding: 0 20px;
    margin: 20px auto;
  }
  
  .preview-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .preview-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
