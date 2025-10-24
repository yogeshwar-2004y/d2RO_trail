<template>
  <div class="group-detail-page">
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
        <h1 class="page-title">{{ groupName }}</h1>
        <p class="page-subtitle">
          Manage sub-tests and bulletins for this group
        </p>
      </div>
      <div class="header-right">
        <button
          class="add-sub-test-btn"
          @click="showAddSubTestForm = !showAddSubTestForm"
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
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          ADD SUB-TEST
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Add Sub-test Form -->
      <div v-if="showAddSubTestForm" class="add-sub-test-form">
        <div class="form-header">
          <h3>Add New Sub-test</h3>
          <button @click="showAddSubTestForm = false" class="close-form-btn">
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
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveSubTest">
          <div class="form-group">
            <label for="subTestName">Sub-test Name *</label>
            <input
              type="text"
              id="subTestName"
              v-model="subTestForm.sub_test_name"
              placeholder="Enter sub-test name"
              required
            />
          </div>

          <div class="form-group">
            <label for="subTestDescription">Description</label>
            <textarea
              id="subTestDescription"
              v-model="subTestForm.sub_test_description"
              placeholder="Enter sub-test description"
              rows="3"
            ></textarea>
          </div>

          <!-- Optional Bulletins Section -->
          <div class="bulletins-section">
            <div class="section-header">
              <h4>Bulletins (Optional)</h4>
              <button
                type="button"
                @click="addBulletinToForm"
                class="add-bulletin-btn"
              >
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
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                Add Bulletin
              </button>
            </div>

            <div v-if="subTestForm.bulletins.length === 0" class="no-bulletins">
              <p>
                No bulletins added yet. Click "Add Bulletin" to add bulletins to
                this sub-test.
              </p>
            </div>

            <div v-else class="bulletins-list">
              <div
                v-for="(bulletin, index) in subTestForm.bulletins"
                :key="index"
                class="bulletin-form-item"
                :class="{ 'sub-bulletin': bulletin.parent_bulletin_id }"
              >
                <div class="bulletin-form-header">
                  <span class="bulletin-type">{{
                    bulletin.parent_bulletin_id ? "Sub-bulletin" : "Bulletin"
                  }}</span>
                  <button
                    type="button"
                    @click="removeBulletinFromForm(index)"
                    class="remove-bulletin-btn"
                  >
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
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path
                        d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                      ></path>
                    </svg>
                  </button>
                </div>

                <div class="bulletin-form-content">
                  <div class="form-group">
                    <label :for="`bulletinName${index}`">Bulletin Name *</label>
                    <input
                      type="text"
                      :id="`bulletinName${index}`"
                      v-model="bulletin.bulletin_name"
                      placeholder="Enter bulletin name"
                      required
                    />
                  </div>

                  <div class="form-group">
                    <label :for="`bulletinDescription${index}`"
                      >Description</label
                    >
                    <textarea
                      :id="`bulletinDescription${index}`"
                      v-model="bulletin.bulletin_description"
                      placeholder="Enter bulletin description"
                      rows="2"
                    ></textarea>
                  </div>

                  <div v-if="!bulletin.parent_bulletin_id" class="form-group">
                    <label :for="`subBulletins${index}`"
                      >Add Sub-bulletins</label
                    >
                    <button
                      type="button"
                      @click="addSubBulletinToForm(index)"
                      class="add-sub-bulletin-btn"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <line x1="12" y1="5" x2="12" y2="19"></line>
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                      </svg>
                      Add Sub-bulletin
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button
              type="button"
              @click="showAddSubTestForm = false"
              class="cancel-btn"
            >
              Cancel
            </button>
            <button type="submit" class="save-btn" :disabled="saving">
              {{ saving ? "Saving..." : "Create Sub-test" }}
            </button>
          </div>
        </form>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Loading sub-tests...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <h3>Error Loading Data</h3>
        <p>{{ error }}</p>
        <button @click="loadSubTests" class="retry-btn">Retry</button>
      </div>

      <!-- Sub-tests List -->
      <div v-else class="sub-tests-section">
        <div class="section-header">
          <h2>Sub-tests</h2>
          <span class="sub-test-count"
            >{{ subTests.length }} sub-test{{
              subTests.length !== 1 ? "s" : ""
            }}</span
          >
        </div>

        <!-- Empty State -->
        <div v-if="subTests.length === 0" class="empty-sub-tests">
          <div class="empty-icon">📋</div>
          <h3>No Sub-tests Found</h3>
          <p>Create your first sub-test to get started.</p>
          <button
            @click="showAddSubTestForm = true"
            class="add-first-sub-test-btn"
          >
            Create First Sub-test
          </button>
        </div>

        <!-- Hierarchical Sub-tests Structure -->
        <div v-else class="hierarchical-structure">
          <div
            v-for="subTest in subTests"
            :key="subTest.sub_test_id"
            class="sub-test-item"
          >
            <!-- Sub-test Header -->
            <div class="sub-test-header">
              <div class="sub-test-icon">
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
                </svg>
              </div>
              <div class="sub-test-info">
                <h3 class="sub-test-name">{{ subTest.sub_test_name }}</h3>
                <p class="sub-test-description">
                  {{
                    subTest.sub_test_description || "No description available"
                  }}
                </p>
                <div class="sub-test-meta">
                  <span class="created-date"
                    >Created: {{ formatDate(subTest.created_at) }}</span
                  >
                  <span class="bulletin-count"
                    >{{ getTotalBulletinCount(subTest.sub_test_id) }} bulletin{{
                      getTotalBulletinCount(subTest.sub_test_id) !== 1
                        ? "s"
                        : ""
                    }}</span
                  >
                </div>
              </div>
              <div class="sub-test-actions">
                <button
                  @click="showAddBulletinForm(subTest.sub_test_id)"
                  class="add-bulletin-btn"
                >
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
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                  Add Bulletins
                </button>
                <button
                  @click="editSubTest(subTest)"
                  class="action-btn edit-btn"
                >
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
                      d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                    ></path>
                    <path
                      d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                    ></path>
                  </svg>
                </button>
                <button
                  @click="deleteSubTest(subTest)"
                  class="action-btn delete-btn"
                >
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
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path
                      d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                    ></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Add Bulletin Form for this Sub-test -->
            <div
              v-if="showAddBulletinFormForSubTest === subTest.sub_test_id"
              class="add-bulletin-form"
            >
              <div class="form-header">
                <h4>Add Bulletin to {{ subTest.sub_test_name }}</h4>
                <button
                  @click="showAddBulletinFormForSubTest = null"
                  class="close-form-btn"
                >
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
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
              <form @submit.prevent="saveBulletin(subTest.sub_test_id)">
                <div class="form-group">
                  <label for="bulletinName">Bulletin Name *</label>
                  <input
                    type="text"
                    id="bulletinName"
                    v-model="bulletinForm.bulletin_name"
                    placeholder="Enter bulletin name"
                    required
                  />
                </div>

                <div class="form-group">
                  <label for="bulletinDescription">Description</label>
                  <textarea
                    id="bulletinDescription"
                    v-model="bulletinForm.bulletin_description"
                    placeholder="Enter bulletin description"
                    rows="3"
                  ></textarea>
                </div>

                <div class="form-actions">
                  <button
                    type="button"
                    @click="showAddBulletinFormForSubTest = null"
                    class="cancel-btn"
                  >
                    Cancel
                  </button>
                  <button type="submit" class="save-btn" :disabled="saving">
                    {{ saving ? "Saving..." : "Create Bulletin" }}
                  </button>
                </div>
              </form>
            </div>

            <!-- Bulletins for this Sub-test -->
            <div
              v-if="getBulletinsForSubTest(subTest.sub_test_id).length > 0"
              class="bulletins-section"
            >
              <div
                v-for="bulletin in getParentBulletins(subTest.sub_test_id)"
                :key="bulletin.bulletin_id"
                class="bulletin-item"
              >
                <!-- Parent Bulletin -->
                <div class="bulletin-content">
                  <div class="bulletin-header">
                    <div class="bulletin-icon">
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
                    </div>
                    <div class="bulletin-info">
                      <h4 class="bulletin-name">
                        {{ bulletin.bulletin_name }}
                      </h4>
                      <p class="bulletin-description">
                        {{
                          bulletin.bulletin_description ||
                          "No description available"
                        }}
                      </p>
                      <div class="bulletin-meta">
                        <span class="created-date"
                          >Created: {{ formatDate(bulletin.created_at) }}</span
                        >
                        <span class="sub-bulletin-count"
                          >{{
                            getSubBulletins(
                              subTest.sub_test_id,
                              bulletin.bulletin_id
                            ).length
                          }}
                          sub-bulletin{{
                            getSubBulletins(
                              subTest.sub_test_id,
                              bulletin.bulletin_id
                            ).length !== 1
                              ? "s"
                              : ""
                          }}</span
                        >
                      </div>
                    </div>
                    <div class="bulletin-actions">
                      <button
                        @click="showAddSubBulletinForm(bulletin.bulletin_id)"
                        class="add-sub-bulletin-btn"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="14"
                          height="14"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        >
                          <line x1="12" y1="5" x2="12" y2="19"></line>
                          <line x1="5" y1="12" x2="19" y2="12"></line>
                        </svg>
                        Add Sub-bulletin
                      </button>
                      <button
                        @click="editBulletin(bulletin)"
                        class="action-btn edit-btn"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="14"
                          height="14"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        >
                          <path
                            d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                          ></path>
                          <path
                            d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                          ></path>
                        </svg>
                      </button>
                      <button
                        @click="deleteBulletin(bulletin)"
                        class="action-btn delete-btn"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="14"
                          height="14"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        >
                          <polyline points="3 6 5 6 21 6"></polyline>
                          <path
                            d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                          ></path>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Add Sub-bulletin Form -->
                <div
                  v-if="showAddSubBulletinFormId === bulletin.bulletin_id"
                  class="add-sub-bulletin-form"
                >
                  <div class="form-header">
                    <h5>Add Sub-bulletin to {{ bulletin.bulletin_name }}</h5>
                    <button
                      @click="showAddSubBulletinFormId = null"
                      class="close-form-btn"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="14"
                        height="14"
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
                  <form @submit.prevent="saveBulletin(subTest.sub_test_id)">
                    <div class="form-group">
                      <label for="subBulletinName">Sub-bulletin Name *</label>
                      <input
                        type="text"
                        id="subBulletinName"
                        v-model="bulletinForm.bulletin_name"
                        placeholder="Enter sub-bulletin name"
                        required
                      />
                    </div>

                    <div class="form-group">
                      <label for="subBulletinDescription">Description</label>
                      <textarea
                        id="subBulletinDescription"
                        v-model="bulletinForm.bulletin_description"
                        placeholder="Enter sub-bulletin description"
                        rows="2"
                      ></textarea>
                    </div>

                    <div class="form-actions">
                      <button
                        type="button"
                        @click="showAddSubBulletinFormId = null"
                        class="cancel-btn"
                      >
                        Cancel
                      </button>
                      <button type="submit" class="save-btn" :disabled="saving">
                        {{ saving ? "Saving..." : "Create Sub-bulletin" }}
                      </button>
                    </div>
                  </form>
                </div>

                <!-- Edit Bulletin Form -->
                <div
                  v-if="showEditBulletinFormId === bulletin.bulletin_id"
                  class="edit-bulletin-form"
                >
                  <div class="form-header">
                    <h5>Edit Bulletin</h5>
                    <button
                      @click="closeEditBulletinForm"
                      class="close-form-btn"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="14"
                        height="14"
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
                  <form @submit.prevent="updateBulletinFromForm">
                    <div class="form-group">
                      <label for="editBulletinName">Bulletin Name *</label>
                      <input
                        type="text"
                        id="editBulletinName"
                        v-model="editingBulletinForm.bulletin_name"
                        placeholder="Enter bulletin name"
                        required
                      />
                    </div>

                    <div class="form-group">
                      <label for="editBulletinDescription">Description</label>
                      <textarea
                        id="editBulletinDescription"
                        v-model="editingBulletinForm.bulletin_description"
                        placeholder="Enter bulletin description"
                        rows="2"
                      ></textarea>
                    </div>

                    <div class="form-actions">
                      <button
                        type="button"
                        @click="closeEditBulletinForm"
                        class="cancel-btn"
                      >
                        Cancel
                      </button>
                      <button type="submit" class="save-btn" :disabled="saving">
                        {{ saving ? "Saving..." : "Update Bulletin" }}
                      </button>
                    </div>
                  </form>
                </div>

                <!-- Sub-bulletins -->
                <div
                  v-if="
                    getSubBulletins(subTest.sub_test_id, bulletin.bulletin_id)
                      .length > 0
                  "
                  class="sub-bulletins-list"
                >
                  <div
                    v-for="subBulletin in getSubBulletins(
                      subTest.sub_test_id,
                      bulletin.bulletin_id
                    )"
                    :key="subBulletin.bulletin_id"
                    class="sub-bulletin-item"
                  >
                    <div class="sub-bulletin-content">
                      <div class="sub-bulletin-icon">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="14"
                          height="14"
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
                      <div class="sub-bulletin-info">
                        <h5 class="sub-bulletin-name">
                          {{ subBulletin.bulletin_name }}
                        </h5>
                        <p class="sub-bulletin-description">
                          {{
                            subBulletin.bulletin_description ||
                            "No description available"
                          }}
                        </p>
                        <div class="sub-bulletin-meta">
                          <span class="created-date"
                            >Created:
                            {{ formatDate(subBulletin.created_at) }}</span
                          >
                        </div>
                      </div>
                      <div class="sub-bulletin-actions">
                        <button
                          @click="editBulletin(subBulletin)"
                          class="action-btn edit-btn"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="12"
                            height="12"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
                            <path
                              d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
                            ></path>
                            <path
                              d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
                            ></path>
                          </svg>
                        </button>
                        <button
                          @click="deleteBulletin(subBulletin)"
                          class="action-btn delete-btn"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="12"
                            height="12"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path
                              d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
                            ></path>
                          </svg>
                        </button>
                      </div>
                    </div>

                    <!-- Edit Sub-bulletin Form -->
                    <div
                      v-if="showEditBulletinFormId === subBulletin.bulletin_id"
                      class="edit-sub-bulletin-form"
                    >
                      <div class="form-header">
                        <h6>Edit Sub-bulletin</h6>
                        <button
                          @click="closeEditBulletinForm"
                          class="close-form-btn"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="12"
                            height="12"
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
                      <form @submit.prevent="updateBulletinFromForm">
                        <div class="form-group">
                          <label for="editSubBulletinName"
                            >Sub-bulletin Name *</label
                          >
                          <input
                            type="text"
                            id="editSubBulletinName"
                            v-model="editingBulletinForm.bulletin_name"
                            placeholder="Enter sub-bulletin name"
                            required
                          />
                        </div>

                        <div class="form-group">
                          <label for="editSubBulletinDescription"
                            >Description</label
                          >
                          <textarea
                            id="editSubBulletinDescription"
                            v-model="editingBulletinForm.bulletin_description"
                            placeholder="Enter sub-bulletin description"
                            rows="2"
                          ></textarea>
                        </div>

                        <div class="form-actions">
                          <button
                            type="button"
                            @click="closeEditBulletinForm"
                            class="cancel-btn"
                          >
                            Cancel
                          </button>
                          <button
                            type="submit"
                            class="save-btn"
                            :disabled="saving"
                          >
                            {{ saving ? "Saving..." : "Update Sub-bulletin" }}
                          </button>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Sub-test Form -->
    <div v-if="showEditSubTestForm" class="edit-sub-test-form">
      <div class="form-header">
        <h3>Edit Sub-test</h3>
        <button @click="closeEditForm" class="close-form-btn">
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
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <form @submit.prevent="updateSubTest">
        <div class="form-group">
          <label for="editSubTestName">Sub-test Name *</label>
          <input
            type="text"
            id="editSubTestName"
            v-model="editingSubTestForm.sub_test_name"
            placeholder="Enter sub-test name"
            required
          />
        </div>

        <div class="form-group">
          <label for="editSubTestDescription">Description</label>
          <textarea
            id="editSubTestDescription"
            v-model="editingSubTestForm.sub_test_description"
            placeholder="Enter sub-test description"
            rows="3"
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="button" @click="closeEditForm" class="cancel-btn">
            Cancel
          </button>
          <button type="submit" class="save-btn" :disabled="saving">
            {{ saving ? "Saving..." : "Update Sub-test" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { userStore } from "@/stores/userStore";

export default {
  name: "GroupDetail",
  data() {
    return {
      // Data
      subTests: [],
      bulletinCounts: {},
      subTestBulletins: {}, // Store bulletins for each sub-test

      // Loading states
      loading: false,
      saving: false,

      // Error handling
      error: null,

      // Form states
      showAddSubTestForm: false,
      showEditSubTestForm: false,
      showAddBulletinFormForSubTest: null, // Track which sub-test is adding bulletins
      showAddSubBulletinFormId: null, // Track which bulletin is adding sub-bulletins
      showEditBulletinFormId: null, // Track which bulletin is being edited

      // Selected items
      editingSubTest: null,
      editingBulletin: null,

      // Forms
      subTestForm: {
        sub_test_name: "",
        sub_test_description: "",
        bulletins: [],
      },
      editingSubTestForm: {
        sub_test_name: "",
        sub_test_description: "",
      },
      bulletinForm: {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      },
      editingBulletinForm: {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      },
    };
  },
  computed: {
    groupId() {
      return this.$route.params.groupId;
    },
    groupName() {
      return this.$route.params.groupName;
    },
  },
  mounted() {
    this.loadSubTests();
  },
  methods: {
    // API Methods
    async loadSubTests() {
      this.loading = true;
      this.error = null;

      try {
        const response = await fetch(
          `http://localhost:8000/api/test-groups/${this.groupId}/sub-tests`
        );
        const data = await response.json();

        if (data.success) {
          this.subTests = data.sub_tests;
          console.log(`=== SUB-TESTS API RESPONSE ===`);
          console.log(`Group ID: ${this.groupId}`);
          console.log(
            `Loaded ${data.sub_tests.length} sub-tests:`,
            data.sub_tests
          );
          data.sub_tests.forEach((subTest, index) => {
            console.log(`Sub-test ${index + 1}:`, subTest);
          });
          console.log(`=== END SUB-TESTS RESPONSE ===`);
          await this.loadBulletinCounts();
        } else {
          this.error = data.message || "Failed to load sub-tests";
        }
      } catch (error) {
        console.error("Error loading sub-tests:", error);
        this.error = "Failed to load sub-tests. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    async loadBulletinCounts() {
      // First, load bulletins for each sub-test
      for (const subTest of this.subTests) {
        try {
          const response = await fetch(
            `http://localhost:8000/api/sub-tests/${subTest.sub_test_id}/bulletins`
          );
          const data = await response.json();

          if (data.success) {
            // Process the nested structure from API response
            const allBulletins = [];

            // Add parent bulletins
            data.bulletins.forEach((parentBulletin) => {
              // Add the parent bulletin
              allBulletins.push(parentBulletin);

              // Add sub-bulletins from the nested structure
              if (
                parentBulletin.sub_bulletins &&
                parentBulletin.sub_bulletins.length > 0
              ) {
                parentBulletin.sub_bulletins.forEach((subBulletin) => {
                  // Ensure sub-bulletin has the correct parent_bulletin_id
                  subBulletin.parent_bulletin_id = parentBulletin.bulletin_id;
                  allBulletins.push(subBulletin);
                });
              }
            });

            // Store all bulletins (both parent and sub-bulletins) in flat structure
            this.subTestBulletins[subTest.sub_test_id] = allBulletins;

            // Count only parent bulletins for the count display (legacy method)
            const parentBulletins = allBulletins.filter(
              (bulletin) => !bulletin.parent_bulletin_id
            );
            this.bulletinCounts[subTest.sub_test_id] = parentBulletins.length;

            console.log(
              `=== BULLETINS FOR SUB-TEST ${subTest.sub_test_id} ===`
            );
            console.log(`Sub-test: ${subTest.sub_test_name}`);
            console.log(`Total bulletins: ${allBulletins.length}`);
            console.log(`Parent bulletins: ${parentBulletins.length}`);
            console.log(
              `Sub-bulletins: ${allBulletins.length - parentBulletins.length}`
            );
            console.log(`Raw API data:`, data.bulletins);
            console.log(`Processed flat data:`, allBulletins);
            allBulletins.forEach((bulletin, index) => {
              console.log(`Bulletin ${index + 1}:`, bulletin);
            });
            console.log(
              `=== END BULLETINS FOR SUB-TEST ${subTest.sub_test_id} ===`
            );
          }
        } catch (error) {
          console.error(
            `Error loading bulletins for sub-test ${subTest.sub_test_id}:`,
            error
          );
          this.bulletinCounts[subTest.sub_test_id] = 0;
          this.subTestBulletins[subTest.sub_test_id] = [];
        }
      }

      // Then, handle cross-sub-test relationships by redistributing sub-bulletins
      this.redistributeSubBulletins();
    },

    redistributeSubBulletins() {
      console.log(`=== REDISTRIBUTING SUB-BULLETINS ===`);

      // Get all bulletins from all sub-tests
      const allBulletins = [];
      for (const testId in this.subTestBulletins) {
        allBulletins.push(...this.subTestBulletins[testId]);
      }

      console.log(`All bulletins across sub-tests:`, allBulletins);

      // Find sub-bulletins that belong to bulletins in different sub-tests
      for (const bulletin of allBulletins) {
        if (bulletin.parent_bulletin_id) {
          // This is a sub-bulletin, find its parent
          const parentBulletin = allBulletins.find(
            (b) => b.bulletin_id === bulletin.parent_bulletin_id
          );
          if (
            parentBulletin &&
            parentBulletin.sub_test_id !== bulletin.sub_test_id
          ) {
            console.log(`Found cross-sub-test sub-bulletin:`, bulletin);
            console.log(`Parent bulletin:`, parentBulletin);

            // Move this sub-bulletin to the parent's sub-test
            const parentSubTestId = parentBulletin.sub_test_id;
            if (!this.subTestBulletins[parentSubTestId]) {
              this.subTestBulletins[parentSubTestId] = [];
            }

            // Remove from current sub-test
            const currentSubTestBulletins =
              this.subTestBulletins[bulletin.sub_test_id];
            const index = currentSubTestBulletins.findIndex(
              (b) => b.bulletin_id === bulletin.bulletin_id
            );
            if (index > -1) {
              currentSubTestBulletins.splice(index, 1);
            }

            // Add to parent's sub-test
            this.subTestBulletins[parentSubTestId].push(bulletin);

            console.log(
              `Moved sub-bulletin ${bulletin.bulletin_id} to sub-test ${parentSubTestId}`
            );
          }
        }
      }

      // Update counts after redistribution
      for (const subTest of this.subTests) {
        const bulletins = this.subTestBulletins[subTest.sub_test_id] || [];
        const parentBulletins = bulletins.filter(
          (bulletin) => !bulletin.parent_bulletin_id
        );
        this.bulletinCounts[subTest.sub_test_id] = parentBulletins.length;

        console.log(
          `Sub-test ${subTest.sub_test_id} final count: ${bulletins.length} total, ${parentBulletins.length} parent`
        );
      }

      console.log(`=== END REDISTRIBUTING SUB-BULLETINS ===`);
    },

    async saveSubTest() {
      this.saving = true;

      try {
        // Get current user ID
        const currentUser = userStore.getters.currentUser();
        const userId = currentUser ? currentUser.id : null;

        // First, create the sub-test
        const subTestData = {
          sub_test_name: this.subTestForm.sub_test_name,
          sub_test_description: this.subTestForm.sub_test_description,
          created_by: userId,
        };

        const response = await fetch(
          `http://localhost:8000/api/test-groups/${this.groupId}/sub-tests`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(subTestData),
          }
        );

        const data = await response.json();

        if (data.success) {
          const subTestId = data.sub_test_id;

          // Now create bulletins if any
          if (this.subTestForm.bulletins.length > 0) {
            await this.createBulletinsForSubTest(subTestId);
          }

          await this.loadSubTests();
          this.showAddSubTestForm = false;
          this.resetSubTestForm();
        } else {
          alert(data.message || "Failed to save sub-test");
        }
      } catch (error) {
        console.error("Error saving sub-test:", error);
        alert("Failed to save sub-test. Please try again.");
      } finally {
        this.saving = false;
      }
    },

    async updateSubTest() {
      this.saving = true;

      try {
        // Get current user ID
        const currentUser = userStore.getters.currentUser();
        const userId = currentUser ? currentUser.id : null;

        const updateData = {
          ...this.editingSubTestForm,
          updated_by: userId,
        };

        const response = await fetch(
          `http://localhost:8000/api/sub-tests/${this.editingSubTest.sub_test_id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updateData),
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.loadSubTests();
          this.closeEditForm();
        } else {
          alert(data.message || "Failed to update sub-test");
        }
      } catch (error) {
        console.error("Error updating sub-test:", error);
        alert("Failed to update sub-test. Please try again.");
      } finally {
        this.saving = false;
      }
    },

    async deleteSubTest(subTest) {
      if (
        !confirm(
          `Are you sure you want to delete "${subTest.sub_test_name}"? This will also delete all bulletins.`
        )
      ) {
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/api/sub-tests/${subTest.sub_test_id}`,
          {
            method: "DELETE",
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.loadSubTests();
        } else {
          alert(data.message || "Failed to delete sub-test");
        }
      } catch (error) {
        console.error("Error deleting sub-test:", error);
        alert("Failed to delete sub-test. Please try again.");
      }
    },

    // Navigation Methods
    goToSubTest(subTest) {
      // Navigate to sub-test detail page (bulletins)
      this.$router.push({
        name: "SubTestDetail",
        params: {
          groupId: this.groupId,
          groupName: this.groupName,
          subTestId: subTest.sub_test_id,
          subTestName: subTest.sub_test_name,
        },
      });
    },

    // UI Methods
    editSubTest(subTest) {
      this.editingSubTest = subTest;
      this.editingSubTestForm = {
        sub_test_name: subTest.sub_test_name,
        sub_test_description: subTest.sub_test_description || "",
      };
      this.showEditSubTestForm = true;
    },

    closeEditForm() {
      this.showEditSubTestForm = false;
      this.editingSubTest = null;
      this.editingSubTestForm = {
        sub_test_name: "",
        sub_test_description: "",
      };
    },

    // Form Management
    resetSubTestForm() {
      this.subTestForm = {
        sub_test_name: "",
        sub_test_description: "",
        bulletins: [],
      };
    },

    // Bulletin Form Management
    addBulletinToForm() {
      this.subTestForm.bulletins.push({
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      });
    },

    addSubBulletinToForm(parentIndex) {
      this.subTestForm.bulletins.push({
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: parentIndex, // Store the index as temporary parent reference
      });
    },

    removeBulletinFromForm(index) {
      this.subTestForm.bulletins.splice(index, 1);
    },

    async createBulletinsForSubTest(subTestId) {
      // Get current user ID
      const currentUser = userStore.getters.currentUser();
      const userId = currentUser ? currentUser.id : null;

      const parentBulletins = [];
      const subBulletins = [];

      // Separate parent bulletins and sub-bulletins
      this.subTestForm.bulletins.forEach((bulletin, index) => {
        if (bulletin.parent_bulletin_id === null) {
          parentBulletins.push({ ...bulletin, tempIndex: index });
        } else {
          subBulletins.push({
            ...bulletin,
            parentTempIndex: bulletin.parent_bulletin_id,
          });
        }
      });

      // Create parent bulletins first
      for (const bulletin of parentBulletins) {
        try {
          const response = await fetch(
            `http://localhost:8000/api/sub-tests/${subTestId}/bulletins`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                bulletin_name: bulletin.bulletin_name,
                bulletin_description: bulletin.bulletin_description,
                parent_bulletin_id: null,
                created_by: userId,
              }),
            }
          );

          const data = await response.json();
          if (data.success) {
            // Store the actual bulletin ID for sub-bulletins
            bulletin.actualId = data.bulletin_id;
          }
        } catch (error) {
          console.error("Error creating parent bulletin:", error);
        }
      }

      // Create sub-bulletins
      for (const subBulletin of subBulletins) {
        const parentBulletin = parentBulletins.find(
          (pb) => pb.tempIndex === subBulletin.parentTempIndex
        );
        if (parentBulletin && parentBulletin.actualId) {
          try {
            await fetch(
              `http://localhost:8000/api/sub-tests/${subTestId}/bulletins`,
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  bulletin_name: subBulletin.bulletin_name,
                  bulletin_description: subBulletin.bulletin_description,
                  parent_bulletin_id: parentBulletin.actualId,
                  created_by: userId,
                }),
              }
            );
          } catch (error) {
            console.error("Error creating sub-bulletin:", error);
          }
        }
      }
    },

    // Bulletin Management Methods
    showAddBulletinForm(subTestId) {
      this.showAddBulletinFormForSubTest = subTestId;
      this.bulletinForm = {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      };
    },

    showAddSubBulletinForm(bulletinId) {
      this.showAddSubBulletinFormId = bulletinId;
      this.bulletinForm = {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: bulletinId,
      };
    },

    async saveBulletin(subTestId) {
      this.saving = true;

      try {
        // Get current user ID
        const currentUser = userStore.getters.currentUser();
        const userId = currentUser ? currentUser.id : null;

        const bulletinData = {
          ...this.bulletinForm,
          created_by: userId,
        };

        const response = await fetch(
          `http://localhost:8000/api/sub-tests/${subTestId}/bulletins`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(bulletinData),
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.loadBulletinCounts();
          this.showAddBulletinFormForSubTest = null;
          this.showAddSubBulletinFormId = null;
          this.resetBulletinForm();
        } else {
          alert(data.message || "Failed to save bulletin");
        }
      } catch (error) {
        console.error("Error saving bulletin:", error);
        alert("Failed to save bulletin. Please try again.");
      } finally {
        this.saving = false;
      }
    },

    resetBulletinForm() {
      this.bulletinForm = {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      };
    },

    // Bulletin CRUD Operations
    async updateBulletin(bulletin) {
      this.saving = true;

      try {
        // Get current user ID
        const currentUser = userStore.getters.currentUser();
        const userId = currentUser ? currentUser.id : null;

        const updateData = {
          bulletin_name: bulletin.bulletin_name,
          bulletin_description: bulletin.bulletin_description,
          parent_bulletin_id: bulletin.parent_bulletin_id,
          updated_by: userId,
        };

        const response = await fetch(
          `http://localhost:8000/api/bulletins/${bulletin.bulletin_id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updateData),
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.loadBulletinCounts();
        } else {
          alert(data.message || "Failed to update bulletin");
        }
      } catch (error) {
        console.error("Error updating bulletin:", error);
        alert("Failed to update bulletin. Please try again.");
      } finally {
        this.saving = false;
      }
    },

    async deleteBulletin(bulletin) {
      const bulletinType = bulletin.parent_bulletin_id
        ? "sub-bulletin"
        : "bulletin";
      if (
        !confirm(
          `Are you sure you want to delete "${
            bulletin.bulletin_name
          }"? This will also delete all related ${
            bulletinType === "bulletin" ? "sub-bulletins" : "data"
          }.`
        )
      ) {
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/api/bulletins/${bulletin.bulletin_id}`,
          {
            method: "DELETE",
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.loadBulletinCounts();
        } else {
          alert(data.message || "Failed to delete bulletin");
        }
      } catch (error) {
        console.error("Error deleting bulletin:", error);
        alert("Failed to delete bulletin. Please try again.");
      }
    },

    // Bulletin Edit Methods
    editBulletin(bulletin) {
      this.editingBulletin = bulletin;
      this.editingBulletinForm = {
        bulletin_name: bulletin.bulletin_name,
        bulletin_description: bulletin.bulletin_description || "",
        parent_bulletin_id: bulletin.parent_bulletin_id,
      };
      this.showEditBulletinFormId = bulletin.bulletin_id;
    },

    closeEditBulletinForm() {
      this.showEditBulletinFormId = null;
      this.editingBulletin = null;
      this.editingBulletinForm = {
        bulletin_name: "",
        bulletin_description: "",
        parent_bulletin_id: null,
      };
    },

    async updateBulletinFromForm() {
      this.saving = true;

      try {
        // Get current user ID
        const currentUser = userStore.getters.currentUser();
        const userId = currentUser ? currentUser.id : null;

        const updateData = {
          bulletin_name: this.editingBulletinForm.bulletin_name,
          bulletin_description: this.editingBulletinForm.bulletin_description,
          parent_bulletin_id: this.editingBulletinForm.parent_bulletin_id,
          updated_by: userId,
        };

        const response = await fetch(
          `http://localhost:8000/api/bulletins/${this.editingBulletin.bulletin_id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updateData),
          }
        );

        const data = await response.json();

        if (data.success) {
          await this.loadBulletinCounts();
          this.closeEditBulletinForm();
        } else {
          alert(data.message || "Failed to update bulletin");
        }
      } catch (error) {
        console.error("Error updating bulletin:", error);
        alert("Failed to update bulletin. Please try again.");
      } finally {
        this.saving = false;
      }
    },

    getBulletinsForSubTest(subTestId) {
      return this.subTestBulletins[subTestId] || [];
    },

    getParentBulletins(subTestId) {
      const bulletins = this.getBulletinsForSubTest(subTestId);
      return bulletins.filter((bulletin) => !bulletin.parent_bulletin_id);
    },

    getSubBulletins(subTestId, parentBulletinId) {
      // Get bulletins for the specific sub-test first
      const subTestBulletins = this.subTestBulletins[subTestId] || [];

      // Filter for sub-bulletins that belong to this parent bulletin
      const subBulletins = subTestBulletins.filter(
        (bulletin) => bulletin.parent_bulletin_id === parentBulletinId
      );

      console.log(`=== GET SUB-BULLETINS DEBUG ===`);
      console.log(`Sub-test ID: ${subTestId}`);
      console.log(`Parent bulletin ID: ${parentBulletinId}`);
      console.log(`Total bulletins in sub-test: ${subTestBulletins.length}`);
      console.log(`Found ${subBulletins.length} sub-bulletins:`, subBulletins);
      console.log(`All bulletins in sub-test:`, subTestBulletins);
      console.log(`=== END GET SUB-BULLETINS DEBUG ===`);

      return subBulletins;
    },

    // Utility Methods
    getBulletinCount(subTestId) {
      return this.bulletinCounts[subTestId] || 0;
    },

    getTotalBulletinCount(subTestId) {
      // Get bulletins for this specific sub-test
      const subTestBulletins = this.subTestBulletins[subTestId] || [];

      // Count all bulletins (both parent and sub-bulletins) in this sub-test
      return subTestBulletins.length;
    },

    formatDate(dateString) {
      if (!dateString) return "Unknown";
      return new Date(dateString).toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.group-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
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

.page-subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1em;
  margin: 5px 0 0 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.add-sub-test-btn {
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

.add-sub-test-btn:hover {
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

/* Add Sub-test Form */
.add-sub-test-form,
.edit-sub-test-form {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 25px;
  margin-bottom: 30px;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e9ecef;
}

.form-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: 1.4em;
  font-weight: 600;
}

.close-form-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: #6c757d;
}

.close-form-btn:hover {
  background: #f8f9fa;
  color: #dc3545;
}

/* Form Styles */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2d3748;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 25px;
}

.cancel-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #5a6268;
}

.save-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover:not(:disabled) {
  background: #0056b3;
}

.save-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Error State */
.error-state {
  text-align: center;
  padding: 60px 20px;
}

.error-icon {
  font-size: 4em;
  margin-bottom: 20px;
}

.error-state h3 {
  color: #dc3545;
  font-size: 1.5em;
  margin-bottom: 10px;
}

.error-state p {
  color: #6c757d;
  margin-bottom: 20px;
}

.retry-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.retry-btn:hover {
  background: #0056b3;
}

/* Sub-tests Section */
.sub-tests-section {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e9ecef;
}

.section-header h2 {
  margin: 0;
  color: #2d3748;
  font-size: 1.8em;
  font-weight: 600;
}

.sub-test-count {
  color: #6c757d;
  font-size: 1em;
  font-weight: 500;
}

/* Empty State */
.empty-sub-tests {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 4em;
  margin-bottom: 20px;
  opacity: 0.6;
}

.empty-sub-tests h3 {
  color: #6c757d;
  font-size: 1.5em;
  margin-bottom: 10px;
}

.empty-sub-tests p {
  color: #6c757d;
  font-size: 1em;
  margin-bottom: 30px;
}

.add-first-sub-test-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 10px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-first-sub-test-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

/* Sub-tests Grid */
.sub-tests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
}

.sub-test-card {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sub-test-card:hover {
  background: #e9ecef;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  border-color: #007bff;
}

.sub-test-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.sub-test-icon {
  color: #007bff;
}

.sub-test-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: none;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  transform: scale(1.1);
}

.edit-btn:hover {
  background: #e3f2fd;
  border-color: #2196f3;
  color: #2196f3;
}

.delete-btn:hover {
  background: #ffebee;
  border-color: #f44336;
  color: #f44336;
}

.sub-test-content {
  text-align: left;
}

.sub-test-name {
  color: #2d3748;
  font-size: 1.2em;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.sub-test-description {
  color: #6c757d;
  font-size: 0.9em;
  line-height: 1.4;
  margin: 0 0 12px 0;
}

.sub-test-meta {
  display: flex;
  gap: 15px;
  font-size: 0.8em;
  color: #6c757d;
}

.created-date {
  font-style: italic;
}

.bulletin-count {
  font-weight: 500;
  color: #007bff;
}

/* Bulletin Form Styles */
.bulletins-section {
  margin-top: 25px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.bulletins-section .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e9ecef;
}

.bulletins-section .section-header h4 {
  margin: 0;
  color: #2d3748;
  font-size: 1.1em;
  font-weight: 600;
}

.add-bulletin-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 6px;
  font-size: 0.9em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.add-bulletin-btn:hover {
  background: #218838;
}

.no-bulletins {
  text-align: center;
  padding: 20px;
  color: #6c757d;
  font-style: italic;
}

.bulletins-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.bulletin-form-item {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  transition: all 0.3s ease;
}

.bulletin-form-item.sub-bulletin {
  margin-left: 20px;
  background: #f0f8ff;
  border-left: 4px solid #28a745;
}

.bulletin-form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e9ecef;
}

.bulletin-type {
  font-size: 0.9em;
  font-weight: 600;
  color: #007bff;
  background: #e3f2fd;
  padding: 4px 8px;
  border-radius: 4px;
}

.bulletin-form-item.sub-bulletin .bulletin-type {
  color: #28a745;
  background: #d4edda;
}

.remove-bulletin-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 6px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-bulletin-btn:hover {
  background: #c82333;
}

.bulletin-form-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.bulletin-form-content .form-group {
  margin-bottom: 0;
}

.bulletin-form-content .form-group label {
  font-size: 0.9em;
  margin-bottom: 5px;
}

.bulletin-form-content .form-group input,
.bulletin-form-content .form-group textarea {
  padding: 8px;
  font-size: 0.9em;
}

.add-sub-bulletin-btn {
  background: #17a2b8;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  font-size: 0.8em;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
  width: fit-content;
}

.add-sub-bulletin-btn:hover {
  background: #138496;
}

/* Hierarchical Structure Styles */
.hierarchical-structure {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.sub-test-item {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.sub-test-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.sub-test-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.sub-test-icon {
  color: #007bff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sub-test-info {
  flex: 1;
}

.sub-test-name {
  margin: 0 0 8px 0;
  color: #2d3748;
  font-size: 1.3em;
  font-weight: 600;
}

.sub-test-description {
  margin: 0 0 10px 0;
  color: #6c757d;
  font-size: 0.95em;
  line-height: 1.4;
}

.sub-test-meta {
  display: flex;
  gap: 15px;
  font-size: 0.85em;
  color: #6c757d;
}

.sub-test-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.add-bulletin-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 6px;
  font-size: 0.9em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 5px;
}

.add-bulletin-btn:hover {
  background: #218838;
}

/* Bulletin Forms */
.add-bulletin-form,
.add-sub-bulletin-form {
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  padding: 20px;
}

.add-bulletin-form .form-header,
.add-sub-bulletin-form .form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e9ecef;
}

.add-bulletin-form .form-header h4,
.add-sub-bulletin-form .form-header h5 {
  margin: 0;
  color: #2d3748;
  font-size: 1.1em;
  font-weight: 600;
}

.add-sub-bulletin-form .form-header h5 {
  font-size: 1em;
}

.close-form-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 6px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-form-btn:hover {
  background: #c82333;
}

/* Bulletins Section */
.bulletins-section {
  padding: 20px;
  background: #f8f9fa;
}

.bulletin-item {
  margin-bottom: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  overflow: hidden;
}

.bulletin-content {
  padding: 15px;
}

.bulletin-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.bulletin-icon {
  color: #007bff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bulletin-info {
  flex: 1;
}

.bulletin-name {
  margin: 0 0 5px 0;
  color: #2d3748;
  font-size: 1.1em;
  font-weight: 600;
}

.bulletin-description {
  margin: 0 0 8px 0;
  color: #6c757d;
  font-size: 0.9em;
  line-height: 1.4;
}

.bulletin-meta {
  display: flex;
  gap: 15px;
  font-size: 0.8em;
  color: #6c757d;
}

.bulletin-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.add-sub-bulletin-btn {
  background: #17a2b8;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  font-size: 0.8em;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 4px;
}

.add-sub-bulletin-btn:hover {
  background: #138496;
}

/* Sub-bulletins */
.sub-bulletins-list {
  margin-top: 15px;
  margin-left: 20px;
  border-left: 3px solid #28a745;
  padding-left: 15px;
}

.sub-bulletin-item {
  background: #f0f8ff;
  border-radius: 6px;
  border: 1px solid #e3f2fd;
  margin-bottom: 10px;
}

.sub-bulletin-content {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
}

.sub-bulletin-icon {
  color: #28a745;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sub-bulletin-info {
  flex: 1;
}

.sub-bulletin-name {
  margin: 0 0 4px 0;
  color: #2d3748;
  font-size: 1em;
  font-weight: 600;
}

.sub-bulletin-description {
  margin: 0 0 6px 0;
  color: #6c757d;
  font-size: 0.85em;
  line-height: 1.3;
}

.sub-bulletin-meta {
  font-size: 0.75em;
  color: #6c757d;
}

.sub-bulletin-actions {
  display: flex;
  gap: 6px;
  align-items: center;
}

.sub-bulletin-actions .action-btn {
  padding: 4px;
  border-radius: 4px;
}

/* Edit Bulletin Form */
.edit-bulletin-form {
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  padding: 15px;
  margin-top: 10px;
}

.edit-bulletin-form .form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e9ecef;
}

.edit-bulletin-form .form-header h5 {
  margin: 0;
  color: #2d3748;
  font-size: 0.95em;
  font-weight: 600;
}

.edit-bulletin-form .form-group {
  margin-bottom: 12px;
}

.edit-bulletin-form .form-group label {
  font-size: 0.85em;
  margin-bottom: 4px;
}

.edit-bulletin-form .form-group input,
.edit-bulletin-form .form-group textarea {
  padding: 6px;
  font-size: 0.85em;
}

.edit-bulletin-form .form-actions {
  margin-top: 15px;
  gap: 10px;
}

.edit-bulletin-form .cancel-btn,
.edit-bulletin-form .save-btn {
  padding: 8px 15px;
  font-size: 0.85em;
}

/* Edit Sub-bulletin Form */
.edit-sub-bulletin-form {
  background: #f0f8ff;
  border: 1px solid #e3f2fd;
  border-radius: 6px;
  padding: 12px;
  margin-top: 8px;
}

.edit-sub-bulletin-form .form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 6px;
  border-bottom: 1px solid #e3f2fd;
}

.edit-sub-bulletin-form .form-header h6 {
  margin: 0;
  color: #2d3748;
  font-size: 0.9em;
  font-weight: 600;
}

.edit-sub-bulletin-form .form-group {
  margin-bottom: 10px;
}

.edit-sub-bulletin-form .form-group label {
  font-size: 0.8em;
  margin-bottom: 3px;
}

.edit-sub-bulletin-form .form-group input,
.edit-sub-bulletin-form .form-group textarea {
  padding: 5px;
  font-size: 0.8em;
}

.edit-sub-bulletin-form .form-actions {
  margin-top: 12px;
  gap: 8px;
}

.edit-sub-bulletin-form .cancel-btn,
.edit-sub-bulletin-form .save-btn {
  padding: 6px 12px;
  font-size: 0.8em;
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

  .sub-test-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .sub-test-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .add-sub-test-form,
  .edit-sub-test-form {
    padding: 20px;
  }

  .sub-tests-section {
    padding: 20px;
  }

  .bulletins-section {
    padding: 15px;
  }

  .bulletin-form-item.sub-bulletin {
    margin-left: 10px;
  }

  .bulletin-form-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .sub-bulletins-list {
    margin-left: 10px;
  }

  .bulletin-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .bulletin-actions {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
