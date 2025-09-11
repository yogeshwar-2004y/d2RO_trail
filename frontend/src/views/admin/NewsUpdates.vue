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
           <!-- Filter Tabs -->
           <div class="filter-tabs">
             <button 
               @click="setNewsFilter('all')" 
               :class="['filter-tab', { active: newsFilter === 'all' }]"
             >
               All News ({{ allNews.length }})
             </button>
             <button 
               @click="setNewsFilter('active')" 
               :class="['filter-tab', { active: newsFilter === 'active' }]"
             >
               Active ({{ activeNewsCount }})
             </button>
             <button 
               @click="setNewsFilter('expired')" 
               :class="['filter-tab', { active: newsFilter === 'expired' }]"
             >
               Expired ({{ expiredNewsCount }})
             </button>
             <button 
               @click="setNewsFilter('hidden')" 
               :class="['filter-tab', { active: newsFilter === 'hidden' }]"
             >
               Hidden ({{ hiddenNewsCount }})
             </button>
           </div>
           
           <div v-if="loadingAllNews" class="loading-container">
             <div class="loading-spinner"></div>
             <p>Loading all news...</p>
           </div>
           
           <div v-else-if="filteredNews.length === 0" class="no-data-message">
             <p v-if="allNews.length === 0">No news updates found in the database.</p>
             <p v-else>No {{ newsFilter }} news items found.</p>
           </div>
           
           <div v-else class="news-list modal-news-list">
             <div v-for="news in filteredNews" :key="news.id" class="news-card enhanced-news-card">
               <div class="news-card-header">
                 <div class="news-info">
                   <span class="news-title">News Update</span>
                   <span v-if="isNewsExpired(news)" class="news-status expired">Expired</span>
                   <span v-else-if="news.hidden" class="news-status hidden">Hidden</span>
                   <span v-else class="news-status active">Active</span>
                 </div>
                 <div class="news-actions">
                   <button 
                     v-if="isNewsExpired(news) || news.hidden" 
                     @click="repostNewsItem(news.id)" 
                     class="btn btn-repost-small"
                     :disabled="reposting"
                   >
                     <svg v-if="!reposting" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                       <polyline points="23,4 23,10 17,10"></polyline>
                       <polyline points="1,20 1,14 7,14"></polyline>
                       <path d="M20.49,9A9,9,0,0,0,5.64,5.64L1,10m22,4L18.36,18.36A9,9,0,0,1,3.51,15"></path>
                     </svg>
                     <div v-if="reposting" class="loading-spinner-small"></div>
                     Repost
                   </button>
                   <button @click="permanentlyDeleteNewsItem(news.id)" class="btn btn-delete-small">
                     <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                       <polyline points="3,6 5,6 21,6"></polyline>
                       <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                     </svg>
                   </button>
                 </div>
               </div>
               <div class="news-content">
                 {{ news.news_text }}
               </div>
               <div class="news-meta">
                 <div class="meta-row">
                   <span class="meta-label">Created:</span>
                   <span class="meta-value">{{ formatDateTime(news.created_at) }}</span>
                 </div>
                 <div v-if="news.updated_at && news.updated_at !== news.created_at" class="meta-row">
                   <span class="meta-label">Last Updated:</span>
                   <span class="meta-value">{{ formatDateTime(news.updated_at) }}</span>
                 </div>
                 <div class="meta-row">
                   <span class="meta-label">Status:</span>
                   <span class="meta-value status-indicator">
                     <span v-if="isNewsActive(news)" class="status-dot active"></span>
                     <span v-else-if="isNewsExpired(news)" class="status-dot expired"></span>
                     <span v-else-if="news.hidden" class="status-dot hidden"></span>
                     {{ getNewsStatusText(news) }}
                   </span>
                 </div>
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
       reposting: false,
       loadingNews: false,
       loadingAllNews: false,
       showManageModal: false,
       newsFilter: 'all',
       nextId: 1
     };
   },
  computed: {
    recentNews() {
      const twentyFourHoursAgo = new Date();
      twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24);
      
      return this.existingNews.filter(news => {
        const newsDate = new Date(news.updated_at || news.created_at);
        return newsDate >= twentyFourHoursAgo && !news.hidden;
      });
    },
    
    filteredNews() {
      if (this.newsFilter === 'all') {
        return this.allNews;
      } else if (this.newsFilter === 'active') {
        return this.allNews.filter(news => this.isNewsActive(news));
      } else if (this.newsFilter === 'expired') {
        return this.allNews.filter(news => this.isNewsExpired(news));
      } else if (this.newsFilter === 'hidden') {
        return this.allNews.filter(news => news.hidden);
      }
      return this.allNews;
    },
    
    activeNewsCount() {
      return this.allNews.filter(news => this.isNewsActive(news)).length;
    },
    
    expiredNewsCount() {
      return this.allNews.filter(news => this.isNewsExpired(news)).length;
    },
    
    hiddenNewsCount() {
      return this.allNews.filter(news => news.hidden).length;
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
       if (!confirm('Are you sure you want to hide this news item from the frontend? It will remain stored in the database.')) {
         return;
       }
       
       try {
         const response = await fetch(`http://localhost:5000/api/news/${newsId}`, {
           method: 'DELETE'
         });
         
         const data = await response.json();
         
         if (data.success) {
           this.existingNews = this.existingNews.filter(news => news.id !== newsId);
           alert('News item hidden successfully!');
         } else {
           throw new Error(data.message);
         }
       } catch (error) {
         console.error('Error hiding news item:', error);
         alert('Error hiding news item: ' + error.message);
       }
     },
     
     async permanentlyDeleteNewsItem(newsId) {
       if (!confirm('Are you sure you want to PERMANENTLY DELETE this news item? This action cannot be undone.')) {
         return;
       }
       
       try {
         const response = await fetch(`http://localhost:5000/api/news/${newsId}/permanent`, {
           method: 'DELETE'
         });
         
         const data = await response.json();
         
         if (data.success) {
           this.existingNews = this.existingNews.filter(news => news.id !== newsId);
           this.allNews = this.allNews.filter(news => news.id !== newsId);
           alert('News item permanently deleted!');
         } else {
           throw new Error(data.message);
         }
       } catch (error) {
         console.error('Error permanently deleting news item:', error);
         alert('Error permanently deleting news item: ' + error.message);
       }
     },
     
     async repostNewsItem(newsId) {
       if (!confirm('Are you sure you want to repost this news item? It will be visible for another 24 hours.')) {
         return;
       }
       
       this.reposting = true;
       try {
         const response = await fetch(`http://localhost:5000/api/news/${newsId}/repost`, {
           method: 'PUT'
         });
         
         const data = await response.json();
         
         if (data.success) {
           alert('News item reposted successfully!');
           await this.loadExistingNews();
           await this.loadAllNews();
         } else {
           throw new Error(data.message);
         }
       } catch (error) {
         console.error('Error reposting news item:', error);
         alert('Error reposting news item: ' + error.message);
       } finally {
         this.reposting = false;
       }
     },
     
     isNewsExpired(news) {
       if (!news.updated_at) return false;
       const twentyFourHoursAgo = new Date();
       twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24);
       const newsDate = new Date(news.updated_at);
       return newsDate < twentyFourHoursAgo && !news.hidden;
     },
     
     isNewsActive(news) {
       if (news.hidden) return false;
       if (!news.updated_at) return false;
       const twentyFourHoursAgo = new Date();
       twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24);
       const newsDate = new Date(news.updated_at);
       return newsDate >= twentyFourHoursAgo;
     },
     
     setNewsFilter(filter) {
       this.newsFilter = filter;
     },
     
     getNewsStatusText(news) {
       if (news.hidden) return 'Hidden';
       if (this.isNewsActive(news)) return 'Active';
       if (this.isNewsExpired(news)) return 'Expired';
       return 'Inactive';
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
       this.newsFilter = 'all'; // Reset filter when closing modal
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
       if (!confirm('Are you sure you want to PERMANENTLY DELETE ALL news records? This action cannot be undone.')) {
         return;
       }
       
       this.deleting = true;
       try {
         const response = await fetch('http://localhost:5000/api/news/permanent/all', {
           method: 'DELETE'
         });
         
         const data = await response.json();
         
         if (data.success) {
           alert('All news records permanently deleted!');
           this.allNews = [];
           this.existingNews = [];
           this.closeManageNewsModal();
         } else {
           throw new Error(data.message);
         }
       } catch (error) {
         console.error('Error permanently deleting all news:', error);
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
 
 .btn-repost-small {
   background: #28a745;
   color: white;
   padding: 8px 12px;
   border-radius: 6px;
   margin-right: 8px;
 }
 
 .btn-repost-small:hover:not(:disabled) {
   background: #218838;
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
  gap: 8px;
}

.news-title {
  font-weight: 600;
  color: #495057;
  font-size: 1.1em;
}

.news-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  font-weight: 600;
  text-transform: uppercase;
  width: fit-content;
}

.news-status.active {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.news-status.expired {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.news-status.hidden {
  background-color: #e2e3e5;
  color: #383d41;
  border: 1px solid #d6d8db;
}

.news-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading-spinner-small {
  width: 12px;
  height: 12px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.news-content {
  margin-bottom: 15px;
  line-height: 1.6;
  color: #495057;
}

.news-meta {
  font-size: 0.85em;
  color: #6c757d;
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e9ecef;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-label {
  font-weight: 600;
  color: #495057;
  min-width: 120px;
}

.meta-value {
  text-align: right;
  flex: 1;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot.active {
  background-color: #28a745;
  box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.3);
}

.status-dot.expired {
  background-color: #dc3545;
  box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.3);
}

.status-dot.hidden {
  background-color: #6c757d;
  box-shadow: 0 0 0 2px rgba(108, 117, 125, 0.3);
}

.enhanced-news-card {
  border-left: 4px solid #e9ecef;
  transition: all 0.3s ease;
}

.enhanced-news-card:hover {
  border-left-color: #007bff;
  transform: translateX(4px);
}

/* Filter Tabs */
.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.filter-tab {
  padding: 12px 16px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #6c757d;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  white-space: nowrap;
}

.filter-tab:hover {
  background: #e9ecef;
  color: #495057;
}

.filter-tab.active {
  background: #007bff;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
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
  
  /* Responsive Filter Tabs */
  .filter-tabs {
    flex-wrap: wrap;
    gap: 6px;
  }
  
  .filter-tab {
    padding: 10px 12px;
    font-size: 13px;
    flex: 1;
    min-width: calc(50% - 3px);
  }
  
  /* Responsive News Cards */
  .meta-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .meta-label {
    min-width: auto;
  }
  
  .meta-value {
    text-align: left;
  }
  
  .news-actions {
    flex-direction: column;
    gap: 8px;
    width: 100%;
  }
  
  .btn-repost-small {
    margin-right: 0;
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
