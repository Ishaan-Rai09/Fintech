// Test Data and Samples for All Features

const TEST_DATA = {
    portfolio: {
        title: "Portfolio Optimization",
        description: "Sample portfolio data with multiple assets for optimization analysis",
        csvSample: `Symbol,Weight,ExpectedReturn,Volatility
AAPL,0.25,0.15,0.22
GOOGL,0.20,0.18,0.25
MSFT,0.15,0.14,0.20
AMZN,0.15,0.16,0.28
TSLA,0.10,0.20,0.35
JPM,0.10,0.09,0.18
JNJ,0.05,0.07,0.15`,
        jsonSample: {
            portfolio: {
                assets: [
                    { symbol: "AAPL", shares: 100, purchasePrice: 150, currentPrice: 185 },
                    { symbol: "GOOGL", shares: 50, purchasePrice: 2800, currentPrice: 3100 },
                    { symbol: "MSFT", shares: 75, purchasePrice: 300, currentPrice: 380 },
                    { symbol: "AMZN", shares: 30, purchasePrice: 3200, currentPrice: 3500 }
                ],
                totalValue: 350000,
                investedAmount: 300000,
                returns: 16.67
            }
        },
        apiExample: {
            endpoint: "/api/v1/portfolio/optimize",
            method: "POST",
            headers: {
                "Authorization": "Bearer YOUR_JWT_TOKEN",
                "Content-Type": "application/json"
            },
            body: {
                symbols: ["AAPL", "GOOGL", "MSFT", "AMZN"],
                start_date: "2023-01-01",
                end_date: "2024-12-31",
                risk_tolerance: "moderate"
            }
        },
        features: [
            "Efficient Frontier Calculation",
            "Sharpe Ratio Optimization",
            "Mean-Variance Optimization",
            "Risk-Return Trade-off Analysis",
            "Portfolio Rebalancing Suggestions"
        ]
    },
    
    risk: {
        title: "Risk Analysis & VaR Calculation",
        description: "Value at Risk (VaR) calculation using multiple methodologies",
        csvSample: `Date,Close,Returns
2024-01-01,150.25,0.0
2024-01-02,152.30,0.0136
2024-01-03,148.90,-0.0223
2024-01-04,151.20,0.0154
2024-01-05,149.80,-0.0093
2024-01-08,153.50,0.0247
2024-01-09,152.10,-0.0091`,
        jsonSample: {
            portfolio_value: 100000,
            confidence_level: 0.95,
            time_horizon: 1,
            historical_returns: [-0.02, 0.01, 0.03, -0.01, 0.02, -0.015, 0.025],
            method: "historical"
        },
        methods: [
            {
                name: "Historical VaR",
                description: "Uses historical price data",
                endpoint: "/api/v1/risk/historical-var"
            },
            {
                name: "Parametric VaR",
                description: "Assumes normal distribution",
                endpoint: "/api/v1/risk/parametric-var"
            },
            {
                name: "Monte Carlo VaR",
                description: "Simulation-based approach",
                endpoint: "/api/v1/risk/monte-carlo-var"
            }
        ],
        apiExample: {
            endpoint: "/api/v1/risk/dual-stock-var",
            method: "POST",
            body: {
                stock1: "AAPL",
                stock2: "GOOGL",
                start_date: "2023-01-01",
                end_date: "2024-12-31",
                confidence_level: 0.95,
                investment: 10000
            }
        }
    },
    
    predictions: {
        title: "ML Predictions & Time Series Forecasting",
        description: "ARIMA, LSTM, and sentiment analysis for price predictions",
        csvSample: `Date,Open,High,Low,Close,Volume
2024-01-01,150.25,152.80,149.90,152.30,1234567
2024-01-02,152.40,154.20,151.80,153.90,1345678
2024-01-03,153.90,155.50,153.20,154.70,1456789
2024-01-04,154.80,156.30,154.20,155.90,1567890
2024-01-05,156.00,158.20,155.50,157.40,1678901`,
        models: [
            {
                name: "ARIMA",
                description: "Auto-Regressive Integrated Moving Average",
                best_for: "Univariate time series with trends",
                endpoint: "/api/v1/predictions/stock-arima"
            },
            {
                name: "LSTM",
                description: "Long Short-Term Memory Neural Network",
                best_for: "Complex patterns and long-term dependencies",
                endpoint: "/api/v1/predictions/stock-lstm"
            },
            {
                name: "Sentiment Analysis",
                description: "News and social media sentiment",
                best_for: "Incorporating market sentiment",
                endpoint: "/api/v1/predictions/stock-sentiment"
            }
        ],
        apiExample: {
            endpoint: "/api/v1/predictions/stock-arima",
            method: "POST",
            body: {
                symbol: "AAPL",
                start_date: "2023-01-01",
                end_date: "2024-12-31",
                forecast_days: 30
            },
            response: {
                predictions: [180.5, 181.2, 182.0, 181.8, 183.1],
                confidence_intervals: {
                    lower: [178.0, 178.5, 179.0, 179.2, 180.0],
                    upper: [183.0, 183.9, 185.0, 184.4, 186.2]
                },
                metrics: {
                    mae: 2.45,
                    rmse: 3.12,
                    mape: 1.35
                }
            }
        }
    },
    
    roboAdvisor: {
        title: "Robo Advisor - Personalized Investment Advice",
        description: "AI-powered investment recommendations based on your risk profile",
        questionnaire: [
            {
                question: "What is your investment goal?",
                options: ["Retirement", "Wealth Building", "Income Generation", "Capital Preservation"]
            },
            {
                question: "What is your investment time horizon?",
                options: ["< 3 years", "3-5 years", "5-10 years", "> 10 years"]
            },
            {
                question: "How do you react to market volatility?",
                options: ["Sell immediately", "Concerned but hold", "Comfortable", "Opportunity to buy more"]
            },
            {
                question: "What is your annual income?",
                options: ["< $50K", "$50K-$100K", "$100K-$250K", "> $250K"]
            }
        ],
        sampleProfile: {
            age: 35,
            income: 120000,
            investmentAmount: 50000,
            riskTolerance: "moderate",
            investmentGoal: "wealth building",
            timeHorizon: "10+ years"
        },
        apiExample: {
            endpoint: "/api/v1/robo-advisory/questionnaire",
            method: "POST",
            body: {
                responses: {
                    age: 35,
                    income: 120000,
                    goal: "wealth_building",
                    horizon: "long_term",
                    risk_comfort: "moderate"
                }
            },
            response: {
                riskProfile: "Moderate",
                recommendedAllocation: {
                    stocks: 70,
                    bonds: 20,
                    cash: 10
                },
                portfolioSuggestions: [
                    { symbol: "VTI", allocation:40, reason: "Total US Market" },
                    { symbol: "VXUS", allocation: 30, reason: "International Diversification" },
                    { symbol: "BND", allocation: 20, reason: "Bond Stability" },
                    { symbol: "VCSH", allocation: 10, reason: "Short-term Bonds" }
                ]
            }
        }
    },
    
    tax: {
        title: "Tax Calculator - Capital Gains & Optimization",
        description: "Calculate taxes on investments and find optimization strategies",
        csvSample: `Symbol,PurchaseDate,PurchasePrice,Shares,SaleDate,SalePrice
AAPL,2023-01-15,150.50,100,2024-12-31,185.30
GOOGL,2023-03-20,2800.00,20,2024-12-31,3100.00
MSFT,2022-06-10,280.00,50,2024-12-31,380.00
AMZN,2023-08-05,3200.00,15,2024-12-31,3500.00`,
        jsonSample: {
            transactions: [
                {
                    symbol: "AAPL",
                    purchaseDate: "2023-01-15",
                    purchasePrice: 150.50,
                    saleDate: "2024-12-31",
                    salePrice: 185.30,
                    shares: 100,
                    holdingPeriod: "long_term"
                }
            ],
            filingStatus: "single",
            taxableIncome: 120000
        },
        taxRates: {
            shortTerm: "Ordinary income tax rates (10% to 37%)",
            longTerm: {
                "0%": "Income up to $44,625 (single)",
                "15%": "Income $44,625 to $492,300",
                "20%": "Income above $492,300"
            }
        },
        apiExample: {
            endpoint: "/api/v1/tax/calculate",
            method: "POST",
            body: {
                purchase_price: 15000,
                sale_price: 18500,
                holding_period: "long_term",
                tax_bracket: "22%"
            },
            response: {
                capitalGain: 3500,
                taxRate: 15,
                taxOwed: 525,
                netProfit: 2975
            }
        }
    },
    
    transactions: {
        title: "Transaction Analysis & Fraud Detection",
        description: "Analyze spending patterns and detect fraudulent transactions",
        csvSample: `TransactionID,Date,Amount,Category,Merchant,Location
TXN001,2024-01-15,125.50,Groceries,Walmart,New York
TXN002,2024-01-16,45.20,Gas,Shell,New York
TXN003,2024-01-16,2500.00,Electronics,BestBuy,New York
TXN004,2024-01-17,15.80,Food,McDonald's,New York
TXN005,2024-01-17,8500.00,Travel,Expedia,New York
TXN006,2024-01-18,30.00,Subscription,Netflix,Online`,
        jsonSample: {
            transactions: [
                { id: "TXN001", amount: 125.50, category: "groceries", timestamp: "2024-01-15T10:30:00", location: "NY" },
                { id: "TXN002", amount: 5500.00, category: "electronics", timestamp: "2024-01-15T14:20:00", location: "CA" }
            ]
        },
        fraudIndicators: [
            "Large unusual transactions",
            "Multiple transactions in short time",
            "Transactions in different locations",
            "Unusual merchant categories",
            "High-risk merchant types"
        ],
        apiExample: {
            endpoint: "/api/v1/transactions/analyze",
            method: "POST",
            description: "Upload CSV file with transaction data",
            responseExample: {
                summary: {
                    totalTransactions: 156,
                    totalAmount: 45230.50,
                    avgTransaction: 290.06,
                    suspiciousCount: 3
                },
                fraudDetected: true,
                suspiciousTransactions: [
                    { id: "TXN089", reason: "Unusually large amount", riskScore: 0.85 },
                    { id: "TXN102", reason: "Multiple locations", riskScore: 0.72 }
                ],
                categoryBreakdown: {
                    groceries: 12500,
                    electronics: 8900,
                    travel: 15200
                }
            }
        }
    },
    
    compliance: {
        title: "Regulatory Compliance Checker",
        description: "Check compliance with financial regulations (MiFID II, GDPR, Dodd-Frank)",
        regulations: [
            {
                name: "MiFID II",
                description: "Markets in Financial Instruments Directive",
                requirements: [
                    "Best execution reporting",
                    "Transaction reporting",
                    "Client categorization",
                    "Product governance"
                ]
            },
            {
                name: "GDPR",
                description: "General Data Protection Regulation",
                requirements: [
                    "Data privacy protection",
                    "Right to be forgotten",
                    "Data breach notification",
                    "Consent management"
                ]
            },
            {
                name: "Dodd-Frank",
                description: "Wall Street Reform Act",
                requirements: [
                    "Volcker Rule compliance",
                    "Stress testing",
                    "Capital requirements",
                    "Risk management standards"
                ]
            }
        ],
        apiExample: {
            endpoint: "/api/v1/compliance/regulations",
            method: "GET",
            response: {
                regulations: [
                    {
                        name: "MiFID II",
                        effectiveDate: "2018-01-03",
                        description: "EU financial markets regulation",
                        keyRequirements: ["transparency", "investor protection"]
                    }
                ]
            }
        }
    },
    
    data: {
        title: "Data Management & Analysis",
        description: "Upload and analyze financial data with AI-powered insights",
        supportedFormats: ["CSV", "Excel (.xlsx, .xls)", "JSON"],
        csvSample: `Date,Symbol,Open,High,Low,Close,Volume
2024-01-01,AAPL,180.25,182.50,179.80,182.30,45678900
2024-01-02,AAPL,182.40,184.20,181.90,183.50,48901234
2024-01-03,AAPL,183.60,185.30,182.50,184.90,52345678`,
        apiExample: {
            endpoint: "/api/v1/data/upload",
            method: "POST",
            contentType: "multipart/form-data",
            body: "file: (binary data)",
            response: {
                success: true,
                summary: {
                    rows: 250,
                    columns: 7,
                    dateRange: "2023-01-01 to 2024-12-31",
                    symbols: ["AAPL", "GOOGL", "MSFT"],
                    missingValues: 3
                },
                insights: {
                    correlations: { "AAPL-GOOGL": 0.85, "AAPL-MSFT": 0.78 },
                    volatility: { AAPL: 0.22, GOOGL: 0.25, MSFT: 0.20 },
                    trends: { AAPL: "upward", GOOGL: "stable", MSFT: "upward" }
                }
            }
        }
    }
};

// Show test data modal
function showTestData() {
    const modal = document.getElementById('testDataModal');
    const content = document.getElementById('testDataContent');
    
    let html = `
        <div class="test-data-nav">
            <button onclick="showTestDataSection('portfolio')" class="active">Portfolio</button>
            <button onclick="showTestDataSection('risk')">Risk Analysis</button>
            <button onclick="showTestDataSection('predictions')">Predictions</button>
            <button onclick="showTestDataSection('roboAdvisor')">Robo Advisor</button>
            <button onclick="showTestDataSection('tax')">Tax Calculator</button>
            <button onclick="showTestDataSection('transactions')">Transactions</button>
            <button onclick="showTestDataSection('compliance')">Compliance</button>
            <button onclick="showTestDataSection('data')">Data Management</button>
        </div>
    `;
    
    // Generate sections for each feature
    Object.keys(TEST_DATA).forEach(key => {
        html += generateTestDataSection(key, TEST_DATA[key]);
    });
    
    content.innerHTML = html;
    modal.classList.remove('hidden');
}

// Generate test data section
function generateTestDataSection(key, data) {
    const isActive = key === 'portfolio' ? 'active' : '';
    
    let html = `
        <div id="test-section-${key}" class="test-data-section ${isActive}">
            <h3>${data.title}</h3>
            <p>${data.description}</p>
    `;
    
    // CSV Sample
    if (data.csvSample) {
        html += `
            <div class="info-box">
                <h4>📄 Sample CSV Data</h4>
                <p>Copy this and save as .csv file to test the feature:</p>
                <div class="code-block">
                    <pre>${data.csvSample}</pre>
                </div>
                <button class="btn btn-primary" onclick="copyToClipboard('${key}-csv')">Copy CSV</button>
            </div>
        `;
    }
    
    // JSON Sample
    if (data.jsonSample) {
        html += `
            <div class="success-box">
                <h4>📋 Sample JSON Data</h4>
                <div class="code-block">
                    <pre>${JSON.stringify(data.jsonSample, null, 2)}</pre>
                </div>
                <button class="btn btn-primary" onclick="copyToClipboard('${key}-json')">Copy JSON</button>
            </div>
        `;
    }
    
    // API Example
    if (data.apiExample) {
        html += `
            <div class="warning-box">
                <h4>🔧 API Usage Example</h4>
                <p><strong>Endpoint:</strong> <code>${data.apiExample.endpoint}</code></p>
                <p><strong>Method:</strong> <code>${data.apiExample.method}</code></p>
                ${data.apiExample.headers ? `
                    <p><strong>Headers:</strong></p>
                    <div class="code-block">
                        <pre>${JSON.stringify(data.apiExample.headers, null, 2)}</pre>
                    </div>
                ` : ''}
                ${data.apiExample.body ? `
                    <p><strong>Request Body:</strong></p>
                    <div class="code-block">
                        <pre>${JSON.stringify(data.apiExample.body, null, 2)}</pre>
                    </div>
                ` : ''}
                ${data.apiExample.response ? `
                    <p><strong>Sample Response:</strong></p>
                    <div class="code-block">
                        <pre>${JSON.stringify(data.apiExample.response, null, 2)}</pre>
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    // Additional features/methods
    if (data.models) {
        html += `
            <h4>📊 Available Models</h4>
            <table class="sample-table">
                <thead>
                    <tr>
                        <th>Model</th>
                        <th>Description</th>
                        <th>Best For</th>
                        <th>Endpoint</th>
                    </tr>
                </thead>
                <tbody>
        `;
        data.models.forEach(model => {
            html += `
                <tr>
                    <td><strong>${model.name}</strong></td>
                    <td>${model.description}</td>
                    <td>${model.best_for}</td>
                    <td><code>${model.endpoint}</code></td>
                </tr>
            `;
        });
        html += `</tbody></table>`;
    }
    
    if (data.methods) {
        html += `
            <h4>📊 Available Methods</h4>
            <table class="sample-table">
                <thead>
                    <tr>
                        <th>Method</th>
                        <th>Description</th>
                        <th>Endpoint</th>
                    </tr>
                </thead>
                <tbody>
        `;
        data.methods.forEach(method => {
            html += `
                <tr>
                    <td><strong>${method.name}</strong></td>
                    <td>${method.description}</td>
                    <td><code>${method.endpoint}</code></td>
                </tr>
            `;
        });
        html += `</tbody></table>`;
    }
    
    html += `</div>`;
    return html;
}

// Show specific test data section
function showTestDataSection(section) {
    // Update nav buttons
    document.querySelectorAll('.test-data-nav button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Show section
    document.querySelectorAll('.test-data-section').forEach(sec => {
        sec.classList.remove('active');
    });
    document.getElementById(`test-section-${section}`).classList.add('active');
}

// Close modal
function closeTestDataModal() {
    document.getElementById('testDataModal').classList.add('hidden');
}

// Copy to clipboard
function copyToClipboard(dataKey) {
    const [section, type] = dataKey.split('-');
    let text = '';
    
    if (type === 'csv') {
        text = TEST_DATA[section].csvSample;
    } else if (type === 'json') {
        text = JSON.stringify(TEST_DATA[section].jsonSample, null, 2);
    }
    
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard! Save it as a file to test the feature.');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Close modal on outside click
document.addEventListener('click', (e) => {
    const modal = document.getElementById('testDataModal');
    if (e.target === modal) {
        closeTestDataModal();
    }
});
