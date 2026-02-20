# FinSight AI Testing Suite

## Overview
This document outlines the testing strategy for the FinSight AI platform.

## Test Coverage Goals
- Unit Tests: 80%+
- Integration Tests: 70%+
- API Tests: 100% of endpoints

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### With Coverage
```bash
pytest --cov=backend --cov-report=html tests/
```

### Specific Test File
```bash
pytest tests/test_api/test_portfolio.py -v
```

### Load Testing
```bash
locust -f tests/load_test.py --host=http://localhost:8000
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_api/
│   ├── test_auth.py         # Authentication tests
│   ├── test_portfolio.py    # Portfolio optimization tests
│   ├── test_risk.py         # VaR calculation tests
│   ├── test_robo_advisory.py
│   ├── test_tax.py
│   ├── test_ml.py
│   └── test_predictions.py
├── test_services/
│   ├── test_portfolio_service.py
│   ├── test_var_calculator.py
│   ├── test_robo_advisor.py
│   └── test_tax_calculator.py
├── test_ml/
│   ├── test_pipeline.py
│   ├── test_models.py
│   └── test_time_series.py
└── load_test.py             # Locust load testing
```

## Sample Tests

### conftest.py (Fixtures)
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.database.connection import Base, get_db
from backend.models import User

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    from backend.middleware.security import hash_password
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpassword"),
        full_name="Test User"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def auth_token(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    return response.json()["data"]["access_token"]
```

### test_auth.py
```python
def test_register_user(client):
    response = client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "newpassword123"
    })
    assert response.status_code == 201
    assert response.json()["success"] == True
    assert response.json()["data"]["username"] == "newuser"

def test_login_success(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()["data"]

def test_login_invalid_credentials(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_current_user(client, auth_token):
    response = client.get("/api/v1/auth/me", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.json()["data"]["username"] == "testuser"
```

### test_portfolio.py
```python
def test_optimize_portfolio(client, auth_token):
    response = client.post("/api/v1/portfolio/optimize", 
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "tickers": ["AAPL", "MSFT", "GOOGL"],
            "period": "1y"
        }
    )
    assert response.status_code == 200
    assert "optimal_portfolio" in response.json()["data"]
    assert "sharpe_ratio" in response.json()["data"]["optimal_portfolio"]

def test_efficient_frontier(client, auth_token):
    response = client.post("/api/v1/portfolio/efficient-frontier",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "tickers": ["AAPL", "MSFT"],
            "period": "1y",
            "num_portfolios": 100
        }
    )
    assert response.status_code == 200
    assert len(response.json()["data"]["portfolios"]) == 100
```

### test_risk.py (VaR Tests)
```python
def test_dual_stock_var(client, auth_token):
    response = client.post("/api/v1/risk/dual-stock-var",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "ticker1": "AAPL",
            "ticker2": "MSFT",
            "weight1": 0.6,
            "weight2": 0.4,
            "portfolio_value": 100000,
            "confidence_level": 0.95,
            "period": "1y"
        }
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert "var_historical" in data
    assert "var_parametric" in data
    assert "var_monte_carlo" in data
    assert "expected_shortfall" in data
    
    # Validate VaR values are negative (representing losses)
    assert data["var_historical"] < 0
    assert data["var_parametric"] < 0
    assert data["var_monte_carlo"] < 0
```

### test_var_calculator.py (Service Tests)
```python
import pytest
from backend.services.var_calculator import VaRCalculator

def test_historical_var():
    calculator = VaRCalculator()
    returns = [-0.02, -0.01, 0.01, 0.02, 0.015, -0.005]
    var = calculator.historical_simulation(returns, confidence_level=0.95)
    assert var < 0  # VaR should be negative
    assert -0.05 < var < 0  # Reasonable range

def test_parametric_var():
    calculator = VaRCalculator()
    returns = [0.01, -0.01, 0.02, -0.015, 0.005]
    var = calculator.parametric_var(returns, confidence_level=0.95)
    assert var < 0

def test_monte_carlo_var():
    calculator = VaRCalculator()
    mean_return = 0.001
    std_return = 0.02
    var = calculator.monte_carlo_var(mean_return, std_return, days=1, simulations=1000)
    assert var < 0
```

### load_test.py (Locust)
```python
from locust import HttpUser, task, between

class FinSightUser(HttpUser):
    wait_time = between(1, 3)
    token = None
    
    def on_start(self):
        # Register and login
        self.client.post("/api/v1/auth/register", json={
            "username": f"testuser_{self.environment.parsed_options.num_users}",
            "email": f"test_{self.environment.parsed_options.num_users}@example.com",
            "password": "testpassword"
        })
        
        response = self.client.post("/api/v1/auth/login", json={
            "username": f"testuser_{self.environment.parsed_options.num_users}",
            "password": "testpassword"
        })
        self.token = response.json()["data"]["access_token"]
    
    @task(3)
    def get_current_user(self):
        self.client.get("/api/v1/auth/me", headers={
            "Authorization": f"Bearer {self.token}"
        })
    
    @task(2)
    def optimize_portfolio(self):
        self.client.post("/api/v1/portfolio/optimize", 
            headers={"Authorization": f"Bearer {self.token}"},
            json={"tickers": ["AAPL", "MSFT"], "period": "1y"}
        )
    
    @task(1)
    def calculate_var(self):
        self.client.post("/api/v1/risk/dual-stock-var",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "ticker1": "AAPL",
                "ticker2": "MSFT",
                "weight1": 0.6,
                "weight2": 0.4,
                "portfolio_value": 100000,
                "confidence_level": 0.95
            }
        )
```

## CI/CD Integration

### GitHub Actions (.github/workflows/test.yml)
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=backend --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Performance Benchmarks

Expected performance targets:
- API response time: <100ms (p95)
- VaR calculation: <3s (Monte Carlo 10k simulations)
- Portfolio optimization: <1s
- Database queries: <50ms
- Concurrent users: 1000+

## Testing Checklist

- [ ] All API endpoints have tests
- [ ] Service layer unit tests complete
- [ ] ML models validated
- [ ] Authentication flows tested
- [ ] Error handling verified
- [ ] Edge cases covered
- [ ] Load testing passed
- [ ] Security vulnerabilities scanned
- [ ] Database migrations tested
- [ ] Frontend integration tested
