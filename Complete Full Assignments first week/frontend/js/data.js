// Data Management JavaScript

// Sample download functionality
function downloadSample(type) {
    if (type === 'data') {
        // Create sample CSV content
        const csvContent = `date,stock_symbol,open,high,low,close,volume
2025-11-01,AAPL,170.00,176.50,169.50,175.50,52000000
2025-11-02,AAPL,175.60,178.20,174.80,177.30,48500000
2025-11-03,AAPL,177.40,179.50,176.90,178.75,51200000
2025-11-04,GOOGL,2920.00,2960.50,2910.00,2950.75,2800000
2025-11-05,GOOGL,2951.00,2980.00,2930.50,2975.25,2950000
2025-11-06,MSFT,283.50,288.75,282.00,285.25,45600000
2025-11-07,MSFT,285.30,292.50,284.50,290.75,49200000`;

        // Create and download file
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'financial_data_sample.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
}

// Data upload form handler
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('dataUploadForm');
    const resultsDiv = document.getElementById('dataResults');
    
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const fileInput = document.getElementById('dataFile');
            const file = fileInput.files[0];
            
            if (!file) {
                showAlert('Please select a file', 'error');
                return;
            }
            
            // Show loading state
            showLoading(resultsDiv);
            
            try {
                // Upload and analyze data
                const response = await DataAPI.uploadData(file);
                
                if (response.success) {
                    showDataResults(response.data, resultsDiv);
                } else {
                    showAlert(response.message || 'Analysis failed', 'error');
                    showEmptyState(resultsDiv, 'data');
                }
            } catch (error) {
                console.error('Data analysis error:', error);
                showAlert('Failed to analyze data. Please try again.', 'error');
                showEmptyState(resultsDiv, 'data');
            }
        });
    }
});

// Show data analysis results
function showDataResults(data, container) {
    container.innerHTML = `
        <div class="results has-data">
            <div class="alert alert-success">
                ✅ Data analysis completed successfully!
            </div>
            
            <div class="result-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
                <div class="result-card" style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <h3>📊 Data Summary</h3>
                    <p><strong>Total Records:</strong> ${data.total_records || 0}</p>
                    <p><strong>Columns:</strong> ${data.column_count || 0}</p>
                    <p><strong>Missing Values:</strong> ${data.missing_values || 0}</p>
                </div>
                
                <div class="result-card" style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <h3>📈 Statistical Summary</h3>
                    <p><strong>Mean:</strong> ${data.mean || 'N/A'}</p>
                    <p><strong>Median:</strong> ${data.median || 'N/A'}</p>
                    <p><strong>Std Dev:</strong> ${data.std_dev || 'N/A'}</p>
                </div>
                
                <div class="result-card" style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <h3>🔍 Data Quality</h3>
                    <p><strong>Completeness:</strong> ${data.completeness || 'N/A'}%</p>
                    <p><strong>Outliers:</strong> ${data.outliers || 0}</p>
                    <p><strong>Status:</strong> <span style="color: #10b981;">✓ Ready</span></p>
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
            <h3>No Data Yet</h3>
            <p>Upload your financial data file to see analysis, insights, and AI-powered recommendations.</p>
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
                <p style="margin-top: 1rem; color: #6b7280;">Analyzing data...</p>
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
