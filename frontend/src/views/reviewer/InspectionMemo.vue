<template>
  <div class="inspection-memo-container">
    <header class="app-header">
      <div class="logo-section">
        <svg
          class="icon arrow-left"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          @click="goBack"
        >
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
        <span class="logo-text">AVIATRAX</span>
        <span class="memo-id">Memo ID: {{ id }}</span>
      </div>

      <div class="header-actions">
        <button
          class="download-pdf-btn"
          @click="downloadMemoPDF"
          title="Download PDF"
        >
          <svg
            class="icon download"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"
            />
          </svg>
          <span class="download-text">Download PDF</span>
        </button>
      </div>
    </header>

    <div class="form-content">
      <div class="form-card read-only-section">
        <div class="section-header">
          <h2 class="card-title">REQUISITION FOR DGAQA INSPECTION</h2>
        </div>
        <div class="grid-layout">
          <div class="grid-item">
            <span>FROM:</span
            ><input type="text" v-model="memoData.from" readonly />
          </div>
          <div class="grid-item">
            <span>CASCIC Ref No.:</span
            ><input type="text" v-model="memoData.cascicRefNo" readonly />
          </div>
          <div class="grid-item">
            <span>CASCIC/</span
            ><input type="text" v-model="memoData.cascic" readonly />
          </div>
          <div class="grid-item">
            <span>Dated:</span
            ><input type="text" v-model="memoData.dated" readonly />
          </div>
          <div class="grid-item">
            <span>TO:</span><input type="text" v-model="memoData.to" readonly />
          </div>
          <div class="grid-item">
            <span>Wing/Proj Ref No.:</span
            ><input type="text" v-model="memoData.wingProjRefNo" readonly />
          </div>
          <div class="grid-item-full">
            <span>Name & contact No of CASCIC (Designs) coordinator:</span
            ><input
              type="text"
              v-model="memoData.coordinatorContact"
              readonly
            />
          </div>
        </div>
      </div>
      <div class="form-card read-only-section">
        <div class="section-header">
          <h3 class="section-title">LRU/SRU DETAILS</h3>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half">
            <span>LRU/SRU DETAILS</span
            ><input type="text" v-model="memoData.lruSruDetails" readonly />
          </div>
          <div class="grid-item-half">
            <span>LRU/SRU Desc:</span
            ><input type="text" v-model="memoData.lruSruDesc" readonly />
          </div>
        </div>
        <div class="grid-layout two-col-doc">
          <div class="grid-item">
            <span>Ref Doc</span
            ><input type="text" v-model="memoData.refDoc" readonly />
          </div>
          <div class="grid-item">
            <span>Ref No of Document</span
            ><input type="text" v-model="memoData.refNoDocument" readonly />
          </div>
          <div class="grid-item">
            <span>ver</span
            ><input type="text" v-model="memoData.version" readonly />
          </div>
          <div class="grid-item">
            <span>rev</span
            ><input type="text" v-model="memoData.revision" readonly />
          </div>
        </div>
        <div class="grid-layout">
          <div class="grid-item">
            <span>Part No:</span
            ><input type="text" v-model="memoData.partNo" readonly />
          </div>
          <div class="grid-item">
            <span>Manufacturer:</span
            ><input type="text" v-model="memoData.manufacturer" readonly />
          </div>
          <div class="grid-item">
            <span>Sl.No of units:</span
            ><input type="text" v-model="memoData.serialNo" readonly />
          </div>
          <div class="grid-item">
            <span>Drawing no/Rev:</span
            ><input type="text" v-model="memoData.drawingNoRev" readonly />
          </div>
          <div class="grid-item">
            <span>Qty Offered:</span
            ><input type="text" v-model="memoData.qtyOffered" readonly />
          </div>
          <div class="grid-item">
            <span>source:</span
            ><input type="text" v-model="memoData.source" readonly />
          </div>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half">
            <span>UNIT IDENTIFICATION:</span
            ><input
              type="text"
              v-model="memoData.unitIdentification"
              readonly
            />
          </div>
          <div class="grid-item-half">
            <span>MECHANICAL INSPN:</span
            ><input
              type="text"
              v-model="memoData.mechanicalInspection"
              readonly
            />
          </div>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half">
            <span>INSPECTION /TEST STAGE OFFERED NOW:</span
            ><input
              type="text"
              v-model="memoData.inspectionTestStage"
              readonly
            />
          </div>
          <div class="grid-item-half">
            <span>STTE Status:</span
            ><input type="text" v-model="memoData.stteStatus" readonly />
          </div>
        </div>
      </div>
      <div class="form-card read-only-section">
        <div class="section-header">
          <h3 class="section-title">TESTING DETAILS</h3>
        </div>
        <div class="grid-layout">
          <div class="grid-item-half">
            <span>Above Unit is ready for Testing at venue, dated onwards.</span
            ><input type="text" v-model="memoData.testingVenueDate" readonly />
          </div>
          <div class="grid-item-half">
            <span>Test facility to be used:</span
            ><input type="text" v-model="memoData.testFacility" readonly />
          </div>
          <div class="grid-item-half">
            <span>Calibration status OK/Due on:</span
            ><input type="text" v-model="memoData.calibrationStatus" readonly />
          </div>
          <div class="grid-item-half">
            <span>SIGNATURE: NAME / DESIGNATION</span
            ><input
              type="text"
              v-model="memoData.signatureNameDesignation"
              readonly
            />
          </div>
          <div class="grid-item-quarter">
            <span>Test cycle / Duration:</span
            ><input
              type="text"
              v-model="memoData.testCycleDuration"
              readonly
            /><span>hrs</span>
          </div>
          <div class="grid-item-quarter">
            <span>Func. Check(Initial):</span
            ><input
              type="text"
              v-model="memoData.funcCheckInitial"
              readonly
            /><span>date/time</span>
          </div>
          <div class="grid-item-quarter">
            <span>Test Start on:</span
            ><input type="text" v-model="memoData.testStartOn" readonly /><span
              >date/time</span
            >
          </div>
          <div class="grid-item-quarter">
            <span>Perf. check (during):</span
            ><input
              type="text"
              v-model="memoData.perfCheckDuring"
              readonly
            /><span>date/time</span>
          </div>
          <div class="grid-item-half">
            <span>Test complete on:</span
            ><input
              type="text"
              v-model="memoData.testCompleteOn"
              readonly
            /><span>date/time</span>
          </div>
          <div class="grid-item-half">
            <span>Func Check (End):</span
            ><input type="text" v-model="memoData.funcCheckEnd" readonly /><span
              >date/time</span
            >
          </div>
        </div>
      </div>
      <div class="form-card read-only-section">
        <div class="section-header">
          <h3 class="section-title">CERTIFICATIONS</h3>
        </div>
        <div class="grid-layout one-col-checkbox">
          <p class="checkbox-title">It is certified that :</p>
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.mechanicalQualityRecords"
            />Mechanical Quality Records of all the parts (Raw material TC
            (chemical & mechanical), Dimensional reports, NDT reports, Process
            certificates etc.) & Electrical Quality Records (Components
            Screening report, PCB manufacturing report, process compliance
            reports/ test reports, etc.) were verified thoroughly.</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.cocVerified"
            />CoC for SRU, fasteners & standard parts are verified and
            satisfactory</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.sruSerialNoted"
            />Sl no of the SRUs are noted down in the respective log book opened
            on _________</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.noDefectInvestigation"
            />No Defect investigation is pending against this LRU</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.previousTestStagesCleared"
            />All the previous test stages of this LRU/SRU are cleared</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.cascicQAInspected"
            />CASCIC QA has physically inspected and accepted the LRU on
            _________</label
          >
          <span class="signature-line">SIGNATURE of Rep, IQA CASCIC</span>
        </div>
      </div>
      <div class="form-card">
        <div class="section-header">
          <h3 class="section-title">Action taken & remarks by DGAQA</h3>
        </div>
        <div class="grid-layout">
          <div class="readonly-display">{{ memoData.dgaqaRemarks }}</div>
          <span class="signature-line right">SIGNATURE OF DGAQA REP..</span>
        </div>
      </div>
      <div class="form-card editable-section">
        <div class="section-header">
          <h3 class="section-title">TEST STATUS</h3>
        </div>
        <div class="grid-layout one-col-radio">
          <label>
            <input
              type="radio"
              value="Successfully completed"
              v-model="memoData.testStatus"
            />
            Successfully completed
          </label>
          <label>
            <input
              type="radio"
              value="Completed with observations"
              v-model="memoData.testStatus"
            />
            Completed with observations
          </label>
          <label>
            <input
              type="radio"
              value="Test not conducted"
              v-model="memoData.testStatus"
            />
            Test not conducted
          </label>
          <label>
            <input
              type="radio"
              value="Test failed"
              v-model="memoData.testStatus"
            />
            Test failed
          </label>
        </div>
      </div>
      <div class="form-card editable-section">
        <div class="section-header">
          <h3 class="section-title">Remarks by QA Reviewer</h3>
        </div>
        <div class="grid-layout">
          <textarea
            v-model="memoData.reviewerComments"
            class="reviewer-comments"
            placeholder="Enter reviewer comments..."
            rows="4"
          ></textarea>
          <span class="signature-line right">SIGNATURE OF QA REVIEWER</span>
        </div>
      </div>
    </div>
    <!-- 
<div v-if="showShareModal" class="share-modal-overlay" @click.self="toggleShareModal">
      <div class="share-modal-content">
        <h2>Share via Email</h2>
        <p>Enter email addresses separated by commas.</p>
        <input type="text" v-model="emailAddresses" placeholder="e.g., mail1@example.com, mail2@example.com" class="email-input" />
        <div class="modal-actions">
          <button @click="sendEmails" class="send-btn">Send</button>
        </div>
      </div>
    </div>    
-->

    <!-- Submit Button -->
    <div class="submit-section">
      <button class="submit-button" @click="submitMemo">Submit</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "InspectionMemo",
  props: {
    id: {
      type: [String, Number],
      required: true,
    },
  },
  data() {
    return {
      showShareModal: false,
      emailAddresses: "",
      memoData: {
        dgaqaRemarks: "All records verified. Proceed as per plan.",
        from: "CASCIC Design Team",
        cascicRefNo: "CASCIC/2025/001",
        cascic: "CASCIC/DES/2025",
        dated: "15-01-2025",
        to: "DGAQA Inspection Team",
        wingProjRefNo: "WING/PROJ/2025/001",
        coordinatorContact: "Sumith",
        lruSruDetails: "LRU-001",
        lruSruDesc: "Flight Control Unit",
        refDoc: "FCU-SPEC-001",
        refNoDocument: "DOC/FCU/2025/001",
        version: "1.0",
        revision: "A",
        partNo: "FCU-001-REV-A",
        manufacturer: "Aviation Systems Ltd.",
        serialNo: "SN001234567",
        drawingNoRev: "DRW/FCU/001-REV-A",
        qtyOffered: "2",
        source: "Manufacturer",
        unitIdentification: "FCU-001-REV-A-SN001234567",
        mechanicalInspection: "PASSED",
        inspectionTestStage: "Final Assembly Test",
        stteStatus: "READY",
        testingVenueDate: "20-01-2025",
        testFacility: "Test Lab A",
        calibrationStatus: "OK",
        signatureNameDesignation: "Design Engineer",
        testCycleDuration: "24",
        funcCheckInitial: "20-01-2025 09:00",
        testStartOn: "20-01-2025 10:00",
        perfCheckDuring: "20-01-2025 14:00",
        testCompleteOn: "21-01-2025 10:00",
        funcCheckEnd: "21-01-2025 11:00",
        certifications: {
          mechanicalQualityRecords: true,
          cocVerified: true,
          sruSerialNoted: true,
          noDefectInvestigation: true,
          previousTestStagesCleared: true,
          cascicQAInspected: true,
        },
        reviewerComments: "",
        testStatus: "",
      },
    };
  },
  mounted() {
    this.fetchMemoData();
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    async fetchMemoData() {
      try {
        // Check if data was passed via sessionStorage (from dashboard navigation)
        if (this.$route.query.hasData === "true") {
          const storedMemoData = sessionStorage.getItem(`memoData_${this.id}`);
          const storedReferences = sessionStorage.getItem(
            `references_${this.id}`
          );

          if (storedMemoData && storedReferences) {
            const memoData = JSON.parse(storedMemoData);
            const references = JSON.parse(storedReferences);
            this.transformAndSetMemoData(memoData, references);

            // Clean up sessionStorage after use
            sessionStorage.removeItem(`memoData_${this.id}`);
            sessionStorage.removeItem(`references_${this.id}`);
            return;
          }
        }

        // Otherwise, fetch from API
        const response = await fetch(`/api/memos/${this.id}`);
        if (!response.ok) {
          throw new Error(
            `Failed to fetch memo details: ${response.statusText}`
          );
        }

        const data = await response.json();
        if (data.success) {
          this.transformAndSetMemoData(data.memo, data.references || []);
        } else {
          throw new Error(data.message || "Failed to fetch memo details");
        }
      } catch (error) {
        console.error("Error fetching memo data:", error);
        // Fallback to default data if fetch fails
        console.log("Using default memo data due to fetch error");
      }
    },

    transformAndSetMemoData(backendMemo, references) {
      // Transform backend memo data to frontend format
      this.memoData = {
        // Basic memo information
        dgaqaRemarks: backendMemo.remarks || "No remarks provided",
        from: backendMemo.from_person || "CASCIC Design Team",
        cascicRefNo: backendMemo.casdic_ref_no || "",
        cascic: backendMemo.casdic_ref_no || "",
        dated: this.formatDate(backendMemo.dated),
        to: backendMemo.to_person || "DGAQA Inspection Team",
        wingProjRefNo: backendMemo.wing_proj_ref_no || "",
        coordinatorContact: backendMemo.name_designation || "",

        // LRU/SRU Details
        lruSruDetails: backendMemo.part_number || "",
        lruSruDesc: backendMemo.lru_sru_desc || "",
        refDoc: references[0]?.ref_doc || "",
        refNoDocument: references[0]?.ref_no || "",
        version: references[0]?.ver?.toString() || "",
        revision: references[0]?.rev?.toString() || "",
        partNo: backendMemo.part_number || "",
        manufacturer: backendMemo.manufacturer || "",
        serialNo: this.formatSerialNumbers(backendMemo.slno_units),
        drawingNoRev: backendMemo.drawing_no_rev || "",
        qtyOffered: backendMemo.qty_offered?.toString() || "0",
        source: backendMemo.source || "",
        unitIdentification: this.formatUnitIdentification(
          backendMemo.unit_identification
        ),
        mechanicalInspection: backendMemo.mechanical_inspn || "",
        inspectionTestStage: backendMemo.inspn_test_stage_offered || "",
        stteStatus: backendMemo.stte_status || "",

        // Testing Details
        testingVenueDate: this.formatDate(backendMemo.memo_date),
        testFacility: backendMemo.test_facility || "",
        calibrationStatus: backendMemo.calibration_status || "",
        signatureNameDesignation: backendMemo.name_designation || "",
        testCycleDuration: backendMemo.test_cycle_duration || "",
        funcCheckInitial: this.formatDateTime(backendMemo.func_check_initial),
        testStartOn: this.formatDateTime(backendMemo.test_start_on),
        perfCheckDuring: this.formatDateTime(backendMemo.perf_check_during),
        testCompleteOn: this.formatDateTime(backendMemo.test_complete_on),
        funcCheckEnd: this.formatDateTime(backendMemo.func_check_end),

        // Certifications object with all required properties
        certifications: {
          mechanicalQualityRecords:
            backendMemo.certified?.includes("a") || false,
          cocVerified: backendMemo.certified?.includes("b") || false,
          sruSerialNoted: backendMemo.certified?.includes("c") || false,
          noDefectInvestigation: backendMemo.certified?.includes("d") || false,
          previousTestStagesCleared:
            backendMemo.certified?.includes("e") || false,
          cascicQAInspected: backendMemo.certified?.includes("f") || false,
        },

        // Test Status - single string value for radio button selection
        testStatus: "",

        // Reviewer comments (empty for view-only)
        reviewerComments: "",
      };
    },

    formatDate(dateString) {
      if (!dateString) return "";
      try {
        const date = new Date(dateString);
        return date
          .toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          })
          .replace(/\//g, "-");
      } catch {
        return dateString;
      }
    },

    formatDateTime(datetimeString) {
      if (!datetimeString) return "";
      try {
        const date = new Date(datetimeString);
        return date
          .toLocaleString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
          })
          .replace(",", "");
      } catch {
        return datetimeString;
      }
    },

    formatSerialNumbers(serialArray) {
      if (!serialArray || !Array.isArray(serialArray)) return "";
      return serialArray.join(", ");
    },

    formatUnitIdentification(unitIdArray) {
      if (!unitIdArray || !Array.isArray(unitIdArray)) return "";
      return unitIdArray.join(", ");
    },

    /** toggleShareModal() {
      this.showShareModal = !this.showShareModal;
      if (!this.showShareModal) {
        this.emailAddresses = ''; // Clear input on close
      }
    },
    sendEmails() {
      if (this.emailAddresses.trim() === '') {
        alert('Please enter at least one email address.');
        return;
      }
      
      const emails = this.emailAddresses.split(',').map(email => email.trim());
      console.log('Sending memo to:', emails);
      // Here you would add the logic to send the emails, for example, making an API call.
      
      alert(`Memo sent successfully to: ${emails.join(', ')}`);
      this.toggleShareModal(); // Close the modal after "sending"
    },*/
    async submitMemo() {
      // Validate that a test status is selected
      if (!this.memoData.testStatus) {
        alert("Please select a test status.");
        return;
      }

      if (!this.memoData.reviewerComments.trim()) {
        alert("Please provide reviewer comments.");
        return;
      }

      try {
        // Prepare certification data for backend
        const certified = [];
        if (this.memoData.certifications.mechanicalQualityRecords)
          certified.push("a");
        if (this.memoData.certifications.cocVerified) certified.push("b");
        if (this.memoData.certifications.sruSerialNoted) certified.push("c");
        if (this.memoData.certifications.noDefectInvestigation)
          certified.push("d");
        if (this.memoData.certifications.previousTestStagesCleared)
          certified.push("e");
        if (this.memoData.certifications.cascicQAInspected) certified.push("f");

        // Update memo status via API
        const response = await fetch(`/api/memos/${this.id}/status`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            test_status: this.memoData.testStatus,
            reviewer_comments: this.memoData.reviewerComments,
            certified: certified,
          }),
        });

        if (!response.ok) {
          throw new Error(
            `Failed to update memo status: ${response.statusText}`
          );
        }

        const result = await response.json();
        if (result.success) {
          alert("Memo status updated successfully!");
          this.goBack(); // Navigate back after successful submission
        } else {
          throw new Error(result.message || "Failed to update memo status");
        }
      } catch (error) {
        console.error("Error updating memo status:", error);
        alert(`Error updating memo status: ${error.message}`);
      }
    },

    // Download memo PDF
    async downloadMemoPDF() {
      try {
        console.log(`Downloading PDF for memo ID: ${this.id}`);

        // Show loading state
        const button = event.target.closest(".download-pdf-btn");
        const originalText = button.querySelector(".download-text").textContent;
        button.querySelector(".download-text").textContent = "Loading...";
        button.disabled = true;

        // Make request to backend PDF endpoint
        const response = await fetch(
          `http://localhost:8000/api/memos/${this.id}/pdf`,
          {
            method: "GET",
            headers: {
              Accept: "application/pdf",
            },
          }
        );

        if (!response.ok) {
          throw new Error(`Failed to generate PDF: ${response.statusText}`);
        }

        // Get the PDF blob
        const blob = await response.blob();

        // Create download link
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `memo_${this.id}_${new Date()
          .toISOString()
          .slice(0, 19)
          .replace(/:/g, "-")}.pdf`;

        // Trigger download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Clean up
        window.URL.revokeObjectURL(url);

        console.log(`PDF downloaded successfully for memo ${this.id}`);
      } catch (error) {
        console.error("Error downloading memo PDF:", error);
        alert(`Error downloading PDF: ${error.message}`);
      } finally {
        // Restore button state
        if (button) {
          button.querySelector(".download-text").textContent = originalText;
          button.disabled = false;
        }
      }
    },
  },
};
</script>

<style scoped>
/* Scoped styles to prevent them from affecting other components */
:root {
  --background-color: #f0f0f0;
  --card-color: #e0e0e0;
  --text-color: #333;
  --border-color: #999;
  --input-bg: #fff;
  --button-bg: #007bff;
  --button-text: #fff;
}

.inspection-memo-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: sans-serif;
  color: var(--text-color);
  background-color: var(--background-color);
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: var(--card-color);
  border-bottom: 1px solid var(--border-color);
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo-section .icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
  cursor: pointer;
  transition: transform 0.2s;
}

.logo-section .icon:hover {
  transform: scale(1.1);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.download-pdf-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
}

.download-pdf-btn:hover:not(:disabled) {
  background-color: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.download-pdf-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 4px rgba(108, 117, 125, 0.2);
}

.download-pdf-btn .icon {
  width: 16px;
  height: 16px;
}

.download-text {
  font-size: 14px;
  font-weight: 500;
}

.memo-id {
  margin-left: 20px;
  font-size: 0.9em;
  color: #666;
  font-weight: normal;
}

/* removed editable indicator */

.logo-text {
  font-weight: bold;
  font-size: 1.2em;
}

.share-section .share-btn {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: var(--text-color);
  font-size: 1em;
  cursor: pointer;
}

.share-section .icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}

.form-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
}

.form-card {
  background-color: var(--card-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.card-title {
  text-align: center;
  margin-top: 0;
  font-size: 1.1em;
}

.grid-layout {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.grid-layout.two-col {
  grid-template-columns: 1fr 1fr;
}

.grid-layout.two-col-doc {
  grid-template-columns: 1fr 1fr 0.5fr 0.5fr;
}

.grid-layout.one-col-checkbox {
  grid-template-columns: 1fr;
}

.grid-layout.one-col-radio {
  grid-template-columns: 1fr;
}

.grid-item {
  display: flex;
  flex-direction: column;
}

.grid-item-half,
.grid-item-quarter {
  display: flex;
  flex-direction: column;
}

.grid-item-full {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
}

.grid-item input,
.grid-item-full input,
.grid-item-half input,
.grid-item-quarter input {
  width: 100%;
  padding: 8px 12px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--input-bg);
  box-sizing: border-box;
  margin-top: 5px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.grid-item input:focus,
.grid-item-full input:focus,
.grid-item-half input:focus,
.grid-item-quarter input:focus {
  outline: none;
  border-color: #555;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.08);
}

.grid-item input[readonly] {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.grid-item input:not([readonly]) {
  background-color: var(--input-bg);
  color: var(--text-color);
  cursor: text;
}

.grid-item span,
.grid-item-full span,
.grid-item-half span,
.grid-item-quarter span {
  font-size: 0.9em;
}

.remarks-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.signature-line {
  display: block;
  text-align: right;
  margin-top: 20px;
  margin-left: auto;
  font-weight: bold;
}

.one-col-checkbox label {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
  font-size: 0.9em;
  line-height: 1.2;
}

.one-col-checkbox input[type="checkbox"] {
  margin-right: 10px;
  margin-top: 2px;
}

.one-col-checkbox input[type="checkbox"]:not([disabled]) {
  transform: scale(1.2);
  accent-color: #000;
}

.one-col-checkbox input[type="checkbox"][disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}

.one-col-radio label {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 0.9em;
  line-height: 1.2;
  cursor: pointer;
}

.one-col-radio input[type="radio"] {
  margin-right: 10px;
  transform: scale(1.2);
  accent-color: #000;
}

.share-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.share-modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.share-modal-content h2 {
  margin: 0;
  font-size: 1.5em;
  text-align: center;
}

.share-modal-content p {
  margin: 0;
  font-size: 0.9em;
  color: #666;
}

.email-input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  box-sizing: border-box;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
}

.send-btn {
  padding: 10px 20px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.reviewer-comments {
  width: 100%;
  padding: 12px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--input-bg);
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  min-height: 100px;
  margin: 10px 0;
  transition: border-color 0.3s ease;
  color: var(--text-color);
}

.reviewer-comments:focus {
  outline: none;
  border-color: #555;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.08);
}

.reviewer-comments::placeholder {
  color: #999;
}

.submit-section {
  display: flex;
  justify-content: flex-end;
  padding: 20px;
  background-color: transparent;
}

.submit-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.submit-button:hover {
  background-color: #222;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.submit-button:active {
  transform: translateY(0);
}

.submit-button svg {
  width: 20px;
  height: 20px;
}

.editable-section {
  border-left: none;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border-color);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #000;
}

.section-title {
  margin: 0;
  color: #000;
  font-size: 1.1em;
  font-weight: bold;
}

/* remove edit badge + pulse */

.read-only-section {
  border-left: none;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border-color);
}

/* remove read-only badge */

.card-title {
  margin: 0;
  color: #000;
  font-size: 1.2em;
  font-weight: bold;
}
</style>
