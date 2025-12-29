# Complete URL Fix Guide

## Problem
The frontend has many hardcoded URLs pointing to `http://localhost:8000/api` and `http://127.0.0.1:8000/api`, which causes connection errors in production. These need to be changed to relative paths `/api` so Nginx can proxy them correctly.

## ✅ Files Already Fixed

I've manually fixed the most critical files:
- `ActivityLogs.vue` ✅
- `LoginLogs.vue` ✅
- `NotificationBadge.vue` ✅
- `AppSidebar.vue` ✅
- `NotificationsOverlay.vue` ✅
- `QAHeadNotifications.vue` ✅
- `EditUser.vue` ✅
- `AddUpdateUser.vue` ✅
- `TestManagement.vue` ✅
- `MemoForm.vue` ✅
- `NewsUpdates.vue` ✅
- `CustomiseBackground.vue` ✅
- `TechSupportManagement.vue` ✅
- `TechSupportUserDashboard.vue` ✅
- `techSupportSync.js` ✅
- `DocumentTypes.vue` ✅
- `DocumentViewer.vue` ✅
- `ProjectsForAssigning.vue` ✅
- `ProjectsDashboard.vue` ✅
- `MemoDashboard.vue` ✅
- `IndividualReport.vue` ✅

## ⚠️ Remaining Files to Fix

There are still ~30+ files with hardcoded URLs, mostly in:
- Template files (`templates/*.vue`)
- Other component files
- Some view files

## Solution: Use the Automated Script

I've created a script `fix_all_urls.sh` that will fix ALL remaining URLs automatically.

### On Your Local Machine (Before Committing)

```bash
cd ~/Desktop/Trail-drdo/Aviatrax

# Run the fix script
./fix_all_urls.sh

# Review the changes
git diff

# If everything looks good, commit
git add .
git commit -m "Fix all hardcoded API URLs to use relative paths"
git push origin main
```

### On EC2 (After Pulling Changes)

```bash
cd ~/d2RO_trail/Aviatrax

# Pull latest changes
git pull --no-rebase origin main

# Rebuild frontend
docker compose build --no-cache frontend

# Restart frontend
docker compose up -d frontend

# Check logs
docker compose logs -f frontend
```

## Manual Fix (If Script Doesn't Work)

If you prefer to fix manually or the script has issues, use find/replace in your IDE:

1. **Find**: `http://localhost:8000/api`
   **Replace**: `/api`

2. **Find**: `http://127.0.0.1:8000/api`
   **Replace**: `/api`

3. **Find**: `http://localhost:8000/`
   **Replace**: `/`

4. **Find**: `http://127.0.0.1:8000/`
   **Replace**: `/`

## Files That Still Need Fixing

Based on the grep results, these files still have hardcoded URLs:

### Template Files (High Priority)
- `templates/barepcbinspectionreport.vue`
- `templates/RawMaterialInspectionReport.vue`
- `templates/MechanicalInspection.vue`
- `templates/KitOfPartInsp.vue`
- `templates/CotsScreeningInspectionReport.vue`
- `templates/Conformalcoatinginspectionreport.vue`
- `templates/AssembledBoardInspectionReport.vue`

### Component Files
- `components/ViewOnlyMemoForm.vue`
- `components/SubTestDetail.vue`
- `components/ObservationReport.vue`
- `components/LruDashboard.vue`
- `components/GroupDetail.vue`

### View Files
- `views/designhead/ProjectMembers.vue`
- `views/designhead/AddMember.vue`
- `views/admin/SelectUserToEdit.vue`
- `views/admin/SelectProjectToEdit.vue`
- `views/admin/ManageUsers.vue`
- `views/admin/ManageProjects.vue`
- `views/admin/EditProject.vue`
- `views/admin/AddUpdateProjects.vue`
- `views/reviewer/InspectionMemo.vue`
- `views/qahead/QAHeadAssignReviewer.vue`

## Verification

After fixing, verify by searching for remaining hardcoded URLs:

```bash
cd frontend/src
grep -r "http://localhost:8000" .
grep -r "http://127.0.0.1:8000" .
```

If these commands return no results, all URLs are fixed! ✅

## Testing

After rebuilding:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+F5)
3. Test all major features:
   - Login
   - Notifications
   - Activity logs
   - News updates
   - Projects
   - Reports
   - Tech support

All API calls should now work through the Nginx proxy!

