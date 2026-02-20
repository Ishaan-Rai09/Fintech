// Tax Calculator

document.addEventListener('DOMContentLoaded', () => {
    // Show/hide deductions section based on regime
    const regimeSelect = document.getElementById('regime');
    if (regimeSelect) {
        regimeSelect.addEventListener('change', (e) => {
            const deductionsSection = document.getElementById('deductionsSection');
            if (deductionsSection) {
                if (e.target.value === 'old') {
                    deductionsSection.classList.remove('hidden');
                } else {
                    deductionsSection.classList.add('hidden');
                }
            }
        });
    }
    
    // Tax Calculation Form
    const taxForm = document.getElementById('taxForm');
    if (taxForm) {
        taxForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const grossIncome = parseFloat(document.getElementById('grossIncome').value);
            const regime = document.getElementById('regime').value;
            
            let deductions = {};
            if (regime === 'old' || regime === 'compare') {
                deductions = {
                    '80C': parseFloat(document.getElementById('deduction80C').value) || 0,
                    '80D': parseFloat(document.getElementById('deduction80D').value) || 0
                };
            }
            
            showLoading('taxResults');
            
            try {
                const response = await TaxAPI.calculateTax({
                    gross_income: grossIncome,
                    regime,
                    deductions
                });
                
                if (response.success) {
                    displayTaxResults(response.data, regime);
                } else {
                    document.getElementById('taxResults').innerHTML = 
                        `<div class="alert alert-danger">${response.message}</div>`;
                }
            } catch (error) {
                document.getElementById('taxResults').innerHTML = 
                    `<div class="alert alert-danger">${error.message}</div>`;
            }
        });
    }
});

function displayTaxResults(data, regime) {
    let html = '<div class="alert alert-success">Tax calculated successfully!</div>';
    
    if (regime === 'compare') {
        // Comparison view
        html += '<h3>Tax Regime Comparison</h3>';
        html += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">';
        
        // New Regime
        html += '<div class="card">';
        html += '<h4>New Regime</h4>';
        html += '<table>';
        html += `<tr><td>Gross Income</td><td>₹${data.new_regime.gross_income.toLocaleString()}</td></tr>`;
        html += `<tr><td>Taxable Income</td><td>₹${data.new_regime.taxable_income.toLocaleString()}</td></tr>`;
        html += `<tr><td>Total Tax</td><td>₹${data.new_regime.total_tax.toLocaleString()}</td></tr>`;
        html += `<tr><td>Effective Tax Rate</td><td>${data.new_regime.effective_tax_rate.toFixed(2)}%</td></tr>`;
        html += '</table>';
        html += '</div>';
        
        // Old Regime
        html += '<div class="card">';
        html += '<h4>Old Regime</h4>';
        html += '<table>';
        html += `<tr><td>Gross Income</td><td>₹${data.old_regime.gross_income.toLocaleString()}</td></tr>`;
        html += `<tr><td>Total Deductions</td><td>₹${data.old_regime.total_deductions.toLocaleString()}</td></tr>`;
        html += `<tr><td>Taxable Income</td><td>₹${data.old_regime.taxable_income.toLocaleString()}</td></tr>`;
        html += `<tr><td>Total Tax</td><td>₹${data.old_regime.total_tax.toLocaleString()}</td></tr>`;
        html += `<tr><td>Effective Tax Rate</td><td>${data.old_regime.effective_tax_rate.toFixed(2)}%</td></tr>`;
        html += '</table>';
        html += '</div>';
        
        html += '</div>';
        
        // Recommendation
        const savings = Math.abs(data.new_regime.total_tax - data.old_regime.total_tax);
        const betterRegime = data.new_regime.total_tax < data.old_regime.total_tax ? 'New Regime' : 'Old Regime';
        
        html += `<div class="alert alert-info">`;
        html += `<strong>Recommendation:</strong> ${betterRegime} is better for you.`;
        html += `<br>You save ₹${savings.toLocaleString()} by choosing ${betterRegime}.`;
        html += `</div>`;
        
    } else {
        // Single regime view
        const regimeData = regime === 'new' ? data.new_regime : data.old_regime;
        const regimeName = regime === 'new' ? 'New Regime' : 'Old Regime';
        
        html += `<h3>${regimeName} Tax Calculation</h3>`;
        html += '<table>';
        html += `<tr><td>Gross Income</td><td>₹${regimeData.gross_income.toLocaleString()}</td></tr>`;
        
        if (regime === 'old' && regimeData.total_deductions) {
            html += `<tr><td>Total Deductions</td><td>₹${regimeData.total_deductions.toLocaleString()}</td></tr>`;
        }
        
        html += `<tr><td>Taxable Income</td><td>₹${regimeData.taxable_income.toLocaleString()}</td></tr>`;
        html += `<tr><td><strong>Total Tax</strong></td><td><strong>₹${regimeData.total_tax.toLocaleString()}</strong></td></tr>`;
        html += `<tr><td>Effective Tax Rate</td><td>${regimeData.effective_tax_rate.toFixed(2)}%</td></tr>`;
        html += '</table>';
        
        // Tax Breakdown by Slab
        if (regimeData.tax_breakdown) {
            html += '<h4>Tax Breakdown by Slab</h4>';
            html += '<table>';
            html += '<tr><th>Income Slab</th><th>Tax Amount</th></tr>';
            regimeData.tax_breakdown.forEach(slab => {
                html += `<tr><td>${slab.slab}</td><td>₹${slab.tax.toLocaleString()}</td></tr>`;
            });
            html += '</table>';
        }
    }
    
    // Tax Slabs Information
    html += '<div class="alert alert-info">';
    html += '<h4>FY 2025-26 Tax Slabs</h4>';
    html += '<p><strong>New Regime:</strong> 0-3L (Nil), 3-7L (5%), 7-10L (10%), 10-12L (15%), 12-15L (20%), 15L+ (30%)</p>';
    html += '<p><strong>Old Regime:</strong> 0-2.5L (Nil), 2.5-5L (5%), 5-10L (20%), 10L+ (30%) with deductions</p>';
    html += '</div>';
    
    document.getElementById('taxResults').innerHTML = html;
}
