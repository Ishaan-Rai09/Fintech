// Robo Advisor Questionnaire and Recommendations

let questionnaireData = null;
let userAnswers = {};

document.addEventListener('DOMContentLoaded', async () => {
    // Load questionnaire
    try {
        const response = await RoboAdvisoryAPI.getQuestionnaire();
        if (response.success) {
            questionnaireData = response.data.questions;
            displayQuestionnaire(questionnaireData);
        }
    } catch (error) {
        console.error('Failed to load questionnaire:', error);
        document.getElementById('questionnaire').innerHTML = 
            `<div class="alert alert-danger">Failed to load questionnaire: ${error.message}</div>`;
    }
    
    // Submit button handler
    const submitBtn = document.getElementById('submitQuestions');
    if (submitBtn) {
        submitBtn.addEventListener('click', async () => {
            if (!validateAnswers()) {
                alert('Please answer all questions');
                return;
            }
            
            await getRecommendations();
        });
    }
});

function displayQuestionnaire(questions) {
    let html = '';
    
    questions.forEach((question, index) => {
        html += `<div class="form-group">`;
        html += `<label><strong>Q${index + 1}: ${question.question}</strong></label>`;
        
        question.options.forEach((option, optIndex) => {
            html += `
                <div>
                    <input type="radio" 
                           id="q${index}_opt${optIndex}" 
                           name="question_${index}" 
                           value="${option.score}"
                           onchange="saveAnswer(${index}, ${option.score})">
                    <label for="q${index}_opt${optIndex}">${option.text}</label>
                </div>
            `;
        });
        
        html += `</div>`;
    });
    
    document.getElementById('questionnaire').innerHTML = html;
    document.getElementById('submitQuestions').style.display = 'block';
}

function saveAnswer(questionIndex, score) {
    userAnswers[questionIndex] = score;
}

function validateAnswers() {
    return questionnaireData && Object.keys(userAnswers).length === questionnaireData.length;
}

async function getRecommendations() {
    const totalScore = Object.values(userAnswers).reduce((sum, score) => sum + score, 0);
    
    showLoading('recommendations');
    document.getElementById('recommendationsSection').classList.remove('hidden');
    
    try {
        // Get recommendations based on score
        const response = await RoboAdvisoryAPI.getRecommendations({
            risk_score: totalScore
        });
        
        if (response.success) {
            displayRecommendations(response.data);
        } else {
            document.getElementById('recommendations').innerHTML = 
                `<div class="alert alert-danger">${response.message}</div>`;
        }
    } catch (error) {
        document.getElementById('recommendations').innerHTML = 
            `<div class="alert alert-danger">${error.message}</div>`;
    }
}

function displayRecommendations(data) {
    let html = '';
    
    // Risk Profile
    html += '<div class="card">';
    html += '<h3>Your Risk Profile</h3>';
    html += '<table>';
    html += `<tr><td>Risk Score</td><td>${data.risk_score}/10</td></tr>`;
    html += `<tr><td>Risk Category</td><td><strong>${data.risk_category}</strong></td></tr>`;
    html += '</table>';
    html += '</div>';
    
    // Asset Allocation
    if (data.asset_allocation) {
        html += '<div class="card">';
        html += '<h3>Recommended Asset Allocation</h3>';
        html += '<table>';
        Object.entries(data.asset_allocation).forEach(([asset, percentage]) => {
            html += `<tr><td>${asset.charAt(0).toUpperCase() + asset.slice(1)}</td><td>${formatPercentage(percentage / 100)}</td></tr>`;
        });
        html += '</table>';
        html += '</div>';
    }
    
    // Securities Recommendations
    if (data.securities) {
        html += '<div class="card">';
        html += '<h3>Recommended Securities</h3>';
        
        if (data.securities.stocks && data.securities.stocks.length > 0) {
            html += '<h4>Stocks</h4>';
            html += '<ul>';
            data.securities.stocks.forEach(stock => {
                html += `<li>${stock}</li>`;
            });
            html += '</ul>';
        }
        
        if (data.securities.bonds && data.securities.bonds.length > 0) {
            html += '<h4>Bonds</h4>';
            html += '<ul>';
            data.securities.bonds.forEach(bond => {
                html += `<li>${bond}</li>`;
            });
            html += '</ul>';
        }
        
        if (data.securities.etfs && data.securities.etfs.length > 0) {
            html += '<h4>ETFs</h4>';
            html += '<ul>';
            data.securities.etfs.forEach(etf => {
                html += `<li>${etf}</li>`;
            });
            html += '</ul>';
        }
        
        html += '</div>';
    }
    
    // Investment Strategy
    if (data.strategy) {
        html += '<div class="card">';
        html += '<h3>Investment Strategy</h3>';
        html += '<ul>';
        if (data.strategy.description) {
            html += `<li>${data.strategy.description}</li>`;
        }
        if (data.strategy.time_horizon) {
            html += `<li><strong>Time Horizon:</strong> ${data.strategy.time_horizon}</li>`;
        }
        if (data.strategy.rebalancing_frequency) {
            html += `<li><strong>Rebalancing:</strong> ${data.strategy.rebalancing_frequency}</li>`;
        }
        html += '</ul>';
        html += '</div>';
    }
    
    // Disclaimer
    html += '<div class="alert alert-warning">';
    html += '<strong>Disclaimer:</strong> These recommendations are for educational purposes only. ';
    html += 'Please consult with a certified financial advisor before making investment decisions.';
    html += '</div>';
    
    document.getElementById('recommendations').innerHTML = html;
}
