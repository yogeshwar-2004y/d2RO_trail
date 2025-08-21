<template>
  <div class="main-container">
    <header class="app-header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg class="back-icon" viewBox="0 0 24 24">
            <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
          </svg>
        </button>
        <img src="https://placehold.co/150x50/333/fff?text=AVIA+TRAX+LOGO" alt="Aviatrax Logo" class="logo">
      </div>
      <div class="header-title">UPDATE PROJECT</div>
    </header>

    <div class="card">
      <div class="form-grid">
        <div class="form-row">
          <label class="form-label">PROJECT NAME</label>
          <div class="form-input-container">
            <input type="text" class="form-input" value="ERP QA Automation Tool" disabled>
            <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
               <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
        </div>
        <div class="form-row">
          <label class="form-label">PROJECT NUMBER</label>
          <div class="form-input-container">
            <input type="text" class="form-input" value="PRJ-2025-078" disabled>
            <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
               <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
        </div>
        <div class="form-row">
          <label class="form-label">PROJECT DATE</label>
          <div class="form-input-container">
            <input type="date" class="form-input" value="2025-07-01" disabled>
            <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
               <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
        </div>
        <div class="form-row">
          <label class="form-label">LRU</label>
          <div class="form-input-container">
            <input type="text" class="form-input" value="">
            <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
               <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
        </div>
        <div class="form-row">
          <label class="form-label">SL NOS</label>
          <div class="form-input-container">
            <input type="text" class="form-input" value="">
            <svg class="input-icon" viewBox="0 0 24 24" fill="currentColor">
               <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <div class="button-container">
      <button class="action-button update-button">UPDATE PROJECT</button>
      <button class="action-button delete-button">DELETE PROJECT</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UpdateProjects',
  // You would add your data properties here to manage form inputs
  data() {
    return {
      projectName: 'ERP QA Automation Tool',
      projectNumber: 'PRJ-2025-078',
      projectDate: '2025-07-01',
      lru: '',
      slNos: '',
    };
  },
  // You would add your methods here to handle button clicks and form submission
  methods: {
    updateProject() {
      // Logic for updating the project
      console.log('Updated project!');
    },
    deleteProject() {
      // Logic for deleting the project
      console.log('Deleted project!');
    },
  },
};
</script>

<style scoped>
/* General body and container styles */
.main-container {
    width: 100%;
    max-width: 900px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f0f2f5;
    color: #333;
    padding: 20px;
    min-height: 100vh;
    box-sizing: border-box;
}

/* Header styles */
.app-header {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 15px;
}

.back-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
}

.back-icon {
    width: 24px;
    height: 24px;
    fill: #666;
    transition: fill 0.3s;
}

.back-button:hover .back-icon {
    fill: #000;
}

.logo {
    height: 30px;
}

.header-title {
    font-size: 24px;
    font-weight: bold;
    text-transform: uppercase;
    text-align: center;
    flex-grow: 1;
}

/* Card container and form grid */
.card {
    width: 100%;
    background-color: #fff;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 40px;
    margin-bottom: 20px;
    box-sizing: border-box;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 20px;
    align-items: center;
}

.form-row {
    display: contents;
}

.form-label {
    font-weight: bold;
    color: #555;
    font-size: 14px;
    text-align: right;
    padding-right: 20px;
}

.form-input-container {
    position: relative;
}

.form-input {
    width: calc(100% - 30px);
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 14px;
    background-color: #f9f9f9;
    box-sizing: border-box;
}

.form-input:disabled {
    background-color: #e9e9e9;
    color: #888;
    cursor: not-allowed;
}

.input-icon {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    fill: #888;
}

/* Button styles */
.button-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    width: 100%;
    max-width: 600px;
    margin-top: 20px;
}

.action-button {
    padding: 12px 25px;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    flex-grow: 1;
}

.update-button {
    background: linear-gradient(145deg, #f0f0f0, #dcdcdc);
    color: #555;
}

.update-button:hover {
     transform: translateY(-2px);
     box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

.delete-button {
    background: linear-gradient(145deg, #ff6b6b, #ff4d4d);
    color: white;
}

.delete-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

/* Responsive Media Queries */
@media (max-width: 768px) {
    .app-header {
        flex-direction: column;
        align-items: center;
        gap: 15px;
    }

    .header-left {
        width: 100%;
        justify-content: space-between;
    }

    .header-title {
        margin-top: 10px;
    }

    .card {
        padding: 20px;
    }

    .form-grid {
        grid-template-columns: 1fr;
        gap: 15px;
    }

    .form-label {
        text-align: left;
        padding-right: 0;
    }

    .form-input {
        width: 100%;
    }

    .form-input-container {
         width: 100%;
    }

    .button-container {
        flex-direction: column;
    }
}
</style>
