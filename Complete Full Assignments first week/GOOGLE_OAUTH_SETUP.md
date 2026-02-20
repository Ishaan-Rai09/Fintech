# Google OAuth Setup Guide

This guide will help you set up Google OAuth for FinSight AI.

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name your project "FinSight AI" (or any name you prefer)
4. Click "Create"

## Step 2: Enable Google+ API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and press "Enable"

## Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in:
     - App name: FinSight AI
     - User support email: your email
     - Developer contact email: your email
   - Click "Save and Continue"
   - Skip "Scopes" (click "Save and Continue")
   - Add test users if needed
   - Click "Save and Continue"

4. Create OAuth Client ID:
   - Application type: "Web application"
   - Name: "FinSight AI Web Client"
   - Authorized JavaScript origins:
     - http://localhost:8000
   - Authorized redirect URIs:
     - http://localhost:8000/api/v1/auth/google/callback
   - Click "Create"

## Step 4: Copy Credentials

1. After creating, you'll see a popup with:
   - **Client ID** (looks like: xxxxx.apps.googleusercontent.com)
   - **Client Secret** (random string)

2. Copy both values

## Step 5: Update .env File

1. Open `.env` file in your project root
2. Replace the placeholder values:

```env
GOOGLE_CLIENT_ID=your-actual-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-actual-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```

## Step 6: Restart Server

1. Stop the server (Ctrl+C in terminal)
2. Restart: `python run.py`

## Testing

1. Go to http://localhost:8000
2. Click "Sign in with Google" button
3. You'll be redirected to Google login
4. After successful login, you'll be redirected back to the dashboard

## Troubleshooting

### Error: "redirect_uri_mismatch"
- Make sure the redirect URI in Google Console exactly matches: `http://localhost:8000/api/v1/auth/google/callback`
- Check for trailing slashes

### Error: "invalid_client"
- Double-check your Client ID and Client Secret in .env
- Make sure there are no extra spaces

### Error: "access_denied"
- Make sure you added yourself as a test user in OAuth consent screen

## Production Deployment

When deploying to production:

1. Update authorized origins and redirect URIs in Google Console with your production domain
2. Update GOOGLE_REDIRECT_URI in .env with production URL
3. Move OAuth consent screen from "Testing" to "Production" status
