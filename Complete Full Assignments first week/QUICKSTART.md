# FinSight AI - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Python Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Install & Configure MySQL
```bash
# Install MySQL 8.0+ from https://dev.mysql.com/downloads/mysql/
# Or use XAMPP/WAMP which includes MySQL

# Start MySQL service
# Create database:
mysql -u root -p
CREATE DATABASE finsight_db;
EXIT;

# Copy environment template
copy .env.example .env

# Edit .env and set:
# - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_hex(32))")
# - DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/finsight_db
```

### Step 3: Initialize Database
```bash
python -m backend.database.init_db
```

### Step 4: Run the Application
```bash
python run.py
```

### Step 5: Access the Platform
Open your browser and navigate to:
- **Frontend Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🎯 First Steps

### 1. Register an Account
- Click "Register" on the homepage
- Fill in:
  - Username: `demo`
  - Email: `demo@example.com`
  - Password: `demo123456`
- Click "Register"

### 2. Login
- Use credentials from Step 1
- You'll be redirected to the dashboard

### 3. Try Key Features

#### Portfolio Optimization
1. Click "Portfolio" in navigation
2. Enter stock tickers: `AAPL,MSFT,GOOGL`
3. Select period: `1y`
4. Click "Optimize Portfolio"
5. View optimal weights and Sharpe ratio

#### VaR Risk Analysis (Capstone)
1. Navigate to "Capstone" or "Risk Analysis"
2. Enter:
   - Stock 1: `AAPL` (60% weight)
   - Stock 2: `MSFT` (40% weight)
   - Portfolio Value: `100000`
3. Click "Calculate VaR"
4. View 3-method comparison (Historical, Parametric, Monte Carlo)

#### Robo Advisory
1. Click "Robo Advisor"
2. Answer 5-question risk questionnaire
3. Get personalized investment recommendations
4. View asset allocation and securities

#### Tax Calculator
1. Go to "Tax Calculator"
2. Enter gross income: `1200000`
3. Select "Compare Both" regimes
4. Add deductions (80C, 80D)
5. View tax comparison and savings

---

## 📊 Sample Data

### Portfolio Optimization
```
Tickers: AAPL, MSFT, GOOGL, AMZN
Period: 1y or 2y
```

### VaR Analysis
```
Stock 1: AAPL (Weight: 60%)
Stock 2: MSFT (Weight: 40%)
Portfolio Value: $100,000
Confidence: 95%
```

### Time Series Forecasting
Upload CSV with columns:
- `date` (YYYY-MM-DD format)
- `value` (numeric)

Example:
```csv
date,value
2024-01-01,100
2024-01-02,102
2024-01-03,101
```

---

## 🔧 Troubleshooting

### Import Errors
```bash
# Ensure you're in virtual environment
pip install -r requirements.txt --upgrade
```

### Database Connection Issues
```bash
# Check DATABASE_URL in .env
# For quick start, use: sqlite:///./finsight.db

# Reinitialize database
python -m backend.database.init_db
```

### Port Already in Use
```bash
# Change port in run.py or use:
uvicorn backend.main:app --port 8001
```

### Frontend Not Loading
Check that static files are accessible:
```
http://localhost:8000/static/css/style.css
http://localhost:8000/static/js/api.js
```

### MySQL Connection Issues
```bash
# Verify MySQL is running
mysql -u root -p

# Check database exists
SHOW DATABASES;

# Verify connection string in .env
# Format: mysql+mysqlconnector://username:password@localhost:3306/database_name
```

---

## 📖 Next Steps

1. **Explore API Documentation**: http://localhost:8000/docs
2. **Read Full Documentation**:
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
   - [DEPLOYMENT.md](DEPLOYMENT.md)
   - [TESTING.md](TESTING.md)
3. **Try Advanced Features**:
   - ML model training
   - Transaction fraud detection
   - Web scraping
   - Compliance checking

---

## 💡 Key URLs

| Resource | URL |
|----------|-----|
| Dashboard | http://localhost:8000 |
| Login | http://localhost:8000/frontend/html/login.html |
| Portfolio | http://localhost:8000/frontend/html/portfolio.html |
| Risk Analysis | http://localhost:8000/frontend/html/risk.html |
| Capstone | http://localhost:8000/frontend/html/capstone.html |
| Robo Advisor | http://localhost:8000/frontend/html/robo-advisor.html |
| Tax Calculator | http://localhost:8000/frontend/html/tax.html |
| API Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

---

## 🎓 Learning Resources

### Understanding VaR (Capstone Feature)
- **Historical Simulation**: Sorts past returns, finds 5th percentile
- **Parametric VaR**: Uses normal distribution assumption (μ + σ × Z-score)
- **Monte Carlo**: Simulates 10,000 random scenarios

### Modern Portfolio Theory
- **Sharpe Ratio**: (Return - Risk-free rate) / Volatility
- **Efficient Frontier**: Optimal portfolios for given risk levels
- **Diversification**: Correlation reduces portfolio risk

### Tax Planning (Indian Context)
- **New Regime**: Lower rates, no deductions (FY 2025-26)
- **Old Regime**: Higher rates, allows 80C/80D deductions
- **Compare**: Platform shows which saves more

---

## ⚠️ Production Checklist

Before deploying to production:
- [ ] Change SECRET_KEY in .env
- [ ] Use strong MySQL password
- [ ] Enable HTTPS/SSL
- [ ] Set DEBUG=False
- [ ] Configure proper CORS origins
- [ ] Set up authentication rate limiting
- [ ] Enable logging and monitoring
- [ ] Backup MySQL database regularly
- [ ] Run security audit
- [ ] Update all dependencies

---

## 📞 Support

- **Issues**: Create a GitHub issue
- **Documentation**: Check [README.md](README.md)
- **API Reference**: http://localhost:8000/docs

---

**Happy Trading & Analysis! 🚀📈**
