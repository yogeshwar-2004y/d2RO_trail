# Plan Document Assignment and Comment Notifications

## Overview
1. When a QA Head assigns a plan document to a reviewer, the assigned reviewer receives a notification.
2. When version A is uploaded, all QA Heads are notified for assignment.
3. When versions B, C, etc. are uploaded, the assigned reviewer is notified.
4. When a reviewer adds comments to a plan document, all designers in that project receive notifications.
5. When a designer accepts or rejects a reviewer's comment, the reviewer receives a notification.

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

#### 3. When Version A is Uploaded (POST `/api/plan-documents`)
- A designer uploads the first version (Version A) of a plan document
- The system logs the activity
- **All QA Heads** receive a notification with:
  - Activity: "New Document Uploaded (Version A)"
  - Notification type: `document_upload_version_a`
  - Details about which document, LRU, and project
  - A request for review assignment

#### 4. When Versions B, C, etc. are Uploaded (POST `/api/plan-documents`)
- A designer uploads a new version (B, C, D, etc.) of a plan document
- The system logs the activity
- **The assigned reviewer** for that LRU receives a notification with:
  - Activity: "New Document Version Uploaded"
  - Notification type: `document_upload_new_version`
  - Details about which version, document, LRU, and project
  - A request to review the new version

#### 5. When a Reviewer Adds a Comment (POST `/api/comments`)
- The reviewer adds a comment to a plan document
- The system logs the activity
- **All designers** in the project receive a notification with:
  - Activity: "New Comment on Plan Document"
  - Notification type: `plan_document_comment`
  - Details about which document, LRU, and project received the comment
  - Which reviewer added the comment
  - A request to review and address the feedback

#### 6. When a Designer Accepts a Comment (POST `/api/comments/<id>/accept`)
- A designer or design head accepts a reviewer's comment
- The system logs the activity
- The **reviewer** receives a notification with:
  - Activity: "Your Comment Was Accepted"
  - Notification type: `comment_accepted`
  - Details about which document, LRU, and project
  - Who accepted the comment (designer name)
  - The justification provided

#### 7. When a Designer Rejects a Comment (POST `/api/comments/<id>/reject`)
- A designer or design head rejects a reviewer's comment
- The system logs the activity
- The **reviewer** receives a notification with:
  - Activity: "Your Comment Was Rejected"
  - Notification type: `comment_rejected`
  - Details about which document, LRU, and project
  - Who rejected the comment (designer name)
  - The justification provided

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

2. **Version A Upload Notifications**:
   - **Type**: `document_upload_version_a`
   - **Activity**: "New Document Uploaded (Version A)"
   - **Recipients**: All QA Heads

3. **New Version Upload Notifications**:
   - **Type**: `document_upload_new_version`
   - **Activity**: "New Document Version Uploaded"
   - **Recipients**: Assigned reviewer for that LRU

4. **Comment Notifications**:
   - **Type**: `plan_document_comment`
   - **Activity**: "New Comment on Plan Document"
   - **Recipients**: All designers in the project

5. **Comment Accepted Notifications**:
   - **Type**: `comment_accepted`
   - **Activity**: "Your Comment Was Accepted"
   - **Recipients**: Reviewer who submitted the comment

6. **Comment Rejected Notifications**:
   - **Type**: `comment_rejected`
   - **Activity**: "Your Comment Was Rejected"
   - **Recipients**: Reviewer who submitted the comment

### Testing

#### Test Assignment Notifications
1. Log in as a QA Head user
2. Assign a reviewer to a plan document for an LRU
3. Log in as the assigned reviewer
4. Check notifications in the sidebar (should show a badge with unread count)
5. Click on "Notifications" to view the detailed notification

#### Test Version A Upload Notifications
1. Log in as a Designer
2. Upload a plan document version A for an LRU
3. Log in as a QA Head
4. Check notifications in the sidebar
5. You should see a notification about the new document version A
6. Assign a reviewer to that LRU

#### Test Version B/C Upload Notifications
1. Log in as a Designer
2. Upload a new version (B, C, etc.) of a plan document for an LRU that has an assigned reviewer
3. Log in as the assigned Reviewer
4. Check notifications in the sidebar
5. You should see a notification about the new version with details about the document, LRU, and project

#### Test Comment Notifications
1. Log in as a QA Reviewer
2. Open a plan document assigned to you
3. Add a comment to the document
4. Log in as a Designer assigned to that project
5. Check notifications in the sidebar
6. You should see a notification about the new comment with details about the document and reviewer

#### Test Comment Acceptance/Rejection Notifications
1. Log in as a Designer
2. Open a plan document for a project you're assigned to
3. Accept or reject a reviewer's comment
4. Log in as the Reviewer who submitted the comment
5. Check notifications in the sidebar
6. You should see a notification about your comment being accepted or rejected, including:
   - The document, LRU, and project details
   - Who accepted/rejected it
   - The justification provided

