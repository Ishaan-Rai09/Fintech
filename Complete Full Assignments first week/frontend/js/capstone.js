// Capstone Project Dashboard - Comprehensive VaR Analysis

document.addEventListener('DOMContentLoaded', () => {
    const capstoneForm = document.getElementById('capstoneForm');
    if (capstoneForm) {
        capstoneForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const stock1 = document.getElementById('stock1').value.trim().toUpperCase();
            const stock2 = document.getElementById('stock2').value.trim().toUpperCase();
            const weight1 = parseFloat(document.getElementById('weight1').value) / 100;
            const weight2 = parseFloat(document.getElementById('weight2').value) / 100;
            const portfolioValue = parseFloat(document.getElementById('portfolioValue').value);
            const period = document.getElementById('period').value;
            
            // Validate weights
            if (Math.abs((weight1 + weight2) - 1.0) > 0.01) {
                alert('Weights must sum to 100%');
                return;
            }
            
            showLoading('capstoneResults');
            
            try {
                // Calculate VaR using all three methods
                const varResponse = await RiskAPI.dualStockVaR({
                    ticker1: stock1,
                    ticker2: stock2,
                    weight1,
                    weight2,
                    portfolio_value: portfolioValue,
                    confidence_level: 0.95,
                    period
                });
                
                // Get portfolio performance metrics
                const performanceResponse = await PortfolioAPI.getPerformance({
                    tickers: [stock1, stock2],
                    weights: [weight1, weight2],
                    period
                });
                
                if (varResponse.success) {
                    displayCapstoneResults(varResponse.data, performanceResponse.data);
                } else {
                    document.getElementById('capstoneResults').innerHTML = 
                        `<div class="alert alert-danger">${varResponse.message}</div>`;
                }
            } catch (error) {
                document.getElementById('capstoneResults').innerHTML = 
                    `<div class="alert alert-danger">${error.message}</div>`;
            }
        });
    }
});

function displayCapstoneResults(varData, performanceData) {
    let html = '<div class="alert alert-success">✅ Comprehensive analysis complete!</div>';
    
    // Executive Summary Card
    html += '<div class="card">';
    html += '<h3>📊 Executive Summary</h3>';
    html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">';
    
    html += '<div class="stat-card">';
    html += '<h4>Portfolio Value</h4>';
    html += `<div class="value">${formatCurrency(varData.portfolio_value)}</div>`;
    html += '</div>';
    
    html += '<div class="stat-card">';
    html += '<h4>Expected Return</h4>';
    html += `<div class="value">${formatPercentage(varData.portfolio_return)}</div>`;
    html += '</div>';
    
    html += '<div class="stat-card">';
    html += '<h4>Volatility</h4>';
    html += `<div class="value">${formatPercentage(varData.portfolio_volatility)}</div>`;
    html += '</div>';
    
    html += '<div class="stat-card">';
    html += '<h4>Correlation</h4>';
    html += `<div class="value">${varData.correlation.toFixed(3)}</div>`;
    html += '</div>';
    
    html += '</div>';
    html += '</div>';
    
    // Portfolio Composition
    html += '<div class="card">';
    html += '<h3>💼 Portfolio Composition</h3>';
    html += '<table>';
    html += '<tr><th>Stock</th><th>Weight</th><th>Return (Period)</th><th>Volatility</th></tr>';
    html += `<tr><td><strong>${varData.ticker1 || 'Stock 1'}</strong></td><td>${formatPercentage(varData.weight1)}</td>`;
    html += `<td>${varData.stock1_return ? formatPercentage(varData.stock1_return) : 'N/A'}</td>`;
    html += `<td>${varData.stock1_volatility ? formatPercentage(varData.stock1_volatility) : 'N/A'}</td></tr>`;
    html += `<tr><td><strong>${varData.ticker2 || 'Stock 2'}</strong></td><td>${formatPercentage(varData.weight2)}</td>`;
    html += `<td>${varData.stock2_return ? formatPercentage(varData.stock2_return) : 'N/A'}</td>`;
    html += `<td>${varData.stock2_volatility ? formatPercentage(varData.stock2_volatility) : 'N/A'}</td></tr>`;
    html += '</table>';
    html += '</div>';
    
    // VaR Analysis - 3 Methods Comparison (MAIN CAPSTONE FEATURE)
    html += '<div class="card">';
    html += '<h3>⚠️ Value at Risk - 3 Method Comparison (95% Confidence)</h3>';
    html += '<p>Maximum expected loss over 1 day at 95% confidence level:</p>';
    
    html += '<table>';
    html += '<tr><th>Method</th><th>VaR (%)</th><th>Loss Amount</th><th>Description</th></tr>';
    
    // Historical Simulation VaR
    if (varData.var_historical !== undefined) {
        const lossHistorical = varData.portfolio_value * Math.abs(varData.var_historical);
        html += `<tr>`;
        html += `<td><strong>1. Historical Simulation</strong></td>`;
        html += `<td>${formatPercentage(Math.abs(varData.var_historical))}</td>`;
        html += `<td>${formatCurrency(lossHistorical)}</td>`;
        html += `<td>Uses actual historical returns to estimate risk</td>`;
        html += `</tr>`;
    }
    
    // Parametric VaR (Variance-Covariance)
    if (varData.var_parametric !== undefined) {
        const lossParametric = varData.portfolio_value * Math.abs(varData.var_parametric);
        html += `<tr>`;
        html += `<td><strong>2. Parametric (Var-Cov)</strong></td>`;
        html += `<td>${formatPercentage(Math.abs(varData.var_parametric))}</td>`;
        html += `<td>${formatCurrency(lossParametric)}</td>`;
        html += `<td>Assumes normal distribution of returns</td>`;
        html += `</tr>`;
    }
    
    // Monte Carlo Simulation VaR
    if (varData.var_monte_carlo !== undefined) {
        const lossMonteCarlo = varData.portfolio_value * Math.abs(varData.var_monte_carlo);
        html += `<tr>`;
        html += `<td><strong>3. Monte Carlo Simulation</strong></td>`;
        html += `<td>${formatPercentage(Math.abs(varData.var_monte_carlo))}</td>`;
        html += `<td>${formatCurrency(lossMonteCarlo)}</td>`;
        html += `<td>Simulates 10,000 random scenarios</td>`;
        html += `</tr>`;
    }
    
    html += '</table>';
    
    // Method Comparison Analysis
    html += '<div class="alert alert-info" style="margin-top: 1rem;">';
    html += '<h4>📈 Method Comparison Analysis:</h4>';
    html += '<ul>';
    html += '<li><strong>Historical Simulation:</strong> Non-parametric method using actual past returns. Best for capturing tail risks and fat tails.</li>';
    html += '<li><strong>Parametric VaR:</strong> Fast and simple, assumes normal distribution. May underestimate extreme events.</li>';
    html += '<li><strong>Monte Carlo:</strong> Most flexible, can model complex distributions and scenarios. Computationally intensive.</li>';
    html += '</ul>';
    
    // Calculate variance between methods
    const varValues = [
        varData.var_historical,
        varData.var_parametric,
        varData.var_monte_carlo
    ].filter(v => v !== undefined).map(Math.abs);
    
    if (varValues.length === 3) {
        const maxVar = Math.max(...varValues);
        const minVar = Math.min(...varValues);
        const variance = ((maxVar - minVar) / minVar * 100).toFixed(2);
        html += `<p><strong>Variance between methods:</strong> ${variance}% - `;
        if (variance < 10) {
            html += 'Methods show <strong>good agreement</strong> ✅';
        } else if (variance < 20) {
            html += 'Methods show <strong>moderate variance</strong> ⚠️';
        } else {
            html += 'Methods show <strong>significant divergence</strong> - consider reviewing assumptions ⚠️';
        }
        html += '</p>';
    }
    html += '</div>';
    html += '</div>';
    
    // Expected Shortfall (CVaR)
    if (varData.expected_shortfall !== undefined) {
        html += '<div class="card">';
        html += '<h3>💥 Expected Shortfall (CVaR)</h3>';
        html += '<p>Average loss when VaR threshold is exceeded (worse-case scenario):</p>';
        html += '<table>';
        html += `<tr><td><strong>CVaR (95%)</strong></td><td>${formatPercentage(Math.abs(varData.expected_shortfall))}</td></tr>`;
        html += `<tr><td><strong>Expected Loss Amount</strong></td><td>${formatCurrency(varData.portfolio_value * Math.abs(varData.expected_shortfall))}</td></tr>`;
        html += '</table>';
        html += '<div class="alert alert-warning" style="margin-top: 1rem;">';
        html += 'CVaR provides a more comprehensive risk measure than VaR as it captures the tail risk beyond the VaR threshold.';
        html += '</div>';
        html += '</div>';
    }
    
    // Risk Metrics Dashboard
    html += '<div class="card">';
    html += '<h3>📊 Additional Risk Metrics</h3>';
    html += '<table>';
    if (performanceData && performanceData.sharpe_ratio !== undefined) {
        html += `<tr><td>Sharpe Ratio</td><td>${performanceData.sharpe_ratio.toFixed(4)}</td></tr>`;
    }
    if (performanceData && performanceData.sortino_ratio !== undefined) {
        html += `<tr><td>Sortino Ratio</td><td>${performanceData.sortino_ratio.toFixed(4)}</td></tr>`;
    }
    if (performanceData && performanceData.max_drawdown !== undefined) {
        html += `<tr><td>Maximum Drawdown</td><td>${formatPercentage(performanceData.max_drawdown)}</td></tr>`;
    }
    html += `<tr><td>Portfolio Beta (Market)</td><td>${varData.beta !== undefined ? varData.beta.toFixed(4) : 'N/A'}</td></tr>`;
    html += '</table>';
    html += '</div>';
    
    // Stress Testing Scenarios
    html += '<div class="card">';
    html += '<h3>🔥 Stress Testing Scenarios</h3>';
    html += '<table>';
    html += '<tr><th>Scenario</th><th>Portfolio Loss</th></tr>';
    html += `<tr><td>1-Day 1% Market Drop</td><td>${formatCurrency(varData.portfolio_value * 0.01)}</td></tr>`;
    html += `<tr><td>1-Day 5% Market Drop</td><td>${formatCurrency(varData.portfolio_value * 0.05)}</td></tr>`;
    html += `<tr><td>1-Day 10% Market Crash</td><td>${formatCurrency(varData.portfolio_value * 0.10)}</td></tr>`;
    html += `<tr><td>VaR Threshold (95%)</td><td>${formatCurrency(varData.portfolio_value * Math.abs(varData.var_historical || varData.var_parametric || 0.02))}</td></tr>`;
    html += '</table>';
    html += '</div>';
    
    // Recommendations
    html += '<div class="card">';
    html += '<h3>💡 Risk Management Recommendations</h3>';
    html += '<ul class="feature-list">';
    
    if (varData.portfolio_volatility > 0.25) {
        html += '<li>⚠️ High volatility detected - consider diversification or hedging strategies</li>';
    } else {
        html += '<li>✅ Portfolio volatility is within acceptable range</li>';
    }
    
    if (Math.abs(varData.correlation) > 0.7) {
        html += '<li>⚠️ High correlation between stocks - limited diversification benefit</li>';
    } else if (Math.abs(varData.correlation) < 0.3) {
        html += '<li>✅ Low correlation provides good diversification</li>';
    } else {
        html += '<li>✓ Moderate correlation between stocks</li>';
    }
    
    const avgVar = varValues.reduce((a, b) => a + b, 0) / varValues.length;
    if (avgVar > 0.05) {
        html += '<li>⚠️ VaR exceeds 5% - consider risk reduction strategies</li>';
    }
    
    html += '<li>✓ Monitor position limits and stop-loss levels based on VaR calculations</li>';
    html += '<li>✓ Review and rebalance portfolio quarterly</li>';
    html += '<li>✓ Consider implementing hedging strategies (options, futures) for downside protection</li>';
    html += '</ul>';
    html += '</div>';
    
    // Methodology & Technical Details
    html += '<div class="card">';
    html += '<h3>📘 Methodology & Technical Details</h3>';
    html += '<div class="alert alert-info">';
    html += '<h4>VaR Calculation Methodologies:</h4>';
    html += '<ol>';
    html += '<li><strong>Historical Simulation:</strong>';
    html += '<ul>';
    html += '<li>Sorts historical returns and finds 5th percentile (95% confidence)</li>';
    html += '<li>No distributional assumptions required</li>';
    html += '<li>Limited by available historical data</li>';
    html += '</ul></li>';
    html += '<li><strong>Parametric VaR (Variance-Covariance):</strong>';
    html += '<ul>';
    html += '<li>Calculates using formula: VaR = μ + σ × Z-score</li>';
    html += '<li>Z-score for 95% confidence: -1.645</li>';
    html += '<li>Assumes normally distributed returns</li>';
    html += '</ul></li>';
    html += '<li><strong>Monte Carlo Simulation:</strong>';
    html += '<ul>';
    html += '<li>Generates 10,000 random scenarios using Cholesky decomposition</li>';
    html += '<li>Accounts for correlation between assets</li>';
    html += '<li>Provides full distribution of potential outcomes</li>';
    html += '</ul></li>';
    html += '</ol>';
    html += '</div>';
    html += '</div>';
    
    // Data Sources & Compliance
    html += '<div class="alert alert-warning">';
    html += '<strong>⚖️ Regulatory Compliance:</strong> This analysis follows Basel II/III VaR guidelines for risk measurement. ';
    html += 'Data sourced from Yahoo Finance. For regulatory reporting, ensure data quality and model validation per Basel framework requirements.';
    html += '</div>';
    
    document.getElementById('capstoneResults').innerHTML = html;
}
