// Background sync service for tech support requests
class TechSupportSyncService {
  constructor() {
    this.isOnline = navigator.onLine;
    this.syncInterval = null;
    this.setupEventListeners();
    this.startSync();
  }

  setupEventListeners() {
    // Listen for online/offline events
    window.addEventListener("online", () => {
      console.log("Back online - starting sync");
      this.isOnline = true;
      this.syncOfflineRequests();
    });

    window.addEventListener("offline", () => {
      console.log("Gone offline");
      this.isOnline = false;
    });
  }

  startSync() {
    // Check for offline requests every 30 seconds
    this.syncInterval = setInterval(() => {
      if (this.isOnline) {
        this.syncOfflineRequests();
      }
    }, 30000);
  }

  async syncOfflineRequests() {
    try {
      const offlineRequests = JSON.parse(
        localStorage.getItem("tech_support_offline") || "[]"
      );

      if (offlineRequests.length === 0) {
        return;
      }

      console.log(`Found ${offlineRequests.length} offline requests to sync`);

      const successfulSubmissions = [];

      for (const request of offlineRequests) {
        try {
          // Prepare data for backend
          const requestData = {
            username: request.username,
            userId: request.userId,
            date: request.date,
            issue: request.issue,
          };

          const response = await fetch(
            "http://127.0.0.1:5000/api/tech-support",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(requestData),
              mode: "cors",
            }
          );

          const data = await response.json();

          if (data.success) {
            if (data.duplicate) {
              console.log(`Request ${request.id} was already submitted (ID: ${data.existing_request_id})`);
              // Still consider it successful and remove from offline
              successfulSubmissions.push(request.id);
            } else {
              console.log(`Successfully synced request ${request.id}`);
              successfulSubmissions.push(request.id);
            }
          } else {
            console.log(`Failed to sync request ${request.id}:`, data.message);
            // Increment attempt counter
            request.submission_attempts =
              (request.submission_attempts || 0) + 1;
          }
        } catch (error) {
          console.log(`Error syncing request ${request.id}:`, error.message);
          // Increment attempt counter
          request.submission_attempts = (request.submission_attempts || 0) + 1;
        }
      }

      // Remove successfully submitted requests
      const remainingRequests = offlineRequests.filter(
        (request) => !successfulSubmissions.includes(request.id)
      );

      // Remove requests that have failed too many times (more than 10 attempts)
      const finalRequests = remainingRequests.filter(
        (request) => (request.submission_attempts || 0) < 10
      );

      // Update localStorage
      localStorage.setItem(
        "tech_support_offline",
        JSON.stringify(finalRequests)
      );

      if (successfulSubmissions.length > 0) {
        console.log(
          `Successfully synced ${successfulSubmissions.length} requests`
        );
      }
    } catch (error) {
      console.error("Error during sync:", error);
    }
  }

  stopSync() {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }
}

// Initialize the sync service
const techSupportSync = new TechSupportSyncService();

// Export for use in other components if needed
export default techSupportSync;
