# FinSight AI - Quick Start Guide

## 🚀 Running the Application

### Server is Already Running!
Your FastAPI server is running on **http://localhost:8000** with auto-reload enabled.

Any code changes are automatically applied - no need to restart manually!

---

## 🔐 Google OAuth Setup (REQUIRED)

Before you can log in, you need to set up Google OAuth credentials:

### Quick Setup (5 minutes):

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Create new project "FinSight AI"

2. **Create OAuth Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/v1/auth/google/callback`
   - Authorized JavaScript origins: `http://localhost:8000`

3. **Update .env File**
   ```env
   GOOGLE_CLIENT_ID=your-actual-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-actual-client-secret
   ```

4. **Restart Server** (Ctrl+C, then `python run.py`)

📖 **Detailed instructions**: See [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)

---

## 🎯 Using the Platform

### 1. Landing Page
- Visit: **http://localhost:8000**
- Modern professional landing page
- Click "Sign in with Google" to authenticate

### 2. Dashboard
- After login, you'll be redirected to **/dashboard**
- Access all 12 AI-powered modules:
  - 📊 Portfolio Manager
  - ⚠️ Risk Calculator (VaR Analysis)
  - 🔮 ML Predictions
  - 🤖 Robo Advisor
  - 💰 Tax Calculator
  - 📈 Capstone Dashboard
  - And more...

### 3. Navigation
All pages have clean navigation:
- **Home** - Return to landing page
- **Dashboard** - Main dashboard
- **Module Pages** - Direct access to each tool

---

## 🔧 Technical Details

### What Changed:
✅ **Google OAuth Only** - Traditional login/register removed  
✅ **Modern Landing Page** - Professional design with green/orange theme  
✅ **Fixed Navigation** - All 404 errors resolved  
✅ **Clean Routes** - `/dashboard`, `/portfolio`, `/risk`, etc.  
✅ **No Purple/Blue** - Professional color palette  

### Color Scheme:
- Primary: Green (#10b981)
- Secondary: Orange (#f59e0b)
- Accent: Red, Teal
- Background: Light gradients

### Database:
- MySQL running on localhost:3306
- Database: `finsight_db`
- Password: `dare`
- 11 tables initialized

---

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints:
- `GET /api/v1/auth/google/login` - Start OAuth flow
- `GET /api/v1/auth/google/callback` - OAuth callback
- `GET /api/v1/auth/me` - Get current user
- `GET /api/v1/portfolio/*` - Portfolio operations
- `GET /api/v1/risk/*` - Risk analysis
- `GET /api/v1/predictions/*` - ML predictions

---

## 🛠️ Troubleshooting

### Google OAuth Not Working?
1. Check `.env` has correct `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
2. Verify redirect URI: `http://localhost:8000/api/v1/auth/google/callback`
3. Check terminal for error messages
4. See [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md) for detailed help

### Navigation Issues?
- All routes now use clean paths: `/dashboard`, `/portfolio`, etc.
- No more .html extensions
- Server auto-reloads on code changes

### Database Issues?
```bash
# Check MySQL is running
# Database: finsight_db
# User: root
# Password: dare
```

---

## 📦 Installed Packages

Core dependencies:
- FastAPI 0.109.0
- Pydantic 2.5.3
- SQLAlchemy 2.0.25
- authlib 1.6.7 (OAuth)
- google-auth 2.48.0
- statsmodels 0.14.6
- email-validator 2.3.0

---

## 🎨 Design Principles

- **Professional & Modern** - Clean, business-ready design
- **No Glassmorphism** - Solid, professional aesthetics
- **Green/Orange Theme** - Financial growth colors
- **Responsive** - Mobile-friendly layouts
- **Fast & Efficient** - Optimized performance

---

## 🚦 Current Status

✅ Backend API running  
✅ Database connected  
✅ Google OAuth configured (needs credentials)  
✅ All routes fixed  
✅ Modern landing page live  
✅ Auto-reload enabled  

⏳ **Pending**: Add your Google OAuth credentials to `.env`

---

## 📞 Quick Commands

```bash
# Start server (already running!)
python run.py

# Install new package
pip install package-name

# Check Python version
python --version

# Access MySQL
mysql -u root -p
# Password: dare
```

---

## 🎉 You're All Set!

1. Set up Google OAuth credentials (see above)
2. Visit http://localhost:8000
3. Click "Sign in with Google"
4. Start using the platform!

**Enjoy your FinSight AI experience!** 🚀
