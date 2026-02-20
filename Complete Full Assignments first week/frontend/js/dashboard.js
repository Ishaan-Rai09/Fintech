// Dashboard Functionality - Enhanced with Proper Auth

document.addEventListener('DOMContentLoaded', async () => {
    // Extract token from URL if present (OAuth callback)
    const urlParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = urlParams.get('token');
    
    if (tokenFromUrl) {
        localStorage.setItem('access_token', tokenFromUrl);
        // Clean URL by removing token parameter
        window.history.replaceState({}, document.title, '/dashboard');
    }
    
    // Check if user is authenticated
    const token = localStorage.getItem('access_token');;
    
    if (!token) {
        window.location.href = '/';
        return;
    }
    
    // Load user information and display
    try {
        const response = await AuthAPI.getCurrentUser();
        console.log('User info response:', response);
        
        if (response.success && response.data) {
            const user = response.data;
            
            // Update user greeting
            const greeting = document.getElementById('userGreeting');
            if (greeting) {
                const hour = new Date().getHours();
                let timeGreeting = 'Good morning';
                if (hour >= 12 && hour < 18) timeGreeting = 'Good afternoon';
                else if (hour >= 18) timeGreeting = 'Good evening';
                
                greeting.textContent = `${timeGreeting}, ${user.full_name || user.username}! Here's your financial overview.`;
            }
            
            // Update user name in nav
            const userName = document.getElementById('userName');
            if (userName) {
                userName.textContent = user.full_name || user.username;
            }
            
            // Update user avatar with initials
            const avatar = document.getElementById('userAvatar');
            if (avatar && user.full_name) {
                const initials = user.full_name.split(' ').map(n => n[0]).join('').substring(0, 2);
                avatar.textContent = initials;
            }
        }
    } catch (error) {
        console.error('Failed to load user info:', error);
        
        // Only redirect if it's an authentication error
        // Don't redirect on network errors or other issues
        if (error.message && error.message.includes('Authentication')) {
            console.log('Authentication error, redirecting to login');
            localStorage.removeItem('access_token');
            window.location.href = '/';
        } else {
            // Show error but stay on dashboard
            console.log('Non-auth error, staying on dashboard');
            const greeting = document.getElementById('userGreeting');
            if (greeting) {
                greeting.textContent = 'Error loading user info. Please refresh the page.';
            }
        }
    }
    
    // Logout handler
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('access_token');
            window.location.href = '/';
        });
    }
    
    // Data Upload Form
    const dataUploadForm = document.getElementById('dataUploadForm');
    if (dataUploadForm) {
        dataUploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const dataFile = document.getElementById('dataFile').files[0];
            if (!dataFile) {
                showMessage('dataResults', 'Please select a file', 'error');
                return;
            }
            
            showLoading('dataResults');
            
            try {
                const response = await DataAPI.uploadData(dataFile);
                
                if (response.success) {
                    let html = '<div class="alert alert-success">Data uploaded successfully!</div>';
                    
                    if (response.data.summary) {
                        html += '<h3>Data Summary</h3>';
                        html += '<table>';
                        html += '<tr><th>Metric</th><th>Value</th></tr>';
                        Object.entries(response.data.summary).forEach(([key, value]) => {
                            html += `<tr><td>${key}</td><td>${JSON.stringify(value)}</td></tr>`;
                        });
                        html += '</table>';
                    }
                    
                    document.getElementById('dataResults').innerHTML = html;
                } else {
                    showMessage('dataResults', response.message || 'Upload failed', 'error');
                }
            } catch (error) {
                document.getElementById('dataResults').innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
            }
        });
    }
    
    // Transaction Analysis Form
    const transactionForm = document.getElementById('transactionForm');
    if (transactionForm) {
        transactionForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const transactionFile = document.getElementById('transactionFile').files[0];
            if (!transactionFile) {
                showMessage('transactionResults', 'Please select a file', 'error');
                return;
            }
            
            showLoading('transactionResults');
            
            try {
                const response = await TransactionAPI.analyzeTransactions(transactionFile);
                
                if (response.success) {
                    let html = '<div class="alert alert-success">Analysis complete!</div>';
                    
                    if (response.data.summary) {
                        html += '<h3>Transaction Summary</h3>';
                        html += '<table>';
                        html += '<tr><th>Metric</th><th>Value</th></tr>';
                        Object.entries(response.data.summary).forEach(([key, value]) => {
                            html += `<tr><td>${key}</td><td>${typeof value === 'number' ? formatCurrency(value) : value}</td></tr>`;
                        });
                        html += '</table>';
                    }
                    
                    if (response.data.fraud_detected) {
                        html += '<div class="alert alert-warning">⚠️ Potential fraud detected!</div>';
                    }
                    
                    document.getElementById('transactionResults').innerHTML = html;
                } else {
                    document.getElementById('transactionResults').innerHTML = `<div class="alert alert-danger">${response.message}</div>`;
                }
            } catch (error) {
                document.getElementById('transactionResults').innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
            }
        });
    }
});

// Section Toggle
function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.add('hidden');
    });
    
    // Show selected section
    const targetSection = document.getElementById(`${sectionName}Section`);
    if (targetSection) {
        targetSection.classList.remove('hidden');
        
        // Load section-specific data
        if (sectionName === 'compliance') {
            loadComplianceData();
        }
    }
}

// Load Compliance Data
async function loadComplianceData() {
    showLoading('complianceResults');
    
    try {
        const rbiResponse = await ComplianceAPI.getRegulations('RBI');
        const sebiResponse = await ComplianceAPI.getRegulations('SEBI');
        const kycResponse = await ComplianceAPI.getRegulations('KYC-AML');
        
        let html = '<h3>Regulatory Guidelines</h3>';
        
        if (rbiResponse.success) {
            html += '<div class="card"><h4>RBI Guidelines</h4><ul>';
            rbiResponse.data.regulations.forEach(reg => {
                html += `<li>${reg}</li>`;
            });
            html += '</ul></div>';
        }
        
        if (sebiResponse.success) {
            html += '<div class="card"><h4>SEBI Guidelines</h4><ul>';
            sebiResponse.data.regulations.forEach(reg => {
                html += `<li>${reg}</li>`;
            });
            html += '</ul></div>';
        }
        
        if (kycResponse.success) {
            html += '<div class="card"><h4>KYC/AML Guidelines</h4><ul>';
            kycResponse.data.regulations.forEach(reg => {
                html += `<li>${reg}</li>`;
            });
            html += '</ul></div>';
        }
        
        document.getElementById('complianceResults').innerHTML = html;
    } catch (error) {
        document.getElementById('complianceResults').innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
    }
}

// Utility Functions
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner"></div><p style="text-align: center; margin-top: 1rem; color: var(--gray);">Loading...</p>';
    }
}

function showMessage(elementId, message, type = 'info') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

function formatPercentage(value) {
    return `${(value * 100).toFixed(2)}%`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Initialize stat cards with sample data (will be updated with real API data)
function initializeStatCards() {
    // These will be updated with real data from API
    if (document.getElementById('portfolioValue')) {
        document.getElementById('portfolioValue').textContent = '$0';
        document.getElementById('portfolioReturn').textContent = '+0%';
        document.getElementById('riskLevel').textContent = 'Low';
        document.getElementById('predictions').textContent = '0';
    }
}

// Call initialize on load
initializeStatCards();
