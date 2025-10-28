# Plan Document Assignment Notifications

## Overview
When a QA Head assigns a plan document to a reviewer, the assigned reviewer now receives a notification.

## Implementation Details

### Modified Files
- **backend/routes/documents.py**: Added notification logic to `assign_reviewer()` and `update_reviewer()` functions

### What Happens Now

#### 1. When Assigning a Reviewer (POST `/api/assign-reviewer`)
- The QA Head assigns a reviewer to review plan documents
- The system logs the activity
- The assigned reviewer receives a notification with:
  - Activity: "Plan Document Assignment"
  - Notification type: `plan_document_assigned`
  - Details about which LRU and project they've been assigned to
  - Who assigned them (QA Head name)

#### 2. When Updating a Reviewer Assignment (PUT `/api/update-reviewer`)
- The QA Head updates the reviewer assignment
- The system logs the activity
- The new assigned reviewer receives a notification with:
  - Activity: "Plan Document Assignment Updated"
  - Notification type: `plan_document_assigned`
  - Details about which LRU and project they've been assigned to
  - Who assigned them (QA Head name)

### Notification Content
The notification includes:
- **Project**: The project name
- **LRU**: The LRU name they need to review
- **Assigned By**: The QA Head who made the assignment
- **Message**: Clear description of what they need to do

### Integration with Existing Notification System
- Uses the existing `log_notification()` function from `backend/utils/activity_logger.py`
- Notifications appear in the notification overlay in the frontend
- Notifications are marked as unread by default
- Users can mark notifications as read by clicking on them

### Notification Type
- **Type**: `plan_document_assigned`
- **Activity**: "Plan Document Assignment" or "Plan Document Assignment Updated"

### Testing
To test the notification feature:
1. Log in as a QA Head user
2. Assign a reviewer to a plan document for an LRU
3. Log in as the assigned reviewer
4. Check notifications in the sidebar (should show a badge with unread count)
5. Click on "Notifications" to view the detailed notification

