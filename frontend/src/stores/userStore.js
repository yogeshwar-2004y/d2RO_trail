// Global user state management
import { reactive } from 'vue'

// Create reactive global state
const state = reactive({
  user: null,
  isLoggedIn: false,
  currentUserRole: null,
  roleName: null
})

// Actions
const actions = {
  // Set user data after successful login
  setUser(userData) {
    state.user = userData
    state.isLoggedIn = true
    state.currentUserRole = userData.role_id
    state.roleName = userData.role
    
    // Store in localStorage for persistence
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('currentUserRole', userData.role_id)
    localStorage.setItem('roleName', userData.role)
    
    console.log('User set:', userData)
    console.log('Current role ID:', state.currentUserRole)
    console.log('Role name:', state.roleName)
  },

  // Clear user data on logout
  clearUser() {
    state.user = null
    state.isLoggedIn = false
    state.currentUserRole = null
    state.roleName = null
    
    // Clear localStorage
    localStorage.removeItem('user')
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('currentUserRole')
    localStorage.removeItem('roleName')
  },

  // Initialize user from localStorage (for page refresh)
  initializeUser() {
    const storedUser = localStorage.getItem('user')
    const storedIsLoggedIn = localStorage.getItem('isLoggedIn')
    const storedRole = localStorage.getItem('currentUserRole')
    const storedRoleName = localStorage.getItem('roleName')
    
    if (storedUser && storedIsLoggedIn === 'true') {
      state.user = JSON.parse(storedUser)
      state.isLoggedIn = true
      state.currentUserRole = parseInt(storedRole)
      state.roleName = storedRoleName
      
      console.log('User initialized from storage:', state.user)
      console.log('Current role ID:', state.currentUserRole)
      console.log('Role name:', state.roleName)
    }
  },

  // Get current user role
  getCurrentUserRole() {
    return state.currentUserRole
  },

  // Get role name
  getRoleName() {
    return state.roleName
  },

  // Check if user has specific role
  hasRole(roleId) {
    return state.currentUserRole === roleId
  },

  // Check if user has specific role name
  hasRoleName(roleName) {
    return state.roleName && state.roleName.toLowerCase() === roleName.toLowerCase()
  },

  // Logout user
  async logout() {
    try {
      // Call backend logout endpoint to log the logout activity
      if (state.user && state.user.id) {
        await fetch('http://localhost:8000/api/logout', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: state.user.id }),
          mode: 'cors'
        });
      }
    } catch (error) {
      console.error('Error logging logout activity:', error);
      // Don't fail logout if logging fails
    } finally {
      // Always clear user data
      this.clearUser();
    }
  }
}

// Getters
const getters = {
  isLoggedIn: () => state.isLoggedIn,
  currentUser: () => state.user,
  currentUserRole: () => state.currentUserRole,
  roleName: () => state.roleName
}

// Export the store
export const userStore = {
  state,
  actions,
  getters
}

// Export individual functions for easier use
export const {
  setUser,
  clearUser,
  initializeUser,
  getCurrentUserRole,
  getRoleName,
  hasRole,
  hasRoleName,
  logout
} = actions

export const {
  isLoggedIn,
  currentUser,
  currentUserRole,
  roleName
} = getters
