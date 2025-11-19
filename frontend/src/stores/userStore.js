// Global user state management
import { reactive } from "vue";

// Create reactive global state
const state = reactive({
  user: null,
  isLoggedIn: false,
  currentUserRole: null,
  roleName: null,
  statusCheckInterval: null, // Store interval ID for periodic status checks
});

// Helper functions for status checking (defined before actions to avoid circular reference)
const stopStatusCheck = () => {
  if (state.statusCheckInterval) {
    clearInterval(state.statusCheckInterval);
    state.statusCheckInterval = null;
  }
};

// Actions (will be fully defined after the object is created)
let actions = {
  // Set user data after successful login
  setUser(userData) {
    state.user = userData;
    state.isLoggedIn = true;
    state.currentUserRole = userData.role_id;
    state.roleName = userData.role;

    // Store in localStorage for persistence
    localStorage.setItem("user", JSON.stringify(userData));
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("currentUserRole", userData.role_id);
    localStorage.setItem("roleName", userData.role);

    console.log("User set:", userData);
    console.log("Current role ID:", state.currentUserRole);
    console.log("Role name:", state.roleName);
    
    // Start periodic status check
    actions.startStatusCheck();
  },

  // Clear user data on logout
  clearUser() {
    // Stop periodic status check
    stopStatusCheck();
    
    state.user = null;
    state.isLoggedIn = false;
    state.currentUserRole = null;
    state.roleName = null;

    // Clear localStorage
    localStorage.removeItem("user");
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("currentUserRole");
    localStorage.removeItem("roleName");
  },

  // Initialize user from localStorage (for page refresh)
  initializeUser() {
    const storedUser = localStorage.getItem("user");
    const storedIsLoggedIn = localStorage.getItem("isLoggedIn");
    const storedRole = localStorage.getItem("currentUserRole");
    const storedRoleName = localStorage.getItem("roleName");

    if (storedUser && storedIsLoggedIn === "true") {
      state.user = JSON.parse(storedUser);
      state.isLoggedIn = true;
      state.currentUserRole = parseInt(storedRole);
      state.roleName = storedRoleName;

      console.log("User initialized from storage:", state.user);
      console.log("Current role ID:", state.currentUserRole);
      console.log("Role name:", state.roleName);
      
      // Start periodic status check for restored session
      actions.startStatusCheck();
    }
  },

  // Get current user role
  getCurrentUserRole() {
    return state.currentUserRole;
  },

  // Get role name
  getRoleName() {
    return state.roleName;
  },

  // Check if user has specific role
  hasRole(roleId) {
    return state.currentUserRole === roleId;
  },

  // Check if user has specific role name
  hasRoleName(roleName) {
    return (
      state.roleName && state.roleName.toLowerCase() === roleName.toLowerCase()
    );
  },

  // Logout user
  async logout() {
    try {
      // Call backend logout endpoint to log the logout activity
      if (state.user && state.user.id) {
        await fetch("/api/logout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: state.user.id }),
          mode: "cors",
        });
      }
    } catch (error) {
      console.error("Error logging logout activity:", error);
      // Don't fail logout if logging fails
    } finally {
      // Always clear user data
      actions.clearUser();
    }
  },

  // Verify user status (enabled/deleted) - for session validation
  async verifyUserStatus() {
    if (!state.user || !state.user.id) {
      return { canAccess: false, reason: "No user logged in" };
    }

    try {
      const response = await fetch(
        `/api/users/${state.user.id}/verify-status`,
        {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        }
      );

      // Check if response is ok before trying to parse JSON
      if (!response.ok) {
        // If server returns an error, log it but don't fail the user
        console.warn(`User status verification returned ${response.status}`);
        return { canAccess: true }; // Assume OK on server errors
      }

      const data = await response.json();

      if (data.success) {
        if (!data.can_access) {
          // User is disabled or deleted
          let reason = "";
          if (data.deleted) {
            reason = "Your account has been deleted.";
          } else if (!data.enabled) {
            reason = "Your account has been disabled.";
          }

          // Log logout activity before clearing user data
          try {
            await fetch("/api/logout", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ 
                user_id: state.user.id,
                reason: "Account disabled/deleted - automatic logout"
              }),
              mode: "cors",
            });
          } catch (logError) {
            console.error("Error logging automatic logout:", logError);
            // Continue with logout even if logging fails
          }

          // Log out the user
          actions.clearUser();
          return { canAccess: false, reason };
        }
        return { canAccess: true };
      } else {
        // If verification fails, assume user should be logged out
        actions.clearUser();
        return { canAccess: false, reason: "Unable to verify account status." };
      }
    } catch (error) {
      // Handle network errors gracefully
      if (error.message && (error.message.includes("Failed to fetch") || error.message.includes("NetworkError"))) {
        // Network error - backend might be down, don't log out the user
        console.warn("Network error verifying user status - backend may be unavailable:", error.message);
        return { canAccess: true }; // Assume OK if we can't verify due to network issues
      }
      console.error("Error verifying user status:", error);
      // On other errors, assume OK to avoid false logouts
      return { canAccess: true }; // Assume OK if we can't verify
    }
  },

  // Stop periodic status check
  stopStatusCheck,
};

// Now define startStatusCheck after actions is fully created
actions.startStatusCheck = function startStatusCheck() {
  // Clear any existing interval
  stopStatusCheck();
  
  // Start new interval - check every 30 seconds
  state.statusCheckInterval = setInterval(async () => {
    if (state.isLoggedIn && state.user && state.user.id) {
      const statusCheck = await actions.verifyUserStatus();
      if (!statusCheck.canAccess) {
        // User was disabled/deleted - verifyUserStatus already logged them out
        // Just clear the interval
        stopStatusCheck();
      }
    } else {
      // User not logged in, stop checking
      stopStatusCheck();
    }
  }, 30000); // Check every 30 seconds
};

// Getters
const getters = {
  isLoggedIn: () => state.isLoggedIn,
  currentUser: () => state.user,
  currentUserRole: () => state.currentUserRole,
  roleName: () => state.roleName,
};

// Export the store
export const userStore = {
  state,
  actions,
  getters,
};

// Export individual functions for easier use
export const {
  setUser,
  clearUser,
  initializeUser,
  getCurrentUserRole,
  getRoleName,
  hasRole,
  hasRoleName,
  logout,
  verifyUserStatus,
} = actions;

export const { isLoggedIn, currentUser, currentUserRole, roleName } = getters;
