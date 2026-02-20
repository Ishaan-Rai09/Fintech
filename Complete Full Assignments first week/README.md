# FinSight AI – End-to-End FinTech Analytics & Robo Advisory Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🚀 Overview

FinSight AI is a comprehensive web-based financial analytics and robo-advisory platform that enables users to:

- ✅ Analyze financial transactions and detect fraud
- ✅ Perform time-series forecasting
- ✅ Conduct portfolio optimization
- ✅ Calculate financial risk (VaR)
- ✅ Scrape financial market data
- ✅ Build investment strategies
- ✅ Visualize market trends
- ✅ Automate advisory decisions

## 🏗 Architecture

```
Frontend (HTML/CSS/JS)
      ↓ REST API
Backend (Python FastAPI)
      ↓
Data Layer (MySQL)
      ↓
ML Engine (Scikit-Learn)
      ↓
Scraping Engine (Selenium)
```

## 📦 Installation

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- Redis (optional, for caching)
- 4GB RAM minimum

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd "Complete Full Assignments first week"
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup MySQL database**
```bash
# Create database in MySQL
mysql -u root -p
CREATE DATABASE finsight_db;
EXIT;
```

5. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
# DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/finsight_db
```

6. **Initialize database**
```bash
python backend/database/init_db.py
```

6. **Run the application**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access the application**
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## 📚 API Documentation

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user profile

### Data Management
- `POST /api/v1/data/upload` - Upload CSV/Excel/JSON data
- `GET /api/v1/data/fetch` - Fetch data from external APIs
- `POST /api/v1/data/clean` - Clean and normalize data

### Transactions
- `GET /api/v1/transactions/summary` - Get transaction summary
- `POST /api/v1/transactions/analyze` - Analyze transactions
- `GET /api/v1/transactions/suspicious` - Detect fraud

### Machine Learning
- `POST /api/v1/ml/train` - Train ML model
- `POST /api/v1/ml/predict` - Make predictions
- `GET /api/v1/ml/models` - List available models

### Predictions
- `POST /api/v1/predictions/forecast` - Time-series forecast

### Portfolio
- `POST /api/v1/portfolio/create` - Create portfolio
- `POST /api/v1/portfolio/optimize` - Optimize asset allocation
- `GET /api/v1/portfolio/performance` - Get performance metrics

### Risk Management
- `POST /api/v1/risk/var` - Calculate Value at Risk
- `POST /api/v1/risk/monte-carlo` - Run Monte Carlo simulation
- `GET /api/v1/risk/report` - Generate risk report

### Robo Advisory
- `POST /api/v1/advisory/profile` - Create risk profile
- `POST /api/v1/advisory/recommend` - Get investment recommendations
- `POST /api/v1/advisory/strategy` - Generate investment strategy

### Tax
- `POST /api/v1/tax/calculate` - Calculate tax liability
- `GET /api/v1/tax/report` - Generate tax report

### Compliance
- `POST /api/v1/compliance/check` - Check regulatory compliance
- `GET /api/v1/compliance/regulations` - List regulations

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_api/test_auth.py

# Load testing
locust -f tests/load_test.py
```

## 📊 Project Structure

```
FinSight-AI/
│
├── backend/
│   ├── api/              # API endpoints
│   ├── models/           # Database models
│   ├── services/         # Business logic
│   ├── ml/               # ML pipelines
│   ├── scrapers/         # Web scrapers
│   ├── middleware/       # Security & auth
│   └── database/         # DB connection
│
├── frontend/
│   ├── html/             # HTML pages
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript
│
├── database/
│   └── schema.sql        # Database schema
│
├── tests/                # Test suite
├── docs/                 # Documentation
├── models/               # Trained ML models
└── logs/                 # Application logs
```

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting on API endpoints
- SQL injection protection
- Input validation
- HTTPS enforcement

## 📈 Performance Targets

- API Response: < 300ms
- Page Load: < 2s
- Uptime: 99.5%
- Concurrent Users: 1000+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 👥 Team

Built as a comprehensive FinTech learning project.

## 📞 Support

For issues and questions, please open a GitHub issue.

---

**Built with ❤️ using Python, FastAPI, and modern ML libraries**
