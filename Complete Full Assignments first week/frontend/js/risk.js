// Risk Analysis & VaR Calculator

document.addEventListener('DOMContentLoaded', () => {
    // Dual Stock VaR Form
    const dualStockForm = document.getElementById('dualStockForm');
    if (dualStockForm) {
        dualStockForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const ticker1 = document.getElementById('ticker1').value.trim().toUpperCase();
            const ticker2 = document.getElementById('ticker2').value.trim().toUpperCase();
            const weight1 = parseFloat(document.getElementById('weight1').value) / 100;
            const weight2 = parseFloat(document.getElementById('weight2').value) / 100;
            const portfolioValue = parseFloat(document.getElementById('portfolioValue').value);
            const confidence = parseFloat(document.getElementById('confidence').value);
            
            // Validate weights sum to 100%
            if (Math.abs((weight1 + weight2) - 1.0) > 0.01) {
                alert('Weights must sum to 100%');
                return;
            }
            
            showLoading('varResults');
            
            try {
                const response = await RiskAPI.dualStockVaR({
                    ticker1,
                    ticker2,
                    weight1,
                    weight2,
                    portfolio_value: portfolioValue,
                    confidence_level: confidence,
                    period: '1y'
                });
                
                if (response.success) {
                    displayVaRResults(response.data);
                } else {
                    document.getElementById('varResults').innerHTML = 
                        `<div class="alert alert-danger">${response.message}</div>`;
                }
            } catch (error) {
                document.getElementById('varResults').innerHTML = 
                    `<div class="alert alert-danger">${error.message}</div>`;
            }
        });
    }
});

function displayVaRResults(data) {
    let html = '<div class="alert alert-success">VaR calculated successfully!</div>';
    
    // Portfolio Summary
    html += '<div class="card">';
    html += '<h3>Portfolio Summary</h3>';
    html += '<table>';
    html += `<tr><td>Portfolio Value</td><td>${formatCurrency(data.portfolio_value)}</td></tr>`;
    html += `<tr><td>Expected Return</td><td>${formatPercentage(data.portfolio_return)}</td></tr>`;
    html += `<tr><td>Portfolio Volatility</td><td>${formatPercentage(data.portfolio_volatility)}</td></tr>`;
    html += `<tr><td>Correlation</td><td>${data.correlation.toFixed(4)}</td></tr>`;
    html += '</table>';
    html += '</div>';
    
    // VaR Methods Comparison
    html += '<div class="card">';
    html += '<h3>Value at Risk - 3 Method Comparison</h3>';
    html += '<table>';
    html += '<tr><th>Method</th><th>VaR (1-day)</th><th>Loss Amount</th></tr>';
    
    if (data.var_historical !== undefined) {
        const lossHistorical = data.portfolio_value * data.var_historical;
        html += `<tr><td><strong>Historical Simulation</strong></td><td>${formatPercentage(data.var_historical)}</td><td>${formatCurrency(lossHistorical)}</td></tr>`;
    }
    
    if (data.var_parametric !== undefined) {
        const lossParametric = data.portfolio_value * data.var_parametric;
        html += `<tr><td><strong>Parametric (Variance-Covariance)</strong></td><td>${formatPercentage(data.var_parametric)}</td><td>${formatCurrency(lossParametric)}</td></tr>`;
    }
    
    if (data.var_monte_carlo !== undefined) {
        const lossMonteCarlo = data.portfolio_value * data.var_monte_carlo;
        html += `<tr><td><strong>Monte Carlo Simulation</strong></td><td>${formatPercentage(data.var_monte_carlo)}</td><td>${formatCurrency(lossMonteCarlo)}</td></tr>`;
    }
    
    html += '</table>';
    html += '</div>';
    
    // Expected Shortfall (CVaR)
    if (data.expected_shortfall !== undefined) {
        html += '<div class="card">';
        html += '<h3>Expected Shortfall (CVaR)</h3>';
        html += '<p>Expected loss given that VaR threshold is exceeded:</p>';
        html += '<table>';
        html += `<tr><td>CVaR</td><td>${formatPercentage(data.expected_shortfall)}</td></tr>`;
        html += `<tr><td>Expected Loss Amount</td><td>${formatCurrency(data.portfolio_value * data.expected_shortfall)}</td></tr>`;
        html += '</table>';
        html += '</div>';
    }
    
    // Interpretation
    html += '<div class="alert alert-info">';
    html += '<h4>Interpretation:</h4>';
    html += '<ul>';
    html += '<li><strong>Historical Simulation:</strong> Based on actual historical returns</li>';
    html += '<li><strong>Parametric VaR:</strong> Assumes normal distribution of returns</li>';
    html += '<li><strong>Monte Carlo:</strong> Simulates 10,000 possible scenarios</li>';
    html += `<li>At ${(data.confidence_level || 0.95) * 100}% confidence level, the maximum expected loss is shown above</li>`;
    html += '</ul>';
    html += '</div>';
    
    document.getElementById('varResults').innerHTML = html;
}
