# Frontend URL Fix Guide

## Problem

The frontend has many hardcoded URLs pointing to `http://localhost:8000` or `http://127.0.0.1:8000`, but:
- Backend runs on port **5000** (not 8000)
- Nginx proxy handles `/api` requests automatically
- Using relative URLs is the correct approach

## Solution

Change all hardcoded URLs from:
- `http://localhost:8000/api/...` → `/api/...`
- `http://127.0.0.1:8000/api/...` → `/api/...`

## Files Already Fixed

✅ `frontend/src/views/LoginPage.vue` - Fixed
✅ `frontend/src/components/MemoDashboard.vue` - Fixed  
✅ `frontend/src/views/TechSupportPage.vue` - Fixed
✅ `docker-compose.yml` - Removed obsolete version

## Files Still Need Fixing

The following files still have hardcoded URLs (181 instances found):

### Critical Files (High Priority)
- `frontend/src/components/TemplateDashboard.vue`
- `frontend/src/components/ViewOnlyMemoForm.vue`
- `frontend/src/components/MemoForm.vue`
- `frontend/src/services/techSupportSync.js`

### Admin Views
- `frontend/src/views/admin/*.vue` (multiple files)

### Template Files
- `frontend/src/templates/*.vue` (all template files)

### Other Views
- `frontend/src/views/reviewer/*.vue`
- `frontend/src/views/qahead/*.vue`
- `frontend/src/views/designhead/*.vue`

## Quick Fix Script

You can use find and replace in your IDE:

**Find**: `http://localhost:8000/api`
**Replace**: `/api`

**Find**: `http://127.0.0.1:8000/api`
**Replace**: `/api`

**Find**: `http://localhost:8000`
**Replace**: `` (empty, or handle case by case)

**Find**: `http://127.0.0.1:8000`
**Replace**: `` (empty, or handle case by case)

## Testing

After fixing URLs, rebuild frontend:

```bash
docker compose build --no-cache frontend
docker compose up -d frontend
```

Test in browser - all API calls should work through Nginx proxy.

## Current Status

✅ Backend: Running on port 5000 (healthy)
✅ Frontend: Running on port 80
⚠️ Frontend URLs: Partially fixed (need to fix remaining files)

## Immediate Action

For now, the critical login and memo functionality should work. Other features may still have issues until all URLs are fixed.

