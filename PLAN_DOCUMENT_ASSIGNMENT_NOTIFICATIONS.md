# Plan Document Assignment and Comment Notifications

## Overview
1. When a QA Head assigns a plan document to a reviewer, the assigned reviewer receives a notification.
2. When a reviewer adds comments to a plan document, all designers in that project receive notifications.

## Implementation Details

### Modified Files
- **backend/routes/documents.py**: Added notification logic to `assign_reviewer()` and `update_reviewer()` functions
- **backend/app.py**: Added notification logic to `create_comment()` function

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

#### 3. When a Reviewer Adds a Comment (POST `/api/comments`)
- The reviewer adds a comment to a plan document
- The system logs the activity
- **All designers** in the project receive a notification with:
  - Activity: "New Comment on Plan Document"
  - Notification type: `plan_document_comment`
  - Details about which document, LRU, and project received the comment
  - Which reviewer added the comment
  - A request to review and address the feedback

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

### Notification Types
1. **Assignment Notifications**:
   - **Type**: `plan_document_assigned`
   - **Activity**: "Plan Document Assignment" or "Plan Document Assignment Updated"
   - **Recipients**: Assigned reviewer

2. **Comment Notifications**:
   - **Type**: `plan_document_comment`
   - **Activity**: "New Comment on Plan Document"
   - **Recipients**: All designers in the project

### Testing

#### Test Assignment Notifications
1. Log in as a QA Head user
2. Assign a reviewer to a plan document for an LRU
3. Log in as the assigned reviewer
4. Check notifications in the sidebar (should show a badge with unread count)
5. Click on "Notifications" to view the detailed notification

#### Test Comment Notifications
1. Log in as a QA Reviewer
2. Open a plan document assigned to you
3. Add a comment to the document
4. Log in as a Designer assigned to that project
5. Check notifications in the sidebar
6. You should see a notification about the new comment with details about the document and reviewer

