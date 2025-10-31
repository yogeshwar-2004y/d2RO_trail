# Notification Feature Implementation

## Overview
This document describes the notification feature implementation for the AVIATRAX application. When a project is created in the admin flow, notifications are automatically sent to Design Head and QA Head users.

## Database Changes

### Migration File
**Location**: `backend/migrations/add_notifications_to_activity_logs.sql`

**Changes Made**:
1. Added `notified_user_id` column (INT, FK to users table)
2. Added `is_read` column (BOOLEAN, defaults to FALSE)
3. Added `notification_type` column (VARCHAR(50))
4. Created indexes for better query performance

### Migration Execution
Run the migration using:
```bash
cd backend
python run_notifications_migration.py
```

## Backend Implementation

### 1. Enhanced Activity Logger
**File**: `backend/utils/activity_logger.py`

**New Functions**:
- `log_notification()`: Creates a notification entry in the activity_logs table
- `get_users_by_role(role_id)`: Retrieves all users with a specific role

**Parameters for `log_notification()`**:
- `project_id`: ID of the related project
- `activity_performed`: Description of the activity
- `performed_by`: User ID who triggered the notification
- `notified_user_id`: User ID who should receive the notification
- `notification_type`: Type of notification (e.g., 'project_created')
- `additional_info`: Additional details about the notification

### 2. Modified Project Creation
**File**: `backend/routes/projects.py`

**Function**: `create_project()` (lines 105-214)

**Behavior**:
When a project is created, the system:
1. Logs the activity normally
2. Fetches all Design Head users (role_id = 4)
3. Fetches all QA Head users (role_id = 2)
4. Creates notifications for each Design Head and QA Head
5. Returns success response

### 3. New API Endpoints
**File**: `backend/routes/projects.py`

#### Get User Notifications
```
GET /api/notifications/<int:user_id>
```
**Query Parameters**:
- `limit` (optional): Maximum number of notifications to return (default: 50)
- `unread_only` (optional): Filter only unread notifications (default: false)

**Response**:
```json
{
  "success": true,
  "notifications": [
    {
      "activity_id": 1,
      "project_id": 5,
      "project_name": "Flight Control System",
      "activity_performed": "New Project Created",
      "performed_by": 2,
      "performed_by_name": "Admin User",
      "timestamp": "2025-01-15T10:30:00",
      "additional_info": "New project 'Flight Control System'...",
      "is_read": false,
      "notification_type": "project_created"
    }
  ],
  "total": 1
}
```

#### Mark Notification as Read
```
PUT /api/notifications/<int:notification_id>/mark-read
```

**Response**:
```json
{
  "success": true,
  "message": "Notification marked as read"
}
```

## Role IDs Reference

| Role ID | Role Name |
|---------|-----------|
| 1 | Admin |
| 2 | QA Head |
| 3 | QA Reviewer |
| 4 | Design Head |
| 5 | Designer |

## Usage Examples

### Creating a Project (Triggers Notifications)
```javascript
// Frontend request
POST http://localhost:5000/api/projects
{
  "name": "New Project",
  "number": "PROJ001",
  "date": "2025-01-15",
  "lrus": [...],
  "createdBy": 2
}

// This automatically:
// 1. Creates the project
// 2. Logs the activity
// 3. Creates notifications for all Design Head users
// 4. Creates notifications for all QA Head users
```

### Fetching User Notifications
```javascript
// Get all notifications for a user
GET http://localhost:5000/api/notifications/1003

// Get only unread notifications
GET http://localhost:5000/api/notifications/1003?unread_only=true

// Limit results
GET http://localhost:5000/api/notifications/1003?limit=10&unread_only=true
```

### Marking Notification as Read
```javascript
PUT http://localhost:5000/api/notifications/123/mark-read
```

## Notification Flow

```
Admin creates project
    ↓
Project created in database
    ↓
Activity logged
    ↓
System queries for Design Head users (role_id=4)
    ↓
For each Design Head:
    Create notification entry
    ↓
System queries for QA Head users (role_id=2)
    ↓
For each QA Head:
    Create notification entry
    ↓
Return success response
```

## Testing

### Test Project Creation
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "number": "TEST001",
    "date": "2025-01-15",
    "lrus": [{"name": "Test LRU", "serialQuantity": 5}],
    "createdBy": 2
  }'
```

### Test Fetching Notifications
```bash
# For Design Head (user_id=1003)
curl http://localhost:5000/api/notifications/1003

# For QA Head (user_id=1004)
curl http://localhost:5000/api/notifications/1004
```

## Future Enhancements

1. **Frontend Integration**: Create notification components to display notifications to users
2. **Notification Count**: Add endpoint to get unread notification count
3. **Mark All as Read**: Add endpoint to mark all notifications as read
4. **Notification Preferences**: Allow users to configure notification types
5. **Email Notifications**: Send email notifications for important events
6. **Notification Categories**: Organize notifications by category/type

## Notes

- Notifications are stored in the `activity_logs` table for simplicity and reuse of existing infrastructure
- The notification system is flexible and can be extended to notify about other activities
- Notification types can be customized for different events (e.g., 'project_created', 'memo_submitted', etc.)
- The `is_read` flag helps track which notifications have been seen by users

