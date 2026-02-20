# Test Data Files

These CSV files contain sample data ready to use for testing all FinSight AI features.

## Files Overview

### 1. `portfolio_test.csv`
**Use for:** Portfolio Optimization
- Contains 7 different stock symbols
- Includes weights, expected returns, and volatility
- Test portfolio optimization algorithms
- Calculate efficient frontier

### 2. `risk_test.csv`
**Use for:** Risk Analysis & VaR Calculation
- Historical stock price data with returns
- Test all 3 VaR methods:
  * Historical VaR
  * Parametric VaR
  * Monte Carlo VaR
- 15 days of sample data

### 3. `predictions_test.csv`
**Use for:** ML Predictions (ARIMA, LSTM)
- OHLCV (Open, High, Low, Close, Volume) data
- 15 days of historical data
- Test time series forecasting
- Compare different prediction models

### 4. `tax_test.csv`
**Use for:** Tax Calculator
- 7 sample stock transactions
- Mix of short-term and long-term holdings
- Test capital gains calculations
- Calculate tax optimization strategies

### 5. `transactions_test.csv`
**Use for:** Transaction Analysis & Fraud Detection
- 20 sample transactions
- Various categories (groceries, electronics, travel, etc.)
- Includes suspicious patterns for fraud detection:
  * Large unusual amounts (TXN005, TXN008)
  * Multiple locations same day (TXN008, TXN009)
  * Unusual spending patterns

## How to Use

1. **Dashboard Method:**
   - Log in to FinSight AI
   - Click "📊 View Test Data" button
   - Browse samples and copy data
   - Or click "View Sample →" on any feature card

2. **Direct Upload:**
   - Navigate to the specific feature page
   - Click the upload button
   - Select the corresponding CSV file from this folder
   - Submit and view results

3. **Copy-Paste:**
   - Open any CSV file in a text editor
   - Copy the contents
   - Paste into online CSV generators if needed
   - Or use directly in API calls

## Expected Results

### Portfolio Optimization
- Efficient frontier graph
- Optimal portfolio weights
- Sharpe ratio: ~1.2-1.8
- Expected return: 12-18%

### Risk Analysis
- VaR at 95% confidence: $800-$1,200
- Risk metrics visualization
- Historical volatility chart

### Predictions
- 30-day price forecast
- Confidence intervals
- MAE: 2-4, RMSE: 3-5
- Accuracy plot

### Tax Calculator
- Total capital gains: $16,480
- Estimated tax (15% rate): $2,472
- Net profit after tax: $14,008

### Fraud Detection
- 2-3 suspicious transactions detected
- Risk scores: 0.72-0.85
- Category breakdown chart
- Alert recommendations

## API Testing

You can also use these data structures in API calls:

```bash
# Example: Risk Analysis
curl -X POST http://localhost:8000/api/v1/risk/dual-stock-var \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stock1": "AAPL",
    "stock2": "GOOGL",
    "confidence_level": 0.95,
    "investment": 10000
  }'
```

## Need More Data?

Generate additional test data:
1. Use the dashboard modal to view JSON samples
2. Modify existing CSVs with your own values
3. Add more rows following the same format
4. Check `TEST_DATA_GUIDE.md` for detailed API examples

## Troubleshooting

**File won't upload:**
- Check file format (must be .csv)
- Verify columns match exactly
- Remove any extra blank lines

**API returns errors:**
- Ensure you're logged in (token exists)
- Check date formats: YYYY-MM-DD
- Verify numeric values are numbers, not text

**Results look wrong:**
- Check for missing values
- Verify data ranges are realistic
- Ensure dates are in chronological order

---

**Pro Tip:** Use the "View Test Data" modal in the dashboard for interactive samples and API examples!
