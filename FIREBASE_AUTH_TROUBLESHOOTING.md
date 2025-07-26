# Firebase Authentication Troubleshooting Guide

## Issue: "Invalid ID token" Error

### Symptoms

- Backend logs show: `❌ Invalid ID token error`
- Frontend authentication fails with 401 Unauthorized
- Token verification fails in Firebase Admin SDK

### Root Causes & Solutions

## 1. Token Expiration (Most Common)

**Problem**: Firebase ID tokens expire after 1 hour by default.

**Solution**: Force token refresh before sending to backend.

**Status**: ✅ **FIXED** - Added token refresh in `useFirebaseAuth.ts`

```typescript
// Force token refresh to ensure we have a fresh token
await authResult.user.getIdToken(true);
const idToken = await authResult.user.getIdToken();
```

## 2. Firebase Project Configuration Mismatch

**Problem**: Frontend and backend using different Firebase projects.

**Solution**: Verify both are using the same project ID.

**Status**: ✅ **VERIFIED** - Both using `agentic-ai-day-c6f02`

### Verification Steps:

1. **Frontend**: Check `.env` file

   ```bash
   cat frontend/.env | grep PROJECT_ID
   ```

2. **Backend**: Check service account key
   ```bash
   cat backend/keys/serviceAccountKey.json | grep project_id
   ```

## 3. Environment Variables Not Loaded

**Problem**: Frontend Firebase config not properly loaded.

**Solution**: Added validation and debug utilities.

**Status**: ✅ **FIXED** - Added `firebaseDebug.ts` utility

### Debug Steps:

1. Open browser console
2. Look for Firebase configuration logs
3. Verify all required fields are present

## 4. Firebase Admin SDK Initialization Issues

**Problem**: Backend Firebase Admin SDK not properly initialized.

**Solution**: Enhanced error handling and logging.

**Status**: ✅ **FIXED** - Added detailed logging in `firebase_auth.py`

## 5. Token Format Issues

**Problem**: Token might be malformed or truncated.

**Solution**: Added token validation and format checking.

**Status**: ✅ **FIXED** - Added token format validation

## Testing & Debugging

### 1. Use the Debug Script

```bash
cd backend
source .venv/bin/activate
python test_firebase_auth.py <token>
```

### 2. Check Browser Console

1. Open frontend app in browser
2. Open developer tools (F12)
3. Go to Console tab
4. Sign in with FirebaseUI
5. Look for logs:
   - `🔑 Got ID token:`
   - `📏 Token length:`
   - `🔍 Token format check:`

### 3. Check Backend Logs

Look for detailed logs in backend console:

- `🔥 Firebase auth request received`
- `📏 Token length:`
- `🔍 Token format check:`
- `🏢 Backend Firebase project ID:`

### 4. Manual Token Testing

```bash
# Test Firebase setup
cd backend
source .venv/bin/activate
python debug_firebase.py

# Test with actual token
python debug_firebase.py <your-token-here>
```

## Common Error Messages & Solutions

### "Invalid ID token"

- **Cause**: Token expired, malformed, or from wrong project
- **Solution**: Force token refresh, check project configuration

### "Token verification failed"

- **Cause**: Network issues or Firebase Admin SDK problems
- **Solution**: Check backend logs, verify Firebase setup

### "Missing Firebase configuration fields"

- **Cause**: Environment variables not loaded
- **Solution**: Check `.env` file, restart frontend development server

## Prevention Measures

### 1. Token Refresh Strategy

- Always force token refresh before API calls
- Implement automatic token refresh on 401 errors
- Set up token expiration monitoring

### 2. Configuration Validation

- Validate Firebase config on app startup
- Check project ID consistency
- Verify all required environment variables

### 3. Error Handling

- Implement comprehensive error logging
- Provide user-friendly error messages
- Add retry mechanisms for transient failures

## Next Steps

1. **Test the fixes**: Restart both frontend and backend servers
2. **Monitor logs**: Watch for the new detailed logging
3. **Verify authentication**: Try signing in with FirebaseUI
4. **Use debug tools**: Run the test scripts if issues persist

## Files Modified

- `frontend/src/hooks/useFirebaseAuth.ts` - Added token refresh
- `frontend/src/config/firebase.ts` - Added configuration validation
- `frontend/src/utils/firebaseDebug.ts` - Added debug utilities
- `backend/src/auth/firebase_auth.py` - Enhanced error logging
- `backend/debug_firebase.py` - Created debug script
- `backend/test_firebase_auth.py` - Created comprehensive test script

## Support

If issues persist after implementing these fixes:

1. Check the debug logs in browser console and backend
2. Run the test scripts with actual tokens
3. Verify Firebase project configuration in Firebase Console
4. Check that authentication providers are enabled in Firebase Console
