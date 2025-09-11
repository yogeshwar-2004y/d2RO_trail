<template>
  <div class="news-updates-page">
    <!-- Header -->
    <div class="header">
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
      <span class="page-title">NEWS UPDATES</span>
      <button @click="openManageNewsModal" class="btn btn-manage">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
        </svg>
        Manage News
      </button>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- News Form -->
      <div class="news-form-section">
        <div class="form-header">
          <h2>Add News Updates</h2>
          <div class="form-actions">
            <button @click="addNewsItem" class="btn btn-add">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
              Add News Text
            </button>
            <button @click="saveAllNews" class="btn btn-save" :disabled="newsItems.length === 0 || saving">
              <svg v-if="!saving" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                <polyline points="17,21 17,13 7,13 7,21"></polyline>
                <polyline points="7,3 7,8 15,8"></polyline>
              </svg>
              <div v-if="saving" class="loading-spinner"></div>
              {{ saving ? 'Saving...' : 'Save All News' }}
            </button>
          </div>
        </div>

        <!-- News Items Form -->
        <div class="news-items-container">
          <div v-if="newsItems.length === 0" class="no-news-message">
            <p>No news items added yet. Click "Add News Text" to start adding news.</p>
          </div>
          
          <div v-for="(item, index) in newsItems" :key="item.id" class="news-item-form">
            <div class="news-item-header">
              <h3>News Item {{ index + 1 }}</h3>
              <button @click="removeNewsItem(index)" class="btn btn-delete-small">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3,6 5,6 21,6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
            
            
            <div class="form-group">
              <label>News Text *</label>
              <textarea 
                v-model="item.newsText" 
                class="form-textarea"
                placeholder="Enter news content..."
                rows="4"
                required
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- Existing News List -->
      <div class="existing-news-section">
        <div class="section-header">
          <h2>Recent News Updates (Last 24 Hours)</h2>
          <button 
            @click="deleteAllNews" 
            class="btn btn-delete-all" 
            :disabled="recentNews.length === 0 || deleting"
            v-if="recentNews.length > 0"
          >
            <svg v-if="!deleting" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3,6 5,6 21,6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
            <div v-if="deleting" class="loading-spinner"></div>
            {{ deleting ? 'Deleting...' : 'Delete All Records' }}
          </button>
        </div>

        <div v-if="loadingNews" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading news...</p>
        </div>

        <div v-else-if="recentNews.length === 0" class="no-data-message">
          <p>No news updates found in the last 24 hours.</p>
        </div>

        <div v-else class="news-list">
          <div v-for="news in recentNews" :key="news.id" class="news-card">
            <div class="news-card-header">
              <div class="news-info">
                <span class="news-title">News Update</span>
              </div>
              <button @click="deleteNewsItem(news.id)" class="btn btn-delete-small">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3,6 5,6 21,6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
            <div class="news-content">
              {{ news.news_text }}
            </div>
            <div class="news-meta">
              Created: {{ formatDateTime(news.created_at) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Manage News Modal -->
    <div v-if="showManageModal" class="modal-overlay" @click="closeManageNewsModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Manage All News</h2>
          <button @click="closeManageNewsModal" class="btn-close">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div v-if="loadingAllNews" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading all news...</p>
          </div>
          
          <div v-else-if="allNews.length === 0" class="no-data-message">
            <p>No news updates found in the database.</p>
          </div>
          
          <div v-else class="news-list modal-news-list">
            <div v-for="news in allNews" :key="news.id" class="news-card">
              <div class="news-card-header">
                <div class="news-info">
                  <span class="news-title">News Update</span>
                </div>
                <button @click="deleteNewsItem(news.id)" class="btn btn-delete-small">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="3,6 5,6 21,6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
              <div class="news-content">
                {{ news.news_text }}
              </div>
              <div class="news-meta">
                Created: {{ formatDateTime(news.created_at) }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button 
            @click="deleteAllNewsFromModal" 
            class="btn btn-delete-all" 
            :disabled="allNews.length === 0 || deleting"
            v-if="allNews.length > 0"
          >
            <svg v-if="!deleting" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3,6 5,6 21,6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
            <div v-if="deleting" class="loading-spinner"></div>
            {{ deleting ? 'Deleting...' : 'Delete All News' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NewsUpdates',
  data() {
    return {
      newsItems: [],
      existingNews: [],
      allNews: [],
      saving: false,
      deleting: false,
      loadingNews: false,
      loadingAllNews: false,
      showManageModal: false,
      nextId: 1
    };
  },
  computed: {
    recentNews() {
      const twentyFourHoursAgo = new Date();
      twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24);
      
      return this.existingNews.filter(news => {
        const newsDate = new Date(news.created_at);
        return newsDate >= twentyFourHoursAgo;
      });
    }
  },
  mounted() {
    this.loadExistingNews();
  },
  methods: {
    addNewsItem() {
      const newItem = {
        id: this.nextId++,
        newsText: ''
      };
      this.newsItems.push(newItem);
    },
    
    removeNewsItem(index) {
      this.newsItems.splice(index, 1);
    },
    
    async saveAllNews() {
      if (this.newsItems.length === 0) {
        alert('Please add at least one news item');
        return;
      }
      
      // Validate required fields
      for (let i = 0; i < this.newsItems.length; i++) {
        const item = this.newsItems[i];
        if (!item.newsText.trim()) {
          alert(`Please enter news text for News Item ${i + 1}`);
          return;
        }
      }
      
      this.saving = true;
      try {
        const response = await fetch('http://localhost:5000/api/news', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            news_items: this.newsItems.map(item => ({
              news_text: item.newsText
            }))
          })
        });
        
        const data = await response.json();
        
        if (data.success) {
          alert('News updates saved successfully!');
          this.newsItems = [];
          this.nextId = 1;
          await this.loadExistingNews();
        } else {
          throw new Error(data.message);
        }
      } catch (error) {
        console.error('Error saving news:', error);
        alert('Error saving news updates: ' + error.message);
      } finally {
        this.saving = false;
      }
    },
    
    async loadExistingNews() {
      this.loadingNews = true;
      try {
        const response = await fetch('http://localhost:5000/api/news');
        const data = await response.json();
        
        if (data.success) {
          this.existingNews = data.news;
        } else {
          console.error('Error loading news:', data.message);
        }
      } catch (error) {
        console.error('Error loading news:', error);
      } finally {
        this.loadingNews = false;
      }
    },
    
    async deleteAllNews() {
      if (!confirm('Are you sure you want to delete ALL news records? This action cannot be undone.')) {
        return;
      }
      
      this.deleting = true;
      try {
        const response = await fetch('http://localhost:5000/api/news/all', {
          method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
          alert('All news records deleted successfully!');
          this.existingNews = [];
        } else {
          throw new Error(data.message);
        }
      } catch (error) {
        console.error('Error deleting all news:', error);
        alert('Error deleting news records: ' + error.message);
      } finally {
        this.deleting = false;
      }
    },
    
    async deleteNewsItem(newsId) {
      if (!confirm('Are you sure you want to delete this news item?')) {
        return;
      }
      
      try {
        const response = await fetch(`http://localhost:5000/api/news/${newsId}`, {
          method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
          this.existingNews = this.existingNews.filter(news => news.id !== newsId);
          this.allNews = this.allNews.filter(news => news.id !== newsId);
          alert('News item deleted successfully!');
        } else {
          throw new Error(data.message);
        }
      } catch (error) {
        console.error('Error deleting news item:', error);
        alert('Error deleting news item: ' + error.message);
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '';
      const date = new Date(dateTimeString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    async openManageNewsModal() {
      this.showManageModal = true;
      await this.loadAllNews();
    },
    
    closeManageNewsModal() {
      this.showManageModal = false;
    },
    
    async loadAllNews() {
      this.loadingAllNews = true;
      try {
        const response = await fetch('http://localhost:5000/api/news');
        const data = await response.json();
        
        if (data.success) {
          this.allNews = data.news;
        } else {
          console.error('Error loading all news:', data.message);
        }
      } catch (error) {
        console.error('Error loading all news:', error);
      } finally {
        this.loadingAllNews = false;
      }
    },
    
    async deleteAllNewsFromModal() {
      if (!confirm('Are you sure you want to delete ALL news records? This action cannot be undone.')) {
        return;
      }
      
      this.deleting = true;
      try {
        const response = await fetch('http://localhost:5000/api/news/all', {
          method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
          alert('All news records deleted successfully!');
          this.allNews = [];
          this.existingNews = [];
          this.closeManageNewsModal();
        } else {
          throw new Error(data.message);
        }
      } catch (error) {
        console.error('Error deleting all news:', error);
        alert('Error deleting news records: ' + error.message);
      } finally {
        this.deleting = false;
      }
    }
  }
};
</script>

<style scoped>
.news-updates-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 30px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  gap: 20px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #f0f0f0;
}

.logos-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo {
  width: 150px;
}

.vista-logo {
  width: 120px;
}

.page-title {
  font-size: 1.8em;
  font-weight: bold;
  color: #333;
  flex-grow: 1;
  text-align: center;
}

.btn-manage {
  background: #17a2b8;
  color: white;
}

.btn-manage:hover:not(:disabled) {
  background: #138496;
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

/* Form Section */
.news-form-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.form-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5em;
}

.form-actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 14px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-add {
  background: #28a745;
  color: white;
}

.btn-add:hover:not(:disabled) {
  background: #218838;
}

.btn-save {
  background: #007bff;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #0056b3;
}

.btn-delete-all {
  background: #dc3545;
  color: white;
}

.btn-delete-all:hover:not(:disabled) {
  background: #c82333;
}

.btn-delete-small {
  background: #dc3545;
  color: white;
  padding: 8px;
  border-radius: 6px;
}

.btn-delete-small:hover {
  background: #c82333;
}

/* News Items */
.news-items-container {
  max-height: 600px;
  overflow-y: auto;
}

.no-news-message {
  text-align: center;
  padding: 40px;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.news-item-form {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 25px;
  margin-bottom: 25px;
  background: #fafafa;
}

.news-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.news-item-header h3 {
  margin: 0;
  color: #495057;
  font-size: 1.2em;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 8px;
  color: #495057;
}

.form-input, .form-textarea {
  padding: 12px;
  border: 2px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #007bff;
}

.form-input[readonly] {
  background-color: #e9ecef;
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

/* Existing News Section */
.existing-news-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.section-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5em;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  color: #666;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-data-message {
  text-align: center;
  padding: 40px;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
}

.news-list {
  max-height: 600px;
  overflow-y: auto;
}

.news-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  background: #fafafa;
  transition: box-shadow 0.3s ease;
}

.news-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.news-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.news-info {
  display: flex;
  flex-direction: column;
}

.news-title {
  font-weight: 600;
  color: #495057;
  font-size: 1.1em;
}

.news-content {
  margin-bottom: 15px;
  line-height: 1.6;
  color: #495057;
}

.news-meta {
  font-size: 0.8em;
  color: #6c757d;
  font-style: italic;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5em;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.btn-close:hover {
  background-color: #f8f9fa;
}

.modal-body {
  padding: 30px;
  flex-grow: 1;
  overflow-y: auto;
}

.modal-news-list {
  max-height: 400px;
  overflow-y: auto;
}

.modal-footer {
  padding: 20px 30px;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-end;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 30px;
    padding: 20px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .form-actions {
    justify-content: center;
  }
  
  /* Responsive Modal */
  .modal-content {
    width: 95%;
    max-height: 90vh;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 15px 20px;
  }
}
</style>
