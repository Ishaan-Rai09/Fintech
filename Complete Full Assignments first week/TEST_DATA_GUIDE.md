# FinSight AI - Complete Test Data & API Guide

## 🚀 Quick Start

After logging in with Google OAuth, you'll have a JWT token stored in `localStorage`. This token is automatically sent with all API requests.

## 📊 Test Data for All Features

### 1. Portfolio Optimization

**CSV Sample (`portfolio_test.csv`):**
```csv
Symbol,Weight,ExpectedReturn,Volatility
AAPL,0.25,0.15,0.22
GOOGL,0.20,0.18,0.25
MSFT,0.15,0.14,0.20
AMZN,0.15,0.16,0.28
TSLA,0.10,0.20,0.35
JPM,0.10,0.09,0.18
JNJ,0.05,0.07,0.15
```

**API Endpoint:** `POST /api/v1/portfolio/optimize`
```json
{
  "symbols": ["AAPL", "GOOGL", "MSFT", "AMZN"],
  "start_date": "2023-01-01",
  "end_date": "2024-12-31",
  "risk_tolerance": "moderate"
}
```

**Features:**
- Efficient Frontier calculation
- Sharpe Ratio optimization
- Mean-Variance optimization
- Portfolio rebalancing suggestions

---

### 2. Risk Analysis (VaR)

**CSV  Sample (`risk_test.csv`):**
```csv
Date,Close,Returns
2024-01-01,150.25,0.0
2024-01-02,152.30,0.0136
2024-01-03,148.90,-0.0223
2024-01-04,151.20,0.0154
2024-01-05,149.80,-0.0093
2024-01-08,153.50,0.0247
2024-01-09,152.10,-0.0091
2024-01-10,154.80,0.0177
2024-01-11,153.20,-0.0103
2024-01-12,155.90,0.0176
```

**API Endpoints:**
1. **Historical VaR:** `POST /api/v1/risk/historical-var`
2. **Parametric VaR:** `POST /api/v1/risk/parametric-var`
3. **Monte Carlo VaR:** `POST /api/v1/risk/monte-carlo-var`
4. **Dual Stock VaR:** `POST /api/v1/risk/dual-stock-var`

**Sample Request (Dual Stock VaR):**
```json
{
  "stock1": "AAPL",
  "stock2": "GOOGL",
  "start_date": "2023-01-01",
  "end_date": "2024-12-31",
  "confidence_level": 0.95,
  "investment": 10000
}
```

---

### 3. ML Predictions

**CSV Sample (`predictions_test.csv`):**
```csv
Date,Open,High,Low,Close,Volume
2024-01-01,150.25,152.80,149.90,152.30,1234567
2024-01-02,152.40,154.20,151.80,153.90,1345678
2024-01-03,153.90,155.50,153.20,154.70,1456789
2024-01-04,154.80,156.30,154.20,155.90,1567890
2024-01-05,156.00,158.20,155.50,157.40,1678901
2024-01-08,157.50,159.80,157.00,158.90,1789012
2024-01-09,159.00,160.50,158.30,159.70,1890123
2024-01-10,159.80,161.20,159.20,160.50,1901234
```

**Available Models:**
1. **ARIMA:** `POST /api/v1/predictions/stock-arima`
2. **LSTM:** `POST /api/v1/predictions/stock-lstm`
3. **Sentiment Analysis:** `POST /api/v1/predictions/stock-sentiment`

**Sample Request (ARIMA):**
```json
{
  "symbol": "AAPL",
  "start_date": "2023-01-01",
  "end_date": "2024-12-31",
  "forecast_days": 30
}
```

**Expected Response:**
```json
{
  "predictions": [180.5, 181.2, 182.0, 181.8, 183.1],
  "confidence_intervals": {
    "lower": [178.0, 178.5, 179.0, 179.2, 180.0],
    "upper": [183.0, 183.9, 185.0, 184.4, 186.2]
  },
  "metrics": {
    "mae": 2.45,
    "rmse": 3.12,
    "mape": 1.35
  }
}
```

---

### 4. Robo Advisor

**API Endpoint:** `POST /api/v1/robo-advisory/questionnaire`

**Sample Questionnaire Response:**
```json
{
  "responses": {
    "age": 35,
    "income": 120000,
    "investment_amount": 50000,
    "goal": "wealth_building",
    "horizon": "long_term",
    "risk_comfort": "moderate"
  }
}
```

**Expected Response:**
```json
{
  "riskProfile": "Moderate",
  "recommendedAllocation": {
    "stocks": 70,
    "bonds": 20,
    "cash": 10
  },
  "portfolioSuggestions": [
    { "symbol": "VTI", "allocation": 40, "reason": "Total US Market" },
    { "symbol": "VXUS", "allocation": 30, "reason": "International Diversification" },
    { "symbol": "BND", "allocation": 20, "reason": "Bond Stability" },
    { "symbol": "VCSH", "allocation": 10, "reason": "Short-term Bonds" }
  ]
}
```

**Questionnaire Questions:**
1. What is your investment goal? (Retirement, Wealth Building, Income Generation, Capital Preservation)
2. What is your investment time horizon? (< 3 years, 3-5 years, 5-10 years, > 10 years)
3. How do you react to market volatility? (Sell immediately, Concerned but hold, Comfortable, Opportunity to buy more)
4. What is your annual income? (< $50K, $50K-$100K, $100K-$250K, > $250K)

---

### 5. Tax Calculator

**CSV Sample (`tax_test.csv`):**
```csv
Symbol,PurchaseDate,PurchasePrice,Shares,SaleDate,SalePrice
AAPL,2023-01-15,150.50,100,2024-12-31,185.30
GOOGL,2023-03-20,2800.00,20,2024-12-31,3100.00
MSFT,2022-06-10,280.00,50,2024-12-31,380.00
AMZN,2023-08-05,3200.00,15,2024-12-31,3500.00
TSLA,2022-11-12,180.00,75,2024-12-31,225.00
```

**API Endpoint:** `POST /api/v1/tax/calculate`

**Sample Request:**
```json
{
  "purchase_price": 15000,
  "sale_price": 18500,
  "holding_period": "long_term",
  "tax_bracket": "22%"
}
```

**Tax Rates:**
- **Short-term gains:** Taxed as ordinary income (10% to 37%)
- **Long-term gains (hold > 1 year):**
  - 0%: Income up to $44,625 (single) / $89,250 (married)
  - 15%: Income $44,625 to $492,300
  - 20%: Income above $492,300

---

### 6. Transaction Analysis & Fraud Detection

**CSV Sample (`transactions_test.csv`):**
```csv
TransactionID,Date,Amount,Category,Merchant,Location
TXN001,2024-01-15,125.50,Groceries,Walmart,New York
TXN002,2024-01-16,45.20,Gas,Shell,New York
TXN003,2024-01-16,2500.00,Electronics,BestBuy,New York
TXN004,2024-01-17,15.80,Food,McDonald's,New York
TXN005,2024-01-17,8500.00,Travel,Expedia,New York
TXN006,2024-01-18,30.00,Subscription,Netflix,Online
TXN007,2024-01-18,75.30,Groceries,Whole Foods,New York
TXN008,2024-01-19,12000.00,Electronics,Apple Store,California
TXN009,2024-01-19,18.50,Food,Starbucks,California
TXN010,2024-01-20,150.00,Utilities,ConEd,New York
```

**API Endpoint:** `POST /api/v1/transactions/analyze`
- Upload CSV file

**Fraud Detection Indicators:**
- Large unusual transactions
- Multiple transactions in short time
- Transactions in different locations
- Unusual merchant categories
- High-risk merchant types

**Expected Response:**
```json
{
  "summary": {
    "totalTransactions": 10,
    "totalAmount": 23522.30,
    "avgTransaction": 2352.23,
    "suspiciousCount": 2
  },
  "fraudDetected": true,
  "suspiciousTransactions": [
    { "id": "TXN005", "reason": "Unusually large amount", "riskScore": 0.85 },
    { "id": "TXN008", "reason": "Multiple locations same day", "riskScore": 0.72 }
  ],
  "categoryBreakdown": {
    "groceries": 200.80,
    "electronics": 14500.00,
    "travel": 8500.00
  }
}
```

---

### 7. Compliance Checker

**API Endpoint:** `GET /api/v1/compliance/regulations`

**Available Regulations:**
1. **MiFID II** (Markets in Financial Instruments Directive)
   - Best execution reporting
   - Transaction reporting
   - Client categorization
   - Product governance

2. **GDPR** (General Data Protection Regulation)
   - Data privacy protection
   - Right to be forgotten
   - Data breach notification
   - Consent management

3. **Dodd-Frank** (Wall Street Reform Act)
   - Volcker Rule compliance
   - Stress testing
   - Capital requirements
   - Risk management standards

---

### 8. Data Management

**Supported Formats:** CSV, Excel (.xlsx, .xls), JSON

**CSV Sample (`data_test.csv`):**
```csv
Date,Symbol,Open,High,Low,Close,Volume
2024-01-01,AAPL,180.25,182.50,179.80,182.30,45678900
2024-01-02,AAPL,182.40,184.20,181.90,183.50,48901234
2024-01-03,AAPL,183.60,185.30,182.50,184.90,52345678
2024-01-04,AAPL,184.80,186.50,183.90,185.70,49012345
2024-01-05,AAPL,185.90,187.20,185.30,186.50,51234567
```

**API Endpoint:** `POST /api/v1/data/upload`
- Content-Type: multipart/form-data
- Field: file

**Expected Response:**
```json
{
  "success": true,
  "summary": {
    "rows": 250,
    "columns": 7,
    "dateRange": "2023-01-01 to 2024-12-31",
    "symbols": ["AAPL", "GOOGL", "MSFT"],
    "missingValues": 3
  },
  "insights": {
    "correlations": { "AAPL-GOOGL": 0.85, "AAPL-MSFT": 0.78 },
    "volatility": { "AAPL": 0.22, "GOOGL": 0.25, "MSFT": 0.20 },
    "trends": { "AAPL": "upward", "GOOGL": "stable", "MSFT": "upward" }
  }
}
```

---

## 🔐 Authentication

All API requests require a Bearer token in the Authorization header:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

The token is automatically included by the JavaScript API functions after Google OAuth login.

**Get Current User:**
```
GET /api/v1/auth/me
```

**Logout:**
Simply remove the token from localStorage and redirect to landing page.

---

## 🧪 Testing APIs with cURL

**Example: Get Current User Info**
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Example: Calculate Tax**
```bash
curl -X POST http://localhost:8000/api/v1/tax/calculate \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "purchase_price": 15000,
    "sale_price": 18500,
    "holding_period": "long_term",
    "tax_bracket": "22%"
  }'
```

**Example: Portfolio Optimization**
```bash
curl -X POST http://localhost:8000/api/v1/portfolio/optimize \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": ["AAPL", "GOOGL", "MSFT"],
    "start_date": "2023-01-01",
    "end_date": "2024-12-31",
    "risk_tolerance": "moderate"
  }'
```

---

## 📝 Quick Test Steps

1. **Login via Google OAuth**
   - Go to http://localhost:8000
   - Click "Sign in with Google"
   - Authorize the app

2. **View Test Data**
   - Click "📊 View Test Data" button on dashboard
   - Browse samples for each feature
   - Copy CSV/JSON data

3. **Test Features:**
   - **Portfolio:** Go to Portfolio page, click "Optimize", enter symbols
   - **Risk:** Go to Risk Analysis, select VaR method, upload data
   - **Predictions:** Choose model (ARIMA/LSTM), enter symbol
   - **Robo Advisor:** Complete questionnaire
   - **Tax:** Upload transactions or enter manually
   - **Fraud Detection:** Upload transaction CSV

4. **Check API Documentation**
   - Visit: http://localhost:8000/docs
   - Interactive Swagger UI with all endpoints

---

## 🎯 Success Indicators

✅ OAuth login successful (token in localStorage)
✅ Dashboard displays user name
✅ API calls return data (not 403 errors)
✅ Test data modal opens and displays samples
✅ Each feature page loads correctly
✅ File uploads work  
✅ Results display properly

---

## 🐛 Troubleshooting

**403 Forbidden errors:**
- Check if logged in (token exists in localStorage)
- Token might be expired (logout and login again)
- Check network console for request headers

**API not responding:**
- Ensure backend is running: `python -m uvicorn backend.main:app --reload`
- Check server logs in terminal
- Verify MySQL is running

**OAuth not working:**
- Check Google OAuth credentials in .env
- Verify redirect URI matches: http://localhost:8000/api/v1/auth/google/callback

**Features not loading:**
- Clear browser cache
- Check browser console for JavaScript errors
- Refresh the page

---

## 📚 Additional Resources

- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **GitHub Repository:** [Your repo URL]

---

**Need Help?** Check the test data modal in the dashboard for interactive examples!
