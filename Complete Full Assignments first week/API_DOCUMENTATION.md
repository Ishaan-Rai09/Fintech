# API Documentation - FinSight AI

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require JWT authentication via Bearer token.

**Header Format:**
```
Authorization: Bearer <your_jwt_token>
```

---

## 1. Authentication Endpoints

### 1.1 Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securePassword123",
  "full_name": "John Doe",
  "phone": "+1234567890"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe"
  }
}
```

### 1.2 Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
  }
}
```

### 1.3 Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true
  }
}
```

---

## 2. Portfolio Management

### 2.1 Optimize Portfolio
```http
POST /portfolio/optimize
Authorization: Bearer <token>
Content-Type: application/json

{
  "tickers": ["AAPL", "MSFT", "GOOGL"],
  "period": "1y"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "optimal_portfolio": {
      "weights": {
        "AAPL": 0.35,
        "MSFT": 0.42,
        "GOOGL": 0.23
      },
      "expected_return": 0.185,
      "volatility": 0.142,
      "sharpe_ratio": 1.304
    }
  }
}
```

### 2.2 Generate Efficient Frontier
```http
POST /portfolio/efficient-frontier
Authorization: Bearer <token>
Content-Type: application/json

{
  "tickers": ["AAPL", "MSFT", "GOOGL"],
  "period": "2y",
  "num_portfolios": 1000
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "portfolios": [
      {
        "return": 0.15,
        "volatility": 0.12,
        "sharpe_ratio": 1.25,
        "weights": [0.33, 0.33, 0.34]
      }
    ]
  }
}
```

---

## 3. Risk Management (VaR)

### 3.1 Dual Stock VaR Analysis (Capstone Feature)
```http
POST /risk/dual-stock-var
Authorization: Bearer <token>
Content-Type: application/json

{
  "ticker1": "AAPL",
  "ticker2": "MSFT",
  "weight1": 0.6,
  "weight2": 0.4,
  "portfolio_value": 100000,
  "confidence_level": 0.95,
  "period": "1y"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "portfolio_value": 100000,
    "portfolio_return": 0.152,
    "portfolio_volatility": 0.138,
    "correlation": 0.687,
    "var_historical": -0.0234,
    "var_parametric": -0.0227,
    "var_monte_carlo": -0.0241,
    "expected_shortfall": -0.0312
  }
}
```

### 3.2 Calculate VaR (Single Method)
```http
POST /risk/var
Authorization: Bearer <token>
Content-Type: application/json

{
  "ticker": "AAPL",
  "portfolio_value": 100000,
  "confidence_level": 0.95,
  "method": "historical"
}
```

---

## 4. Robo Advisory

### 4.1 Get Risk Questionnaire
```http
GET /robo-advisory/questionnaire
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "questions": [
      {
        "id": 1,
        "question": "What is your investment time horizon?",
        "options": [
          {"text": "Less than 3 years", "score": 1},
          {"text": "3-5 years", "score": 2},
          {"text": "5-10 years", "score": 3},
          {"text": "More than 10 years", "score": 4}
        ]
      }
    ]
  }
}
```

### 4.2 Get Investment Recommendations
```http
POST /robo-advisory/recommend
Authorization: Bearer <token>
Content-Type: application/json

{
  "risk_score": 7
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "risk_score": 7,
    "risk_category": "Moderate",
    "asset_allocation": {
      "stocks": 60,
      "bonds": 30,
      "cash": 5,
      "alternative": 5
    },
    "securities": {
      "stocks": ["SPY", "QQQ", "VTI"],
      "bonds": ["AGG", "BND"],
      "etfs": ["VT", "VXUS"]
    }
  }
}
```

---

## 5. Tax Calculator

### 5.1 Calculate Income Tax
```http
POST /tax/calculate
Authorization: Bearer <token>
Content-Type: application/json

{
  "gross_income": 1200000,
  "regime": "compare",
  "deductions": {
    "80C": 150000,
    "80D": 25000
  }
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "new_regime": {
      "gross_income": 1200000,
      "taxable_income": 1200000,
      "total_tax": 135000,
      "effective_tax_rate": 11.25
    },
    "old_regime": {
      "gross_income": 1200000,
      "total_deductions": 175000,
      "taxable_income": 1025000,
      "total_tax": 122500,
      "effective_tax_rate": 10.21
    }
  }
}
```

### 5.2 Get Tax Slabs
```http
GET /tax/slabs
Authorization: Bearer <token>
```

---

## 6. Time Series Predictions

### 6.1 Generate Forecast
```http
POST /predictions/forecast
Authorization: Bearer <token>
Content-Type: application/json

{
  "data": [
    {"date": "2024-01-01", "value": 100},
    {"date": "2024-01-02", "value": 102}
  ],
  "method": "auto",
  "periods": 30
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "method": "arima",
    "forecast": [
      {
        "value": 105.2,
        "lower_bound": 103.1,
        "upper_bound": 107.3
      }
    ],
    "metrics": {
      "aic": 245.3,
      "rmse": 2.15
    }
  }
}
```

---

## 7. Machine Learning

### 7.1 Train Model
```http
POST /ml/train
Authorization: Bearer <token>
Content-Type: application/json

{
  "data": [[1, 2], [2, 3], [3, 4]],
  "target": [10, 20, 30],
  "model_type": "random_forest",
  "model_name": "my_model_v1"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "model_filename": "my_model_v1_20240115.joblib",
    "metrics": {
      "mse": 0.15,
      "rmse": 0.39,
      "mae": 0.32,
      "r2": 0.95
    }
  }
}
```

### 7.2 Make Prediction
```http
POST /ml/predict
Authorization: Bearer <token>
Content-Type: application/json

{
  "model_filename": "my_model_v1_20240115.joblib",
  "data": [[4, 5], [5, 6]]
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "predictions": [40.2, 50.1]
  }
}
```

---

## 8. Compliance

### 8.1 Get Regulations
```http
GET /compliance/regulations?type=RBI
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "type": "RBI",
    "regulations": [
      "KYC norms as per RBI guidelines",
      "PML rules compliance required",
      "Transaction limits: Cash deposits >₹50,000 require PAN"
    ]
  }
}
```

### 8.2 Check Compliance
```http
POST /compliance/check
Authorization: Bearer <token>
Content-Type: application/json

{
  "transaction_type": "cash_deposit",
  "amount": 75000,
  "has_pan": true
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Invalid input data",
  "errors": {
    "field": "error details"
  }
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Authentication required"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Internal server error",
  "detail": "Error description"
}
```

---

## Rate Limiting
- 100 requests per minute per IP
- 1000 requests per hour per authenticated user

## WebSocket Support
Not currently implemented.

## Pagination
For endpoints returning lists:
```http
GET /endpoint?page=1&limit=50
```

---

For complete interactive documentation, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
