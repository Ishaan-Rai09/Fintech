-- FinSight AI Database Schema
-- MySQL 8.0+ Database

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    transaction_date DATE NOT NULL,
    description TEXT,
    amount DECIMAL(15, 2) NOT NULL,
    category VARCHAR(100),
    transaction_type VARCHAR(50),
    is_suspicious BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolios table
CREATE TABLE IF NOT EXISTS portfolios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    total_value DECIMAL(15, 2) DEFAULT 0,
    cash_balance DECIMAL(15, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stocks table
CREATE TABLE IF NOT EXISTS stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker_symbol VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    industry VARCHAR(100),
    current_price DECIMAL(15, 4),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolio holdings
CREATE TABLE IF NOT EXISTS portfolio_holdings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolios(id) ON DELETE CASCADE,
    stock_id INTEGER REFERENCES stocks(id) ON DELETE CASCADE,
    quantity DECIMAL(15, 4) NOT NULL,
    purchase_price DECIMAL(15, 4) NOT NULL,
    purchase_date DATE NOT NULL,
    current_value DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    model_type VARCHAR(100) NOT NULL,
    prediction_type VARCHAR(100) NOT NULL,
    input_data TEXT,
    prediction_result TEXT,
    confidence_score DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Risk reports table
CREATE TABLE IF NOT EXISTS risk_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolios(id) ON DELETE CASCADE,
    report_date DATE NOT NULL,
    var_95 DECIMAL(15, 2),
    var_99 DECIMAL(15, 2),
    expected_shortfall DECIMAL(15, 2),
    method VARCHAR(50),
    timeframe VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tax records table
CREATE TABLE IF NOT EXISTS tax_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    financial_year VARCHAR(10) NOT NULL,
    gross_income DECIMAL(15, 2),
    deductions DECIMAL(15, 2),
    taxable_income DECIMAL(15, 2),
    tax_liability DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scraped data table
CREATE TABLE IF NOT EXISTS scraped_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    data_type VARCHAR(100),
    ticker_symbol VARCHAR(20),
    data_content TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Risk profiles table
CREATE TABLE IF NOT EXISTS risk_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    risk_score INTEGER CHECK (risk_score BETWEEN 1 AND 10),
    risk_category VARCHAR(50),
    time_horizon INTEGER,
    investment_goals TEXT,
    questionnaire_responses TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Advisory recommendations table
CREATE TABLE IF NOT EXISTS advisory_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    risk_profile_id INTEGER REFERENCES risk_profiles(id),
    asset_allocation TEXT,
    recommended_securities TEXT,
    rebalancing_strategy TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_portfolios_user_id ON portfolios(user_id);
CREATE INDEX IF NOT EXISTS idx_portfolio_holdings_portfolio_id ON portfolio_holdings(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_risk_reports_portfolio_id ON risk_reports(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_scraped_data_ticker ON scraped_data(ticker_symbol);
CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id);
