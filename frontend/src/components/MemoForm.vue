<template>
  <div class="memo-form">
    <!-- Header -->
    <div class="form-header">
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

      <h1 class="form-title">REQUISITION FOR DGAQA INSPECTION</h1>
      <button class="share-btn" @click="toggleShareBox">
        <svg
          class="icon share"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path
            d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"
          />
        </svg>
      </button>
    </div>

    <!-- Requisition Details Section -->
    <div class="form-section requisition-details">
      <table class="form-table">
        <tr>
          <td class="form-cell">
            <label>From :</label>
            <input
              type="text"
              v-model="formData.from1"
              placeholder="MED, CASDIC (DARE), Bangalore"
              :readonly="isNewMemo"
              :class="{ 'readonly-field': isNewMemo }"
            />
          </td>
          <td class="form-cell">
            <label>CASDIC Ref No.:</label>
          </td>
          <td class="form-cell">
            <label>CASDIC/</label>
            <input type="text" v-model="formData.casdic" placeholder="" />
          </td>
          <td class="form-cell">
            <label>Dated:</label>
            <input type="date" v-model="formData.casdicDate" />
          </td>
        </tr>
        <tr>
          <td class="form-cell">
            <label>To :</label>
            <input
              type="text"
              v-model="formData.from2"
              placeholder="DGAQA cell,"
              :readonly="isNewMemo"
              :class="{ 'readonly-field': isNewMemo }"
            />
            <input
              type="text"
              v-model="formData.from3"
              placeholder="ORDAQA(ADE), Bangalore"
              :readonly="isNewMemo"
              :class="{ 'readonly-field': isNewMemo }"
            />
          </td>
          <td class="form-cell">
            <label>Thru/: O I/c, WH</label>
          </td>
          <td class="form-cell">
            <label>Wing/Proj Ref No.:</label>
            <input type="text" v-model="formData.wingRef" placeholder="" />
          </td>
          <td class="form-cell"></td>
        </tr>
        <tr>
          <td class="form-cell"></td>
          <td class="form-cell wide-field" colspan="3">
            <label>Name & contact No of CASDIC (Designs) coordinator:</label>
            <input type="text" v-model="formData.coordinator" placeholder="" />
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
                <input type="text" v-model="formData.partNo" placeholder="" />
              </div>
              <div class="lru-field">
                <label>Manufacturer:</label>
                <input
                  type="text"
                  v-model="formData.manufacturer"
                  placeholder=""
                />
              </div>
            </td>
            <td class="desc-cell">
              <select
                v-model="formData.description"
                class="lru-description-select"
                :disabled="lruLoading"
              >
                <option value="">
                  {{
                    lruLoading
                      ? "Loading LRUs..."
                      : lruError
                      ? "Error loading LRUs"
                      : "Select LRU"
                  }}
                </option>
                <option
                  v-for="lru in lruData"
                  :key="lru.lru_id"
                  :value="lru.lru_name"
                >
                  {{ lru.lru_name }} ({{ lru.project_name }})
                </option>
              </select>
              <div v-if="lruError" class="error-message">
                <span>{{ lruError }}</span>
                <button @click="fetchLruOptions" class="retry-btn">
                  Retry
                </button>
              </div>
              <div v-if="lruData.length > 0 && lruError" class="info-message">
                Using fallback data. Start the backend server for live data.
              </div>
            </td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc" placeholder="" />
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo" placeholder="" />
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version" placeholder="" />
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision" placeholder="" />
            </td>
          </tr>

          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>Sl.No of units :</label>
                <div class="serial-number-dropdown-container">
                  <div
                    class="serial-number-dropdown"
                    :class="{ active: showSerialNumberDropdown }"
                    @click="toggleSerialNumberDropdown"
                    :disabled="
                      !selectedLruInfo ||
                      serialNumberLoading ||
                      availableSerialNumbers.length === 0
                    "
                  >
                    <div class="selected-value">
                      <span v-if="!selectedLruInfo" class="placeholder-text"
                        >Select LRU first</span
                      >
                      <span v-else-if="serialNumberLoading" class="loading-text"
                        >Loading serial numbers...</span
                      >
                      <span v-else-if="serialNumberError" class="error-text"
                        >Error loading serial numbers</span
                      >
                      <span
                        v-else-if="availableSerialNumbers.length === 0"
                        class="no-data-text"
                        >No serial numbers available</span
                      >
                      <div
                        v-else-if="formData.slNo && formData.slNo.length > 0"
                        class="selected-serials"
                      >
                        <span class="serial-list">{{
                          selectedSerialNumbersDisplay
                        }}</span>
                      </div>
                      <span v-else class="placeholder-text"
                        >Select Serial Numbers</span
                      >
                    </div>
                    <div class="dropdown-icon">▾</div>
                  </div>

                  <!-- Serial Number Checkbox Dropdown -->
                  <div
                    v-if="
                      showSerialNumberDropdown &&
                      availableSerialNumbers.length > 0
                    "
                    class="serial-number-menu"
                  >
                    <div class="serial-menu-header">
                      <span class="menu-title">Select Serial Numbers</span>
                      <button
                        @click.stop="clearSerialNumbers"
                        class="clear-btn"
                      >
                        Clear All
                      </button>
                    </div>
                    <div class="serial-menu-content">
                      <div
                        v-for="option in availableSerialNumbers"
                        :key="option.value"
                        class="serial-checkbox-item"
                        :class="{
                          selected: isSerialNumberSelected(option.value),
                        }"
                        @click="toggleSerialNumber(option.value)"
                      >
                        <div class="checkbox-wrapper">
                          <input
                            type="checkbox"
                            :checked="isSerialNumberSelected(option.value)"
                            class="serial-checkbox"
                            @click.stop
                          />
                          <div
                            class="checkbox-custom"
                            :class="{
                              checked: isSerialNumberSelected(option.value),
                            }"
                          >
                            <svg
                              v-if="isSerialNumberSelected(option.value)"
                              class="check-icon"
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              stroke-width="2"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                            >
                              <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                          </div>
                        </div>
                        <span class="serial-label"
                          >Serial {{ option.label }}</span
                        >
                        <div
                          v-if="isSerialNumberSelected(option.value)"
                          class="selected-indicator"
                        >
                          ✓
                        </div>
                      </div>
                    </div>
                  </div>

                  <div v-if="serialNumberError" class="error-message">
                    <span>{{ serialNumberError }}</span>
                    <button
                      @click="fetchSerialNumbers(selectedLruInfo.lru_id)"
                      class="retry-btn"
                    >
                      Retry
                    </button>
                  </div>
                </div>
              </div>
              <div class="lru-field">
                <label>Drawing no/Rev:</label>
                <input
                  type="text"
                  v-model="formData.drawingNo"
                  placeholder=""
                />
              </div>
            </td>
            <td class="desc-cell"></td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc2" placeholder="" />
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo2" placeholder="" />
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version2" placeholder="" />
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision2" placeholder="" />
            </td>
          </tr>

          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>Qty Offered:</label>
                <input
                  type="text"
                  :value="quantityOffered"
                  readonly
                  class="readonly-field"
                  placeholder="Auto-calculated from selected serials"
                />
              </div>
              <div class="lru-field">
                <label>source :</label>
                <input
                  type="text"
                  v-model="formData.source"
                  placeholder="NA"
                  class="source-input"
                />
              </div>
            </td>
            <td class="desc-cell"></td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc3" placeholder="" />
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo3" placeholder="" />
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version3" placeholder="" />
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision3" placeholder="" />
            </td>
          </tr>

          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>UNIT IDENTIFICATION :</label>
                <select v-model="formData.unitIdentification" class="lru-select">
                  <option value="">Select Unit Identification</option>
                  <option value="ESS">ESS</option>
                  <option value="SoFT">SoFT</option>
                  <option value="QT">QT</option>
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
              <input type="text" v-model="formData.refDoc4" placeholder="" />
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo4" placeholder="" />
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version4" placeholder="" />
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision4" placeholder="" />
            </td>
          </tr>

          <tr>
            <td class="lru-cell">
              <div class="lru-field unit-identification-container">
                <label>INSPECTION / TEST STAGE OFFERED NOW:</label>
                <div class="cascading-dropdown">
                  <div
                    class="dropdown-trigger"
                    @click="toggleCascadingDropdown"
                  >
                    <span class="selected-text">{{
                      getInspectionStageText() || "Select Test Group"
                    }}</span>
                    <span class="dropdown-arrow">▼</span>
                  </div>

                  <!-- Level 1: Test Groups -->
                  <div
                    v-if="showCascadingDropdown"
                    class="cascading-menu level-1"
                  >
                    <div v-if="loadingTestGroups" class="menu-item loading">
                      Loading test groups...
                    </div>
                    <div
                      v-else-if="testGroups.length === 0"
                      class="menu-item no-data"
                    >
                      No test groups available
                    </div>
                    <div
                      v-else
                      v-for="group in testGroups"
                      :key="group.group_id"
                      class="menu-item"
                      :class="{ active: hoveredTestGroup === group.group_id }"
                      @mouseenter="handleTestGroupHover(group)"
                      @click="selectTestGroup(group)"
                    >
                      <span class="item-text">{{ group.group_name }}</span>
                      <span class="arrow">▶</span>
                    </div>
                  </div>

                  <!-- Level 2: Sub-Tests -->
                  <div
                    v-if="showSubTests && hoveredTestGroup"
                    class="cascading-menu level-2"
                    @mouseenter="keepSubTestsOpen = true"
                    @mouseleave="handleSubTestsLeave"
                  >
                    <div v-if="loadingSubTests" class="menu-item loading">
                      Loading sub-tests...
                    </div>
                    <div
                      v-else-if="subTests.length === 0"
                      class="menu-item no-data"
                    >
                      No sub-tests available
                    </div>
                    <div
                      v-else
                      v-for="subTest in subTests"
                      :key="subTest.sub_test_id"
                      class="menu-item"
                      :class="{
                        active: hoveredSubTest === subTest.sub_test_id,
                      }"
                      @mouseenter="handleSubTestHover(subTest)"
                      @click="selectSubTest(subTest)"
                    >
                      <span class="item-text">{{ subTest.sub_test_name }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </td>
            <td class="desc-cell">
              <div class="lru-field">
                <label>STTE Status:</label>
                <input
                  type="text"
                  v-model="formData.stteStatus"
                  placeholder=""
                />
              </div>
            </td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc5" placeholder="" />
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo5" placeholder="" />
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version5" placeholder="" />
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision5" placeholder="" />
            </td>
          </tr>

          <tr>
            <td class="lru-cell">
              <label>TEST STAGE CLEARED:</label>
              <input
                type="text"
                v-model="formData.testStageCleared"
                placeholder=""
              />
            </td>
            <td class="desc-cell"></td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc6" placeholder="" />
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo6" placeholder="" />
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version6" placeholder="" />
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision6" placeholder="" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Test Details Section -->
    <div
      class="form-section test-details"
      :class="{ 'disabled-section': isTestDetailsDisabled }"
    >
      <table class="test-table">
        <tr>
          <td class="test-left">
            <div class="test-field">
              <label>Above Unit is ready for Testing at</label>
              <input
                type="text"
                v-model="formData.testVenue"
                placeholder=""
                :disabled="isTestDetailsDisabled"
              />
              <span>onwards.</span>
            </div>
            <div class="test-field">
              <label>SIGNATURE :</label>
              <div class="signature-box"></div>
            </div>
            <div class="test-field">
              <label>NAME / DESIGNATION</label>
              <input
                type="text"
                v-model="formData.signatureName"
                placeholder=""
                :disabled="isTestDetailsDisabled"
              />
            </div>
            <div class="test-field">
              <span>It is certified that :</span>
            </div>
          </td>
          <td class="test-middle">
            <div class="test-field">
              <label>i. Test facility to be used :</label>
              <input
                type="text"
                v-model="formData.testFacility"
                placeholder=""
                :disabled="isTestDetailsDisabled"
              />
            </div>
            <div class="test-field">
              <label>ii. Test cycle / Duration:</label>
              <input
                type="text"
                v-model="formData.testCycle"
                placeholder=""
                :disabled="isTestDetailsDisabled"
              />
              <span>hrs</span>
            </div>
            <div class="test-field">
              <label>iii. Test start on:</label>
              <div class="datetime-container">
                <input
                  type="date"
                  v-model="formData.testStartDate"
                  class="date-input"
                  :disabled="isTestDetailsDisabled"
                />
                <div class="time-picker">
                  <select
                    v-model="formData.testStartHour"
                    class="time-select"
                    :disabled="isTestDetailsDisabled"
                  >
                    <option value="">HH</option>
                    <option v-for="hour in hours" :key="hour" :value="hour">
                      {{ hour }}
                    </option>
                  </select>
                  <span class="time-separator">:</span>
                  <select
                    v-model="formData.testStartMinute"
                    class="time-select"
                    :disabled="isTestDetailsDisabled"
                  >
                    <option value="">MM</option>
                    <option
                      v-for="minute in minutes"
                      :key="minute"
                      :value="minute"
                    >
                      {{ minute }}
                    </option>
                  </select>
                  <select
                    v-model="formData.testStartAmPm"
                    class="ampm-select"
                    :disabled="isTestDetailsDisabled"
                  >
                    <option value="">AM/PM</option>
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="test-field">
              <label>iv. Test complete on :</label>
              <div class="datetime-container">
                <input
                  type="date"
                  v-model="formData.testCompleteDate"
                  class="date-input"
                  :disabled="isTestDetailsDisabled"
                />
                <div class="time-picker">
                  <select
                    v-model="formData.testCompleteHour"
                    class="time-select"
                    :disabled="isTestDetailsDisabled"
                  >
                    <option value="">HH</option>
                    <option v-for="hour in hours" :key="hour" :value="hour">
                      {{ hour }}
                    </option>
                  </select>
                  <span class="time-separator">:</span>
                  <select
                    v-model="formData.testCompleteMinute"
                    class="time-select"
                    :disabled="isTestDetailsDisabled"
                  >
                    <option value="">MM</option>
                    <option
                      v-for="minute in minutes"
                      :key="minute"
                      :value="minute"
                    >
                      {{ minute }}
                    </option>
                  </select>
                  <select
                    v-model="formData.testCompleteAmPm"
                    class="ampm-select"
                    :disabled="isTestDetailsDisabled"
                  >
                    <option value="">AM/PM</option>
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                  </select>
                </div>
              </div>
            </div>
          </td>
          <td class="test-right">
            <div class="test-field">
              <label>v. Calibration status: OK / Due on</label>
              <input
                type="text"
                v-model="formData.calibrationStatus"
                placeholder=""
              />
            </div>
            <div class="test-field">
              <label>vi. Func. Check (Initial):</label>
              <div class="datetime-container">
                <input
                  type="date"
                  v-model="formData.funcCheckInitialDate"
                  class="date-input"
                />
                <div class="time-picker">
                  <select
                    v-model="formData.funcCheckInitialHour"
                    class="time-select"
                  >
                    <option value="">HH</option>
                    <option v-for="hour in hours" :key="hour" :value="hour">
                      {{ hour }}
                    </option>
                  </select>
                  <span class="time-separator">:</span>
                  <select
                    v-model="formData.funcCheckInitialMinute"
                    class="time-select"
                  >
                    <option value="">MM</option>
                    <option
                      v-for="minute in minutes"
                      :key="minute"
                      :value="minute"
                    >
                      {{ minute }}
                    </option>
                  </select>
                  <select
                    v-model="formData.funcCheckInitialAmPm"
                    class="ampm-select"
                  >
                    <option value="">AM/PM</option>
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="test-field">
              <label>vii. Perf.check (during):</label>
              <div class="datetime-container">
                <input
                  type="date"
                  v-model="formData.perfCheckDuringDate"
                  class="date-input"
                />
                <div class="time-picker">
                  <select
                    v-model="formData.perfCheckDuringHour"
                    class="time-select"
                  >
                    <option value="">HH</option>
                    <option v-for="hour in hours" :key="hour" :value="hour">
                      {{ hour }}
                    </option>
                  </select>
                  <span class="time-separator">:</span>
                  <select
                    v-model="formData.perfCheckDuringMinute"
                    class="time-select"
                  >
                    <option value="">MM</option>
                    <option
                      v-for="minute in minutes"
                      :key="minute"
                      :value="minute"
                    >
                      {{ minute }}
                    </option>
                  </select>
                  <select
                    v-model="formData.perfCheckDuringAmPm"
                    class="ampm-select"
                  >
                    <option value="">AM/PM</option>
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="test-field">
              <label>viii. Func Check (end):</label>
              <div class="datetime-container">
                <input
                  type="date"
                  v-model="formData.funcCheckEndDate"
                  class="date-input"
                />
                <div class="time-picker">
                  <select
                    v-model="formData.funcCheckEndHour"
                    class="time-select"
                  >
                    <option value="">HH</option>
                    <option v-for="hour in hours" :key="hour" :value="hour">
                      {{ hour }}
                    </option>
                  </select>
                  <span class="time-separator">:</span>
                  <select
                    v-model="formData.funcCheckEndMinute"
                    class="time-select"
                  >
                    <option value="">MM</option>
                    <option
                      v-for="minute in minutes"
                      :key="minute"
                      :value="minute"
                    >
                      {{ minute }}
                    </option>
                  </select>
                  <select
                    v-model="formData.funcCheckEndAmPm"
                    class="ampm-select"
                  >
                    <option value="">AM/PM</option>
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                  </select>
                </div>
              </div>
            </div>
          </td>
        </tr>
      </table>
    </div>

    <!-- Certification Section -->
    <div
      class="form-section certification"
      :class="{ 'disabled-section': isCertificationDisabled }"
    >
      <div class="certification-header">
        <span class="certification-statement">It is certified that:</span>
      </div>
      <div class="certification-list">
        <div class="cert-item">
          <input
            type="checkbox"
            v-model="formData.certificationA"
            class="cert-checkbox"
            id="certA"
            :disabled="isCertificationDisabled"
          />
          <span class="cert-letter">a)</span>
          <span class="cert-text"
            >Mechanical Quality Records of all the parts ( Raw material TC
            (chemical & mechanical), Dimensional reports, NDT reports, Process
            certificates etc. ) & Electrical Quality Records (Components
            Screening report, PCB manufacturing report, process compliance
            reports / test reports, etc.) were verified thoroughly .</span
          >
        </div>
        <div class="cert-item">
          <input
            type="checkbox"
            v-model="formData.certificationB"
            class="cert-checkbox"
            id="certB"
            :disabled="isCertificationDisabled"
          />
          <span class="cert-letter">b)</span>
          <span class="cert-text"
            >CoC for SRU, fasteners & standard parts are verified and
            satisfactory</span
          >
        </div>
        <div class="cert-item">
          <input
            type="checkbox"
            v-model="formData.certificationC"
            class="cert-checkbox"
            id="certC"
            :disabled="isCertificationDisabled"
          />
          <span class="cert-letter">c)</span>
          <span class="cert-text"
            >Sl no of the SRUs are noted down in the respective log book opened
            on
            <input
              type="text"
              v-model="formData.logBookDate"
              placeholder=""
              class="inline-input"
              :disabled="isCertificationDisabled"
          /></span>
        </div>
        <div class="cert-item">
          <input
            type="checkbox"
            v-model="formData.certificationD"
            class="cert-checkbox"
            id="certD"
            :disabled="isCertificationDisabled"
          />
          <span class="cert-letter">d)</span>
          <span class="cert-text"
            >No Defect investigation is pending against this LRU</span
          >
        </div>
        <div class="cert-item">
          <input
            type="checkbox"
            v-model="formData.certificationE"
            class="cert-checkbox"
            id="certE"
            :disabled="isCertificationDisabled"
          />
          <span class="cert-letter">e)</span>
          <span class="cert-text"
            >All the previous test stages of this LRU /SRU are cleared</span
          >
        </div>
        <div class="cert-item">
          <input
            type="checkbox"
            v-model="formData.certificationF"
            class="cert-checkbox"
            id="certF"
            :disabled="isCertificationDisabled"
          />
          <span class="cert-letter">f)</span>
          <span class="cert-text"
            >CASDIC QA has physically inspected and accepted the LRU on
            <input
              type="text"
              v-model="formData.qaInspectionDate"
              placeholder=""
              class="inline-input"
              :disabled="isCertificationDisabled"
          /></span>
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
          <textarea
            v-model="formData.dgaqaRemarks"
            placeholder="Enter DGAQA action taken and remarks..."
            class="dgaqa-textarea"
            :disabled="isCertificationDisabled"
          ></textarea>
        </div>
      </div>

      <!-- DGAQA Signature moved to the end -->
      <div class="dgaqa-signature-section">
        <p class="instruction">(please use space overleaf for details)</p>
        <div class="signature-box-large"></div>
        <p>SIGNATURE OF DGAQA REP..</p>
      </div>
    </div>

    <div class="form-section test-status" v-if="currentUserRole === 3">
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
          <input type="radio" v-model="formData.testStatus" value="failed" />
          Test failed. Test failed.
        </label>
      </div>
    </div>

    <!-- ✅ New Section: Remarks by QA Reviewer -->
    <div class="form-section reviewer-remarks" v-if="currentUserRole === 3">
      <h3>Remarks by QA Reviewer</h3>
      <div class="remarks-container">
        <textarea
          v-model="formData.qaReviewerRemarks"
          placeholder="Enter reviewer comments..."
        ></textarea>
        <div class="signature-box-large"></div>
        <p>SIGNATURE OF QA REVIEWER</p>
      </div>
    </div>

    <div
      class="action-buttons"
      v-if="
        memoData.status === 'Not Assigned' &&
        !showTestReviewSection &&
        !showRejectionSection &&
        canApproveMemo
      "
    >
      <button class="btn btn-accept" @click="showAcceptOverlay = true">
        ACCEPT
      </button>
      <button class="btn btn-reject" @click="showRejectOverlay = true">
        REJECT
      </button>
    </div>

    <!-- Status Display (shown after Accept/Reject) -->
    <div
      v-if="showTestReviewSection || showRejectionSection"
      class="status-display"
    >
      <div
        class="status-badge"
        :class="showTestReviewSection ? 'accepted' : 'rejected'"
      >
        <svg
          v-if="showTestReviewSection"
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
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <svg
          v-else
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
        <span>{{
          showTestReviewSection ? "MEMO ACCEPTED" : "MEMO REJECTED"
        }}</span>
      </div>
      <p class="status-date">
        Processed on: {{ new Date().toLocaleDateString() }}
      </p>
    </div>

    <!-- Accept Overlay - Test or Review Details -->
    <div v-if="showAcceptOverlay" class="overlay" @click="closeAcceptOverlay">
      <div class="overlay-content" @click.stop>
        <div class="overlay-header">
          <h2>TEST OR REVIEW DETAILS</h2>
          <button class="close-button" @click="closeAcceptOverlay">
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

        <div class="overlay-body">
          <div class="form-row">
            <div class="form-field">
              <label>DATE OF TEST OR REVIEW</label>
              <input type="date" v-model="acceptFormData.testDate" />
            </div>
            <div class="form-field">
              <label>INTERNAL TESTER EMP ID</label>
              <input
                type="text"
                v-model="acceptFormData.testerId"
                placeholder="Enter tester ID"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-field">
              <label>INTERNAL TESTER NAME</label>
              <input
                type="text"
                v-model="acceptFormData.testerName"
                placeholder="Enter tester name"
              />
            </div>
            <div class="form-field">
              <label>COMMENTS</label>
              <textarea
                v-model="acceptFormData.comments"
                placeholder="Enter comments"
              ></textarea>
            </div>
          </div>

          <div class="form-row">
            <div class="form-field">
              <label>AUTHENTICATION</label>
              <input
                type="text"
                v-model="acceptFormData.authentication"
                placeholder="Enter authentication"
              />
            </div>
            <div class="form-field">
              <label>ATTACHMENTS</label>
              <input type="file" @change="handleAttachmentUpload" multiple />
            </div>
          </div>
        </div>

        <div class="overlay-footer">
          <button class="btn btn-primary" @click="submitAcceptForm">
            DONE
          </button>
        </div>
      </div>
    </div>

    <!-- Reject Overlay - Memo Rejection Details -->
    <div v-if="showRejectOverlay" class="overlay" @click="closeRejectOverlay">
      <div class="overlay-content" @click.stop>
        <div class="overlay-header">
          <h2>MEMO REJECTION DETAILS</h2>
          <button class="close-button" @click="closeRejectOverlay">
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

        <div class="overlay-body">
          <div
            class="rejection-section"
            :class="{ active: rejectionFormData.section === 'comments' }"
            @click="selectRejectionSection('comments')"
          >
            <div class="section-icon">
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
                  d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                ></path>
              </svg>
            </div>
            <span>COMMENTS</span>
            <div class="notification-icon">!</div>
          </div>

          <div
            class="rejection-section"
            :class="{ active: rejectionFormData.section === 'authentication' }"
            @click="selectRejectionSection('authentication')"
          >
            <div class="section-icon">
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
              </svg>
            </div>
            <span>AUTHENTICATION</span>
            <div class="notification-icon">!</div>
          </div>

          <div
            class="rejection-section"
            :class="{ active: rejectionFormData.section === 'attachments' }"
            @click="selectRejectionSection('attachments')"
          >
            <div class="section-icon">
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
                  d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"
                ></path>
              </svg>
            </div>
            <span>ATTACHMENTS</span>
          </div>

          <!-- Dynamic content based on selected section -->
          <div class="section-content">
            <div
              v-if="rejectionFormData.section === 'comments'"
              class="content-area"
            >
              <label>Rejection Comments:</label>
              <textarea
                v-model="rejectionFormData.comments"
                placeholder="Enter rejection comments..."
              ></textarea>
            </div>

            <div
              v-if="rejectionFormData.section === 'authentication'"
              class="content-area"
            >
              <label>Authentication Details:</label>
              <input
                type="text"
                v-model="rejectionFormData.authentication"
                placeholder="Enter authentication details"
              />
            </div>

            <div
              v-if="rejectionFormData.section === 'attachments'"
              class="content-area"
            >
              <label>Rejection Attachments:</label>
              <input
                type="file"
                @change="handleRejectionAttachmentUpload"
                multiple
              />
            </div>
          </div>
        </div>

        <div class="overlay-footer">
          <button class="btn btn-primary" @click="submitRejectForm">
            DONE
          </button>
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
            <div class="detail-value">
              {{
                acceptFormData.attachments.length > 0
                  ? acceptFormData.attachments.join(", ")
                  : "No attachments"
              }}
            </div>
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
          <div class="rejection-value">
            {{ rejectionFormData.authentication }}
          </div>
        </div>

        <div class="rejection-item">
          <label>Attachments:</label>
          <div class="rejection-value">
            {{
              rejectionFormData.attachments.length > 0
                ? rejectionFormData.attachments.join(", ")
                : "No attachments"
            }}
          </div>
        </div>
      </div>
    </div>

    <!-- Submit section - only show for new memos -->
    <div v-if="canSubmitNewMemo" class="submit-section">
      <button class="submit-button" @click="submitNewMemo">Submit Memo</button>
    </div>
  </div>
</template>

<script>
import { userStore } from "@/stores/userStore";

export default {
  name: "QAHeadMemoForm",
  data() {
    return {
      memoId: "",
      memoData: {
        status: "Not Assigned",
      },
      // Overlay visibility
      showAcceptOverlay: false,
      showRejectOverlay: false,

      // Accept form data
      acceptFormData: {
        testDate: "",
        testerId: "",
        testerName: "",
        comments: "",
        authentication: "",
        attachments: [],
      },

      // Reject form data
      rejectionFormData: {
        section: "comments",
        comments: "",
        authentication: "",
        attachments: [],
      },

      // Additional sections visibility
      showTestReviewSection: false,
      showRejectionSection: false,

      // LRU options from database
      lruOptions: [],
      lruData: [], // Full LRU data with project information
      lruLoading: false,
      lruError: null,
      // Serial number options
      serialNumberOptions: [],
      serialNumberLoading: false,
      serialNumberError: null,
      showSerialNumberDropdown: false,

      // Hierarchical test data for Inspection Stage
      testGroups: [],
      subTests: [],
      loadingTestGroups: false,
      loadingSubTests: false,

      // Cascading dropdown state
      showCascadingDropdown: false,
      showSubTests: false,
      hoveredTestGroup: null,
      hoveredSubTest: null,
      keepSubTestsOpen: false,

      // Time picker options
      hours: [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
      ],
      minutes: [
        "00",
        "05",
        "10",
        "15",
        "20",
        "25",
        "30",
        "35",
        "40",
        "45",
        "50",
        "55",
      ],

      formData: {
        from1: "",
        from2: "",
        from3: "",
        casdicRef: "",
        casdic: "",
        casdicDate: "",
        to1: "",
        to2: "",
        wingRef: "",
        coordinator: "",
        partNo: "",
        manufacturer: "",
        description: "",
        refDoc: "",
        refNo: "",
        version: "",
        revision: "",
        slNo: [],
        drawingNo: "",
        source: "NA",
        refDoc2: "",
        refNo2: "",
        version2: "",
        revision2: "",
        qtyOffered: "",
        description3: "",
        refDoc3: "",
        refNo3: "",
        version3: "",
        revision3: "",
        mechanicalInsp: "",
        unitIdentification: "",
        // Hierarchical test selection for Inspection Stage
        selectedTestGroup: "",
        selectedSubTest: "",
        refDoc4: "",
        refNo4: "",
        version4: "",
        revision4: "",
        inspectionStage: "",
        stteStatus: "",
        refDoc5: "",
        refNo5: "",
        version5: "",
        revision5: "",
        testStageCleared: "",
        refDoc6: "",
        refNo6: "",
        version6: "",
        revision6: "",
        testVenue: "",
        signatureName: "",
        testFacility: "",
        testCycle: "",
        testStartDate: "",
        testStartHour: "",
        testStartMinute: "",
        testStartAmPm: "",
        testCompleteDate: "",
        testCompleteHour: "",
        testCompleteMinute: "",
        testCompleteAmPm: "",
        calibrationStatus: "",
        funcCheckInitialDate: "",
        funcCheckInitialHour: "",
        funcCheckInitialMinute: "",
        funcCheckInitialAmPm: "",
        perfCheckDuringDate: "",
        perfCheckDuringHour: "",
        perfCheckDuringMinute: "",
        perfCheckDuringAmPm: "",
        funcCheckEndDate: "",
        funcCheckEndHour: "",
        funcCheckEndMinute: "",
        funcCheckEndAmPm: "",
        logBookDate: "",
        qaInspectionDate: "",
        testStatus: "",
        qaReviewerRemarks: "",
        certificationA: false,
        certificationB: false,
        certificationC: false,
        certificationD: false,
        certificationE: false,
        certificationF: false,
        dgaqaRemarks: "",
        remarks: "",
      },
    };
  },
  computed: {
    // Get current user role from global store
    currentUserRole() {
      return userStore.getters.currentUserRole();
    },
    canApproveMemo() {
      // The role '2' corresponds to the QA Head/Manager based on the SRS document.
      // This ensures only authorized users see the accept/reject buttons.
      return this.currentUserRole === 2;
    },
    isTestDetailsDisabled() {
      // Disable test details section for Designer (role 5) and Design Head (role 4)
      return [4, 5].includes(this.currentUserRole);
    },
    isCertificationDisabled() {
      // Disable certification section for Designer (role 5) and Design Head (role 4)
      return [4, 5].includes(this.currentUserRole);
    },
    selectedTestName() {
      return this.formData.unitIdentification;
    },
    isNewMemo() {
      // Check if this is a new memo being submitted
      return this.$route.name === "NewMemoForm";
    },
    canSubmitNewMemo() {
      // Only designers (role 5) and design heads (role 4) can submit new memos
      return this.isNewMemo && [4, 5].includes(this.currentUserRole);
    },
    selectedLruInfo() {
      // Get the full LRU information for the selected LRU
      if (!this.formData.description) return null;
      return this.lruData.find(
        (lru) => lru.lru_name === this.formData.description
      );
    },
    availableSerialNumbers() {
      // Return the serial number options for the selected LRU, sorted in ascending order
      return [...this.serialNumberOptions].sort((a, b) => {
        // Convert to numbers for proper numeric sorting
        const numA = Number(a.value);
        const numB = Number(b.value);
        return numA - numB;
      });
    },
    selectedSerialNumbersDisplay() {
      // Return a display string for selected serial numbers
      if (!this.formData.slNo || this.formData.slNo.length === 0) {
        return "Select Serial Numbers";
      }

      // Show all selected serial numbers
      const sortedSerials = [...this.formData.slNo].sort((a, b) => a - b);
      return sortedSerials.join(", ");
    },
    quantityOffered() {
      // Auto-calculate quantity based on selected serial numbers
      return this.formData.slNo ? this.formData.slNo.length : 0;
    },

    // Computed properties to combine date and time fields (convert 12-hour to 24-hour format)
    testStartOn() {
      if (
        this.formData.testStartDate &&
        this.formData.testStartHour &&
        this.formData.testStartMinute &&
        this.formData.testStartAmPm
      ) {
        const time24 = this.convertTo24Hour(
          this.formData.testStartHour,
          this.formData.testStartMinute,
          this.formData.testStartAmPm
        );
        return `${this.formData.testStartDate}T${time24}`;
      }
      return "";
    },

    testCompleteOn() {
      if (
        this.formData.testCompleteDate &&
        this.formData.testCompleteHour &&
        this.formData.testCompleteMinute &&
        this.formData.testCompleteAmPm
      ) {
        const time24 = this.convertTo24Hour(
          this.formData.testCompleteHour,
          this.formData.testCompleteMinute,
          this.formData.testCompleteAmPm
        );
        return `${this.formData.testCompleteDate}T${time24}`;
      }
      return "";
    },

    funcCheckInitial() {
      if (
        this.formData.funcCheckInitialDate &&
        this.formData.funcCheckInitialHour &&
        this.formData.funcCheckInitialMinute &&
        this.formData.funcCheckInitialAmPm
      ) {
        const time24 = this.convertTo24Hour(
          this.formData.funcCheckInitialHour,
          this.formData.funcCheckInitialMinute,
          this.formData.funcCheckInitialAmPm
        );
        return `${this.formData.funcCheckInitialDate}T${time24}`;
      }
      return "";
    },

    perfCheckDuring() {
      if (
        this.formData.perfCheckDuringDate &&
        this.formData.perfCheckDuringHour &&
        this.formData.perfCheckDuringMinute &&
        this.formData.perfCheckDuringAmPm
      ) {
        const time24 = this.convertTo24Hour(
          this.formData.perfCheckDuringHour,
          this.formData.perfCheckDuringMinute,
          this.formData.perfCheckDuringAmPm
        );
        return `${this.formData.perfCheckDuringDate}T${time24}`;
      }
      return "";
    },

    funcCheckEnd() {
      if (
        this.formData.funcCheckEndDate &&
        this.formData.funcCheckEndHour &&
        this.formData.funcCheckEndMinute &&
        this.formData.funcCheckEndAmPm
      ) {
        const time24 = this.convertTo24Hour(
          this.formData.funcCheckEndHour,
          this.formData.funcCheckEndMinute,
          this.formData.funcCheckEndAmPm
        );
        return `${this.formData.funcCheckEndDate}T${time24}`;
      }
      return "";
    },
  },
  watch: {
    "formData.description"(newValue, oldValue) {
      // When LRU is selected, log the selection and fetch serial numbers
      if (newValue) {
        const selectedLru = this.selectedLruInfo;
        console.log("LRU selected:", selectedLru);

        if (selectedLru) {
          console.log(
            `Selected LRU: ${selectedLru.lru_name} from project: ${selectedLru.project_name}`
          );
          
          // Dynamically fetch and set part number based on selected LRU
          // If LRU has part number, populate it; otherwise set to blank
          this.formData.partNo = selectedLru.lru_part_number || "";
          if (selectedLru.lru_part_number) {
            console.log(`Auto-populated part number: ${selectedLru.lru_part_number}`);
          } else {
            console.log("Selected LRU does not have a part number, field set to blank");
          }
          
          // Fetch serial numbers for the selected LRU
          this.fetchSerialNumbers(selectedLru.lru_id);
        }
      }

      // Clear serial number selection and part number when LRU changes or is cleared
      if (newValue !== oldValue) {
        this.formData.slNo = [];
        this.formData.qtyOffered = 0;
        this.serialNumberOptions = [];
        this.serialNumberError = null;
        this.showSerialNumberDropdown = false;
        
        // Clear part number if LRU is deselected
        if (!newValue) {
          this.formData.partNo = "";
        }
      }
    },
  },
  async mounted() {
    this.memoId = this.$route.params.memoId;
    this.loadMemoData();

    // Always try to fetch real data first
    console.log("Attempting to fetch data from backend...");
    await this.fetchLruOptions();
    await this.fetchTestGroups();

    // Add click outside handler for dropdowns
    document.addEventListener("click", this.handleClickOutside);
    document.addEventListener("click", this.handleCascadingClickOutside);

    console.log("Component mounted, initial data:", {
      memoId: this.memoId,
      isNewMemo: this.isNewMemo,
      rejectionFormData: this.rejectionFormData,
      acceptFormData: this.acceptFormData,
      lruData: this.lruData,
    });
  },

  beforeUnmount() {
    // Remove click outside handler
    document.removeEventListener("click", this.handleClickOutside);
    document.removeEventListener("click", this.handleCascadingClickOutside);
  },
  methods: {
    // Convert 12-hour time format to 24-hour format
    convertTo24Hour(hour, minute, ampm) {
      let hour24 = parseInt(hour);

      if (ampm === "AM") {
        if (hour24 === 12) {
          hour24 = 0; // 12 AM becomes 00
        }
      } else if (ampm === "PM") {
        if (hour24 !== 12) {
          hour24 += 12; // PM hours except 12 PM
        }
        // 12 PM stays 12
      }

      // Format with leading zeros
      const formattedHour = hour24.toString().padStart(2, "0");
      return `${formattedHour}:${minute}`;
    },

    loadMemoData() {
      if (this.isNewMemo) {
        // For new memos, initialize with empty/default data
        this.memoData = {
          id: null,
          status: "New",
          title: "DGAQA Inspection Requisition",
          project: "New Memo",
          date: new Date().toISOString().split("T")[0],
        };

        // Auto-fill and lock From/To fields for new memos
        this.formData.casdicDate = new Date().toISOString().split("T")[0];
        this.formData.casdic = "CASDIC/QA/2025";
        this.formData.from1 = "MED, CASDIC (DARE), Bangalore";
        this.formData.from2 = "DGAQA cell,";
        this.formData.from3 = "ORDAQA(ADE), Bangalore";
      } else {
        // For existing memos, simulate loading memo data based on memoId
        // In a real application, this would fetch from an API
        this.memoData = {
          id: this.memoId,
          status: "Not Assigned",
          title: "DGAQA Inspection Requisition",
          project: "PRJ-2025-078",
          date: "2025-01-15",
        };

        // Auto-fill some sample data for existing memos
        this.formData.from1 = "CASDIC QA Department";
        this.formData.casdic = "CAS-2025-001";
        this.formData.casdicDate = "2025-01-15";
        this.formData.from2 = "DGAQA Office";
        this.formData.wingRef = "WING-2025-078";
        this.formData.coordinator = "John Smith (Designs) - +91-98765-43210";
        this.formData.partNo = "LRU-001";
        this.formData.manufacturer = "Aviatrax Industries";
        this.formData.description =
          "Main Control Unit for Aircraft Navigation System";
      }
    },

    toggleSerialNumberDropdown() {
      this.showSerialNumberDropdown = !this.showSerialNumberDropdown;
    },

    toggleSerialNumber(serialNumber) {
      if (!this.formData.slNo) {
        this.formData.slNo = [];
      }

      // Convert to string for consistency
      const serialStr = String(serialNumber);
      const index = this.formData.slNo.indexOf(serialStr);
      if (index > -1) {
        // Remove if already selected
        this.formData.slNo.splice(index, 1);
      } else {
        // Add if not selected
        this.formData.slNo.push(serialStr);
      }

      // Update quantity offered automatically
      this.formData.qtyOffered = this.formData.slNo.length;

      console.log("Selected serial numbers:", this.formData.slNo);
      console.log("Quantity offered:", this.formData.qtyOffered);
    },

    isSerialNumberSelected(serialNumber) {
      return (
        this.formData.slNo && this.formData.slNo.includes(String(serialNumber))
      );
    },

    clearSerialNumbers() {
      this.formData.slNo = [];
      this.formData.qtyOffered = 0;
      console.log("Cleared serial numbers and quantity");
    },

    handleClickOutside(event) {
      // Close serial number dropdown if clicking outside
      if (
        this.showSerialNumberDropdown &&
        !event.target.closest(".serial-number-dropdown-container")
      ) {
        this.showSerialNumberDropdown = false;
      }
    },

    async fetchLruOptions() {
      try {
        this.lruLoading = true;
        this.lruError = null;
        console.log("Fetching LRU options...");

        // Get current user information
        const currentUser = userStore.getters.currentUser();
        const currentUserRole = userStore.getters.currentUserRole();

        if (!currentUser || !currentUserRole) {
          console.error("User information not available");
          this.lruError = "User information not available";
          this.loadFallbackLruOptions();
          return;
        }

        // Use the new filtered API endpoint
        const response = await fetch(
          `http://localhost:5000/api/lrus-filtered?user_id=${currentUser.id}&user_role=${currentUserRole}`
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
          // Store both the simple names for the dropdown and full LRU data
          this.lruOptions = data.lrus.map((lru) => lru.lru_name);
          this.lruData = data.lrus; // Store full LRU data for future use
          console.log("Loaded LRU options:", this.lruOptions);
          console.log("Full LRU data:", this.lruData);
          console.log(
            `User role ${currentUserRole}: ${data.lrus.length} LRUs available`
          );
        } else {
          this.lruError = data.message || "Failed to fetch LRU options";
          console.error("Failed to fetch LRU options:", data.message);
          this.loadFallbackLruOptions();
        }
      } catch (error) {
        this.lruError = `Network error: ${error.message}`;
        console.error("Error fetching LRU options:", error);
        this.loadFallbackLruOptions();
      } finally {
        this.lruLoading = false;
      }
    },

    loadFallbackLruOptions() {
      // Fallback LRU options when backend is not available
      console.log("Loading fallback LRU options...");
      this.lruData = [
        {
          lru_id: 1,
          lru_name: "Flight Control Unit",
          project_id: 1,
          project_name: "Project Alpha",
        },
        {
          lru_id: 2,
          lru_name: "Navigation System",
          project_id: 1,
          project_name: "Project Alpha",
        },
        {
          lru_id: 3,
          lru_name: "Communication Module",
          project_id: 2,
          project_name: "Project Beta",
        },
        {
          lru_id: 4,
          lru_name: "Power Management Unit",
          project_id: 2,
          project_name: "Project Beta",
        },
        {
          lru_id: 5,
          lru_name: "Sensor Array",
          project_id: 3,
          project_name: "Project Gamma",
        },
      ];
      this.lruOptions = this.lruData.map((lru) => lru.lru_name);
      console.log("Loaded fallback LRU options:", this.lruOptions);
    },

    loadFallbackSerialNumbers(lruId) {
      // Fallback serial numbers when backend is not available
      console.log(`Loading fallback serial numbers for LRU ID: ${lruId}`);

      // Sample serial numbers for different LRUs
      const fallbackSerials = {
        1: [1, 2, 3, 4, 5], // Flight Control Unit
        2: [1, 2, 3], // Navigation System
        3: [1, 2, 3, 4, 5, 6, 7, 8], // Communication Module
        4: [1, 2], // Power Management Unit
        5: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], // Sensor Array
      };

      const serials = fallbackSerials[lruId] || [];
      // Map and sort serial numbers in ascending order
      const mappedSerials = serials.map((serial) => ({
        value: serial,
        label: serial.toString(),
      }));
      // Sort by numeric value in ascending order
      this.serialNumberOptions = mappedSerials.sort((a, b) => {
        const numA = Number(a.value);
        const numB = Number(b.value);
        return numA - numB;
      });

      console.log(
        `Loaded fallback serial numbers for LRU ${lruId}:`,
        this.serialNumberOptions
      );
    },

    async checkBackendStatus() {
      try {
        const response = await fetch("http://localhost:5000/api/lrus", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });
        return response.ok;
      } catch (error) {
        console.log("Backend not available:", error.message);
        return false;
      }
    },

    async fetchSerialNumbers(lruId) {
      try {
        this.serialNumberLoading = true;
        this.serialNumberError = null;
        console.log(`Fetching serial numbers for LRU ID: ${lruId}`);

        const response = await fetch(
          `http://localhost:5000/api/lrus/${lruId}/serial-numbers`
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
          // Map and sort serial numbers in ascending order
          const mappedSerials = data.serial_numbers.map((serial) => ({
            value: serial.serial_number,
            label: serial.serial_number.toString(),
          }));
          // Sort by numeric value in ascending order
          this.serialNumberOptions = mappedSerials.sort((a, b) => {
            const numA = Number(a.value);
            const numB = Number(b.value);
            return numA - numB;
          });
          console.log(
            `Loaded serial numbers for LRU ${lruId}:`,
            this.serialNumberOptions
          );
        } else {
          this.serialNumberError =
            data.message || "Failed to fetch serial numbers";
          console.error("Failed to fetch serial numbers:", data.message);
          this.serialNumberOptions = [];
        }
      } catch (error) {
        this.serialNumberError = `Network error: ${error.message}`;
        console.error(`Error fetching serial numbers for LRU ${lruId}:`, error);
        console.log("Using fallback serial numbers...");
        this.loadFallbackSerialNumbers(lruId);
      } finally {
        this.serialNumberLoading = false;
      }
    },

    // Hierarchical test data fetching methods for Unit Identification
    async fetchTestGroups() {
      try {
        this.loadingTestGroups = true;
        const response = await fetch("http://localhost:5000/api/test-groups");
        const data = await response.json();

        if (data.success) {
          this.testGroups = data.groups;
          console.log("Test groups loaded:", this.testGroups);
        } else {
          console.error("Failed to fetch test groups:", data.message);
        }
      } catch (error) {
        console.error("Error fetching test groups:", error);
      } finally {
        this.loadingTestGroups = false;
      }
    },

    async fetchSubTests(groupId) {
      try {
        this.loadingSubTests = true;
        // Reset dependent data
        this.subTests = [];
        this.formData.selectedSubTest = "";

        const response = await fetch(
          `http://localhost:5000/api/test-groups/${groupId}/sub-tests`
        );
        const data = await response.json();

        if (data.success) {
          this.subTests = data.sub_tests;
          console.log("Sub-tests loaded:", this.subTests);
        } else {
          console.error("Failed to fetch sub-tests:", data.message);
        }
      } catch (error) {
        console.error("Error fetching sub-tests:", error);
      } finally {
        this.loadingSubTests = false;
      }
    },

    // Event handlers for cascading dropdown
    toggleCascadingDropdown() {
      this.showCascadingDropdown = !this.showCascadingDropdown;
      if (!this.showCascadingDropdown) {
        this.closeAllMenus();
      }
    },

    closeAllMenus() {
      this.showCascadingDropdown = false;
      this.showSubTests = false;
      this.hoveredTestGroup = null;
      this.hoveredSubTest = null;
      this.keepSubTestsOpen = false;
    },

    handleTestGroupHover(group) {
      this.hoveredTestGroup = group.group_id;
      this.showSubTests = true;
      this.fetchSubTests(group.group_id);

      // Reset sub-test selection
      this.hoveredSubTest = null;
    },

    handleSubTestHover(subTest) {
      this.hoveredSubTest = subTest.sub_test_id;
      // No need to fetch bulletins anymore - we only show test groups and sub-tests
    },

    selectTestGroup(group) {
      // Capture the simplified hierarchy path (only test groups and sub-tests)
      this.captureInspectionStageHierarchy(group.group_id, null);
      this.closeAllMenus();
    },

    selectSubTest(subTest) {
      // Capture the simplified hierarchy path (only test groups and sub-tests)
      this.captureInspectionStageHierarchy(
        this.hoveredTestGroup,
        subTest.sub_test_id
      );
      this.closeAllMenus();
    },

    handleSubTestsLeave() {
      if (!this.keepSubTestsOpen) {
        this.showSubTests = false;
        this.hoveredSubTest = null;
      }
    },

    getInspectionStageText() {
      return this.formData.inspectionStage;
    },

    // Capture the simplified hierarchy path (only test groups and sub-tests) for Inspection Stage
    captureInspectionStageHierarchy(testGroupId, subTestId) {
      // Set the selected IDs
      this.formData.selectedTestGroup = testGroupId || "";
      this.formData.selectedSubTest = subTestId || "";

      // Build the display text
      const parts = [];

      if (testGroupId) {
        const testGroupName = this.getTestGroupName(testGroupId);
        if (testGroupName) parts.push(testGroupName);
      }

      if (subTestId) {
        const subTestName = this.getSubTestName(subTestId);
        if (subTestName) parts.push(subTestName);
      }

      this.formData.inspectionStage = parts.join(" > ");
    },

    // Build inspection stage as array for database storage (only test groups and sub-tests)
    buildInspectionStageArray() {
      const parts = [];

      // Get test group name
      const testGroupName =
        this.getTestGroupName(this.formData.selectedTestGroup) || "";
      parts.push(testGroupName);

      // Get sub-test name
      const subTestName =
        this.getSubTestName(this.formData.selectedSubTest) || "";
      parts.push(subTestName);

      return parts;
    },

    getTestGroupName(groupId) {
      const group = this.testGroups.find((g) => g.group_id === groupId);
      return group ? group.group_name : "";
    },

    getSubTestName(subTestId) {
      const subTest = this.subTests.find((s) => s.sub_test_id === subTestId);
      return subTest ? subTest.sub_test_name : "";
    },


    handleCascadingClickOutside(event) {
      const cascadingDropdown = event.target.closest(".cascading-dropdown");
      if (!cascadingDropdown) {
        this.closeAllMenus();
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
      console.log("Selecting rejection section:", section);
      this.rejectionFormData.section = section;
      console.log("Updated rejection form data:", this.rejectionFormData);
    },

    // File upload handlers
    handleAttachmentUpload(event) {
      const files = Array.from(event.target.files);
      this.acceptFormData.attachments = files.map((file) => file.name);
    },

    handleRejectionAttachmentUpload(event) {
      const files = Array.from(event.target.files);
      this.rejectionFormData.attachments = files.map((file) => file.name);
    },

    // Form submission
    submitAcceptForm() {
      if (
        !this.acceptFormData.testDate ||
        !this.acceptFormData.testerId ||
        !this.acceptFormData.testerName
      ) {
        alert("Please fill in all required fields");
        return;
      }

      this.showTestReviewSection = true;
      this.closeAcceptOverlay();
      alert("Memo accepted successfully! Test/Review details have been added.");
    },

    submitRejectForm() {
      console.log("Submit reject form called");
      console.log("Rejection form data:", this.rejectionFormData);

      if (
        !this.rejectionFormData.comments &&
        !this.rejectionFormData.authentication &&
        this.rejectionFormData.attachments.length === 0
      ) {
        alert("Please fill in at least one field for rejection details.");
        return;
      }

      this.showRejectionSection = true;
      this.closeRejectOverlay();
      alert("Memo rejected! Rejection details have been added.");
      console.log("Rejection form submitted successfully");
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
        this.emailAddresses = ""; // Clear input on close
      }
    },
    sendEmails() {
      if (this.emailAddresses.trim() === "") {
        alert("Please enter at least one email address.");
        return;
      }

      const emails = this.emailAddresses
        .split(",")
        .map((email) => email.trim());
      console.log("Sending memo to:", emails);
      // Here you would add the logic to send the emails, for example, making an API call.

      alert(`Memo sent successfully to: ${emails.join(", ")}`);
      this.toggleShareBox(); // Close the share box after "sending"
    },

    toggleShareBox() {
      this.showShareBox = !this.showShareBox;
      if (!this.showShareBox) {
        this.emailAddresses = ""; // Clear input on close
      }
    },
    sendEmails() {
      if (this.emailAddresses.trim() === "") {
        alert("Please enter at least one email address.");
        return;
      }

      const emails = this.emailAddresses
        .split(",")
        .map((email) => email.trim());
      console.log("Sending memo to:", emails);
      // Here you would add the logic to send the emails, for example, making an API call.

      alert(`Memo sent successfully to: ${emails.join(", ")}`);
      this.toggleShareBox(); // Close the share box after "sending"
    },

    submitMemo() {
      // Validate that at least one test status is selected
      const testStatusSelected = Object.values(this.memoData.testStatus).some(
        (status) => status
      );

      if (!testStatusSelected) {
        alert("Please select at least one test status.");
        return;
      }

      if (!this.memoData.reviewerComments.trim()) {
        alert("Please provide reviewer comments.");
        return;
      }

      // Here you would add the logic to submit the memo, for example, making an API call.
      console.log("Submitting memo:", {
        memoId: this.id,
        testStatus: this.memoData.testStatus,
        reviewerComments: this.memoData.reviewerComments,
      });

      alert("Memo submitted successfully!");
      this.goBack(); // Navigate back after successful submission
    },

    async submitNewMemo() {
      // Validate required fields for new memo submission
      if (!this.formData.description) {
        alert("Please select an LRU from the dropdown.");
        return;
      }

      if (!this.formData.partNo) {
        alert("Please enter Part Number.");
        return;
      }

      if (!this.formData.manufacturer) {
        alert("Please enter Manufacturer.");
        return;
      }

      if (!this.formData.unitIdentification) {
        alert("Please select Unit Identification (ESS, SoFT, or QT).");
        return;
      }

      if (!this.formData.mechanicalInsp) {
        alert("Please select Mechanical Inspection stage.");
        return;
      }

      if (!this.formData.selectedTestGroup) {
        alert("Please select Inspection / Test Stage Offered Now.");
        return;
      }

      try {
        // Get current user info
        const currentUser = userStore.getters.currentUser();
        if (!currentUser) {
          alert("User not logged in. Please login first.");
          return;
        }

        // Prepare memo data for submission
        const memoData = {
          from_person: this.formData.from1 || currentUser.name,
          to_person: this.formData.from2 || "QA Head",
          thru_person: this.formData.from3 || "",
          submitted_by: currentUser.id,
          formData: {
            // Basic Information
            casdicRef: this.formData.casdic,
            dated: this.formData.casdicDate,
            wingProjRef: this.formData.wingRef,
            lruSruDesc: this.formData.description,
            partNo: this.formData.partNo,
            manufacturer: this.formData.manufacturer,
            drawingNoRev: this.formData.drawingNo,
            source: this.formData.source,

            // Serial Numbers (checkboxes) - send the actual array instead of individual boolean fields
            // The backend will process the array directly
            slNo: this.formData.slNo || [],

            // Unit Identification - simple dropdown value
            unitIdentification: this.formData.unitIdentification,
            // Inspection Stage - send as array (test groups and sub-tests only)
            inspectionStageArray: this.buildInspectionStageArray(),
            mechanicalInsp: this.formData.mechanicalInsp,

            // Test Information
            inspnTestStageOffered: this.formData.inspectionStage || "",
            stteStatus: this.formData.stteStatus,
            testStageCleared: this.formData.testStageCleared,
            venue: this.formData.testVenue,
            memoDate: this.formData.casdicDate,
            nameDesignation: this.formData.signatureName,
            coordinator: this.formData.coordinator,
            testFacility: this.formData.testFacility,
            testCycleDuration: this.formData.testCycle,
            testStartOn: this.testStartOn,
            testCompleteOn: this.testCompleteOn,
            calibrationStatus: this.formData.calibrationStatus,
            funcCheckInitial: this.funcCheckInitial,
            perfCheckDuring: this.perfCheckDuring,
            funcCheckEnd: this.funcCheckEnd,

            // Certified checkboxes
            certifiedA: this.formData.certificationA,
            certifiedB: this.formData.certificationB,
            certifiedC: this.formData.certificationC,
            certifiedD: this.formData.certificationD,
            certifiedE: this.formData.certificationE,
            certifiedF: this.formData.certificationF,

            // References
            refDoc: this.formData.refDoc,
            refNo: this.formData.refNo,
            version: this.formData.version,
            revision: this.formData.revision,
            refDoc2: this.formData.refDoc2,
            refNo2: this.formData.refNo2,
            version2: this.formData.version2,
            revision2: this.formData.revision2,
            refDoc3: this.formData.refDoc3,
            refNo3: this.formData.refNo3,
            version3: this.formData.version3,
            revision3: this.formData.revision3,
            refDoc4: this.formData.refDoc4,
            refNo4: this.formData.refNo4,
            version4: this.formData.version4,
            revision4: this.formData.revision4,
            refDoc5: this.formData.refDoc5,
            refNo5: this.formData.refNo5,
            version5: this.formData.version5,
            revision5: this.formData.revision5,
            refDoc6: this.formData.refDoc6,
            refNo6: this.formData.refNo6,
            version6: this.formData.version6,
            revision6: this.formData.revision6,

            // Additional fields
            remarks: this.formData.dgaqaRemarks,
          },
        };

        console.log("Submitting memo to backend:", memoData);
        console.log("=== DEBUG: Serial numbers data ===");
        console.log("formData.slNo:", this.formData.slNo);
        console.log(
          "slNo1:",
          this.formData.slNo && this.formData.slNo.includes("1")
        );
        console.log(
          "slNo2:",
          this.formData.slNo && this.formData.slNo.includes("2")
        );
        console.log(
          "slNo3:",
          this.formData.slNo && this.formData.slNo.includes("3")
        );
        console.log("=== END DEBUG ===");

        // Submit memo to backend
        const response = await fetch("http://localhost:5000/api/memos", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(memoData),
        });

        const result = await response.json();

        if (result.success) {
          alert(`Memo submitted successfully! Memo ID: ${result.memo_id}`);
          this.$router.push({ name: "MemoDashboard" }); // Navigate back to dashboard
        } else {
          alert(`Error submitting memo: ${result.message}`);
        }
      } catch (error) {
        console.error("Error submitting memo:", error);
        alert("Error submitting memo. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
.memo-form {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ebf7fd;
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

.form-table td,
.form-table th {
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

.readonly-field {
  background-color: #f8f9fa !important;
  color: #6c757d !important;
  cursor: not-allowed !important;
  border-color: #dee2e6 !important;
}

.readonly-field:focus {
  background-color: #f8f9fa !important;
  border-color: #dee2e6 !important;
  box-shadow: none !important;
}

.readonly-field {
  background-color: #e9ecef !important;
  color: #495057 !important;
  cursor: not-allowed !important;
  border-color: #ced4da !important;
  font-weight: 500;
}

.readonly-field::placeholder {
  color: #6c757d !important;
  font-style: italic;
}

.wide-field {
  grid-column: span 2;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #333;
}

.details-table th,
.details-table td {
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

.source-input {
  width: 100%;
  padding: 4px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
  box-sizing: border-box;
}

.source-input:focus {
  border-color: #80bdff;
  outline: none;
}

.ver-header,
.rev-header {
  width: 7.5%;
}

.lru-cell,
.desc-cell,
.ref-cell,
.refno-cell,
.ver-cell,
.rev-cell {
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

/* Cascading Dropdown for Unit Identification */
.cascading-dropdown {
  position: relative;
  width: 100%;
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  min-height: 36px;
}

.dropdown-trigger:hover {
  border-color: #007bff;
}

.selected-text {
  flex: 1;
  text-align: left;
  color: #333;
}

.dropdown-arrow {
  color: #666;
  font-size: 12px;
  transition: transform 0.2s;
}

.dropdown-trigger:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.cascading-menu {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  min-width: 200px;
  max-height: 300px;
  overflow-y: auto;
}

.level-1 {
  top: 100%;
  left: 0;
  right: 0;
  background: #e3f2fd; /* Light blue */
  border-color: #2196f3;
}

.level-2 {
  top: 0;
  left: 200px; /* Fixed position to the right of level-1 */
  background: #f3e5f5; /* Light purple */
  border-color: #9c27b0;
}

.level-3 {
  top: 0;
  left: 400px; /* Fixed position to the right of level-2 */
  background: #e8f5e8; /* Light green */
  border-color: #4caf50;
}

.level-4 {
  top: 0;
  left: 600px; /* Fixed position to the right of level-3 */
  background: #fff3e0; /* Light orange */
  border-color: #ff9800;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:hover,
.menu-item.active {
  background-color: #f8f9fa;
}

/* Level-specific hover colors */
.level-1 .menu-item:hover,
.level-1 .menu-item.active {
  background-color: #bbdefb; /* Darker blue */
}

.level-2 .menu-item:hover,
.level-2 .menu-item.active {
  background-color: #e1bee7; /* Darker purple */
}

.level-3 .menu-item:hover,
.level-3 .menu-item.active {
  background-color: #c8e6c9; /* Darker green */
}

.level-4 .menu-item:hover,
.level-4 .menu-item.active {
  background-color: #ffcc80; /* Darker orange */
}

.menu-item.loading {
  color: #666;
  font-style: italic;
  cursor: default;
}

.menu-item.no-data {
  color: #999;
  font-style: italic;
  cursor: default;
}

.item-text {
  flex: 1;
  text-align: left;
}

.arrow {
  color: #666;
  font-size: 12px;
  margin-left: 8px;
}

/* Level-specific arrow colors */
.level-1 .arrow {
  color: #2196f3; /* Blue */
}

.level-2 .arrow {
  color: #9c27b0; /* Purple */
}

.level-3 .arrow {
  color: #4caf50; /* Green */
}

.level-4 .arrow {
  color: #ff9800; /* Orange */
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .cascading-menu {
    min-width: 150px;
  }

  .level-2 {
    left: 0;
    top: 100%;
    margin-top: 10px;
  }

  .level-3 {
    left: 0;
    top: 200%;
    margin-top: 10px;
  }

  .level-4 {
    left: 0;
    top: 300%;
    margin-top: 10px;
  }
}

/* Unit Identification Container */
.unit-identification-container {
  position: relative;
}

.dropdown-wrapper {
  position: relative;
  width: 100%;
}

/* Tests dropdown (Unit Identification) */
.test-dropdown {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  padding: 10px 12px;
  background: #fff;
  cursor: pointer;
  width: 100%;
  box-sizing: border-box;
  transition: all 0.2s ease;
  font-size: 0.85em;
}

.test-dropdown:hover {
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.test-dropdown .selected-value {
  color: #2c3e50;
  flex: 1;
  font-weight: 500;
}

.test-dropdown .dropdown-icon {
  color: #6c757d;
  font-size: 12px;
  margin-left: 8px;
  transition: transform 0.2s ease;
}

.test-dropdown.active .dropdown-icon {
  transform: rotate(180deg);
}

/* Main dropdown menu */
.tests-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 4px;
  background: #fff;
  border: 1px solid #e1e5e9;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  z-index: 1000;
  overflow: hidden;
  animation: menuFadeIn 0.15s ease-out;
}

@keyframes menuFadeIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.menu-item-container {
  padding: 8px 0;
  max-height: 240px;
  overflow-y: auto;
}

.menu-item-container::-webkit-scrollbar {
  width: 6px;
}

.menu-item-container::-webkit-scrollbar-track {
  background: transparent;
}

.menu-item-container::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.1s ease;
  font-size: 0.9em;
  color: #374151;
  position: relative;
}

.menu-item:hover {
  background-color: #f8fafc;
}

.menu-item.has-submenu:hover {
  background-color: #e3f2fd;
}

.menu-item.active {
  background-color: #e3f2fd;
  border-left: 3px solid #2563eb;
}

.menu-item.no-data {
  color: #9ca3af;
  font-style: italic;
  cursor: default;
}

.menu-item.no-data:hover {
  background-color: transparent;
}

.menu-text {
  flex: 1;
  font-weight: 500;
}

.menu-arrow {
  color: #9ca3af;
  font-size: 12px;
  margin-left: 8px;
  transition: color 0.1s ease;
}

.menu-item:hover .menu-arrow {
  color: #6b7280;
}

/* Separate Stages Submenu */
.stages-submenu {
  position: absolute;
  top: 0;
  left: calc(100% + 8px);
  min-width: 220px;
  max-width: 320px;
  background: #fff;
  border: 1px solid #e1e5e9;
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  animation: submenuSlideIn 0.2s ease-out;
  z-index: 1003;
  overflow: hidden;
  transform: translateY(var(--submenu-offset, 0));
}

@keyframes submenuSlideIn {
  from {
    opacity: 0;
    transform: translateX(-8px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.submenu-header {
  padding: 12px 16px 8px;
  border-bottom: 1px solid #f1f5f9;
  background-color: #f8fafc;
}

.submenu-title {
  font-size: 0.75em;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.loading-indicator {
  font-size: 0.7em;
  color: #9ca3af;
  font-style: italic;
  margin-left: 8px;
}

.submenu-item-container {
  max-height: 200px;
  overflow-y: auto;
}

.submenu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.15s ease;
  font-size: 0.85em;
  color: #374151;
  border-bottom: 1px solid #f8fafc;
}

.submenu-item:last-child {
  border-bottom: none;
}

.submenu-item:hover {
  background-color: #f0f9ff;
  color: #0369a1;
  padding-left: 20px;
}

.submenu-text {
  flex: 1;
  font-weight: 500;
}

.check-icon {
  color: #10b981;
  font-weight: bold;
  font-size: 14px;
  margin-left: 8px;
}

.stage-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.type-names {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 2px;
}

.type-name {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 0.7em;
  font-weight: 500;
  border: 1px solid #bbdefb;
}

.type-item {
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.15s ease;
  border-radius: 6px;
  margin: 2px 0;
}

.type-item:hover {
  background-color: #f0f9ff;
  transform: translateX(2px);
}

.type-item .submenu-text {
  font-weight: 500;
  color: #374151;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .submenu {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin: 0;
    max-width: 280px;
    width: 90vw;
  }

  .tests-menu {
    max-width: 95vw;
  }

  .menu-item-container {
    max-height: 200px;
  }
}

.lru-select option {
  padding: 4px 6px;
  font-size: 0.8em;
}

.serial-number-select {
  width: 100%;
  padding: 4px 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 0.8em;
  box-sizing: border-box;
  background-color: white;
  cursor: pointer;
}

.serial-number-select:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
  opacity: 0.6;
}

.serial-number-select:focus {
  border-color: #80bdff;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Serial Number Checkbox Dropdown Styles */
.serial-number-dropdown-container {
  position: relative;
  width: 100%;
}

.serial-number-dropdown {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #ccc;
  border-radius: 3px;
  padding: 4px 6px;
  background-color: white;
  cursor: pointer;
  font-size: 0.8em;
  min-height: 28px;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

.serial-number-dropdown:hover:not(:disabled) {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.1);
}

.serial-number-dropdown:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
  opacity: 0.6;
}

.serial-number-dropdown.active {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.serial-number-dropdown .selected-value {
  flex: 1;
  color: #333;
  font-size: 0.9em;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.selected-serials {
  display: flex;
  flex-direction: column;
}

.serial-list {
  color: #495057;
  font-size: 0.9em;
  word-break: break-all;
  line-height: 1.3;
  font-weight: 500;
}

.placeholder-text {
  color: #6c757d;
  font-style: italic;
}

.loading-text {
  color: #007bff;
  font-style: italic;
}

.error-text {
  color: #dc3545;
  font-style: italic;
}

.no-data-text {
  color: #6c757d;
  font-style: italic;
}

.serial-number-dropdown .dropdown-icon {
  color: #6c757d;
  font-size: 12px;
  margin-left: 8px;
  transition: transform 0.2s ease;
}

.serial-number-dropdown.active .dropdown-icon {
  transform: rotate(180deg);
}

.serial-number-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 4px;
  background: #fff;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08);
  z-index: 1000;
  overflow: hidden;
  animation: menuFadeIn 0.2s ease-out;
  backdrop-filter: blur(10px);
}

.serial-menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  border-radius: 6px 6px 0 0;
}

.serial-menu-header .menu-title {
  font-size: 0.8em;
  font-weight: 600;
  color: #495057;
  display: flex;
  align-items: center;
  gap: 8px;
}

.serial-menu-header .menu-title::before {
  content: "☑️";
  font-size: 0.9em;
}

.clear-btn {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  border: none;
  color: white;
  font-size: 0.7em;
  font-weight: 500;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(220, 53, 69, 0.2);
}

.clear-btn:hover {
  background: linear-gradient(135deg, #c82333 0%, #a71e2a 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
}

.clear-btn:active {
  transform: translateY(0);
}

.serial-menu-content {
  max-height: 200px;
  overflow-y: auto;
  padding: 4px 0;
}

.serial-menu-content::-webkit-scrollbar {
  width: 6px;
}

.serial-menu-content::-webkit-scrollbar-track {
  background: transparent;
}

.serial-menu-content::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.serial-menu-content::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

.serial-checkbox-item {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.8em;
  border-bottom: 1px solid #f1f3f4;
  position: relative;
}

.serial-checkbox-item:last-child {
  border-bottom: none;
}

.serial-checkbox-item:hover {
  background-color: #f8f9fa;
  transform: translateX(2px);
}

.serial-checkbox-item.selected {
  background-color: #e3f2fd;
  border-left: 3px solid #2196f3;
}

.checkbox-wrapper {
  position: relative;
  margin-right: 12px;
}

.serial-checkbox {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  background-color: #fff;
  border: 2px solid #ddd;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  cursor: pointer;
}

.checkbox-custom:hover {
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
}

.checkbox-custom.checked {
  background-color: #2196f3;
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
}

.check-icon {
  width: 12px;
  height: 12px;
  color: white;
  stroke-width: 3;
}

.serial-label {
  color: #333;
  font-size: 0.8em;
  font-weight: 500;
  flex: 1;
}

.selected-indicator {
  color: #2196f3;
  font-weight: bold;
  font-size: 14px;
  margin-left: 8px;
}

@keyframes menuFadeIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

.lru-description-select:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
  opacity: 0.6;
}

.error-message {
  color: #dc3545;
  font-size: 0.75em;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.retry-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 0.7em;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-btn:hover {
  background-color: #0056b3;
}

.info-message {
  color: #6c757d;
  font-size: 0.75em;
  margin-top: 4px;
  font-style: italic;
}

.desc-cell span {
  color: #666;
  font-size: 0.8em;
  font-style: italic;
}

.ref-cell input,
.refno-cell input,
.ver-cell input,
.rev-cell input {
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

.test-left,
.test-middle,
.test-right {
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

  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .lru-column,
  .desc-column,
  .checkbox-column,
  .ref-column,
  .refno-column,
  .ver-column,
  .rev-column {
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
  box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.2),
    inset 0 2px 4px rgba(0, 0, 0, 0.1);
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

  .send-btn,
  .cancel-btn {
    width: 100%;
    min-width: auto;
  }
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
  box-shadow: 0 0 0 3px rgba(108, 117, 125, 0.2),
    inset 0 2px 4px rgba(0, 0, 0, 0.1);
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

  .send-btn,
  .cancel-btn {
    width: 100%;
    min-width: auto;
  }
}

/* DateTime container styling */
.datetime-container {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.date-input {
  padding: 8px 12px;
  border: 1px solid #e1e5e9;
  border-radius: 6px;
  font-size: 0.9em;
  background: white;
  transition: all 0.2s ease;
  flex: 1;
  min-width: 140px;
}

.date-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.date-input:hover {
  border-color: #007bff;
}

/* Custom time picker styling */
.time-picker {
  display: flex;
  align-items: center;
  gap: 4px;
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 6px;
  padding: 4px 8px;
  transition: all 0.2s ease;
}

.time-picker:hover {
  border-color: #007bff;
}

.time-picker:focus-within {
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.time-select,
.ampm-select {
  border: none;
  background: transparent;
  font-size: 0.9em;
  padding: 4px 2px;
  cursor: pointer;
  outline: none;
  min-width: 45px;
}

.time-select:focus,
.ampm-select:focus {
  background: rgba(0, 123, 255, 0.1);
  border-radius: 3px;
}

.time-separator {
  font-weight: bold;
  color: #6c757d;
  margin: 0 2px;
}

.ampm-select {
  min-width: 55px;
  font-weight: 500;
}

/* Responsive adjustments for datetime containers */
@media (max-width: 768px) {
  .datetime-container {
    flex-direction: column;
    gap: 4px;
    align-items: stretch;
  }

  .date-input {
    width: 100%;
    min-width: unset;
  }

  .time-picker {
    justify-content: center;
  }
}

/* Disabled section styling */
.disabled-section {
  opacity: 0.6;
  pointer-events: none;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 5px;
  padding: 10px;
  margin: 5px 0;
}

.disabled-section input,
.disabled-section select,
.disabled-section textarea {
  background-color: #e9ecef !important;
  color: #6c757d !important;
  cursor: not-allowed;
}

.disabled-section .cert-checkbox {
  cursor: not-allowed;
}
</style>

