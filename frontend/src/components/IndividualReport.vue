<template>
  <div class="individual-report-page">
    <!-- Header -->
    <div class="page-header">
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
        <h1 class="page-title">INDIVIDUAL REPORT</h1>
      </div>
      <div class="header-right">
        <button
          v-if="selectedTemplate && !showTemplateSelection && canDownloadReport"
          class="export-button"
          @click="downloadReportPDF"
        >
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
            <path
              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
            ></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          DOWNLOAD PDF
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Report Header -->
      <div class="report-header">
        <div class="report-title">
          <h2>{{ reportName || "Report Details" }}</h2>
          <div class="report-meta">
            <span class="report-id">Report ID: {{ reportId }}</span>
            <span class="project-name">Project: {{ projectName }}</span>
          </div>
        </div>
      </div>

      <!-- Template Selection State -->
      <div v-if="!selectedTemplate" class="no-reports-state">
        <div class="empty-icon">📄</div>

        <!-- Design Head can select template -->
        <div v-if="isDesignHead" class="template-message">
          <h3>Template not yet chosen</h3>
          <p>Please select a template to proceed with this report.</p>

          <div class="template-action">
            <button @click="selectTemplate" class="choose-template-btn">
              Choose Template
            </button>
          </div>
        </div>

        <!-- Other roles wait for Design Head to select template -->
        <div v-else class="report-message">
          <h3>Waiting for template selection</h3>
          <p>
            The Design Head needs to select a template before this report can be
            accessed.
          </p>

          <!-- Show different messages based on role -->
          <div v-if="isQAReviewer" class="role-message qa-reviewer">
            <div class="role-icon">🔍</div>
            <p>
              <strong>QA Reviewer Access:</strong> Once the Design Head assigns
              a template, you will be able to fill out and submit this report.
            </p>
          </div>
          <div v-else-if="isQAHead" class="role-message qa-head">
            <div class="role-icon">
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
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </div>
            <p>
              <strong
                >Quality Assurance Head - Read-Only Access Privilege:</strong
              >
              Upon template assignment by the Design Head, this report will be
              accessible for review and inspection purposes. Modification
              capabilities are not available at this access level.
            </p>
          </div>
          <div v-else class="role-message other-role">
            <div class="role-icon">
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
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </div>
            <p>
              <strong>Read-Only Access Privilege:</strong> Upon template
              assignment, this report will be accessible for review purposes.
              Modification capabilities are restricted to authorized QA Reviewer
              personnel exclusively.
            </p>
          </div>
        </div>
      </div>

      <!-- Template Form Display -->
      <div v-else class="template-form-container">
        <!-- Template Header -->
        <div class="template-form-header">
          <div class="template-info">
            <h3>{{ selectedTemplate.displayName }}</h3>
            <p>{{ selectedTemplate.description }}</p>
          </div>
          <div v-if="isDesignHead" class="template-actions">
            <button @click="selectTemplate" class="change-template-btn">
              Change Template
            </button>
          </div>
        </div>

        <!-- Template Form Content -->
        <div class="template-form-content">
          <!-- Role-based access message -->
          <div v-if="selectedTemplate" class="access-message">
            <!-- Assigned Reviewer (can edit) -->
            <div
              v-if="canEditReport && isQAReviewer"
              class="access-info qa-reviewer"
            >
              <div class="access-icon">🔍</div>
              <h4>Assigned Reviewer Access</h4>
              <p>
                You are the assigned reviewer for this report. You can edit and
                submit this report. All fields are enabled for input.
              </p>
              <p v-if="!isReportSubmitted" class="download-info">
                <strong>Note:</strong> Download PDF will be available after
                submitting the report.
              </p>
              <p v-else class="download-info success">
                <strong>✓</strong> Report submitted! You can now download the
                PDF.
              </p>
            </div>
            <!-- QA Reviewer but not assigned (read-only) -->
            <div
              v-else-if="isQAReviewer && !canEditReport"
              class="access-info view-only"
            >
              <div class="access-icon">
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
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </div>
              <h4>QA Reviewer - Read-Only Access</h4>
              <p>
                You are a QA Reviewer, but this report is assigned to another
                reviewer. You can view the report but cannot edit it. Only the
                assigned reviewer can modify report data.
              </p>
            </div>
            <div v-else-if="isQAHead" class="access-info qa-head">
              <div class="access-icon">
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
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </div>
              <h4>Quality Assurance Head - Read-Only Access Privilege</h4>
              <p>
                This report is available for review and inspection purposes
                only. Modification privileges are restricted to authorized QA
                Reviewer personnel exclusively. Report data modifications are
                not permitted at your current access level.
              </p>
            </div>
            <div v-else class="access-info view-only">
              <div class="access-icon">
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
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </div>
              <h4>Read-Only Access Privilege</h4>
              <p>
                This report is available for review and inspection purposes
                only. Modification privileges are restricted to authorized QA
                Reviewer personnel exclusively.
              </p>
            </div>
          </div>

          <!-- Dynamic Template Component -->
          <component
            v-if="currentTemplateComponent"
            :is="currentTemplateComponent"
            :projectName="projectName"
            :reportId="reportId"
            :reportName="reportName"
            :templateId="selectedTemplate.template_id"
            :templateName="selectedTemplate.name"
            :readonly="!canEditReport"
            :isTemplatePreview="false"
            @report-submitted="updateReportStatus"
          />

          <!-- Fallback if component not found -->
          <div v-else class="template-error">
            <div class="error-icon">
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
            </div>
            <h4>Template Component Not Found</h4>
            <p>
              The template "{{ selectedTemplate.displayName }}" could not be
              loaded.
            </p>
            <button @click="selectTemplate" class="change-template-btn">
              Select Different Template
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Template Selection Overlay -->
    <div
      v-if="showTemplateOverlay"
      class="template-overlay"
      @click="closeOverlay"
    >
      <div class="template-overlay-content" @click.stop>
        <!-- Loading Overlay -->
        <div v-if="loading" class="loading-overlay">
          <div class="loading-spinner"></div>
        </div>
        <div class="template-overlay-header">
          <h2>Choose Report Template</h2>
          <button class="close-btn" @click="closeOverlay">
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
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="template-overlay-body">
          <p class="template-description">
            Select a template for your report. Each template is designed for
            specific inspection types.
          </p>

          <div class="templates-grid">
            <div
              v-for="template in availableTemplates"
              :key="template.name"
              class="template-card"
              @click="selectTemplateOption(template)"
            >
              <div class="template-icon">
                <svg
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
                  <polyline points="14,2 14,8 20,8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10,9 9,9 8,9"></polyline>
                </svg>
              </div>
              <div class="template-info">
                <h3>{{ template.displayName }}</h3>
                <p>{{ template.description }}</p>
              </div>
              <div class="template-action">
                <button class="select-template-btn">Select</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from "@/stores/userStore";
// jsPDF will be dynamically imported when needed

// Import all template components
import ObservationReport from "@/templates/ObservationReport.vue";
import BarePcbInspectionReport from "@/templates/barepcbinspectionreport.vue";
import Conformalcoatinginspectionreport from "@/templates/Conformalcoatinginspectionreport.vue";
import RawMaterialInspectionReport from "@/templates/RawMaterialInspectionReport.vue";
import CotsScreeningInspectionReport from "@/templates/CotsScreeningInspectionReport.vue";
import AssembledBoardInspectionReport from "@/templates/AssembledBoardInspectionReport.vue";
import KitOfPartInsp from "@/templates/KitOfPartInsp.vue";
import MechanicalInspection from "@/templates/MechanicalInspection.vue";

export default {
  name: "IndividualReport",
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
      reportId: "",
      reportName: "",
      projectName: "",
      showTemplateOverlay: false,
      availableTemplates: [
        {
          template_id: 1,
          name: "Conformalcoatinginspectionreport",
          displayName: "Conformal Coating Inspection Report",
          description:
            "Template for creating conformal coating inspection reports with quality testing criteria",
          component: "Conformalcoatinginspectionreport",
        },
        {
          template_id: 2,
          name: "CotsScreeningInspectionReport",
          displayName: "COTS Screening Inspection Report",
          description:
            "Template for creating COTS screening inspection reports with test case validation",
          component: "CotsScreeningInspectionReport",
        },
        {
          template_id: 3,
          name: "BarePcbInspectionReport",
          displayName: "Bare PCB Inspection Report",
          description:
            "Template for creating bare PCB inspection reports with comprehensive testing criteria",
          component: "BarePcbInspectionReport",
        },
        {
          template_id: 4,
          name: "MechanicalInspection",
          displayName: "Mechanical Inspection Report",
          description:
            "Template for creating mechanical inspection reports with structural testing criteria",
          component: "MechanicalInspection",
        },
        {
          template_id: 5,
          name: "AssembledBoardInspectionReport",
          displayName: "Assembled Board Inspection Report",
          description:
            "Template for creating assembled board inspection reports with comprehensive testing criteria",
          component: "AssembledBoardInspectionReport",
        },
        {
          template_id: 6,
          name: "RawMaterialInspectionReport",
          displayName: "Raw Material Inspection Report",
          description:
            "Template for creating raw material inspection reports with compliance checking",
          component: "RawMaterialInspectionReport",
        },
        {
          template_id: 7,
          name: "KitOfPartInsp",
          displayName: "Kit of Part Inspection Report",
          description:
            "Template for creating kit of part inspection reports with component verification",
          component: "KitOfPartInsp",
        },
      ],
      selectedTemplate: null,
      loading: false,
      showTemplateSelection: false,
      reportStatus: null,
      assignedReviewerId: null,
    };
  },
  computed: {
    canSelectTemplate() {
      // Only Design Head (role_id = 4) can select templates
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 4;
    },

    isDesignHead() {
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 4;
    },

    isQAReviewer() {
      // QA Reviewer has role_id = 3
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 3;
    },

    isQAHead() {
      // QA Head has role_id = 2
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 2;
    },

    canEditReport() {
      // Only the assigned reviewer can edit reports
      // Check if current user is the assigned reviewer
      const currentUser = userStore.getters.currentUser();
      const currentUserId = currentUser?.id || currentUser?.user_id;

      // If no template is selected, cannot edit
      if (!this.selectedTemplate) {
        return false;
      }

      // If no assigned reviewer, cannot edit
      if (!this.assignedReviewerId) {
        return false;
      }

      // If report is already submitted, make it readonly
      if (this.isReportSubmitted) {
        return false;
      }

      // Only the assigned reviewer can edit
      return currentUserId === this.assignedReviewerId;
    },

    isReportSubmitted() {
      // Check if report has been submitted (status is not 'ASSIGNED')
      return this.reportStatus && this.reportStatus !== "ASSIGNED";
    },

    canDownloadReport() {
      // Allow download if template is selected and user has access to view the report
      // All users who can view the report should be able to download it
      if (!this.selectedTemplate) {
        return false;
      }
      
      // QA Reviewer can download anytime once template is selected
      if (this.isQAReviewer) {
        return true;
      }
      
      // QA Head can download
      if (this.isQAHead) {
        return true;
      }
      
      // Design Head can download
      if (this.isDesignHead) {
        return true;
      }
      
      // Designer can download
      const currentUserRole = userStore.getters.currentUserRole();
      if (currentUserRole === 5) {
        return true;
      }
      
      // Default: allow download if template is selected
      return true;
    },

    currentTemplateComponent() {
      if (!this.selectedTemplate) return null;

      // Map template names to component names
      const componentMap = {
        ObservationReport: "ObservationReport",
        BarePcbInspectionReport: "BarePcbInspectionReport",
        Conformalcoatinginspectionreport: "Conformalcoatinginspectionreport",
        RawMaterialInspectionReport: "RawMaterialInspectionReport",
        CotsScreeningInspectionReport: "CotsScreeningInspectionReport",
        AssembledBoardInspectionReport: "AssembledBoardInspectionReport",
        KitOfPartInsp: "KitOfPartInsp",
        MechanicalInspection: "MechanicalInspection",
      };

      return componentMap[this.selectedTemplate.name] || null;
    },
  },
  mounted() {
    // Get parameters from route
    this.reportId = this.$route.params.reportId || "";
    this.reportName = this.$route.params.reportName || "";
    this.projectName = this.$route.params.projectName || "";

    // Load report details to check if template is already selected
    this.loadReportDetails();
  },
  methods: {
    selectTemplate() {
      console.log(
        "Opening template selection overlay for report:",
        this.reportId
      );
      this.showTemplateOverlay = true;
      this.showTemplateSelection = true;
    },

    closeOverlay() {
      this.showTemplateOverlay = false;
      this.showTemplateSelection = false;
    },

    async selectTemplateOption(template) {
      console.log(
        "Selected template:",
        template.name,
        "for report:",
        this.reportId
      );

      try {
        this.loading = true;

        // Update report with selected template_id
        const response = await fetch(`/api/reports/${this.reportId}/template`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            template_id: template.template_id,
          }),
        });

        const result = await response.json();

        if (result.success) {
          // Set the selected template
          this.selectedTemplate = template;

          // Close the overlay
          this.closeOverlay();

          // Show success message
          alert(
            `Template "${template.displayName}" has been selected successfully!`
          );
        } else {
          alert(`Error: ${result.message}`);
        }
      } catch (error) {
        console.error("Error selecting template:", error);
        alert(
          "An error occurred while selecting the template. Please try again."
        );
      } finally {
        this.loading = false;
      }
    },

    // Method to update report status (called when report is submitted)
    updateReportStatus(newStatus) {
      this.reportStatus = newStatus;
      console.log("Report status updated to:", newStatus);
    },

    async loadReportDetails() {
      if (!this.reportId) return;

      try {
        const response = await fetch(
          `http://localhost:8000/api/reports/${this.reportId}`
        );
        const result = await response.json();

        if (result.success) {
          // Set report status
          this.reportStatus = result.report.status;

          // Store assigned reviewer ID
          this.assignedReviewerId = result.report.assigned_reviewer_id || null;

          // Find the template that matches the template_id
          if (result.report.template_id) {
            const template = this.availableTemplates.find(
              (t) => t.template_id === result.report.template_id
            );
            if (template) {
              this.selectedTemplate = template;

              // If template is selected and it's Conformal Coating, fetch the inspection data
              // The template component will receive reportId prop and should load data automatically
              // But we can also trigger a manual load here if needed
            }
          }
        }
      } catch (error) {
        console.error("Error loading report details:", error);
      }
    },

    uploadReport() {
      console.log("Uploading report:", this.reportId);
      alert(
        `Report upload for Report ID: ${this.reportId} will be implemented soon!`
      );
    },

    createReport() {
      console.log("Creating new report for:", this.reportId);
      alert(
        `Create new report for Report ID: ${this.reportId} will be implemented soon!`
      );
    },

    async downloadReportPDF() {
      try {
        // Dynamically import jsPDF
        const { jsPDF } = await import("jspdf");

        // Helper function to convert image to base64
        const imageToBase64 = async (imagePath) => {
          try {
            const response = await fetch(imagePath);
            const blob = await response.blob();
            return new Promise((resolve, reject) => {
              const reader = new FileReader();
              reader.onloadend = () => resolve(reader.result);
              reader.onerror = reject;
              reader.readAsDataURL(blob);
            });
          } catch (error) {
            console.warn(`Could not load image: ${imagePath}`, error);
            return null;
          }
        };

        // Fetch basic report details to get template_id
        const reportResponse = await fetch(
          `http://localhost:8000/api/reports/${this.reportId}`
        );

        if (!reportResponse.ok) {
          throw new Error(`Failed to fetch report: ${reportResponse.statusText}`);
        }

        const reportResult = await reportResponse.json();
        if (!reportResult.success) {
          throw new Error(reportResult.message || "Failed to fetch report details");
        }

        const reportData = reportResult.report;
        const templateId = reportData.template_id;

        // Fetch template-specific data based on template_id
        let templateData = null;
        const templateEndpoints = {
          1: `/api/reports/conformal-coating-inspection/${this.reportId}`,
          2: `/api/reports/cot-screening-inspection/${this.reportId}`,
          3: `/api/reports/bare-pcb-inspection/${this.reportId}`,
          4: `/api/reports/mechanical-inspection/by-report-card/${this.reportId}`,
          5: `/api/reports/assembled-board-inspection/${this.reportId}`,
          6: `/api/reports/raw-material-inspection/${this.reportId}`,
          7: `/api/reports/kit-of-part-inspection/${this.reportId}`,
        };

        if (templateEndpoints[templateId]) {
          const templateResponse = await fetch(
            `http://localhost:8000${templateEndpoints[templateId]}`
          );
          if (templateResponse.ok) {
            const templateResult = await templateResponse.json();
            if (templateResult.success) {
              templateData = templateResult.report;
            }
          }
        }

        // Create PDF document
        const doc = new jsPDF("p", "mm", "a4");
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 15;
        const contentWidth = pageWidth - 2 * margin;
        let yPosition = margin;

        // Load DRDO logo
        let drdoLogoBase64 = null;
        
        // Import image - Vite will handle the path resolution
        try {
          const drdoLogoUrl = new URL("../assets/images/DRDO.png", import.meta.url).href;
          drdoLogoBase64 = await imageToBase64(drdoLogoUrl);
        } catch (e) {
          console.warn("Could not load DRDO logo:", e);
        }

        // Helper function to add a new page if needed
        const checkPageBreak = (requiredHeight) => {
          if (yPosition + requiredHeight > pageHeight - margin) {
            doc.addPage();
            yPosition = margin;
            return true;
          }
          return false;
        };

        // Helper function to add text with wrapping and return height
        const addText = (text, x, y, maxWidth, fontSize = 10, isBold = false, align = "left") => {
          doc.setFontSize(fontSize);
          doc.setFont("helvetica", isBold ? "bold" : "normal");
          const lines = doc.splitTextToSize(text, maxWidth);
          const lineHeight = fontSize * 0.4;
          lines.forEach((line, index) => {
            let xPos = x;
            if (align === "center") {
              const textWidth = doc.getTextWidth(line);
              xPos = x + (maxWidth - textWidth) / 2;
            } else if (align === "right") {
              const textWidth = doc.getTextWidth(line);
              xPos = x + maxWidth - textWidth;
            }
            doc.text(line, xPos, y + (index * lineHeight));
          });
          return lines.length * lineHeight;
        };

        // ===== HEADER SECTION WITH LOGO =====
        const headerHeight = 25;
        yPosition = margin;
        
        // Add DRDO logo (left corner)
        let textStartX = margin + 18;
        if (drdoLogoBase64) {
          try {
            doc.addImage(drdoLogoBase64, "PNG", margin, yPosition, 15, 15);
            textStartX = margin + 18;
          } catch (e) {
            console.warn("Could not add DRDO logo:", e);
            textStartX = margin;
          }
        }
        
        // Add AVIATRAX text (centered)
        doc.setFontSize(14);
        doc.setFont("helvetica", "bold");
        doc.setTextColor(75, 0, 130); // Purple color
        const aviatraxText = "AVIATRAX™";
        const aviatraxWidth = doc.getTextWidth(aviatraxText);
        doc.text(aviatraxText, (pageWidth - aviatraxWidth) / 2, yPosition + 8);
        
        // Add Defence Research text below AVIATRAX (centered)
        doc.setFontSize(8);
        doc.setFont("helvetica", "normal");
        doc.setTextColor(0, 0, 0); // Black
        const drdoText = "Defence Research and Development Org. (DRDO)";
        const drdoTextWidth = doc.getTextWidth(drdoText);
        doc.text(drdoText, (pageWidth - drdoTextWidth) / 2, yPosition + 12);
        doc.setFont("helvetica", "italic");
        doc.setFontSize(7);
        const centreText = "Combat Aircraft Systems Development and Integration Centre";
        const centreTextWidth = doc.getTextWidth(centreText);
        doc.text(centreText, (pageWidth - centreTextWidth) / 2, yPosition + 16);
        
        // CASDIC path (left, below header)
        yPosition += headerHeight + 5;
        doc.setFontSize(9);
        doc.setFont("helvetica", "normal");
        const projectName = templateData?.project_name || reportData.project_name || "";
        const lruName = templateData?.lru_name || reportData.lru_name || "";
        const serialNumber = templateData?.serial_number || "SL-001";
        const inspectionCount = templateData?.inspection_count || "INS-001";
        const currentYear = new Date().getFullYear();
        const casdicPath = `CASDIC/${projectName}/${lruName}/SL.${serialNumber}/${inspectionCount}/${currentYear}`;
        doc.text(casdicPath, margin, yPosition);
        
        // Date (right)
        const currentDate = new Date().toLocaleDateString("en-GB");
        const dateText = `Date: ${currentDate}`;
        const dateWidth = doc.getTextWidth(dateText);
        doc.text(dateText, pageWidth - margin - dateWidth, yPosition);
        yPosition += 10;

        // ===== SUBJECT LINE (CENTERED) =====
        const templateName = reportData.template_name || "Inspection Report";
        const subjectText = `SUB: ${templateName} for ${lruName || projectName || ""}`;
        doc.setFontSize(11);
        doc.setFont("helvetica", "bold");
        const subjectWidth = doc.getTextWidth(subjectText);
        doc.text(subjectText, (pageWidth - subjectWidth) / 2, yPosition);
        yPosition += 12;

        // ===== REPORT DETAILS SECTION =====
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        doc.text("Report Details", margin, yPosition);
        yPosition += 8;

        doc.setFontSize(10);
        const colWidth = (contentWidth - 10) / 2;
        let leftY = yPosition;
        let rightY = yPosition;

        // Left column fields
        const leftFields = [
          { label: "Project Name", value: templateData?.project_name || reportData.project_name || "N/A" },
          { label: "Report Ref No", value: templateData?.report_ref_no || "N/A" },
          { label: "Memo Ref No", value: templateData?.memo_ref_no || "N/A" },
          { label: "LRU Name", value: templateData?.lru_name || reportData.lru_name || "N/A" },
          { label: "Inspection Stage", value: templateData?.inspection_stage || reportData.inspection_stage || "N/A" },
          { label: "Test Venue", value: templateData?.test_venue || reportData.review_venue || "N/A" },
          { label: "SL.NO'S", value: templateData?.sl_nos || "N/A" }
        ];

        // Right column fields
        const rightFields = [
          { label: "DP Name", value: templateData?.dp_name || "N/A" },
          { label: "Dated", value: templateData?.dated1 ? new Date(templateData.dated1).toLocaleDateString("en-GB") : "dd/mm/yyyy" },
          { label: "Dated", value: templateData?.dated2 ? new Date(templateData.dated2).toLocaleDateString("en-GB") : "dd/mm/yyyy" },
          { label: "SRU Name", value: templateData?.sru_name || "N/A" },
          { label: "Part No", value: templateData?.part_no || "N/A" },
          { label: "Quantity", value: templateData?.quantity ? templateData.quantity.toString() : "N/A" },
          { label: "Start Date", value: templateData?.start_date ? new Date(templateData.start_date).toLocaleDateString("en-GB") : "N/A" },
          { label: "End Date", value: templateData?.end_date ? new Date(templateData.end_date).toLocaleDateString("en-GB") : "N/A" }
        ];

        // Draw left column
        leftFields.forEach(field => {
          checkPageBreak(12);
          doc.setFont("helvetica", "bold");
          doc.setFontSize(10);
          const labelText = `${field.label}:`;
          doc.text(labelText, margin, leftY);
          doc.setFont("helvetica", "normal");
          const valueText = field.value || "N/A";
          const valueLines = doc.splitTextToSize(valueText, colWidth - 20);
          const valueHeight = valueLines.length * 4;
          doc.text(valueLines, margin + doc.getTextWidth(labelText) + 3, leftY);
          leftY += Math.max(valueHeight, 10);
        });

        // Draw right column
        rightFields.forEach(field => {
          checkPageBreak(12);
          doc.setFont("helvetica", "bold");
          doc.setFontSize(10);
          const labelText = `${field.label}:`;
          const rightX = margin + colWidth + 10;
          doc.text(labelText, rightX, rightY);
          doc.setFont("helvetica", "normal");
          const valueText = field.value || "N/A";
          const valueLines = doc.splitTextToSize(valueText, colWidth - 20);
          const valueHeight = valueLines.length * 4;
          doc.text(valueLines, rightX + doc.getTextWidth(labelText) + 3, rightY);
          rightY += Math.max(valueHeight, 10);
        });

        yPosition = Math.max(leftY, rightY) + 10;
        checkPageBreak(50);

        // ===== INSPECTION TESTS SECTION (for Conformal Coating) =====
        if (templateId === 1 && templateData) {
          yPosition += 5;
          checkPageBreak(80);
          
          // Heading
          doc.setFontSize(12);
          doc.setFont("helvetica", "bold");
          const headingText = "Inspection Tests";
          const headingWidth = doc.getTextWidth(headingText);
          doc.text(headingText, (pageWidth - headingWidth) / 2, yPosition);
          yPosition += 10;

          const testCaseNames = [
            "Uncoated patches",
            "Entrapped air bubbles",
            "Enclosed foreign particles in the cracks",
            "Residue of masking material",
            "Dis-coloration",
            "Pin holes and Soft spots",
            "Connectors surrounding and beneath",
            "Uniformity in coating across the board",
            "Conformal coating thickness of 30 to 130 microns for acrylic material as per IPC-CC-830B"
          ];

          // Table column widths with better spacing - ensure SL.NO, EXPECTED, OBSERVATIONS fit on one line
          // Calculate widths to ensure they add up exactly to contentWidth
          const colWidths = [
            contentWidth * 0.09,  // SL.NO (slightly wider to ensure it fits)
            contentWidth * 0.29,  // TEST CASES
            contentWidth * 0.12,  // EXPECTED (wider to ensure it fits)
            contentWidth * 0.13,  // OBSERVATIONS (wider to ensure it fits)
            contentWidth * 0.19,  // REMARKS
            contentWidth * 0.18   // UPLOAD
          ];
          
          // Ensure columns add up exactly to contentWidth (fix any rounding issues)
          const totalWidth = colWidths.reduce((sum, width) => sum + width, 0);
          if (Math.abs(totalWidth - contentWidth) > 0.1) {
            const adjustment = (contentWidth - totalWidth) / colWidths.length;
            colWidths.forEach((width, i) => {
              colWidths[i] = width + adjustment;
            });
          }

          const rowHeight = 12;
          
          // Draw header cells with borders and background
          doc.setFontSize(7);
          doc.setFont("helvetica", "bold");
          const headers = ["SL.NO", "TEST CASES", "EXPECTED", "OBSERVATIONS", "REMARKS (OK/NOT OK)", "UPLOAD"];
          
          // First pass: calculate maximum lines needed for headers
          let maxHeaderLines = 1;
          const headerLinesArray = [];
          headers.forEach((header, i) => {
            const availableWidth = colWidths[i] - 6; // More padding to prevent overflow
            const textWidth = doc.getTextWidth(header);
            let headerLines;
            
            // Keep single-word headers (SL.NO, EXPECTED, OBSERVATIONS) on one line
            // Only wrap multi-word headers that exceed the width
            if (textWidth <= availableWidth) {
              headerLines = [header];
            } else {
              // For single-word headers, keep them on one line even if slightly over
              // Only split multi-word headers
              if (header === "SL.NO" || header === "EXPECTED" || header === "OBSERVATIONS") {
                headerLines = [header]; // Force single line
              } else {
                headerLines = doc.splitTextToSize(header, availableWidth);
              }
            }
            headerLinesArray.push(headerLines);
            maxHeaderLines = Math.max(maxHeaderLines, headerLines.length);
          });
          
          // Calculate header height based on maximum lines
          const lineHeight = 4.5;
          const headerHeight = Math.max(12, maxHeaderLines * lineHeight + 4);
          
          // Draw header cells individually to ensure proper alignment
          let xPos = margin;
          headers.forEach((header, i) => {
            // Draw cell border and background
            doc.setFillColor(240, 240, 240);
            doc.rect(xPos, yPosition - 7, colWidths[i], headerHeight, "FD");
            
            const headerLines = headerLinesArray[i];
            const totalTextHeight = headerLines.length * lineHeight;
            const startY = yPosition - 7 + (headerHeight - totalTextHeight) / 2 + lineHeight;
            
            headerLines.forEach((line, lineIdx) => {
              const lineTextWidth = doc.getTextWidth(line);
              const cellCenterX = xPos + colWidths[i] / 2;
              // Ensure text doesn't overflow cell boundaries
              const textX = Math.max(xPos + 2, Math.min(cellCenterX - lineTextWidth / 2, xPos + colWidths[i] - lineTextWidth - 2));
              doc.text(line, textX, startY + (lineIdx * lineHeight));
            });
            
            xPos += colWidths[i];
          });
          yPosition += headerHeight + 3;

          // Draw rows with proper spacing
          doc.setFont("helvetica", "normal");
          doc.setFontSize(9);
          for (let i = 1; i <= 9; i++) {
            checkPageBreak(rowHeight + 5);
            
            const obs = templateData[`obs${i}`] || "";
            const expected = templateData[`expected${i}`] || "";
            const rem = templateData[`rem${i}`] || "";
            const upload = templateData[`upload${i}`] ? "File uploaded" : "No file chosen";

            // Calculate row height based on content
            const testCaseLines = doc.splitTextToSize(testCaseNames[i - 1], colWidths[1] - 6);
            const uploadLines = doc.splitTextToSize(upload, colWidths[5] - 6);
            const maxLines = Math.max(testCaseLines.length, uploadLines.length, 1);
            const currentRowHeight = Math.max(rowHeight, maxLines * 5 + 4);

            // Draw cell borders - draw outer border first, then internal lines
            doc.setLineWidth(0.1);
            // Draw outer rectangle for the entire row
            doc.rect(margin, yPosition - 6, contentWidth, currentRowHeight, "D");
            
            // Draw vertical lines between columns
            xPos = margin;
            for (let colIdx = 1; colIdx < colWidths.length; colIdx++) {
              xPos += colWidths[colIdx - 1];
              doc.line(xPos, yPosition - 6, xPos, yPosition - 6 + currentRowHeight);
            }

            // Draw cell content with proper alignment
            xPos = margin;
            
            // SL.NO - centered
            doc.setFont("helvetica", "bold");
            const slNoText = i.toString();
            const slNoWidth = doc.getTextWidth(slNoText);
            doc.text(slNoText, xPos + colWidths[0] / 2 - slNoWidth / 2, yPosition + 3);
            xPos += colWidths[0];
            doc.setFont("helvetica", "normal");
            
            // TEST CASES - left aligned with padding
            doc.text(testCaseLines, xPos + 3, yPosition + 3);
            xPos += colWidths[1];
            
            // EXPECTED - centered
            const expectedText = expected === "yes" ? "yes" : expected === "no" ? "no" : "";
            const expectedWidth = doc.getTextWidth(expectedText);
            doc.text(expectedText, xPos + colWidths[2] / 2 - expectedWidth / 2, yPosition + 3);
            xPos += colWidths[2];
            
            // OBSERVATIONS - centered
            const obsText = obs === "yes" ? "yes" : obs === "no" ? "no" : "";
            const obsWidth = doc.getTextWidth(obsText);
            doc.text(obsText, xPos + colWidths[3] / 2 - obsWidth / 2, yPosition + 3);
            xPos += colWidths[3];
            
            // REMARKS - centered
            const remWidth = doc.getTextWidth(rem || "");
            doc.text(rem || "", xPos + colWidths[4] / 2 - remWidth / 2, yPosition + 3);
            xPos += colWidths[4];
            
            // UPLOAD - left aligned with padding
            doc.text(uploadLines, xPos + 3, yPosition + 3);
            
            yPosition += currentRowHeight + 1;
          }
          yPosition += 5;
        }

        // ===== CHECK POINTS TABLE (for Raw Material Inspection) =====
        if (templateId === 6 && templateData) {
          yPosition += 5;
          checkPageBreak(80);
          
          // Heading
          doc.setFontSize(12);
          doc.setFont("helvetica", "bold");
          const headingText = "CHECK POINTS";
          const headingWidth = doc.getTextWidth(headingText);
          doc.text(headingText, (pageWidth - headingWidth) / 2, yPosition);
          yPosition += 10;

          const checkPointNames = [
            "Dimensions of the Raw Materials Received as per Certificate",
            "CoC of Raw Materials",
            "Chemical Reports as specified in QAP",
            "Tensile Strength",
            "Hardness Test Results as specified in QAP",
            "UT Test",
            "Any Other Observations:"
          ];

          // Table column widths with better spacing
          // Calculate widths to ensure they add up exactly to contentWidth
          const colWidths = [
            contentWidth * 0.08,  // SL.NO
            contentWidth * 0.25,  // CHECK POINTS
            contentWidth * 0.26,  // APPLICABILITY
            contentWidth * 0.16,  // COMPLIANCE
            contentWidth * 0.25   // REMARKS
          ];
          
          // Ensure columns add up exactly to contentWidth (fix any rounding issues)
          const totalWidth = colWidths.reduce((sum, width) => sum + width, 0);
          if (Math.abs(totalWidth - contentWidth) > 0.1) {
            const adjustment = (contentWidth - totalWidth) / colWidths.length;
            colWidths.forEach((width, i) => {
              colWidths[i] = width + adjustment;
            });
          }

          const rowHeight = 12;
          
          // Draw header cells with borders and background
          doc.setFontSize(9);
          doc.setFont("helvetica", "bold");
          const headers = ["SL.NO", "CHECK POINTS", "APPLICABILITY (A/NA)", "COMPLIANCE (YES/NO)", "REMARKS (OK/NOT OK)"];
          
          // First pass: calculate maximum lines needed for headers
          let maxHeaderLines = 1;
          const headerLinesArray = [];
          headers.forEach((header, i) => {
            const availableWidth = colWidths[i] - 6; // More padding to prevent overflow
            const textWidth = doc.getTextWidth(header);
            let headerLines;
            
            // Keep single-word headers (SL.NO) on one line
            // Only wrap multi-word headers that exceed the width
            if (textWidth <= availableWidth) {
              headerLines = [header];
            } else {
              // For single-word headers, keep them on one line even if slightly over
              // Only split multi-word headers
              if (header === "SL.NO") {
                headerLines = [header]; // Force single line
              } else {
                headerLines = doc.splitTextToSize(header, availableWidth);
              }
            }
            headerLinesArray.push(headerLines);
            maxHeaderLines = Math.max(maxHeaderLines, headerLines.length);
          });
          
          // Calculate header height based on maximum lines
          const lineHeight = 4.5;
          const headerHeight = Math.max(12, maxHeaderLines * lineHeight + 4);
          
          // Draw header cells individually to ensure proper alignment
          let xPos = margin;
          headers.forEach((header, i) => {
            // Draw cell border and background
            doc.setFillColor(240, 240, 240);
            doc.rect(xPos, yPosition - 7, colWidths[i], headerHeight, "FD");
            
            const headerLines = headerLinesArray[i];
            const totalTextHeight = headerLines.length * lineHeight;
            const startY = yPosition - 7 + (headerHeight - totalTextHeight) / 2 + lineHeight;
            
            headerLines.forEach((line, lineIdx) => {
              const lineTextWidth = doc.getTextWidth(line);
              const cellCenterX = xPos + colWidths[i] / 2;
              // Ensure text doesn't overflow cell boundaries
              const textX = Math.max(xPos + 2, Math.min(cellCenterX - lineTextWidth / 2, xPos + colWidths[i] - lineTextWidth - 2));
              doc.text(line, textX, startY + (lineIdx * lineHeight));
            });
            
            xPos += colWidths[i];
          });
          yPosition += headerHeight + 3;

          // Draw rows with proper spacing
          doc.setFont("helvetica", "normal");
          doc.setFontSize(9);
          for (let i = 1; i <= 7; i++) {
            const applicability = templateData[`applicability${i}`] || "";
            const compliance = templateData[`compliance${i}`] || "";
            const remarks = templateData[`rem${i}`] || "";

            if (applicability || compliance || remarks) {
              checkPageBreak(rowHeight + 5);
              
              // Calculate row height based on content
              const checkPointLines = doc.splitTextToSize(checkPointNames[i - 1], colWidths[1] - 6);
              const maxLines = Math.max(checkPointLines.length, 1);
              const currentRowHeight = Math.max(rowHeight, maxLines * 5 + 4);

              // Draw cell borders - draw outer border first, then internal lines
              doc.setLineWidth(0.1);
              // Draw outer rectangle for the entire row
              doc.rect(margin, yPosition - 6, contentWidth, currentRowHeight, "D");
              
              // Draw vertical lines between columns
              xPos = margin;
              for (let colIdx = 1; colIdx < colWidths.length; colIdx++) {
                xPos += colWidths[colIdx - 1];
                doc.line(xPos, yPosition - 6, xPos, yPosition - 6 + currentRowHeight);
              }

              // Draw cell content with proper alignment
              xPos = margin;
              
              // SL.NO - centered
              doc.setFont("helvetica", "bold");
              const slNoText = i.toString();
              const slNoWidth = doc.getTextWidth(slNoText);
              doc.text(slNoText, xPos + colWidths[0] / 2 - slNoWidth / 2, yPosition + 3);
              xPos += colWidths[0];
              doc.setFont("helvetica", "normal");
              
              // CHECK POINTS - left aligned with padding
              doc.text(checkPointLines, xPos + 3, yPosition + 3);
              xPos += colWidths[1];
              
              // APPLICABILITY - centered
              const appWidth = doc.getTextWidth(applicability);
              doc.text(applicability, xPos + colWidths[2] / 2 - appWidth / 2, yPosition + 3);
              xPos += colWidths[2];
              
              // COMPLIANCE - centered
              const compWidth = doc.getTextWidth(compliance);
              doc.text(compliance, xPos + colWidths[3] / 2 - compWidth / 2, yPosition + 3);
              xPos += colWidths[3];
              
              // REMARKS - centered
              const remWidth = doc.getTextWidth(remarks || "");
              doc.text(remarks || "", xPos + colWidths[4] / 2 - remWidth / 2, yPosition + 3);
              
              yPosition += currentRowHeight + 1;
            }
          }
          yPosition += 5;
        }

        // ===== SIGNATURE SECTION (VERTICAL LAYOUT) =====
        if (templateData && (templateData.prepared_by || templateData.verified_by || templateData.approved_by)) {
          checkPageBreak(60);
          yPosition += 10;
          doc.setFontSize(12);
          doc.setFont("helvetica", "bold");
          doc.text("Signatures", margin, yPosition);
          yPosition += 10;
          
          const signatures = [
            { label: "Prepared By", value: templateData.prepared_by },
            { label: "Verified By", value: templateData.verified_by },
            { label: "Approved By", value: templateData.approved_by }
          ];

          signatures.forEach((sig) => {
            checkPageBreak(15);
            doc.setFontSize(10);
            doc.setFont("helvetica", "bold");
            doc.text(`${sig.label}:`, margin, yPosition);
            yPosition += 6;
            doc.setFont("helvetica", "normal");
            const valueText = sig.value || "N/A";
            const valueLines = doc.splitTextToSize(valueText, contentWidth - 10);
            doc.text(valueLines, margin + 5, yPosition);
            yPosition += valueLines.length * 5 + 5;
          });
        }

        // ===== FOOTER =====
        const totalPages = doc.internal.pages.length - 1;
        for (let i = 1; i <= totalPages; i++) {
          doc.setPage(i);
          doc.setFontSize(8);
          doc.setFont("helvetica", "normal");
          doc.setTextColor(128, 128, 128);
          const footerText = `Generated on ${new Date().toLocaleString()} | Page ${i} of ${totalPages}`;
          doc.text(footerText, pageWidth / 2, pageHeight - 10, { align: "center" });
        }

        // Save PDF
        const filename = `Report_${this.reportId}_${
          this.reportName?.replace(/[^a-zA-Z0-9]/g, "_") || "Report"
        }_${new Date().toISOString().slice(0, 10)}.pdf`;
        doc.save(filename);

        alert("Report PDF downloaded successfully!");
      } catch (error) {
        console.error("Error downloading report PDF:", error);
        alert(
          `Error downloading report PDF: ${
            error.message || "Unknown error"
          }. Please try again.`
        );
      }
    },
  },
};
</script>

<style scoped>
.individual-report-page {
  min-height: 100vh;
  background: #ebf7fd;
}

/* Header */
.page-header {
  background: #2d3748;
  padding: 20px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: white;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.app-logo {
  width: 120px;
  height: auto;
  filter: brightness(0) invert(1);
}

.header-center {
  flex: 1;
  text-align: center;
}

.page-title {
  color: white;
  font-size: 2.2em;
  font-weight: 700;
  margin: 0;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.header-right {
  display: flex;
  align-items: center;
}

.export-button {
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 25px;
  padding: 12px 20px;
  font-weight: 600;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.export-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  background: white;
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 30px;
}

/* Report Header */
.report-header {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.report-title h2 {
  color: #2d3748;
  font-size: 1.8em;
  margin: 0 0 15px 0;
  font-weight: 600;
}

.report-meta {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
}

.report-id,
.project-name {
  color: #4a5568;
  font-size: 1em;
  font-weight: 500;
}

.report-id {
  background: #e2e8f0;
  padding: 8px 15px;
  border-radius: 20px;
}

.project-name {
  background: #f0f4f8;
  padding: 8px 15px;
  border-radius: 20px;
}

/* No Reports State */
.no-reports-state {
  background: white;
  padding: 60px 40px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.empty-icon {
  font-size: 5em;
  opacity: 0.6;
}

.no-reports-state h3 {
  color: #ffc107;
  font-size: 2.2em;
  margin: 0;
  font-weight: 600;
}

.template-message h3 {
  color: #007bff;
  font-size: 2.2em;
  margin: 0;
  font-weight: 600;
}

.report-message h3 {
  color: #ffc107;
  font-size: 2.2em;
  margin: 0;
  font-weight: 600;
}

.no-reports-state p {
  color: #6c757d;
  font-size: 1.2em;
  margin: 0;
  max-width: 600px;
  line-height: 1.6;
}

.template-action {
  margin-top: 30px;
}

.choose-template-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 18px 40px;
  border-radius: 10px;
  font-size: 1.3em;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(0, 123, 255, 0.3);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.choose-template-btn:hover {
  background-color: #0056b3;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.4);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    padding: 15px 20px;
    flex-direction: column;
    gap: 15px;
  }

  .page-title {
    font-size: 1.8em;
  }

  .main-content {
    padding: 0 20px;
    margin: 20px auto;
  }

  .report-meta {
    flex-direction: column;
    gap: 10px;
  }

  .no-reports-state {
    padding: 40px 20px;
  }

  .empty-icon {
    font-size: 4em;
  }

  .no-reports-state h3 {
    font-size: 1.8em;
  }

  .template-message h3,
  .report-message h3 {
    font-size: 1.8em;
  }

  .no-reports-state p {
    font-size: 1.1em;
  }

  .choose-template-btn {
    padding: 15px 30px;
    font-size: 1.1em;
    width: 250px;
  }
}

/* Template Form Container Styles */
.template-form-container {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.template-form-header {
  background: #f8f9fa;
  padding: 25px 30px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.template-info h3 {
  color: #2d3748;
  font-size: 1.8em;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.template-info p {
  color: #6c757d;
  font-size: 1em;
  margin: 0;
  line-height: 1.5;
}

.template-form-header .template-actions {
  flex-shrink: 0;
}

.template-form-content {
  padding: 0;
}

.template-placeholder {
  text-align: center;
  padding: 40px 20px;
}

.template-icon-large {
  color: #007bff;
  margin: 0 auto 20px auto;
  display: flex;
  justify-content: center;
}

.template-placeholder h4 {
  color: #2d3748;
  font-size: 1.5em;
  font-weight: 600;
  margin: 0 0 15px 0;
}

.template-placeholder p {
  color: #6c757d;
  font-size: 1.1em;
  margin: 0 0 30px 0;
  line-height: 1.6;
}

.template-placeholder .open-template-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 10px;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.template-placeholder .open-template-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
}

/* Template Error State */
.template-error {
  text-align: center;
  padding: 40px 20px;
}

.error-icon {
  color: #dc3545;
  margin: 0 auto 20px auto;
  display: flex;
  justify-content: center;
}

.template-error h4 {
  color: #dc3545;
  font-size: 1.5em;
  font-weight: 600;
  margin: 0 0 15px 0;
}

.template-error p {
  color: #6c757d;
  font-size: 1.1em;
  margin: 0 0 30px 0;
  line-height: 1.6;
}

.change-template-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9em;
}

.change-template-btn:hover {
  background: #5a6268;
  transform: scale(1.05);
}

/* Loading state */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Responsive Design for Template Form */
@media (max-width: 768px) {
  .template-form-header {
    flex-direction: column;
    text-align: center;
    gap: 20px;
    padding: 20px;
  }

  .template-form-content {
    padding: 0;
  }

  .template-placeholder {
    padding: 30px 15px;
  }

  .template-placeholder h4 {
    font-size: 1.3em;
  }

  .template-placeholder p {
    font-size: 1em;
  }

  .template-placeholder .open-template-btn {
    padding: 12px 25px;
    font-size: 1em;
    width: 100%;
    max-width: 300px;
  }

  .change-template-btn {
    padding: 12px 20px;
    font-size: 0.9em;
    width: 100%;
    max-width: 200px;
  }
}

/* Template Overlay Styles */
.template-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease-out;
}

.template-overlay-content {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 900px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  animation: slideIn 0.3s ease-out;
}

.template-overlay-header {
  background: #2d3748;
  color: white;
  padding: 25px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e2e8f0;
}

.template-overlay-header h2 {
  margin: 0;
  font-size: 1.8em;
  font-weight: 600;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.template-overlay-body {
  padding: 30px;
  max-height: calc(80vh - 100px);
  overflow-y: auto;
}

.template-description {
  color: #6c757d;
  font-size: 1.1em;
  margin: 0 0 30px 0;
  text-align: center;
  line-height: 1.6;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.template-card {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 15px;
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  overflow: hidden;
}

.template-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(0, 123, 255, 0.05) 0%,
    rgba(0, 123, 255, 0.1) 100%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.template-card:hover {
  border-color: #007bff;
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 123, 255, 0.2);
}

.template-card:hover::before {
  opacity: 1;
}

.template-icon {
  color: #007bff;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.template-card:hover .template-icon {
  transform: scale(1.1);
}

.template-info {
  flex: 1;
  z-index: 1;
  position: relative;
}

.template-info h3 {
  color: #2d3748;
  font-size: 1.3em;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.template-info p {
  color: #6c757d;
  font-size: 0.95em;
  margin: 0;
  line-height: 1.5;
}

.template-action {
  flex-shrink: 0;
  z-index: 1;
  position: relative;
}

.select-template-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9em;
}

.select-template-btn:hover {
  background: #0056b3;
  transform: scale(1.05);
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive Design for Overlay */
@media (max-width: 768px) {
  .template-overlay-content {
    width: 95%;
    margin: 20px;
  }

  .template-overlay-header {
    padding: 20px;
  }

  .template-overlay-header h2 {
    font-size: 1.5em;
  }

  .template-overlay-body {
    padding: 20px;
  }

  .templates-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .template-card {
    padding: 20px;
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .template-info h3 {
    font-size: 1.2em;
  }

  .template-info p {
    font-size: 0.9em;
  }
}

/* Role-based Access Messages */
.role-message {
  margin-top: 20px;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 15px;
  animation: fadeIn 0.5s ease-in-out;
}

.role-message.qa-reviewer {
  background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
  border: 2px solid #28a745;
  border-left: 6px solid #28a745;
}

.role-message.qa-head {
  background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 50%, #faf5ff 100%);
  border: 1.5px solid #4a90e2;
  border-left: 5px solid #2c5282;
  box-shadow: 0 2px 8px rgba(44, 82, 130, 0.12),
    0 1px 3px rgba(44, 82, 130, 0.08);
  padding: 20px 24px;
  position: relative;
  overflow: hidden;
}

.role-message.qa-head::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #2c5282 0%, #4a90e2 50%, #2c5282 100%);
}

.role-message.other-role {
  background: linear-gradient(135deg, #fff3cd, #fef9e7);
  border: 2px solid #ffc107;
  border-left: 6px solid #ffc107;
}

.role-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(44, 82, 130, 0.15);
}

.role-icon svg {
  width: 24px;
  height: 24px;
  color: #2c5282;
}

.role-message.qa-head .role-icon {
  background: linear-gradient(
    135deg,
    rgba(44, 82, 130, 0.1),
    rgba(74, 144, 226, 0.1)
  );
  border-color: rgba(44, 82, 130, 0.2);
}

.role-message.qa-head .role-icon svg {
  color: #2c5282;
}

.role-message p {
  margin: 0;
  color: #4a5568;
  font-size: 0.94em;
  line-height: 1.65;
  letter-spacing: 0.1px;
}

.role-message.qa-head p {
  color: #2d3748;
}

.role-message strong {
  color: #2c5282;
  font-weight: 700;
  letter-spacing: 0.2px;
}

.role-message.qa-head strong {
  color: #2c5282;
  font-size: 1.02em;
}

/* Access Message in Template Form */
.access-message {
  margin-bottom: 25px;
  padding: 20px;
  border-radius: 12px;
  animation: slideIn 0.6s ease-out;
}

.access-info {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 20px 24px;
  border-radius: 6px;
}

.access-info.qa-reviewer {
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
  border: 2px solid #28a745;
  border-left: 6px solid #28a745;
}

.access-info.qa-head {
  background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 50%, #faf5ff 100%);
  border: 1.5px solid #4a90e2;
  border-left: 5px solid #2c5282;
  box-shadow: 0 2px 8px rgba(44, 82, 130, 0.12),
    0 1px 3px rgba(44, 82, 130, 0.08);
  border-radius: 6px;
  position: relative;
  overflow: hidden;
}

.access-info.qa-head::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #2c5282 0%, #4a90e2 50%, #2c5282 100%);
}

.access-info.view-only {
  background: linear-gradient(135deg, #fff5f5 0%, #ffffff 50%, #fef5e7 100%);
  border: 1.5px solid #e53e3e;
  border-left: 5px solid #c53030;
  box-shadow: 0 2px 8px rgba(197, 48, 48, 0.12),
    0 1px 3px rgba(197, 48, 48, 0.08);
  border-radius: 6px;
  position: relative;
  overflow: hidden;
}

.access-info.view-only::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #c53030 0%, #e53e3e 50%, #c53030 100%);
}

.access-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(44, 82, 130, 0.15);
}

.access-icon svg {
  width: 24px;
  height: 24px;
  color: #2c5282;
}

.access-info.qa-head .access-icon {
  background: linear-gradient(
    135deg,
    rgba(44, 82, 130, 0.1),
    rgba(74, 144, 226, 0.1)
  );
  border-color: rgba(44, 82, 130, 0.2);
}

.access-info.qa-head .access-icon svg {
  color: #2c5282;
}

.access-info.view-only .access-icon {
  background: linear-gradient(
    135deg,
    rgba(197, 48, 48, 0.1),
    rgba(229, 62, 62, 0.1)
  );
  border-color: rgba(197, 48, 48, 0.2);
}

.access-info.view-only .access-icon svg {
  color: #c53030;
}

.access-info h4 {
  margin: 0 0 10px 0;
  color: #1a202c;
  font-size: 1.05em;
  font-weight: 600;
  letter-spacing: 0.3px;
  line-height: 1.4;
  text-transform: none;
}

.access-info.qa-head h4 {
  color: #2c5282;
  font-size: 1.08em;
  font-weight: 700;
}

.access-info.view-only h4 {
  color: #c53030;
  font-size: 1.08em;
  font-weight: 700;
}

.access-info p {
  margin: 0;
  color: #4a5568;
  font-size: 0.92em;
  line-height: 1.6;
  letter-spacing: 0.1px;
  text-align: left;
}

.access-info.qa-head p {
  color: #2d3748;
  font-size: 0.94em;
}

.access-info.view-only p {
  color: #4a5568;
  font-size: 0.94em;
}

.download-info {
  margin-top: 8px !important;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.85em !important;
  background: rgba(255, 193, 7, 0.1);
  border-left: 3px solid #ffc107;
}

.download-info.success {
  background: rgba(40, 167, 69, 0.1);
  border-left: 3px solid #28a745;
  color: #155724;
}

/* Responsive Design for Role Messages */
@media (max-width: 768px) {
  .role-message,
  .access-info {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }

  .role-icon,
  .access-icon {
    font-size: 1.5em;
  }

  .access-info h4 {
    font-size: 1em;
  }

  .role-message p,
  .access-info p {
    font-size: 0.85em;
  }
}
</style>
