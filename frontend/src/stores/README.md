# Global User Role Management System

This document explains how to use the global user role management system in the AVIATRAX project.

## Overview

The global role system provides centralized user authentication and role-based access control throughout the entire application. It automatically fetches user roles from the database and makes them available to all components.

## Features

- **Automatic Role Fetching**: User roles are fetched from the database during login
- **Global State Management**: User data and roles are stored in a global reactive state
- **Persistent Storage**: User data persists across browser sessions using localStorage
- **Role-based Access Control**: Easy role checking throughout the application
- **Automatic Initialization**: User state is restored on page refresh

## Database Integration

### Backend Changes

The login endpoint now returns both `role_id` and `role_name`:

```python
# Backend login response
{
    "success": True,
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "role_id": 2,        # NEW: Role ID from database
        "role": "QA Head"    # Role name from database
    }
}
```

### Role ID Mapping

| Role ID | Role Name | Description |
|---------|-----------|-------------|
| 1 | Admin | System Administrator |
| 2 | QA Head | Quality Assurance Head |
| 3 | QA Reviewer | Quality Assurance Reviewer |
| 4 | Design Head | Design Team Head |
| 5 | Designer | Design Team Member |

## Usage in Components

### 1. Import the Store

```javascript
import { userStore } from '@/stores/userStore'
```

### 2. Access User Data

```javascript
export default {
  computed: {
    // Get current user role ID
    currentUserRole() {
      return userStore.getters.currentUserRole()
    },
    
    // Get current user role name
    roleName() {
      return userStore.getters.roleName()
    },
    
    // Check if user is logged in
    isLoggedIn() {
      return userStore.getters.isLoggedIn()
    },
    
    // Get current user data
    currentUser() {
      return userStore.getters.currentUser()
    }
  }
}
```

### 3. Role-based Conditional Rendering

```vue
<template>
  <div>
    <!-- Show only for QA Head (role ID: 2) -->
    <button v-if="currentUserRole === 2" @click="assignReviewer">
      Assign Reviewer
    </button>
    
    <!-- Show only for Design Head or Designer -->
    <button v-if="[4, 5].includes(currentUserRole)" @click="submitMemo">
      Submit Memo
    </button>
    
    <!-- Show only for QA Reviewer (role ID: 3) -->
    <div v-if="currentUserRole === 3" class="shared-memos">
      Shared with Me
    </div>
  </div>
</template>
```

### 4. Role Checking Methods

```javascript
methods: {
  // Check if user has specific role ID
  hasRole(roleId) {
    return userStore.actions.hasRole(roleId)
  },
  
  // Check if user has specific role name
  hasRoleName(roleName) {
    return userStore.actions.hasRoleName(roleName)
  },
  
  // Example usage
  canApproveMemo() {
    return this.hasRole(2) // Only QA Head can approve
  },
  
  canUploadDocuments() {
    return this.hasRoleName('Design Head') || this.hasRoleName('Designer')
  }
}
```

## Store API Reference

### Actions

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `setUser(userData)` | Store user data after login | `userData` object | void |
| `clearUser()` | Clear user data on logout | none | void |
| `initializeUser()` | Initialize from localStorage | none | void |
| `hasRole(roleId)` | Check if user has role ID | `roleId` (number) | boolean |
| `hasRoleName(roleName)` | Check if user has role name | `roleName` (string) | boolean |
| `logout()` | Logout user and clear data | none | void |

### Getters

| Method | Description | Returns |
|--------|-------------|---------|
| `isLoggedIn()` | Check if user is logged in | boolean |
| `currentUser()` | Get current user data | object |
| `currentUserRole()` | Get current user role ID | number |
| `roleName()` | Get current user role name | string |

## Testing the System

### Test Component

A test component is available at `/test-role-system` to verify the role system:

1. Login with different user accounts
2. Navigate to `/test-role-system`
3. Verify role information is displayed correctly
4. Test role-based access checks

### Manual Testing

1. **Login Test**: Login with different users and verify roles are set correctly
2. **Persistence Test**: Refresh the page and verify user data persists
3. **Component Test**: Check that components show/hide based on user roles
4. **Logout Test**: Logout and verify all data is cleared

## Migration Guide

### For Existing Components

1. **Remove hardcoded roles**:
   ```javascript
   // OLD
   data() {
     return {
       currentUserRole: 2 // Remove this
     }
   }
   
   // NEW
   computed: {
     currentUserRole() {
       return userStore.getters.currentUserRole()
     }
   }
   ```

2. **Import the store**:
   ```javascript
   import { userStore } from '@/stores/userStore'
   ```

3. **Update role checks**:
   ```javascript
   // OLD
   if (this.currentUserRole === 2) { ... }
   
   // NEW (same syntax, but now dynamic)
   if (this.currentUserRole === 2) { ... }
   ```

## Security Considerations

- User data is stored in localStorage (client-side)
- Role checks are performed client-side (for UI purposes)
- **Important**: Server-side validation should always be implemented for sensitive operations
- The system is designed for UI/UX purposes, not security enforcement

## Troubleshooting

### Common Issues

1. **Role not updating**: Ensure `setUser()` is called after successful login
2. **Data not persisting**: Check if localStorage is enabled in browser
3. **Components not reacting**: Ensure you're using computed properties, not data properties

### Debug Information

Use the test component at `/test-role-system` to see:
- Current user data
- Role information
- localStorage contents
- Role-based access checks

## Future Enhancements

- Add role-based route guards
- Implement server-side role validation
- Add role change notifications
- Implement role-based API permissions
