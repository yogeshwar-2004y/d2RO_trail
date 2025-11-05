<template>
  <div class="template-dashboard">
    <div class="header">
      <div class="header-left">
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
      </div>
      <div class="header-center">
        <div class="page-title">
          <svg
            class="title-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
            ></path>
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
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search Templates"
            class="search-input"
          />
          <svg
            class="search-icon"
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
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
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="48"
          height="48"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        <h3>Error Loading Templates</h3>
        <p>{{ error }}</p>
        <button @click="loadTemplates" class="retry-button">Retry</button>
      </div>
    </div>

    <div v-else-if="!selectedTemplate" class="template-grid">
      <div
        v-for="template in filteredTemplates"
        :key="template.name"
        class="template-card"
        @click="viewTemplate(template)"
      >
        <div class="card-icon">
          <!-- Custom icon for Bare PCB Inspection Report -->
          <svg
            v-if="template.name === 'BarePcbInspectionReport'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
            <circle cx="8" cy="8" r="1"></circle>
            <circle cx="12" cy="8" r="1"></circle>
            <circle cx="16" cy="8" r="1"></circle>
            <circle cx="8" cy="12" r="1"></circle>
            <circle cx="12" cy="12" r="1"></circle>
            <circle cx="16" cy="12" r="1"></circle>
          </svg>
          <!-- Custom icon for Conformal Coating Inspection Report -->
          <svg
            v-else-if="template.name === 'Conformalcoatinginspectionreport'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
            <path d="M6 8h12M6 12h12M6 16h8"></path>
            <circle cx="18" cy="8" r="1"></circle>
            <circle cx="18" cy="12" r="1"></circle>
            <circle cx="18" cy="16" r="1"></circle>
          </svg>
          <!-- Custom icon for Raw Material Inspection Report -->
          <svg
            v-else-if="template.name === 'RawMaterialInspectionReport'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
            <path d="M6 8h12M6 12h12M6 16h8"></path>
            <circle cx="18" cy="8" r="1"></circle>
            <circle cx="18" cy="12" r="1"></circle>
            <circle cx="18" cy="16" r="1"></circle>
            <path d="M3 6h18M3 10h18M3 14h12"></path>
          </svg>
          <!-- Custom icon for COTS Screening Inspection Report -->
          <svg
            v-else-if="template.name === 'CotsScreeningInspectionReport'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
            <path d="M6 8h12M6 12h12M6 16h8"></path>
            <circle cx="18" cy="8" r="1"></circle>
            <circle cx="18" cy="12" r="1"></circle>
            <circle cx="18" cy="16" r="1"></circle>
            <path d="M3 6h18M3 10h18M3 14h12"></path>
            <circle cx="4" cy="6" r="1"></circle>
            <circle cx="4" cy="10" r="1"></circle>
            <circle cx="4" cy="14" r="1"></circle>
          </svg>
          <!-- Custom icon for Assembled Board Inspection Report -->
          <svg
            v-else-if="template.name === 'AssembledBoardInspectionReport'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
            <circle cx="8" cy="8" r="1"></circle>
            <circle cx="12" cy="8" r="1"></circle>
            <circle cx="16" cy="8" r="1"></circle>
            <circle cx="8" cy="12" r="1"></circle>
            <circle cx="12" cy="12" r="1"></circle>
            <circle cx="16" cy="12" r="1"></circle>
            <circle cx="8" cy="16" r="1"></circle>
            <circle cx="12" cy="16" r="1"></circle>
            <circle cx="16" cy="16" r="1"></circle>
            <path d="M4 4h16M4 8h16M4 12h16M4 16h16"></path>
          </svg>
          <!-- Custom icon for Kit of Part Inspection Report -->
          <svg
            v-else-if="template.name === 'KitOfPartInsp'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
            <path d="M6 8h12M6 12h12M6 16h8"></path>
            <circle cx="18" cy="8" r="1"></circle>
            <circle cx="18" cy="12" r="1"></circle>
            <circle cx="18" cy="16" r="1"></circle>
            <path d="M3 6h18M3 10h18M3 14h12"></path>
            <circle cx="4" cy="6" r="1"></circle>
            <circle cx="4" cy="10" r="1"></circle>
            <circle cx="4" cy="14" r="1"></circle>
            <path d="M8 4h8M8 8h8M8 12h6"></path>
          </svg>
          <!-- Custom icon for Mechanical Inspection Report -->
          <svg
            v-else-if="template.name === 'MechanicalInspection'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
            <path d="M6 8h12M6 12h12M6 16h8"></path>
            <circle cx="18" cy="8" r="1"></circle>
            <circle cx="18" cy="12" r="1"></circle>
            <circle cx="18" cy="16" r="1"></circle>
            <path d="M3 6h18M3 10h18M3 14h12"></path>
            <circle cx="4" cy="6" r="1"></circle>
            <circle cx="4" cy="10" r="1"></circle>
            <circle cx="4" cy="14" r="1"></circle>
            <path d="M8 4h8M8 8h8M8 12h6"></path>
            <path d="M10 2h4M10 6h4M10 10h2"></path>
          </svg>
          <!-- Different icons for different template types -->
          <svg
            v-if="template.name === 'ObservationReport'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
            ></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          <!-- Mechanical/Engineering icon for MechanicalInspection -->
          <svg
            v-else-if="template.name === 'MechanicalInspection'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
            <circle cx="6" cy="8" r="1"></circle>
            <circle cx="10" cy="8" r="1"></circle>
            <circle cx="14" cy="8" r="1"></circle>
            <circle cx="18" cy="8" r="1"></circle>
          </svg>
          <!-- Kit/Package icon for KitOfPartInsp -->
          <svg
            v-else-if="template.name === 'KitOfPartInsp'"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"
            ></path>
            <polyline points="3.27,6.96 12,12.01 20.73,6.96"></polyline>
            <line x1="12" y1="22.08" x2="12" y2="12"></line>
            <circle cx="8" cy="10" r="1"></circle>
            <circle cx="16" cy="10" r="1"></circle>
            <circle cx="12" cy="14" r="1"></circle>
          </svg>
          <!-- Default icon for other templates -->
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
            ></path>
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
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="64"
            height="64"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
            ></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <h3>No Templates Found</h3>
        <p>No templates match your current search.</p>
      </div>
    </div>

    <!-- Template Display Area -->
    <div v-if="selectedTemplate" class="template-display-container">
      <div class="template-display-header">
        <button class="back-to-grid-button" @click="backToGrid">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
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
          Back to Templates
        </button>
        <h2 class="template-display-title">
          {{ selectedTemplate.displayName }}
        </h2>
        <div class="template-actions">
          <button class="use-template-btn" @click="useTemplate">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path
                d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
              ></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            Use Template
          </button>
        </div>
      </div>

      <div class="template-content-wrapper">
        <component
          v-if="selectedTemplateComponent"
          :is="selectedTemplateComponent"
          :readonly="true"
          :isTemplatePreview="true"
          class="template-preview-component"
        />
        <div v-else class="template-not-found">
          <h3>Template Component Not Found</h3>
          <p>
            The template component for "{{ selectedTemplate.displayName }}"
            could not be loaded.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ObservationReport from "@/templates/ObservationReport.vue";
import BarePcbInspectionReport from "@/templates/BarePcbInspectionReport.vue";
import Conformalcoatinginspectionreport from "@/templates/Conformalcoatinginspectionreport.vue";
import RawMaterialInspectionReport from "@/templates/RawMaterialInspectionReport.vue";
import CotsScreeningInspectionReport from "@/templates/CotsScreeningInspectionReport.vue";
import AssembledBoardInspectionReport from "@/templates/AssembledBoardInspectionReport.vue";
import KitOfPartInsp from "@/templates/KitOfPartInsp.vue";
import MechanicalInspection from "@/templates/MechanicalInspection.vue";

export default {
  name: "TemplateDashboard",
  components: {
    ObservationReport,
    BarePcbInspectionReport,
    Conformalcoatinginspectionreport,
    RawMaterialInspectionReport,
    CotsScreeningInspectionReport,
    AssembledBoardInspectionReport,
    KitOfPartInsp,
    MechanicalInspection,
  },
  data() {
    return {
      searchQuery: "",
      templates: [],
      loading: true,
      error: null,
      selectedTemplate: null,
      selectedTemplateComponent: null,
    };
  },
  computed: {
    filteredTemplates() {
      if (!this.searchQuery) {
        return this.templates;
      }

      const query = this.searchQuery.toLowerCase();
      return this.templates.filter(
        (template) =>
          template.displayName.toLowerCase().includes(query) ||
          template.description.toLowerCase().includes(query)
      );
    },
  },
  mounted() {
    this.loadTemplates();
  },
  methods: {
    async loadTemplates() {
      try {
        this.loading = true;
        this.error = null;

        // Fetch templates from API
        const response = await fetch(
          "http://localhost:5000/api/report-templates"
        );
        const data = await response.json();

        if (data.success) {
          this.templates = data.templates;
        } else {
          this.error = data.message || "Failed to load templates";
        }

        this.loading = false;
      } catch (error) {
        console.error("Error loading templates:", error);
        this.error = "Error loading templates. Please try again.";
        this.loading = false;
      }
    },

    viewTemplate(template) {
      // Set the selected template and load its component
      this.selectedTemplate = template;
      this.loadTemplateComponent(template);
    },

    loadTemplateComponent(template) {
      try {
        // Map template names to components
        const templateComponents = {
          ObservationReport: ObservationReport,
          BarePcbInspectionReport: BarePcbInspectionReport,
          Conformalcoatinginspectionreport: Conformalcoatinginspectionreport,
          RawMaterialInspectionReport: RawMaterialInspectionReport,
          CotsScreeningInspectionReport: CotsScreeningInspectionReport,
          AssembledBoardInspectionReport: AssembledBoardInspectionReport,
          KitOfPartInsp: KitOfPartInsp,
          MechanicalInspection: MechanicalInspection,
        };

        // Map API template names to component names
        const componentName = this.getComponentName(template.name);
        this.selectedTemplateComponent =
          templateComponents[componentName] || null;

        if (!this.selectedTemplateComponent) {
          console.error(`Template component not found: ${componentName}`);
        }
      } catch (error) {
        console.error("Error loading template component:", error);
        this.selectedTemplateComponent = null;
      }
    },

    getComponentName(templateName) {
      // Map API template names to component names
      const nameMapping = {
        "assembled board inspection report": "AssembledBoardInspectionReport",
        "bare pcb inspection report": "BarePcbInspectionReport",
        "conformal coating inspection report":
          "Conformalcoatinginspectionreport",
        "cots screening inspection report": "CotsScreeningInspectionReport",
        "kit of part inspection report": "KitOfPartInsp",
        "mechanical inspection report": "MechanicalInspection",
        "raw material inspection report": "RawMaterialInspectionReport",
      };

      return nameMapping[templateName.toLowerCase()] || templateName;
    },

    backToGrid() {
      this.selectedTemplate = null;
      this.selectedTemplateComponent = null;
    },

    useTemplate() {
      if (!this.selectedTemplate) return;

      // Navigate to the actual form based on template type
      const componentName = this.getComponentName(this.selectedTemplate.name);

      const routeMapping = {
        BarePcbInspectionReport: "BarePcbInspectionReport",
        ObservationReport: "ObservationReport",
        Conformalcoatinginspectionreport: "Conformalcoatinginspectionreport",
        RawMaterialInspectionReport: "RawMaterialInspectionReport",
        CotsScreeningInspectionReport: "CotsScreeningInspectionReport",
        AssembledBoardInspectionReport: "AssembledBoardInspectionReport",
        KitOfPartInsp: "KitOfPartInsp",
        MechanicalInspection: "MechanicalInspection",
      };

      const routeName = routeMapping[componentName];
      if (routeName) {
        this.$router.push({
          name: routeName,
          params: {
            projectName: "Default Project",
            lruName: "Default LRU",
          },
        });
      } else {
        alert(
          `Template "${this.selectedTemplate.displayName}" will be used to create a new report. This functionality will be implemented soon!`
        );
      }
    },
  },
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
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
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

/* Template Display Styles */
.template-display-container {
  padding: 30px;
  background-color: #f8f9fa;
  min-height: calc(100vh - 120px);
}

.template-display-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.back-to-grid-button {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.back-to-grid-button:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.template-display-title {
  color: #2d3748;
  margin: 0;
  font-size: 1.8em;
  font-weight: bold;
}

.template-actions {
  display: flex;
  gap: 15px;
}

.use-template-btn {
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

.use-template-btn:hover {
  background: linear-gradient(135deg, #218838, #1ea085);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
}

.template-content-wrapper {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.template-preview-component {
  /* Styles for the template component */
  border: none;
  border-radius: 0;
}

.template-not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.template-not-found h3 {
  color: #e74c3c;
  margin-bottom: 10px;
}

.template-not-found p {
  color: #6c757d;
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

  .template-display-container {
    padding: 20px;
  }

  .template-display-header {
    flex-direction: column;
    gap: 20px;
    align-items: flex-start;
  }

  .template-actions {
    width: 100%;
    justify-content: center;
  }

  .back-to-grid-button,
  .use-template-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
