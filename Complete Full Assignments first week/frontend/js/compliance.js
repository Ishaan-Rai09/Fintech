// Compliance JavaScript

// Compliance form handler
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('complianceForm');
    const resultsDiv = document.getElementById('complianceResults');
    
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const complianceType = document.getElementById('complianceType').value;
            
            if (!complianceType) {
                showAlert('Please select a compliance type', 'error');
                return;
            }
            
            // Show loading state
            showLoading(resultsDiv);
            
            try {
                // Check compliance
                const response = await ComplianceAPI.checkCompliance(complianceType);
                
                if (response.success) {
                    showComplianceResults(response.data, resultsDiv, complianceType);
                } else {
                    showAlert(response.message || 'Compliance check failed', 'error');
                    showEmptyState(resultsDiv, 'compliance');
                }
            } catch (error) {
                console.error('Compliance check error:', error);
                showAlert('Failed to check compliance. Please try again.', 'error');
                showEmptyState(resultsDiv, 'compliance');
            }
        });
    }
});

// Show compliance results
function showComplianceResults(data, container, type) {
    const typeLabels = {
        'aml': 'Anti-Money Laundering (AML)',
        'kyc': 'Know Your Customer (KYC)',
        'sebi': 'SEBI Regulations',
        'gst': 'GST Compliance',
        'it': 'Income Tax Compliance'
    };
    
    container.innerHTML = `
        <div class="results has-data">
            <div class="alert alert-success">
                ✅ Compliance check completed for ${typeLabels[type]}!
            </div>
            
            <div class="result-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
                <div class="result-card" style="background: #f0fdf4; padding: 1.5rem; border-radius: 8px; border: 2px solid #10b981;">
                    <h3>✓ Compliance Status</h3>
                    <p><strong>Status:</strong> <span style="color: #10b981; font-weight: 600;">COMPLIANT</span></p>
                    <p><strong>Last Updated:</strong> Today</p>
                    <p><strong>Next Review:</strong> In 30 days</p>
                </div>
                
                <div class="result-card" style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <h3>📋 Requirements</h3>
                    <p><strong>Total Requirements:</strong> ${data.total_requirements || 0}</p>
                    <p><strong>Met:</strong> ${data.requirements_met || 0}</p>
                    <p><strong>Pending:</strong> ${data.requirements_pending || 0}</p>
                </div>
                
                <div class="result-card" style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <h3>🔐 Key Documents</h3>
                    <p><strong>Documents Required:</strong> ${data.documents_required || 0}</p>
                    <p><strong>Documents Submitted:</strong> ${data.documents_submitted || 0}</p>
                    <p><strong>Completion:</strong> ${data.completion_percentage || 0}%</p>
                </div>
            </div>
            
            <div style="margin-top: 2rem; padding: 1.5rem; background: #f3f4f6; border-radius: 8px;">
                <h3>📌 Action Items</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="padding: 0.75rem 0; border-bottom: 1px solid #e5e7eb;">✓ KYC Documentation - Completed</li>
                    <li style="padding: 0.75rem 0; border-bottom: 1px solid #e5e7eb;">⏳ Risk Assessment - In Progress</li>
                    <li style="padding: 0.75rem 0;">📅 Regulatory Training - Scheduled for next month</li>
                </ul>
            </div>
        </div>
    `;
}

// Show empty state
function showEmptyState(container, type) {
    container.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">✓</div>
            <h3>No Compliance Check Yet</h3>
            <p>Select a compliance type to check your regulatory status and requirements.</p>
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
                <p style="margin-top: 1rem; color: #6b7280;">Checking compliance status...</p>
            </div>
        </div>
    `;
}

// Compliance API
const ComplianceAPI = {
    async checkCompliance(type) {
        return apiRequest('/compliance/regulations', {
            method: 'POST',
            body: JSON.stringify({ compliance_type: type })
        });
    }
};

// CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
