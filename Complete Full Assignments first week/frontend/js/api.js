// API Base URL Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Token Management
function getToken() {
    return localStorage.getItem('access_token');
}

function setToken(token) {
    localStorage.setItem('access_token', token);
}

function removeToken() {
    localStorage.removeItem('access_token');
}

// API Request Helper
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        ...options,
        headers
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        // Handle 401 Unauthorized
        if (response.status === 401) {
            removeToken();
            window.location.href = '/';
            throw new Error('Authentication required');
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'API request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// File Upload Helper
async function uploadFile(endpoint, file, additionalData = {}) {
    const token = getToken();
    const formData = new FormData();
    formData.append('file', file);
    
    // Add additional form fields
    Object.keys(additionalData).forEach(key => {
        formData.append(key, additionalData[key]);
    });
    
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers,
            body: formData
        });
        
        if (response.status === 401) {
            removeToken();
            window.location.href = '/';
            throw new Error('Authentication required');
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Upload failed');
        }
        
        return data;
    } catch (error) {
        console.error('Upload Error:', error);
        throw error;
    }
}

// Authentication APIs
const AuthAPI = {
    async register(userData) {
        return apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },
    
    async login(credentials) {
        return apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    },
    
    async getCurrentUser() {
        return apiRequest('/auth/me');
    }
};

// Data Management APIs
const DataAPI = {
    async uploadData(file) {
        return uploadFile('/data/upload', file);
    },
    
    async cleanData(data) {
        return apiRequest('/data/clean', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async validateData(data) {
        return apiRequest('/data/validate', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

// Transaction APIs
const TransactionAPI = {
    async getSummary() {
        return apiRequest('/transactions/summary');
    },
    
    async analyzeTransactions(file) {
        return uploadFile('/transactions/analyze', file);
    },
    
    async detectFraud(data) {
        return apiRequest('/transactions/detect-fraud', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async getSuspicious() {
        return apiRequest('/transactions/suspicious');
    }
};

// ML APIs
const MLAPI = {
    async trainModel(data) {
        return apiRequest('/ml/train', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async predict(data) {
        return apiRequest('/ml/predict', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async getModels() {
        return apiRequest('/ml/models');
    },
    
    async getMetrics(modelFilename) {
        return apiRequest(`/ml/metrics/${modelFilename}`);
    }
};

// Prediction APIs
const PredictionAPI = {
    async forecast(data) {
        return apiRequest('/predictions/forecast', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async movingAverage(data) {
        return apiRequest('/predictions/moving-average', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

// Portfolio APIs
const PortfolioAPI = {
    async uploadAndAnalyze(file) {
        return uploadFile('/portfolio/analyze', file);
    },
    
    async optimize(data) {
        return apiRequest('/portfolio/optimize', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async efficientFrontier(data) {
        return apiRequest('/portfolio/efficient-frontier', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async getPerformance(data) {
        return apiRequest('/portfolio/performance', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

// Risk APIs
const RiskAPI = {
    async calculateVaR(data) {
        return apiRequest('/risk/var', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async dualStockVaR(data) {
        return apiRequest('/risk/dual-stock-var', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async monteCarloVaR(data) {
        return apiRequest('/risk/monte-carlo', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async getReport() {
        return apiRequest('/risk/report');
    }
};

// Robo Advisory APIs
const RoboAdvisoryAPI = {
    async getQuestionnaire() {
        return apiRequest('/robo-advisory/questionnaire');
    },
    
    async saveProfile(data) {
        return apiRequest('/robo-advisory/profile', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async getRecommendations(data) {
        return apiRequest('/robo-advisory/recommend', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async getStrategy(data) {
        return apiRequest('/robo-advisory/strategy', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async rebalance(data) {
        return apiRequest('/robo-advisory/rebalance', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

// Tax APIs
const TaxAPI = {
    async calculateTax(data) {
        return apiRequest('/tax/calculate', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async getSuggestions(income) {
        return apiRequest(`/tax/suggestions?income=${income}`);
    },
    
    async getSlabs() {
        return apiRequest('/tax/slabs');
    }
};

// Compliance APIs
const ComplianceAPI = {
    async getRegulations(type) {
        return apiRequest(`/compliance/regulations?type=${type}`);
    },
    
    async checkCompliance(data) {
        return apiRequest('/compliance/check', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
};

// Utility Functions
function showMessage(elementId, message, type = 'info') {
    const messageEl = document.getElementById(elementId);
    if (messageEl) {
        messageEl.textContent = message;
        messageEl.className = `message ${type}`;
        messageEl.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageEl.style.display = 'none';
        }, 5000);
    }
}

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner"></div>';
    }
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

function formatPercentage(value) {
    return `${(value * 100).toFixed(2)}%`;
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}
