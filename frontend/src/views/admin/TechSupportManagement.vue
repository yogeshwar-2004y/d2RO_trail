<template>
  <div class="tech-support-management">
    <div class="page-header">
      <h1>Tech Support Management</h1>
      <p>Manage and respond to technical support requests</p>
    </div>

    <div class="filters-section">
      <div class="filter-group">
        <label for="statusFilter">Filter by Status:</label>
        <select id="statusFilter" v-model="statusFilter" @change="filterRequests">
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
        </select>
      </div>
      <div class="filter-group">
        <label for="searchInput">Search:</label>
        <input 
          id="searchInput" 
          type="text" 
          v-model="searchQuery" 
          @input="filterRequests"
          placeholder="Search by username or issue..."
        />
      </div>
    </div>

    <div class="requests-container">
      <div v-if="loading" class="loading">
        <p>Loading tech support requests...</p>
      </div>
      
      <div v-else-if="filteredRequests.length === 0" class="no-requests">
        <p>No tech support requests found.</p>
      </div>
      
      <div v-else class="requests-list">
        <div 
          v-for="request in filteredRequests" 
          :key="request.id" 
          class="request-card"
          :class="getStatusClass(request.status)"
        >
          <div class="request-header">
            <div class="request-info">
              <h3>{{ request.username }} (ID: {{ request.user_id }})</h3>
              <div class="date-info">
                <span class="submitted-date">
                  <strong>Submitted:</strong> {{ formatDateTime(request.created_at) }}
                </span>
                <span v-if="request.updated_at && request.updated_at !== request.created_at" class="updated-date">
                  <strong>Last Updated:</strong> {{ formatDateTime(request.updated_at) }}
                </span>
                <span v-if="request.status_updated_at && request.status_updated_at !== request.created_at" class="status-updated-info">
                  <strong>Status Updated:</strong> {{ formatDateTime(request.status_updated_at) }}
                  <span v-if="request.status_updated_by" class="updated-by">
                    by User ID {{ request.status_updated_by }}
                  </span>
                </span>
              </div>
            </div>
            <div class="request-status">
              <span class="status-badge" :class="request.status">{{ request.status.toUpperCase() }}</span>
            </div>
          </div>
          
          <div class="request-content">
            <div class="issue-date">
              <strong>Issue Date (User Specified):</strong> {{ formatDateOnly(request.issue_date) }}
            </div>
            <div class="issue-description">
              <strong>Issue Description:</strong>
              <p>{{ request.issue_description }}</p>
            </div>
          </div>
          
          <div class="request-actions">
            <select 
              v-model="request.status" 
              @change="updateStatus(request.id, request.status)"
              class="status-select"
            >
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { currentUser } from '@/stores/userStore'

export default {
  name: "TechSupportManagement",
  data() {
    return {
      requests: [],
      filteredRequests: [],
      loading: true,
      statusFilter: "",
      searchQuery: ""
    };
  },
  async mounted() {
    // Initialize user store if not already done
    const { initializeUser } = await import('@/stores/userStore');
    initializeUser();
    await this.loadRequests();
  },
  methods: {
    async loadRequests() {
      try {
        this.loading = true;
        const response = await fetch("http://127.0.0.1:5000/api/tech-support");
        const data = await response.json();
        
        if (data.success) {
          this.requests = data.requests;
          this.filteredRequests = [...this.requests];
        } else {
          console.error("Failed to load requests:", data.message);
        }
      } catch (error) {
        console.error("Error loading requests:", error);
      } finally {
        this.loading = false;
      }
    },

    async updateStatus(requestId, newStatus) {
      try {
        // Get current admin user ID
        const currentAdmin = currentUser();
        console.log("Current admin user:", currentAdmin); // Debug log
        
        // Try to get user ID from different possible field names
        const adminUserId = currentAdmin?.id || currentAdmin?.user_id || currentAdmin?.userId;
        
        if (!currentAdmin || !adminUserId) {
          console.error("User object structure:", currentAdmin);
          alert("Unable to identify admin user. Please refresh the page and try again.");
          return;
        }

        const response = await fetch(`http://127.0.0.1:5000/api/tech-support/${requestId}/status`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ 
            status: newStatus,
            admin_user_id: adminUserId
          }),
          mode: "cors",
        });

        const data = await response.json();
        console.log("Status update response:", data); // Debug log
        
        if (data.success) {
          // Update the local request status
          const request = this.requests.find(r => r.id === requestId);
          if (request) {
            request.status = newStatus;
            request.status_updated_by = adminUserId;
            request.status_updated_at = new Date().toISOString();
            request.updated_at = new Date().toISOString();
          }
          this.filterRequests();
        } else {
          alert("Failed to update status: " + data.message);
        }
      } catch (error) {
        console.error("Error updating status:", error);
        alert("Error updating status. Please try again.");
      }
    },

    filterRequests() {
      let filtered = [...this.requests];

      // Filter by status
      if (this.statusFilter) {
        filtered = filtered.filter(request => request.status === this.statusFilter);
      }

      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(request => 
          request.username.toLowerCase().includes(query) ||
          request.issue_description.toLowerCase().includes(query)
        );
      }

      this.filteredRequests = filtered;
    },

    formatDateTime(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      // Use local timezone for display
      const formatted = date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      });
      // Add timezone info
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      return `${formatted} (${timezone})`;
    },

    formatDateOnly(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      // Format as date only (user-specified issue date)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    },

    getStatusClass(status) {
      return `status-${status}`;
    }
  }
};
</script>

<style scoped>
.tech-support-management {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  color: #162845;
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.page-header p {
  color: #666;
  font-size: 1.1rem;
}

.filters-section {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-weight: bold;
  color: #162845;
}

.filter-group select,
.filter-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.requests-container {
  min-height: 400px;
}

.loading, .no-requests {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1rem;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.request-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #ddd;
  transition: all 0.3s ease;
}

.request-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.request-card.status-pending {
  border-left-color: #ffc107;
}

.request-card.status-in_progress {
  border-left-color: #17a2b8;
}

.request-card.status-resolved {
  border-left-color: #28a745;
}

.request-card.status-closed {
  border-left-color: #6c757d;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.request-info h3 {
  margin: 0 0 10px 0;
  color: #162845;
  font-size: 1.2rem;
}

.date-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.submitted-date,
.updated-date {
  color: #666;
  font-size: 0.9rem;
}

.submitted-date strong,
.updated-date strong {
  color: #162845;
}

.updated-date {
  font-style: italic;
  color: #888;
}

.status-updated-info {
  color: #666;
  font-size: 0.9rem;
  background: #e8f4fd;
  padding: 4px 8px;
  border-radius: 4px;
  border-left: 3px solid #17a2b8;
}

.status-updated-info strong {
  color: #17a2b8;
}

.updated-by {
  font-style: italic;
  color: #555;
  margin-left: 5px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.in_progress {
  background: #d1ecf1;
  color: #0c5460;
}

.status-badge.resolved {
  background: #d4edda;
  color: #155724;
}

.status-badge.closed {
  background: #e2e3e5;
  color: #383d41;
}

.request-content {
  margin-bottom: 15px;
}

.issue-date {
  margin-bottom: 10px;
  color: #666;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 5px;
  border-left: 3px solid #162845;
}

.issue-date strong {
  color: #162845;
}

.issue-description {
  color: #333;
}

.issue-description p {
  margin: 5px 0 0 0;
  line-height: 1.5;
  white-space: pre-wrap;
}

.request-actions {
  display: flex;
  justify-content: flex-end;
}

.status-select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: #fff;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
    gap: 15px;
  }
  
  .request-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .request-actions {
    justify-content: flex-start;
  }
}
</style>
