// Transaction Analysis JavaScript

// Sample download functionality
function downloadSample(type) {
    if (type === 'transactions') {
        // Create sample CSV content
        const csvContent = `date,amount,category,merchant,description
2025-11-01,500.00,Groceries,Whole Foods,Weekly groceries shopping
2025-11-02,45.99,Dining,Starbucks,Coffee and breakfast
2025-11-02,89.50,Transport,Shell Gas Station,Fuel
2025-11-03,120.00,Entertainment,Netflix,Monthly subscription
2025-11-04,245.75,Shopping,Amazon,Electronics purchase
2025-11-05,1200.00,Utilities,State Power Corp,Monthly electricity bill
2025-11-06,350.00,Healthcare,Apollo Hospital,Doctor visit
2025-11-07,75.00,Dining,Pizza Hut,Dinner with friends`;

        // Create and download file
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'transactions_sample.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
}

// Transaction upload form handler
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('transactionUploadForm');
    const resultsDiv = document.getElementById('transactionResults');
    
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const fileInput = document.getElementById('transactionFile');
            const file = fileInput.files[0];
            
            if (!file) {
                showAlert('Please select a file', 'error');
                return;
            }
            
            // Show loading state
            showLoading(resultsDiv);
            
            try {
                // Upload and analyze transactions
                const response = await TransactionAPI.uploadAndAnalyze(file);
                
                if (response.success) {
                    showTransactionResults(response.data, resultsDiv);
                } else {
                    showAlert(response.message || 'Analysis failed', 'error');
                    showEmptyState(resultsDiv, 'transactions');
                }
            } catch (error) {
                console.error('Transaction analysis error:', error);
                showAlert('Failed to analyze transactions. Please try again.', 'error');
                showEmptyState(resultsDiv, 'transactions');
            }
        });
    }
});

// Show transaction analysis results
function showTransactionResults(data, container) {
    container.innerHTML = `
        <div class="results has-data">
            <div class="alert alert-success">
                ✅ Transaction analysis completed successfully!
            </div>
            
            <div class="result-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
                <div class="result-card" style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <h3>📊 Transaction Summary</h3>
                    <p><strong>Total Transactions:</strong> ${data.total_transactions || 0}</p>
                    <p><strong>Total Amount:</strong> $${(data.total_amount || 0).toFixed(2)}</p>
                    <p><strong>Average Transaction:</strong> $${(data.average_amount || 0).toFixed(2)}</p>
                </div>
                
                <div class="result-card" style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <h3>🏪 Top Categories</h3>
                    ${data.top_categories ? Object.entries(data.top_categories).map(([cat, count]) => 
                        `<p><strong>${cat}:</strong> ${count} transactions</p>`
                    ).join('') : '<p>No category data</p>'}
                </div>
                
                <div class="result-card" style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <h3>⚠️ Fraud Detection</h3>
                    <p><strong>Suspicious Transactions:</strong> ${data.suspicious_count || 0}</p>
                    <p><strong>Risk Level:</strong> ${data.risk_level || 'Low'}</p>
                </div>
            </div>
        </div>
    `;
}

// Show empty state
function showEmptyState(container, type) {
    container.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">📈</div>
            <h3>No Transaction Data</h3>
            <p>Upload your transaction CSV to see spending patterns, fraud detection, and category analysis.</p>
        </div>
    `;
}

// Helper function to show alerts
function showAlert(message, type) {
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Helper function to show loading state
function showLoading(container) {
    container.innerHTML = `
        <div class="loading">
            <div style="text-align: center; padding: 2rem;">
                <div class="spinner" style="border: 4px solid #e5e7eb; border-top: 4px solid #10b981; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto;"></div>
                <p style="margin-top: 1rem; color: #6b7280;">Analyzing transactions...</p>
            </div>
        </div>
    `;
}

// CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
