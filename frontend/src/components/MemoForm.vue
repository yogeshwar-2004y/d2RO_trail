<template>
  <div class="memo-form">
    <!-- Header -->
    <div class="form-header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
     
      <h1 class="form-title">REQUISITION FOR DGAQA INSPECTION</h1>
       <button class="share-btn" @click="toggleShareBox">
          <svg class="icon share" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/>
          </svg>
        </button>
          <div class="logos-container">
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
      <div class="logos-container">
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
        <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
      </div>
      </div>
    </div>

    <!-- Share Overlay -->
    <div v-if="showShareBox" class="share-overlay" @click.self="toggleShareBox">
      <div class="share-overlay-content">
        <div class="share-overlay-header">
          <h3>Share via Email</h3>
          <button class="close-btn" @click="toggleShareBox">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="share-overlay-body">
          <input 
            type="text" 
            v-model="emailAddresses" 
            placeholder="Enter email addresses (comma separated)" 
            class="email-input"
          />
          <div class="share-actions">
            <button @click="sendEmails" class="send-btn">Send</button>
            <button @click="toggleShareBox" class="cancel-btn">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Requisition Details Section -->
    <div class="form-section requisition-details">
      <div class="form-grid">
        <div class="form-row">
          <div class="form-field">
            <label>FROM:</label>
            <input type="text" v-model="formData.from" placeholder="Enter sender details">
          </div>
          <div class="form-field">
            <label>CASDIC Ref No.:</label>
            <input type="text" v-model="formData.casdicRef" placeholder="Enter CASDIC reference">
          </div>
          <div class="form-field">
            <label>CASDIC/</label>
            <input type="text" v-model="formData.casdic" placeholder="Enter CASDIC details">
          </div>
          <div class="form-field">
            <label>Dated:</label>
            <input type="date" v-model="formData.casdicDate">
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-field">
            <label>TO:</label>
            <input type="text" v-model="formData.to" placeholder="Enter recipient details">
          </div>
          <div class="form-field">
            <label>Wing/Proj Ref No.:</label>
            <input type="text" v-model="formData.wingRef" placeholder="Enter wing/project reference">
          </div>
          <div class="form-field"></div>
          <div class="form-field"></div>
        </div>
        
        <div class="form-row">
          <div class="form-field"></div>
          <div class="form-field wide-field">
            <label>Name & contact No of CASDIC (Designs) coordinator:</label>
            <input type="text" v-model="formData.coordinator" placeholder="Enter coordinator details">
          </div>
          <div class="form-field"></div>
          <div class="form-field"></div>
        </div>
      </div>
    </div>

    <!-- LRU/SRU Details Section -->
    <div class="form-section lru-details">
      <div class="details-table">
        <div class="table-header">
          <div class="lru-column">LRU/SRU DETAILS</div>
          <div class="desc-column">LRU/SRU Desc:</div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.lruReady" id="lruReady">
            <label for="lruReady"></label>
          </div>
          <div class="ref-column">Ref Doc</div>
          <div class="refno-column">Ref No of Document</div>
          <div class="ver-column">ver</div>
          <div class="rev-column">rev</div>
        </div>
        
        <div class="table-row">
          <div class="lru-column">
            <div class="lru-field">
              <label>Part No:</label>
              <input type="text" v-model="formData.partNo" placeholder="Enter part number">
            </div>
            <div class="lru-field">
              <label>Manufacturer:</label>
              <input type="text" v-model="formData.manufacturer" placeholder="Enter manufacturer">
            </div>
          </div>
          <div class="desc-column">
            <textarea v-model="formData.description" placeholder="Enter LRU/SRU description"></textarea>
          </div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.unitsNoted" id="unitsNoted">
            <label for="unitsNoted"></label>
          </div>
          <div class="ref-column">
            <input type="text" v-model="formData.refDoc" placeholder="Enter reference document">
          </div>
          <div class="refno-column">
            <input type="text" v-model="formData.refNo" placeholder="Enter reference number">
          </div>
          <div class="ver-column">
            <input type="text" v-model="formData.version" placeholder="ver">
          </div>
          <div class="rev-column">
            <input type="text" v-model="formData.revision" placeholder="rev">
          </div>
        </div>
        
        <div class="table-row">
          <div class="lru-column">
            <div class="lru-field">
              <label>Sl.No of units:</label>
              <input type="text" v-model="formData.slNo" placeholder="Enter serial number">
            </div>
            <div class="lru-field">
              <label>Drawing no /Rev:</label>
              <input type="text" v-model="formData.drawingNo" placeholder="Enter drawing number">
            </div>
          </div>
          <div class="desc-column">
            <textarea v-model="formData.description2" placeholder="Additional description"></textarea>
          </div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.unitsNoted2" id="unitsNoted2">
            <label for="unitsNoted2"></label>
          </div>
          <div class="ref-column">
            <input type="text" v-model="formData.refDoc2" placeholder="Enter reference document">
          </div>
          <div class="refno-column">
            <input type="text" v-model="formData.refNo2" placeholder="Enter reference number">
          </div>
          <div class="ver-column">
            <input type="text" v-model="formData.version2" placeholder="ver">
          </div>
          <div class="rev-column">
            <input type="text" v-model="formData.revision2" placeholder="rev">
          </div>
        </div>
        
        <div class="table-row">
          <div class="lru-column">
            <div class="lru-field">
              <label>Qty Offered:</label>
              <input type="text" v-model="formData.qtyOffered" placeholder="Enter quantity">
            </div>
            <div class="lru-field">
              <label>source:</label>
              <input type="text" v-model="formData.source" placeholder="Enter source">
            </div>
          </div>
          <div class="desc-column">
            <textarea v-model="formData.description3" placeholder="Additional description"></textarea>
          </div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.unitsNoted3" id="unitsNoted3">
            <label for="unitsNoted3"></label>
          </div>
          <div class="ref-column">
            <input type="text" v-model="formData.refDoc3" placeholder="Enter reference document">
          </div>
          <div class="refno-column">
            <input type="text" v-model="formData.refNo3" placeholder="Enter reference number">
          </div>
          <div class="ver-column">
            <input type="text" v-model="formData.version3" placeholder="ver">
          </div>
          <div class="rev-column">
            <input type="text" v-model="formData.revision3" placeholder="rev">
          </div>
        </div>
        
        <div class="table-row">
          <div class="lru-column">
            <div class="lru-field">
              <label>UNIT IDENTIFICATION:</label>
              <input type="text" v-model="formData.unitId" placeholder="Enter unit identification">
            </div>
            <div class="lru-field">
              <label>MECHANICAL INSPN:</label>
              <input type="text" v-model="formData.mechanicalInsp" placeholder="Enter mechanical inspection">
            </div>
          </div>
          <div class="desc-column">
            <textarea v-model="formData.description4" placeholder="Additional description"></textarea>
          </div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.unitsNoted4" id="unitsNoted4">
            <label for="unitsNoted4"></label>
          </div>
          <div class="ref-column">
            <input type="text" v-model="formData.refDoc4" placeholder="Enter reference document">
          </div>
          <div class="refno-column">
            <input type="text" v-model="formData.refNo4" placeholder="Enter reference number">
          </div>
          <div class="ver-column">
            <input type="text" v-model="formData.version4" placeholder="ver">
          </div>
          <div class="rev-column">
            <input type="text" v-model="formData.revision4" placeholder="rev">
          </div>
        </div>
      </div>
    </div>

    <!-- Inspection/Test Stage Section -->
    <div class="form-section inspection-stage">
      <div class="stage-header">
        <div class="stage-field">
          <label>INSPECTION / TEST STAGE OFFERED NOW :</label>
          <input type="text" v-model="formData.inspectionStage" placeholder="Enter inspection/test stage">
        </div>
        <div class="stage-field">
          <label>STTE Status:</label>
          <input type="text" v-model="formData.stteStatus" placeholder="Enter STTE status">
        </div>
      </div>
    </div>

    <!-- Test Details Section -->
    <div class="form-section test-details">
      <div class="test-grid">
        <div class="test-column">
          <div class="test-field">
            <label>Above Unit is ready for Testing at</label>
            <input type="text" v-model="formData.testVenue" placeholder="venue, dated">
            <span>onwards.</span>
          </div>
          <div class="test-field">
            <label>SIGNATURE:</label>
            <div class="signature-box"></div>
          </div>
          <div class="test-field">
            <label>NAME / DESIGNATION</label>
            <input type="text" v-model="formData.signatureName" placeholder="Enter name and designation">
          </div>
        </div>
        
        <div class="test-column">
          <div class="test-field">
            <label>Test facility to be used:</label>
            <input type="text" v-model="formData.testFacility" placeholder="Enter test facility">
          </div>
          <div class="test-field">
            <label>Test cycle / Duration:</label>
            <input type="text" v-model="formData.testCycle" placeholder="Enter test cycle">
            <span>hrs</span>
          </div>
          <div class="test-field">
            <label>Test Start on:</label>
            <input type="datetime-local" v-model="formData.testStart">
          </div>
          <div class="test-field">
            <label>Test complete on :</label>
            <input type="datetime-local" v-model="formData.testComplete">
          </div>
        </div>
        
        <div class="test-column">
          <div class="test-field">
            <label>Calibration status OK/Due on :</label>
            <input type="date" v-model="formData.calibrationStatus">
          </div>
          <div class="test-field">
            <label>Func. Check(Initial) :</label>
            <input type="datetime-local" v-model="formData.funcCheckInitial">
          </div>
          <div class="test-field">
            <label>Perf. check (during) :</label>
            <input type="datetime-local" v-model="formData.perfCheckDuring">
          </div>
          <div class="test-field">
            <label>Func Check (end) :</label>
            <input type="datetime-local" v-model="formData.funcCheckEnd">
          </div>
        </div>
      </div>
    </div>

    <!-- Certification Section -->
    <div class="form-section certification">
      <h3>It is certified that :</h3>
      <div class="certification-list">
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert1" id="cert1">
          <label for="cert1">Mechanical Quality Records of all the parts (Raw material TC (chemical & mechanical), Dimensional reports, NDT reports, Process certificates etc.) & Electrical Quality Records (Components Screening report, PCB manufacturing report, process compliance reports/ test reports, etc.) were verified thoroughly.</label>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert2" id="cert2">
          <label for="cert2">CoC for SRU, fasteners & standard parts are verified and satisfactory</label>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert3" id="cert3">
          <label for="cert3">Sl no of the SRUs are noted down in the respective log book opened on</label>
          <input type="text" v-model="formData.logBookDate" placeholder="Enter date">
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert4" id="cert4">
          <label for="cert4">No Defect investigation is pending against this LRU</label>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert5" id="cert5">
          <label for="cert5">All the previous test stages of this LRU/SRU are cleared</label>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert6" id="cert6">
          <label for="cert6">CASDIC QA has physically inspected and accepted the LRU on</label>
          <input type="text" v-model="formData.qaInspectionDate" placeholder="Enter date">
        </div>
      </div>
      
      <div class="signature-section">
        <div class="signature-box-large"></div>
        <p>SIGNATURE of Rep, IQA CASDIC</p>
      </div>
    </div>

    <!-- Action Taken Section -->
    <div class="form-section action-taken">
      <h3>Action taken & remarks by DGAQA</h3>
      <p class="instruction">(please use space overleaf for details)</p>
      <div class="remarks-area">
        <textarea v-model="formData.dgaqaRemarks" placeholder="Enter DGAQA remarks and actions taken..."></textarea>
      </div>
      <div class="signature-section">
        <div class="signature-box-large"></div>
        <p>SIGNATURE OF DGAQA REP..</p>
      </div>
    </div>

    <div 
      class="form-section test-status" 
      v-if="currentUserRole === 3"
    >
      <h3>TEST STATUS</h3>
      <div class="status-options">
        <label>
          <input 
            type="radio" 
            v-model="formData.testStatus" 
            value="successful"
          />
          Successfully completed
        </label>
        <label>
          <input 
            type="radio" 
            v-model="formData.testStatus" 
            value="withObservations"
          />
          Completed with observations
        </label>
        <label>
          <input 
            type="radio" 
            v-model="formData.testStatus" 
            value="notConducted"
          />
          Test not conducted
        </label>
        <label>
          <input 
            type="radio" 
            v-model="formData.testStatus" 
            value="failed"
          />
          Test failed. 
        </label>
      </div>
    </div>


    <!-- ✅ New Section: Remarks by QA Reviewer -->
    <div 
      class="form-section reviewer-remarks" 
      v-if="currentUserRole === 3"
    >
      <h3>Remarks by QA Reviewer</h3>
      <div class="remarks-container">
        <textarea v-model="formData.qaReviewerRemarks" placeholder="Enter reviewer comments..."></textarea>
        <div class="signature-box-large"></div>
        <p>SIGNATURE OF QA REVIEWER</p>
      </div>
    </div>

    <div
      class="action-buttons"
      v-if="memoData.status === 'Not Assigned' 
            && !showTestReviewSection 
            && !showRejectionSection 
            && canApproveMemo"
    >
      <button class="btn btn-accept" @click="showAcceptOverlay = true">ACCEPT</button>
      <button class="btn btn-reject" @click="showRejectOverlay = true">REJECT</button>
    </div>

    <!-- Status Display (shown after Accept/Reject) -->
    <div v-if="showTestReviewSection || showRejectionSection" class="status-display">
      <div class="status-badge" :class="showTestReviewSection ? 'accepted' : 'rejected'">
        <svg v-if="showTestReviewSection" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
        <span>{{ showTestReviewSection ? 'MEMO ACCEPTED' : 'MEMO REJECTED' }}</span>
      </div>
      <p class="status-date">Processed on: {{ new Date().toLocaleDateString() }}</p>
    </div>

    <!-- Accept Overlay - Test or Review Details -->
    <div v-if="showAcceptOverlay" class="overlay" @click="closeAcceptOverlay">
      <div class="overlay-content" @click.stop>
        <div class="overlay-header">
          <h2>TEST OR REVIEW DETAILS</h2>
          <button class="close-button" @click="closeAcceptOverlay">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="overlay-body">
          <div class="form-row">
            <div class="form-field">
              <label>DATE OF TEST OR REVIEW</label>
              <input type="date" v-model="acceptFormData.testDate">
            </div>
            <div class="form-field">
              <label>INTERNAL TESTER EMP ID</label>
              <input type="text" v-model="acceptFormData.testerId" placeholder="Enter tester ID">
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-field">
              <label>INTERNAL TESTER NAME</label>
              <input type="text" v-model="acceptFormData.testerName" placeholder="Enter tester name">
            </div>
            <div class="form-field">
              <label>COMMENTS</label>
              <textarea v-model="acceptFormData.comments" placeholder="Enter comments"></textarea>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-field">
              <label>AUTHENTICATION</label>
              <input type="text" v-model="acceptFormData.authentication" placeholder="Enter authentication">
            </div>
            <div class="form-field">
              <label>ATTACHMENTS</label>
              <input type="file" @change="handleAttachmentUpload" multiple>
            </div>
          </div>
        </div>
        
        <div class="overlay-footer">
          <button class="btn btn-primary" @click="submitAcceptForm">DONE</button>
        </div>
      </div>
    </div>

    <!-- Reject Overlay - Memo Rejection Details -->
    <div v-if="showRejectOverlay" class="overlay" @click="closeRejectOverlay">
      <div class="overlay-content" @click.stop>
        <div class="overlay-header">
          <h2>MEMO REJECTION DETAILS</h2>
          <button class="close-button" @click="closeRejectOverlay">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="overlay-body">
          <div class="rejection-section" :class="{ 'active': rejectionFormData.section === 'comments' }" @click="selectRejectionSection('comments')">
            <div class="section-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
            </div>
            <span>COMMENTS</span>
            <div class="notification-icon">!</div>
          </div>
          
          <div class="rejection-section" :class="{ 'active': rejectionFormData.section === 'authentication' }" @click="selectRejectionSection('authentication')">
            <div class="section-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
            </div>
            <span>AUTHENTICATION</span>
            <div class="notification-icon">!</div>
          </div>
          
          <div class="rejection-section" :class="{ 'active': rejectionFormData.section === 'attachments' }" @click="selectRejectionSection('attachments')">
            <div class="section-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
              </svg>
            </div>
            <span>ATTACHMENTS</span>
          </div>
          
          <!-- Dynamic content based on selected section -->
          <div class="section-content">
            <div v-if="rejectionFormData.section === 'comments'" class="content-area">
              <label>Rejection Comments:</label>
              <textarea v-model="rejectionFormData.comments" placeholder="Enter rejection comments..."></textarea>
            </div>
            
            <div v-if="rejectionFormData.section === 'authentication'" class="content-area">
              <label>Authentication Details:</label>
              <input type="text" v-model="rejectionFormData.authentication" placeholder="Enter authentication details">
            </div>
            
            <div v-if="rejectionFormData.section === 'attachments'" class="content-area">
              <label>Rejection Attachments:</label>
              <input type="file" @change="handleRejectionAttachmentUpload" multiple>
            </div>
          </div>
        </div>
        
        <div class="overlay-footer">
          <button class="btn btn-primary" @click="submitRejectForm">DONE</button>
        </div>
      </div>
    </div>

    <!-- Additional Section - Test or Review Details (shown after Accept) -->
    <div v-if="showTestReviewSection" class="form-section test-review-details">
      <h3>Test or Review Details</h3>
      <div class="details-grid">
        <div class="detail-row">
          <div class="detail-field">
            <label>Date of Test or Review :</label>
            <div class="detail-value">{{ acceptFormData.testDate }}</div>
          </div>
          <div class="detail-field wide-field">
            <label>Comments :</label>
            <div class="detail-value">{{ acceptFormData.comments }}</div>
          </div>
        </div>
        
        <div class="detail-row">
          <div class="detail-field">
            <label>Internal Tester ID:</label>
            <div class="detail-value">{{ acceptFormData.testerId }}</div>
          </div>
          <div class="detail-field">
            <label>Internal Tester Name :</label>
            <div class="detail-value">{{ acceptFormData.testerName }}</div>
          </div>
        </div>
        
        <div class="detail-row">
          <div class="detail-field">
            <label>Authentication</label>
            <div class="detail-value">{{ acceptFormData.authentication }}</div>
          </div>
          <div class="detail-field">
            <label>Attachments</label>
            <div class="detail-value">{{ acceptFormData.attachments.length > 0 ? acceptFormData.attachments.join(', ') : 'No attachments' }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Additional Section - Rejection Details (shown after Reject) -->
    <div v-if="showRejectionSection" class="form-section rejection-details">
      <h3>Memo Rejection Details</h3>
      <div class="rejection-content">
        <div class="rejection-item">
          <label>Rejection Comments:</label>
          <div class="rejection-value">{{ rejectionFormData.comments }}</div>
        </div>
        
        <div class="rejection-item">
          <label>Authentication:</label>
          <div class="rejection-value">{{ rejectionFormData.authentication }}</div>
        </div>
        
        <div class="rejection-item">
          <label>Attachments:</label>
          <div class="rejection-value">{{ rejectionFormData.attachments.length > 0 ? rejectionFormData.attachments.join(', ') : 'No attachments' }}</div>
        </div>
      </div>
    </div>

    

    <div class="submit-section">
      <button class="submit-button" @click="submitMemo">
        Submit
      </button>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'QAHeadMemoForm',
  data() {
    return {
      memoId: '',
      memoData: {
        status: 'Not Assigned'
      },
      // Overlay visibility
      showAcceptOverlay: false,
      showRejectOverlay: false,
      
      // Accept form data
      acceptFormData: {
        testDate: '',
        testerId: '',
        testerName: '',
        comments: '',
        authentication: '',
        attachments: []
      },
      
      // Reject form data
      rejectionFormData: {
        section: 'comments',
        comments: '',
        authentication: '',
        attachments: []
      },
      
      // Additional sections visibility
      showTestReviewSection: false,
      showRejectionSection: false,
      
      // Share functionality
      showShareBox: false,
      emailAddresses: '',
      
      formData: {
        from: '',
        casdicRef: '',
        casdic: '',
        casdicDate: '',
        to: '',
        wingRef: '',
        coordinator: '',
        partNo: '',
        manufacturer: '',
        description: '',
        lruReady: false,
        refDoc: '',
        refNo: '',
        version: '',
        revision: '',
        slNo: '',
        drawingNo: '',
        description2: '',
        unitsNoted: false,
        refDoc2: '',
        refNo2: '',
        version2: '',
        revision2: '',
        qtyOffered: '',
        source: '',
        description3: '',
        unitsNoted2: false,
        refDoc3: '',
        refNo3: '',
        version3: '',
        revision3: '',
        unitId: '',
        mechanicalInsp: '',
        description4: '',
        unitsNoted3: false,
        refDoc4: '',
        refNo4: '',
        version4: '',
        revision4: '',
        inspectionStage: '',
        stteStatus: '',
        testVenue: '',
        signatureName: '',
        testFacility: '',
        testCycle: '',
        testStart: '',
        testComplete: '',
        calibrationStatus: '',
        funcCheckInitial: '',
        perfCheckDuring: '',
        funcCheckEnd: '',
        cert1: false,
        cert2: false,
        cert3: false,
        cert4: false,
        cert5: false,
        cert6: false,
        logBookDate: '',
        qaInspectionDate: '',
        dgaqaRemarks: '',
        testStatus: '',
        qaReviewerRemarks: ''
      }
    };
  },
  computed: {
    // Get current user role from global store
    currentUserRole() {
      return userStore.getters.currentUserRole()
    },
    canApproveMemo() {
      // The role '2' corresponds to the QA Head/Manager based on the SRS document.
      // This ensures only authorized users see the accept/reject buttons.
      return this.currentUserRole === 2;
    },
  },
  mounted() {
    this.memoId = this.$route.params.memoId;
    this.loadMemoData();
    console.log('Component mounted, initial data:', {
      memoId: this.memoId,
      rejectionFormData: this.rejectionFormData,
      acceptFormData: this.acceptFormData
    });
  },
  methods: {
    loadMemoData() {
      // Simulate loading memo data based on memoId
      // In a real application, this would fetch from an API
      this.memoData = {
        id: this.memoId,
        status: 'Not Assigned',
        title: 'DGAQA Inspection Requisition',
        project: 'PRJ-2025-078',
        date: '2025-01-15'
      };
      
      // Auto-fill some sample data
      this.formData.from = 'CASDIC QA Department';
      this.formData.casdicRef = 'CAS-2025-001';
      this.formData.casdic = 'CASDIC/QA/2025';
      this.formData.casdicDate = '2025-01-15';
      this.formData.to = 'DGAQA Office';
      this.formData.wingRef = 'WING-2025-078';
      this.formData.coordinator = 'John Smith (Designs) - +91-98765-43210';
      this.formData.partNo = 'LRU-001';
      this.formData.manufacturer = 'Aviatrax Industries';
      this.formData.description = 'Main Control Unit for Aircraft Navigation System';
    },
    // Overlay management
    closeAcceptOverlay() {
      this.showAcceptOverlay = false;
    },
    
    closeRejectOverlay() {
      this.showRejectOverlay = false;
    },
    
    // Rejection section selection
    selectRejectionSection(section) {
      console.log('Selecting rejection section:', section);
      this.rejectionFormData.section = section;
      console.log('Updated rejection form data:', this.rejectionFormData);
    },
    
    // File upload handlers
    handleAttachmentUpload(event) {
      const files = Array.from(event.target.files);
      this.acceptFormData.attachments = files.map(file => file.name);
    },
    
    handleRejectionAttachmentUpload(event) {
      const files = Array.from(event.target.files);
      this.rejectionFormData.attachments = files.map(file => file.name);
    },
    
    // Form submission
    submitAcceptForm() {
      if (!this.acceptFormData.testDate || !this.acceptFormData.testerId || !this.acceptFormData.testerName) {
        alert('Please fill in all required fields');
        return;
      }
      
      this.showTestReviewSection = true;
      this.closeAcceptOverlay();
      alert('Memo accepted successfully! Test/Review details have been added.');
    },
    
    submitRejectForm() {
      console.log('Submit reject form called');
      console.log('Rejection form data:', this.rejectionFormData);
      
      if (!this.rejectionFormData.comments && !this.rejectionFormData.authentication && this.rejectionFormData.attachments.length === 0) {
        alert('Please fill in at least one field for rejection details.');
        return;
      }
      
      this.showRejectionSection = true;
      this.closeRejectOverlay();
      alert('Memo rejected! Rejection details have been added.');
      console.log('Rejection form submitted successfully');
    },
    
    // Legacy methods (kept for compatibility)
    acceptMemo() {
      this.showAcceptOverlay = true;
    },
    
    rejectMemo() {
      this.showRejectOverlay = true;
    },

toggleShareBox() {
      this.showShareBox = !this.showShareBox;
      if (!this.showShareBox) {
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
      this.toggleShareBox(); // Close the share box after "sending"
    },

    submitMemo() {
    // Validate that at least one test status is selected
    const testStatusSelected = Object.values(this.memoData.testStatus).some(status => status);
      
      if (!testStatusSelected) {
        alert('Please select at least one test status.');
        return;
      }
      
      if (!this.memoData.reviewerComments.trim()) {
        alert('Please provide reviewer comments.');
        return;
      }
      
      // Here you would add the logic to submit the memo, for example, making an API call.
      console.log('Submitting memo:', {
        memoId: this.id,
        testStatus: this.memoData.testStatus,
        reviewerComments: this.memoData.reviewerComments
      });
      
      alert('Memo submitted successfully!');
      this.goBack(); // Navigate back after successful submission
    }
  }
};
</script>

<style scoped>
.memo-form {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #e9ecef;
}

.form-title {
  margin: 0;
  font-size: 1.8em;
  font-weight: bold;
  color: #333;
  text-align: center;
  flex-grow: 1;
}

.logo {
  height: 40px;
  width: auto;
}

.form-section {
  background-color: white;
  border-radius: 10px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 20px;
  align-items: end;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-field label {
  font-weight: bold;
  color: #495057;
  font-size: 0.9em;
}

.form-field input {
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1em;
  color: #495057;
  background-color: #f8f9fa;
  transition: border-color 0.3s ease;
}

.form-field input:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  outline: none;
}

.wide-field {
  grid-column: span 2;
}

.details-table {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 2fr 0.5fr 1fr 1fr 0.5fr 0.5fr;
  background-color: #e9ecef;
  padding: 15px;
  font-weight: bold;
  color: #495057;
  text-align: center;
  align-items: center;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 2fr 0.5fr 1fr 1fr 0.5fr 0.5fr;
  border-top: 1px solid #dee2e6;
  padding: 20px 15px;
  align-items: start;
  gap: 15px;
}

.lru-column {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.lru-field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.lru-field label {
  font-weight: bold;
  color: #495057;
  font-size: 0.8em;
}

.lru-field input {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 0.9em;
}

.desc-column textarea {
  width: 100%;
  height: 80px;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  resize: vertical;
  font-size: 0.9em;
}

.checkbox-column {
  display: flex;
  justify-content: center;
  align-items: center;
}

.checkbox-column input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.ref-column, .refno-column, .ver-column, .rev-column {
  display: flex;
  justify-content: center;
  align-items: center;
}

.ref-column input, .refno-column input, .ver-column input, .rev-column input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  text-align: center;
  font-size: 0.9em;
}

.stage-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.stage-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stage-field label {
  font-weight: bold;
  color: #495057;
  font-size: 1em;
}

.stage-field input {
  padding: 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1em;
}

.test-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 30px;
}

.test-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.test-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.test-field label {
  font-weight: bold;
  color: #495057;
  font-size: 0.9em;
}

.test-field input {
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1em;
}

.test-field span {
  color: #6c757d;
  font-size: 0.9em;
}

.signature-box {
  width: 100%;
  height: 60px;
  border: 2px dashed #ced4da;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.signature-box-large {
  width: 200px;
  height: 80px;
  border: 2px dashed #ced4da;
  border-radius: 8px;
  background-color: #f8f9fa;
  margin: 0 auto;
}

.certification h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.3em;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.certification-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

.cert-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.cert-item input[type="checkbox"] {
  width: 20px;
  height: 20px;
  margin-top: 3px;
  cursor: pointer;
}

.cert-item label {
  flex-grow: 1;
  color: #495057;
  line-height: 1.5;
}

.cert-item input[type="text"] {
  width: 150px;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  margin-left: 10px;
}

.signature-section {
  text-align: center;
  margin-top: 20px;
}

.signature-section p {
  margin: 10px 0 0 0;
  color: #6c757d;
  font-size: 0.9em;
}

.action-taken h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.3em;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.instruction {
  color: #6c757d;
  font-style: italic;
  margin-bottom: 20px;
}

.remarks-area {
  margin-bottom: 30px;
}

.remarks-area textarea {
  width: 100%;
  height: 120px;
  padding: 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  resize: vertical;
  font-size: 1em;
  font-family: inherit;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 40px;
}

.btn {
  padding: 15px 40px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 150px;
}

.btn-accept {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
}

.btn-accept:hover {
  background: linear-gradient(135deg, #218838, #1ea085);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.btn-reject {
  background: linear-gradient(135deg, #dc3545, #e74c3c);
  color: white;
}

.btn-reject:hover {
  background: linear-gradient(135deg, #c82333, #c0392b);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
}

.btn-primary {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #0056b3, #004085);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

@media (max-width: 768px) {
  .form-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .wide-field {
    grid-column: span 1;
  }
  
  .table-header, .table-row {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .lru-column, .desc-column, .checkbox-column, .ref-column, .refno-column, .ver-column, .rev-column {
    grid-column: span 1;
  }
  
  .stage-header {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .test-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
  }
}

/* Overlay Styles */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.overlay-content {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.overlay-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  background-color: #f8f9fa;
}

.overlay-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5em;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-button:hover {
  background-color: #e9ecef;
}

.overlay-body {
  padding: 20px;
}

.overlay-body .form-row {
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.overlay-body .form-field {
  margin-bottom: 15px;
}

.overlay-body textarea {
  width: 100%;
  height: 80px;
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  resize: vertical;
  font-size: 1em;
}

.overlay-footer {
  padding: 20px;
  border-top: 1px solid #e9ecef;
  background-color: #f8f9fa;
  text-align: center;
}

/* Rejection Section Styles */
.rejection-section {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: white;
  border: 1px solid #e9ecef;
}

.rejection-section:hover {
  background-color: #f8f9fa;
}

.rejection-section.active {
  background-color: #e9ecef;
  border-color: #007bff;
}

.section-icon {
  color: #6c757d;
}

.notification-icon {
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  margin-left: auto;
}

.section-content {
  margin-top: 20px;
}

.content-area {
  margin-bottom: 20px;
}

.content-area label {
  display: block;
  font-weight: bold;
  color: #495057;
  margin-bottom: 8px;
}

.content-area input,
.content-area textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1em;
  background-color: white;
  color: #333;
  cursor: text;
}

.content-area input:focus,
.content-area textarea:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  outline: none;
}

.content-area textarea {
  height: 100px;
  resize: vertical;
}

/* Additional Sections Styles */
.test-review-details,
.rejection-details {
  background-color: white;
  border-radius: 10px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.test-review-details h3,
.rejection-details h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.3em;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.details-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: start;
}

.detail-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-field.wide-field {
  grid-column: span 2;
}

.detail-field label {
  font-weight: bold;
  color: #495057;
  font-size: 0.9em;
}

.detail-value {
  padding: 12px 15px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  color: #333;
  min-height: 20px;
}

.rejection-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.rejection-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rejection-item label {
  font-weight: bold;
  color: #495057;
  font-size: 0.9em;
}

.rejection-value {
  padding: 12px 15px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  color: #333;
  min-height: 20px;
}

/* Status Display Styles */
.status-display {
  text-align: center;
  margin: 40px 0;
  padding: 30px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 15px;
  padding: 20px 40px;
  border-radius: 50px;
  font-size: 1.2em;
  font-weight: bold;
  color: white;
  margin-bottom: 15px;
}

.status-badge.accepted {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.status-badge.rejected {
  background: linear-gradient(135deg, #dc3545, #e74c3c);
}

.status-badge svg {
  width: 28px;
  height: 28px;
}

.status-date {
  color: #6c757d;
  font-size: 1em;
  margin: 0;
}

/* Responsive Design for Overlays */
@media (max-width: 768px) {
  .overlay-content {
    width: 95%;
    margin: 20px;
  }
  
  .overlay-body .form-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .detail-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .detail-field.wide-field {
    grid-column: span 1;
  }
  
  .rejection-section {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .notification-icon {
    margin-left: 0;
  }
  
  .status-badge {
    flex-direction: column;
    gap: 10px;
    padding: 15px 30px;
  }
}

/* Test Status Section */
.test-status .status-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 15px;
}

.test-status label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1em;
  color: #495057;
}

.test-status input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* QA Reviewer Remarks */
.reviewer-remarks .remarks-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.reviewer-remarks textarea {
  width: 100%;
  height: 120px;
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1em;
  resize: vertical;
  font-family: inherit;
  color: #333;
}

.reviewer-remarks p {
  text-align: right;
  font-weight: bold;
  color: #000;
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

/* Share Overlay Styles */
.share-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(8px);
}

.share-overlay-content {
  background: linear-gradient(145deg, #f8f9fa, #e9ecef);
  border-radius: 16px;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.share-overlay-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
  color: #000;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.share-overlay-header h3 {
  margin: 0;
  color: #000;
  font-size: 1.4em;
  font-weight: 600;
  text-shadow: none;
}

.close-btn {
  background: rgba(0, 0, 0, 0.1);
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: #000;
  backdrop-filter: blur(10px);
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.2);
  color: #000;
  transform: scale(1.1);
}

.share-overlay-body {
  padding: 40px;
  background: #f8f9fa;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex: 1;
  min-height: 200px;
}

.email-input {
  width: 100%;
  max-width: 400px;
  padding: 18px 24px;
  border: 2px solid #ced4da;
  border-radius: 12px;
  font-size: 1.1em;
  color: #000;
  background-color: #ffffff;
  transition: all 0.3s ease;
  margin-bottom: 30px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.email-input::placeholder {
  color: #6c757d;
}

.email-input:focus {
  border-color: #6c757d;
  box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.1);
  outline: none;
  background-color: #ffffff;
  transform: translateY(-2px);
}

.share-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  width: 100%;
  max-width: 400px;
}

.send-btn {
  padding: 16px 32px;
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 100px;
  box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
}

.send-btn:hover {
  background: linear-gradient(135deg, #495057 0%, #343a40 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(108, 117, 125, 0.4);
}

.cancel-btn {
  padding: 16px 32px;
  background: #adb5bd;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 100px;
  box-shadow: 0 4px 15px rgba(173, 181, 189, 0.3);
}

.cancel-btn:hover {
  background: #6c757d;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(173, 181, 189, 0.4);
}

/* Share Button Styles - Icon Only */
.share-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 8px;
}

.share-btn:hover {
  transform: scale(1.1);
}

.share-btn .icon {
  width: 24px;
  height: 24px;
  color: #000;
  stroke: #000;
  fill: none;
}

/* Responsive Design for Share Overlay */
@media (max-width: 768px) {
  .share-overlay-content {
    width: 95%;
    margin: 20px;
  }
  
  .share-actions {
    flex-direction: column;
  }
  
  .send-btn, .cancel-btn {
    width: 100%;
    min-width: auto;
  }
}
</style>
