// Portfolio Management JavaScript

// Sample download functionality
function downloadSample(type) {
    if (type === 'portfolio') {
        const csvContent = `symbol,quantity,purchase_price,current_price
AAPL,10,150.00,175.50
GOOGL,5,2800.00,2950.75
MSFT,15,300.00,285.25
TSLA,8,800.00,725.30
AMZN,3,3200.00,3350.25
NVDA,12,220.00,495.80
META,7,350.00,315.40
NFLX,4,500.00,445.60`;

        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'portfolio_sample.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('portfolioUploadForm');
    const resultsDiv = document.getElementById('portfolioResults');
    
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const fileInput = document.getElementById('portfolioFile');
            const file = fileInput.files[0];
            
            if (!file) {
                showAlert('Please select a file', 'error');
                return;
            }
            
            showLoading(resultsDiv);
            
            try {
                // Pointing to PortfolioAPI in api.js
                const response = await PortfolioAPI.uploadAndAnalyze(file);
                
                if (response.status === "success") {
                    showPortfolioResults(response.data, resultsDiv);
                } else {
                    showAlert(response.message || 'Analysis failed', 'error');
                    showEmptyState(resultsDiv, 'portfolio');
                }
            } catch (error) {
                console.error('Portfolio analysis error:', error);
                showAlert(error.message || 'Failed to analyze portfolio', 'error');
                showEmptyState(resultsDiv, 'portfolio');
            }
        });
    }
});

function showPortfolioResults(data, container) {
    container.innerHTML = `
        <div class="results has-data">
            <div class="alert alert-success">
                ✅ Portfolio analysis completed successfully!
            </div>
            
            <div class="result-grid">
                <div class="result-card">
                    <h3>📊 Portfolio Summary</h3>
                    <p><strong>Total Value:</strong> ${formatCurrency(data.total_value)}</p>
                    <p><strong>Total Return:</strong> <span style="color: ${data.total_return_percentage >= 0 ? '#10b981' : '#ef4444'}">${data.total_return_percentage}%</span></p>
                    <p><strong>Holdings:</strong> ${data.holdings_count}</p>
                </div>
                
                <div class="result-card">
                    <h3>⚖️ Risk Metrics</h3>
                    <p><strong>Portfolio Beta:</strong> ${data.beta}</p>
                    <p><strong>Sharpe Ratio:</strong> ${data.sharpe_ratio}</p>
                    <p><strong>Volatility:</strong> ${data.volatility}%</p>
                </div>
                
                <div class="result-card">
                    <h3>🎯 Forecast</h3>
                    <p><strong>Expected Return:</strong> ${data.expected_return}%</p>
                    <p><strong>Risk Score:</strong> ${data.risk_score}/10</p>
                    <button class="btn btn-sm btn-primary" style="margin-top: 10px;" onclick="runOptimization()">Optimize Allocation</button>
                </div>
            </div>
            
            ${data.holdings ? `
                <div class="holdings-table-container">
                    <h3>📋 Holdings Details</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Quantity</th>
                                <th>Purchase Price</th>
                                <th>Current Price</th>
                                <th>Total Value</th>
                                <th>Gain/Loss %</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.holdings.map(holding => `
                                <tr>
                                    <td><strong>${holding.symbol}</strong></td>
                                    <td>${holding.quantity}</td>
                                    <td>${formatCurrency(holding.purchase_price)}</td>
                                    <td>${formatCurrency(holding.current_price)}</td>
                                    <td>${formatCurrency(holding.total_value)}</td>
                                    <td style="color: ${holding.gain_loss >= 0 ? '#10b981' : '#ef4444'}">
                                        ${holding.gain_loss >= 0 ? '+' : ''}${holding.gain_loss}%
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            ` : ''}
            
            <div id="optimizationResults" style="margin-top: 2rem;"></div>
            
            <div class="chart-container" id="portfolioChart">
                <!-- Chart would be rendered here with Chart.js or similar -->
                <p style="text-align: center; color: #6b7280; padding: 2rem; border: 1px dashed #ddd; border-radius: 8px;">
                    📈 Advanced visualization would be initialized here
                </p>
            </div>
        </div>
    `;

    // Store symbols for optimization
    window.currentPortfolioSymbols = data.holdings.map(h => h.symbol);
}

async function runOptimization() {
    const optResultsDiv = document.getElementById('optimizationResults');
    if (!window.currentPortfolioSymbols || window.currentPortfolioSymbols.length < 2) {
        showAlert('Need at least 2 tickers for optimization', 'info');
        return;
    }

    optResultsDiv.innerHTML = '<div class="spinner"></div><p>Calculating optimal allocation...</p>';
    
    try {
        const response = await PortfolioAPI.optimize({
            tickers: window.currentPortfolioSymbols,
            period: '1y'
        });

        if (response.status === "success") {
            const data = response.data;
            let html = `
                <div class="optimization-card" style="background: rgba(16, 185, 129, 0.05); padding: 1.5rem; border-radius: 12px; border: 1px solid #10b981;">
                    <h3>🎯 Optimal Portfolio Allocation</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1rem;">
                        <div>
                            <table class="data-table">
                                <thead>
                                    <tr><th>Symbol</th><th>Weight</th></tr>
                                </thead>
                                <tbody>
                                    ${Object.entries(data.allocation).map(([ticker, weight]) => `
                                        <tr><td>${ticker}</td><td>${(weight * 100).toFixed(2)}%</td></tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        <div>
                            <h4>Performance Stats</h4>
                            <p><strong>Expected Annual Return:</strong> ${(data.expected_return * 100).toFixed(2)}%</p>
                            <p><strong>Volatility:</strong> ${(data.volatility * 100).toFixed(2)}%</p>
                            <p><strong>Sharpe Ratio:</strong> ${data.sharpe_ratio.toFixed(4)}</p>
                            <button class="btn btn-outline btn-sm" style="margin-top: 1rem;" onclick="generateEfficientFrontier()">View Efficient Frontier</button>
                        </div>
                    </div>
                </div>
            `;
            optResultsDiv.innerHTML = html;
        } else {
            optResultsDiv.innerHTML = `<div class="alert alert-danger">${response.message}</div>`;
        }
    } catch (error) {
        optResultsDiv.innerHTML = `<div class="alert alert-danger">Optimization failed: ${error.message}</div>`;
    }
}

async function generateEfficientFrontier() {
    const optResultsDiv = document.getElementById('optimizationResults');
    optResultsDiv.innerHTML += '<div class="spinner"></div><p>Generating efficient frontier...</p>';

    try {
        const response = await PortfolioAPI.efficientFrontier({
            tickers: window.currentPortfolioSymbols,
            period: '1y',
            num_portfolios: 1000
        });

        if (response.status === "success") {
            const portfolios = response.data.portfolios;
            const best = portfolios.reduce((prev, current) => (prev.sharpe > current.sharpe) ? prev : current);
            
            const frontierInfo = `
                <div class="result-card" style="margin-top: 1rem; border-top: 2px solid #3b82f6;">
                    <h4>🚀 Efficient Frontier Insights</h4>
                    <p>Simulated 1,000 random portfolios based on your holdings.</p>
                    <p><strong>Max Sharpe Ratio found:</strong> ${best.sharpe.toFixed(4)}</p>
                    <p><strong>Best Portfolio Return:</strong> ${(best.return * 100).toFixed(2)}% at ${(best.volatility * 100).toFixed(2)}% risk</p>
                    <p><small>Visualization data generated and ready for plotting.</small></p>
                </div>
            `;
            // Remove spinners if any
            const spinners = optResultsDiv.querySelectorAll('.spinner');
            spinners.forEach(s => s.remove());
            
            // Append info
            optResultsDiv.insertAdjacentHTML('beforeend', frontierInfo);
        }
    } catch (error) {
        showAlert('Efficient frontier generation failed', 'error');
    }
}

function showLoading(container) {
    container.innerHTML = `
        <div style="text-align: center; padding: 3rem;">
            <div class="spinner"></div>
            <p style="margin-top: 1rem; color: #6b7280;">Analyzing portfolio...</p>
        </div>
    `;
}

function showEmptyState(container, type) {
    const states = {
        portfolio: {
            icon: '📈',
            title: 'No Portfolio Data',
            message: 'Upload your portfolio CSV to see detailed analysis, optimization suggestions, and risk metrics.'
        }
    };
    
    const state = states[type] || states.portfolio;
    
    container.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">${state.icon}</div>
            <h3>${state.title}</h3>
            <p>${state.message}</p>
        </div>
    `;
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '1000';
    alertDiv.innerHTML = message;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 500);
    }, 5000);
}
