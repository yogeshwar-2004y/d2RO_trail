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
      <div class="logos-container">
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
        <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
      </div>
    </div>

    <!-- Requisition Details Section -->
    <div class="form-section requisition-details">
      <table class="form-table">
        <tr>
          <td class="form-cell">
            <label>From :</label>
            <input type="text" v-model="formData.from1" placeholder="MED, CASDIC (DARE), Bangalore">
            
          </td>
          <td class="form-cell">
            <label>CASDIC Ref No.:</label>
          </td>
          <td class="form-cell">
            <label>CASDIC/</label>
            <input type="text" v-model="formData.casdic" placeholder="">
          </td>
          <td class="form-cell">
            <label>Dated:</label>
            <input type="date" v-model="formData.casdicDate">
          </td>
        </tr>
        <tr>
          <td class="form-cell">
            <label>To :</label>
            <input type="text" v-model="formData.from2" placeholder="DGAQA cell,">
            <input type="text" v-model="formData.from3" placeholder="ORDAQA(ADE), Bangalore">
          </td>
          <td class="form-cell">
            <label>Thru/: O I/c, WH</label>
          </td>
          <td class="form-cell">
            <label>Wing/Proj Ref No.:</label>
            <input type="text" v-model="formData.wingRef" placeholder="">
          </td>
          <td class="form-cell"></td>
        </tr>
        <tr>
          <td class="form-cell"></td>
          <td class="form-cell wide-field" colspan="3">
            <label>Name & contact No of CASDIC (Designs) coordinator:</label>
            <input type="text" v-model="formData.coordinator" placeholder="">
          </td>
        </tr>
      </table>
    </div>

    <!-- LRU/SRU Details Section -->
    <div class="form-section lru-details">
      <table class="details-table">
        <thead>
          <tr>
            <th rowspan="2" class="lru-header">LRU / SRU DETAILS</th>
            <th rowspan="2" class="desc-header">LRU / SRU Desc:</th>
            <th rowspan="2" class="ref-doc-header">Ref Doc</th>
            <th rowspan="2" class="ref-no-header">Ref No of Document</th>
            <th class="ver-header">ver</th>
            <th class="rev-header">rev</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>Part No:</label>
                <input type="text" v-model="formData.partNo" placeholder="">
              </div>
              <div class="lru-field">
                <label>Manufacturer:</label>
                <input type="text" v-model="formData.manufacturer" placeholder="">
              </div>
            </td>
            <td class="desc-cell">
              <select v-model="formData.description" class="lru-description-select">
                <option value="">Select LRU</option>
                <option v-for="lruName in lruOptions" :key="lruName" :value="lruName">
                  {{ lruName }}
                </option>
              </select>
            </td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc" placeholder="">
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo" placeholder="">
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version" placeholder="">
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision" placeholder="">
            </td>
          </tr>
          
          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>Sl.No of units :</label>
                <input type="text" v-model="formData.slNo" placeholder="">
              </div>
              <div class="lru-field">
                <label>Drawing no/Rev:</label>
                <input type="text" v-model="formData.drawingNo" placeholder="">
              </div>
            </td>
            <td class="desc-cell"></td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc2" placeholder="">
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo2" placeholder="">
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version2" placeholder="">
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision2" placeholder="">
            </td>
          </tr>
          
          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>Qty Offered:</label>
                <input type="text" v-model="formData.qtyOffered" placeholder="">
              </div>
              <div class="lru-field">
                <label>source :</label>
                <span>NA</span>
              </div>
            </td>
            <td class="desc-cell"></td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc3" placeholder="">
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo3" placeholder="">
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version3" placeholder="">
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision3" placeholder="">
            </td>
          </tr>
          
          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>UNIT IDENTIFICATION :</label>
                <select v-model="formData.unitIdentification" class="lru-select">
                  <option value="">Select Type</option>
                  <option value="SOFT">SOFT</option>
                  <option value="QT">QT</option>
                  <option value="AT">AT</option>
                  <option value="DT">DT</option>
                  <option value="TS">TS</option>
                  <option value="ESS">ESS</option>
                </select>
              </div>
              <div class="lru-field">
                <label>MECHANICAL INSPN :</label>
                <select v-model="formData.mechanicalInsp" class="lru-select">
                  <option value="">Select Stage</option>
                  <option value="STAGE">STAGE</option>
                  <option value="PARTS">PARTS</option>
                  <option value="ASSY">ASSY</option>
                  <option value="FINAL">FINAL</option>
                  <option value="INSTALL">INSTALL</option>
                </select>
              </div>
            </td>
            <td class="desc-cell"></td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc4" placeholder="">
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo4" placeholder="">
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version4" placeholder="">
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision4" placeholder="">
            </td>
          </tr>
          
          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>INSPECTION / TEST STAGE OFFERED NOW:</label>
                <input type="text" v-model="formData.inspectionStage" placeholder="">
              </div>
            </td>
            <td class="desc-cell">
              <div class="lru-field">
                <label>STTE Status:</label>
                <input type="text" v-model="formData.stteStatus" placeholder="">
              </div>
            </td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc5" placeholder="">
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo5" placeholder="">
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version5" placeholder="">
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision5" placeholder="">
            </td>
          </tr>
          
          <tr>
            <td class="lru-cell">
              <label>TEST STAGE CLEARED:</label>
              <input type="text" v-model="formData.testStageCleared" placeholder="">
            </td>
            <td class="desc-cell"></td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc6" placeholder="">
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo6" placeholder="">
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version6" placeholder="">
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision6" placeholder="">
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Test Details Section -->
    <div class="form-section test-details">
      <table class="test-table">
        <tr>
          <td class="test-left">
            <div class="test-field">
              <label>Above Unit is ready for Testing at</label>
              <input type="text" v-model="formData.testVenue" placeholder="">
              <span>onwards.</span>
            </div>
            <div class="test-field">
              <label>SIGNATURE :</label>
              <div class="signature-box"></div>
            </div>
            <div class="test-field">
              <label>NAME / DESIGNATION</label>
              <input type="text" v-model="formData.signatureName" placeholder="">
            </div>
            <div class="test-field">
              <span>It is certified that :</span>
            </div>
          </td>
          <td class="test-middle">
            <div class="test-field">
              <label>i. Test facility to be used :</label>
              <input type="text" v-model="formData.testFacility" placeholder="">
            </div>
            <div class="test-field">
              <label>ii. Test cycle / Duration:</label>
              <input type="text" v-model="formData.testCycle" placeholder="">
              <span>hrs</span>
            </div>
            <div class="test-field">
              <label>iii. Test start on:</label>
              <input type="text" v-model="formData.testStart" placeholder="date/time">
            </div>
            <div class="test-field">
              <label>iv. Test complete on :</label>
              <input type="text" v-model="formData.testComplete" placeholder="date/time">
            </div>
          </td>
          <td class="test-right">
            <div class="test-field">
              <label>v. Calibration status: OK / Due on</label>
              <input type="text" v-model="formData.calibrationStatus" placeholder="">
            </div>
            <div class="test-field">
              <label>vi. Func. Check (Initial):</label>
              <input type="text" v-model="formData.funcCheckInitial" placeholder="date/time">
            </div>
            <div class="test-field">
              <label>vii. Perf.check (during):</label>
              <input type="text" v-model="formData.perfCheckDuring" placeholder="date/time">
            </div>
            <div class="test-field">
              <label>viii. Func Check (end):</label>
              <input type="text" v-model="formData.funcCheckEnd" placeholder="date/time">
            </div>
          </td>
        </tr>
      </table>
    </div>

    <!-- Certification Section -->
    <div class="form-section certification">
      <div class="certification-header">
        <span class="certification-statement">It is certified that:</span>
      </div>
      <div class="certification-list">
        <div class="cert-item">
          <input type="checkbox" v-model="formData.certificationA" class="cert-checkbox" id="certA">
          <span class="cert-letter">a)</span>
          <span class="cert-text">Mechanical Quality Records of all the parts ( Raw material TC (chemical & mechanical), Dimensional reports, NDT reports, Process certificates etc. ) & Electrical Quality Records (Components Screening report, PCB manufacturing report, process compliance reports / test reports, etc.) were verified thoroughly .</span>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.certificationB" class="cert-checkbox" id="certB">
          <span class="cert-letter">b)</span>
          <span class="cert-text">CoC for SRU, fasteners & standard parts are verified and satisfactory</span>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.certificationC" class="cert-checkbox" id="certC">
          <span class="cert-letter">c)</span>
          <span class="cert-text">Sl no of the SRUs are noted down in the respective log book opened on <input type="text" v-model="formData.logBookDate" placeholder="" class="inline-input"></span>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.certificationD" class="cert-checkbox" id="certD">
          <span class="cert-letter">d)</span>
          <span class="cert-text">No Defect investigation is pending against this LRU</span>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.certificationE" class="cert-checkbox" id="certE">
          <span class="cert-letter">e)</span>
          <span class="cert-text">All the previous test stages of this LRU /SRU are cleared</span>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.certificationF" class="cert-checkbox" id="certF">
          <span class="cert-letter">f)</span>
          <span class="cert-text">CASDIC QA has physically inspected and accepted the LRU on <input type="text" v-model="formData.qaInspectionDate" placeholder="" class="inline-input"></span>
        </div>
      </div>
      
      <!-- IQA CASDIC Signature moved above action taken section -->
      <div class="iqa-signature-section">
        <div class="signature-box-large"></div>
        <p>SIGNATURE of Rep, IQA CASDIC</p>
      </div>
      
      <div class="action-taken-section">
        <span class="action-taken-text">Action taken & remarks by DGAQA</span>
        <div class="dgaqa-remarks-box">
          <textarea v-model="formData.dgaqaRemarks" placeholder="Enter DGAQA action taken and remarks..." class="dgaqa-textarea"></textarea>
        </div>
      </div>
      
      <!-- DGAQA Signature moved to the end -->
      <div class="dgaqa-signature-section">
        <p class="instruction">(please use space overleaf for details)</p>
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
          Test failed
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
      
      // LRU options from database
      lruOptions: [],
      
      formData: {
        from1: '',
        from2: '',
        from3: '',
        casdicRef: '',
        casdic: '',
        casdicDate: '',
        to1: '',
        to2: '',
        wingRef: '',
        coordinator: '',
        partNo: '',
        manufacturer: '',
        description: '',
        refDoc: '',
        refNo: '',
        version: '',
        revision: '',
        slNo: '',
        drawingNo: '',
        refDoc2: '',
        refNo2: '',
        version2: '',
        revision2: '',
        qtyOffered: '',
        description3: '',
        refDoc3: '',
        refNo3: '',
        version3: '',
        revision3: '',
        mechanicalInsp: '',
        unitIdentification: '',
        refDoc4: '',
        refNo4: '',
        version4: '',
        revision4: '',
        inspectionStage: '',
        stteStatus: '',
        refDoc5: '',
        refNo5: '',
        version5: '',
        revision5: '',
        testStageCleared: '',
        refDoc6: '',
        refNo6: '',
        version6: '',
        revision6: '',
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
        logBookDate: '',
        qaInspectionDate: '',
        testStatus: '',
        qaReviewerRemarks: '',
        certificationA: false,
        certificationB: false,
        certificationC: false,
        certificationD: false,
        certificationE: false,
        certificationF: false,
        dgaqaRemarks: ''
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
    }
  },
  mounted() {
    this.memoId = this.$route.params.memoId;
    this.loadMemoData();
    this.fetchLruOptions();
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
    
    async fetchLruOptions() {
      try {
        const response = await fetch('http://localhost:5000/api/lru-names');
        const data = await response.json();
        
        if (data.success) {
          this.lruOptions = data.lru_names;
        } else {
          console.error('Failed to fetch LRU names:', data.message);
          alert('Failed to load LRU names. Please try again.');
        }
      } catch (error) {
        console.error('Error fetching LRU names:', error);
        alert('Error loading LRU names. Please check your connection.');
      }
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

.form-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #333;
}

.form-table td, .form-table th {
  border: 1px solid #333;
  padding: 8px;
  vertical-align: top;
}

.form-cell {
  position: relative;
}

.form-cell label {
  font-weight: bold;
  color: #333;
  font-size: 0.9em;
  display: block;
  margin-bottom: 5px;
}

.form-cell input {
  width: 100%;
  padding: 4px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
  margin-bottom: 3px;
  box-sizing: border-box;
}

.form-cell input:focus {
  border-color: #80bdff;
  outline: none;
}

.wide-field {
  grid-column: span 2;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #333;
}

.details-table th, .details-table td {
  border: 1px solid #333;
  padding: 8px;
  text-align: left;
  vertical-align: top;
}

.details-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  text-align: center;
}

.lru-header {
  width: 25%;
}

.desc-header {
  width: 25%;
}

.ref-doc-header {
  width: 15%;
}

.ref-no-header {
  width: 20%;
}

.ver-header, .rev-header {
  width: 7.5%;
}

.lru-cell, .desc-cell, .ref-cell, .refno-cell, .ver-cell, .rev-cell {
  vertical-align: top;
}

.lru-field {
  margin-bottom: 10px;
}

.lru-field label {
  font-weight: bold;
  color: #333;
  font-size: 0.8em;
  display: block;
  margin-bottom: 3px;
}

.lru-field input {
  width: 100%;
  padding: 4px 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 0.8em;
  box-sizing: border-box;
}

.lru-select {
  width: 100%;
  padding: 4px 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 0.8em;
  box-sizing: border-box;
  background-color: white;
  cursor: pointer;
}

.lru-select:focus {
  border-color: #80bdff;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.lru-select option {
  padding: 4px 6px;
  font-size: 0.8em;
}

.desc-cell textarea {
  width: 100%;
  height: 60px;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  resize: vertical;
  font-size: 0.8em;
  box-sizing: border-box;
}

.lru-description-select {
  width: 100%;
  height: 60px;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 0.8em;
  box-sizing: border-box;
  background-color: white;
  cursor: pointer;
  overflow-y: auto;
}

.lru-description-select:focus {
  border-color: #80bdff;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.lru-description-select option {
  padding: 4px 6px;
  font-size: 0.8em;
}

.desc-cell span {
  color: #666;
  font-size: 0.8em;
  font-style: italic;
}

.ref-cell input, .refno-cell input, .ver-cell input, .rev-cell input {
  width: 100%;
  padding: 4px 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  text-align: center;
  font-size: 0.8em;
  box-sizing: border-box;
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

.test-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #333;
}

.test-table td {
  border: 1px solid #333;
  padding: 15px;
  vertical-align: top;
  width: 33.33%;
}

.test-left, .test-middle, .test-right {
  vertical-align: top;
}

.test-field {
  margin-bottom: 15px;
}

.test-field label {
  font-weight: bold;
  color: #333;
  font-size: 0.9em;
  display: block;
  margin-bottom: 5px;
}

.test-field input {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
  box-sizing: border-box;
}

.test-field span {
  color: #666;
  font-size: 0.9em;
  margin-left: 5px;
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

.certification-header {
  margin-bottom: 20px;
}

.certification-statement {
  font-weight: bold;
  color: #333;
  font-size: 1.1em;
}

.certification-list {
  margin-bottom: 30px;
}

.cert-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 12px;
}

.cert-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  margin-top: 2px;
  flex-shrink: 0;
}

.cert-letter {
  font-weight: bold;
  color: #333;
  min-width: 20px;
}

.cert-text {
  flex-grow: 1;
  color: #333;
  line-height: 1.4;
  font-size: 0.9em;
}

.inline-input {
  display: inline;
  width: 100px;
  padding: 2px 6px;
  border: none;
  border-bottom: 1px solid #333;
  background: transparent;
  font-size: 0.9em;
  margin: 0 3px;
}

.iqa-signature-section {
  text-align: center;
  margin: 30px 0 20px 0;
}

.iqa-signature-section p {
  margin: 10px 0 0 0;
  color: #6c757d;
  font-size: 0.9em;
  font-weight: bold;
}

.action-taken-section {
  margin: 30px 0 20px 0;
}

.action-taken-text {
  font-weight: bold;
  color: #333;
  font-size: 1em;
  display: block;
  margin-bottom: 15px;
}

.dgaqa-remarks-box {
  margin-top: 15px;
}

.dgaqa-textarea {
  width: 100%;
  height: 120px;
  padding: 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  resize: vertical;
  font-size: 1em;
  font-family: inherit;
  color: #333;
  background-color: white;
  box-sizing: border-box;
}

.dgaqa-textarea:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  outline: none;
}

.dgaqa-signature-section {
  text-align: center;
  margin: 30px 0 20px 0;
}

.dgaqa-signature-section p {
  margin: 10px 0 0 0;
  color: #6c757d;
  font-size: 0.9em;
}

.dgaqa-signature-section .instruction {
  font-style: italic;
  margin-bottom: 20px;
}

.signature-sections {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 30px;
  margin-top: 30px;
}

.signature-section.left {
  flex: 1;
}

.remarks-section {
  flex: 1;
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
</style>

