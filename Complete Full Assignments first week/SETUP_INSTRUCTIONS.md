# FinSight AI - Complete Setup Instructions

## 📋 Requirements

- ✅ Python 3.11 or higher
- ✅ MySQL 8.0 or higher (XAMPP recommended for Windows)
- ✅ 4GB RAM minimum
- ✅ 500MB free disk space

---

## 🚀 Installation Steps

### Step 1: Install Python
1. Download Python 3.11+ from https://www.python.org/downloads/
2. During installation, **check "Add Python to PATH"**
3. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install MySQL
**Option A: XAMPP (Recommended for Windows)**
1. Download XAMPP from https://www.apachefriends.org/
2. Install XAMPP (select MySQL component)
3. Open XAMPP Control Panel
4. Click "Start" next to MySQL
5. MySQL will run on port 3306

**Option B: Standalone MySQL**
1. Download from https://dev.mysql.com/downloads/mysql/
2. Install and set root password
3. Start MySQL service

### Step 3: Create Database
```bash
# Open MySQL command line
mysql -u root -p

# Create database (enter password if prompted)
CREATE DATABASE finsight_db;

# Verify
SHOW DATABASES;

# Exit
EXIT;
```

**OR use phpMyAdmin (XAMPP):**
- Open http://localhost/phpmyadmin
- Click "New" → Enter "finsight_db" → Click "Create"

### Step 4: Clone/Download Project
```bash
cd E:\FINTECH\Projects
# Your project is already here in "Complete Full Assignments first week"
```

### Step 5: Create Virtual Environment
```bash
# Navigate to project folder
cd "Complete Full Assignments first week"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
venv\Scripts\activate
# Windows (Command Prompt)
venv\Scripts\activate.bat
```

You should see `(venv)` in your terminal prompt.

### Step 6: Install Python Dependencies
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

This will install:
- FastAPI, SQLAlchemy, MySQL connector
- ML libraries (scikit-learn, XGBoost)
- Financial libraries (yfinance, scipy)
- And 30+ other packages

**Installation time:** ~3-5 minutes

### Step 7: Configure Environment
```bash
# Copy template
copy .env.example .env

# Edit .env file with Notepad
notepad .env
```

**Update these lines in .env:**
```env
# Generate SECRET_KEY (run this command):
python -c "import secrets; print(secrets.token_hex(32))"

# Copy the output and paste in .env:
SECRET_KEY=<paste_generated_key_here>

# Set your MySQL credentials:
# If using XAMPP with no password:
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/finsight_db

# If you set a MySQL password:
DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/finsight_db
```

Save and close the file.

### Step 8: Initialize Database
```bash
# This creates all 11 tables in MySQL
python -m backend.database.init_db
```

**Expected output:**
```
Creating database tables...
✓ users
✓ transactions
✓ portfolios
✓ portfolio_holdings
... (11 tables total)
Database initialized successfully!
```

### Step 9: Run the Application
```bash
python run.py
```

**Expected output:**
```
======================================================================
🚀 Starting FinSight AI Platform
======================================================================
...
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!** The server is now running.

### Step 10: Access the Application
Open your web browser and go to:
- **Main Dashboard:** http://localhost:8000
- **Login Page:** http://localhost:8000/frontend/html/login.html
- **API Documentation:** http://localhost:8000/docs

---

## 🎯 First-Time User Guide

### 1. Register an Account
1. Click "Register" on the login page
2. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123` (min 8 characters)
   - Full Name: `Test User`
3. Click "Register"
4. You'll be redirected to login page

### 2. Login
1. Enter username: `testuser`
2. Enter password: `testpass123`
3. Click "Login"
4. You're now on the dashboard!

### 3. Try Key Features

#### Portfolio Optimization
1. Navigate to **Portfolio** from menu
2. Enter tickers: `AAPL,MSFT,GOOGL`
3. Select period: `1y`
4. Click "Optimize Portfolio"
5. View optimal weights and Sharpe ratio

#### VaR Risk Analysis (Main Feature)
1. Go to **Capstone** from menu
2. Enter:
   - Stock 1: `AAPL` → Weight: `60`
   - Stock 2: `MSFT` → Weight: `40`
   - Portfolio Value: `100000`
3. Click "Generate Complete Analysis"
4. View 3-method VaR comparison

#### Robo Advisor
1. Click **Robo Advisor**
2. Answer 5 questions about risk tolerance
3. Click "Get Recommendations"
4. View personalized asset allocation

#### Tax Calculator
1. Go to **Tax Calculator**
2. Enter gross income: `1200000` (₹12 lakhs)
3. Select "Compare Both" regimes
4. Enter deductions if using old regime
5. Click "Calculate Tax"

---

## 🔧 Troubleshooting

### Issue: "Python is not recognized"
**Solution:** Reinstall Python and check "Add to PATH"

### Issue: "pip is not recognized"
**Solution:**
```bash
python -m ensurepip --upgrade
```

### Issue: "MySQL connection failed"
**Solution:**
1. Check MySQL is running (XAMPP Control Panel)
2. Verify database exists: `SHOW DATABASES;`
3. Check .env file has correct password
4. Try: `mysql -u root -p` to test connection

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
# Make sure venv is activated (should see (venv) in prompt)
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Or use different port
uvicorn backend.main:app --port 8001
```

### Issue: Database tables not created
**Solution:**
```bash
# Drop and recreate database
mysql -u root -p
DROP DATABASE finsight_db;
CREATE DATABASE finsight_db;
EXIT;

# Reinitialize
python -m backend.database.init_db
```

### Issue: Frontend returns 404
**Solution:** Files should be accessed via:
- http://localhost:8000 (redirects to frontend)
- http://localhost:8000/frontend/html/login.html

### Issue: "Access denied for user 'root'"
**Solution:**
```sql
# Reset MySQL root password
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';
FLUSH PRIVILEGES;

# Update .env with new password
```

---

## 📊 Verify Installation

### Check MySQL
```bash
mysql -u root -p
USE finsight_db;
SHOW TABLES;
```

Should show 11 tables.

### Check Python Packages
```bash
pip list | findstr fastapi
pip list | findstr mysql
```

### Check Application Health
Visit: http://localhost:8000/health

Should return:
```json
{
  "status": "healthy",
  "app": "FinSight AI",
  "version": "1.0.0"
}
```

---

## 🎓 Learning Resources

### Explore API Documentation
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Read Documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick reference guide
- [MYSQL_SETUP.md](MYSQL_SETUP.md) - Detailed MySQL setup
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - All API endpoints
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete feature list

### Test Features
1. **Portfolio Optimization** - Try different stock combinations
2. **VaR Calculator** - Compare risk calculation methods
3. **Robo Advisor** - Get investment recommendations
4. **Tax Calculator** - Compare tax regimes
5. **ML Predictions** - Upload time series data

---

## 🔐 Security Notes

- Change SECRET_KEY in .env (never use example key)
- Use strong MySQL password in production
- Keep .env file private (never commit to git)
- Passwords are hashed with bcrypt
- JWT tokens expire after 30 minutes

---

## 📞 Need Help?

1. **Check Logs:** Look at terminal output for errors
2. **MySQL Logs:** Check XAMPP logs if using XAMPP
3. **Review Documentation:** See MYSQL_SETUP.md
4. **API Errors:** Check http://localhost:8000/docs for endpoint details

---

## ✅ Setup Complete!

You should now have:
- ✅ Python virtual environment
- ✅ MySQL database with 11 tables
- ✅ Application running on port 8000
- ✅ Access to dashboard and API docs

**Next:** Register an account and start using the platform!

---

**Platform Status:** 🟢 Ready for use
**Documentation:** 📚 Complete
**Support:** See documentation files
