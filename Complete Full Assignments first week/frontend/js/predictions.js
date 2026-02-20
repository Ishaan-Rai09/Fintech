// Time Series Predictions

document.addEventListener('DOMContentLoaded', () => {
    const forecastForm = document.getElementById('forecastForm');
    if (forecastForm) {
        forecastForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const dataFile = document.getElementById('dataFile').files[0];
            const dateColumn = document.getElementById('dateColumn').value;
            const valueColumn = document.getElementById('valueColumn').value;
            const method = document.getElementById('method').value;
            const periods = parseInt(document.getElementById('periods').value);
            
            if (!dataFile) {
                showMessage('forecastResults', 'Please select a file', 'error');
                return;
            }
            
            showLoading('forecastResults');
            
            try {
                // Read CSV file
                const text = await dataFile.text();
                const lines = text.split('\n');
                const headers = lines[0].split(',').map(h => h.trim());
                
                const data = [];
                for (let i = 1; i < lines.length; i++) {
                    if (lines[i].trim()) {
                        const values = lines[i].split(',');
                        const row = {};
                        headers.forEach((header, index) => {
                            row[header] = values[index].trim();
                        });
                        data.push(row);
                    }
                }
                
                // Validate columns exist
                if (!headers.includes(dateColumn) || !headers.includes(valueColumn)) {
                    throw new Error('Date or value column not found in CSV');
                }
                
                // Prepare data for API
                const timeSeriesData = data.map(row => ({
                    date: row[dateColumn],
                    value: parseFloat(row[valueColumn])
                }));
                
                // Call forecast API
                const response = await PredictionAPI.forecast({
                    data: timeSeriesData,
                    method,
                    periods
                });
                
                if (response.success) {
                    displayForecastResults(response.data);
                } else {
                    document.getElementById('forecastResults').innerHTML = 
                        `<div class="alert alert-danger">${response.message}</div>`;
                }
            } catch (error) {
                document.getElementById('forecastResults').innerHTML = 
                    `<div class="alert alert-danger">${error.message}</div>`;
            }
        });
    }
});

function displayForecastResults(data) {
    let html = '<div class="alert alert-success">Forecast generated successfully!</div>';
    
    // Method Info
    if (data.method) {
        html += '<div class="card">';
        html += `<h3>Method Used: ${data.method}</h3>`;
        if (data.metrics) {
            html += '<h4>Model Metrics</h4>';
            html += '<table>';
            Object.entries(data.metrics).forEach(([metric, value]) => {
                html += `<tr><td>${metric}</td><td>${typeof value === 'number' ? value.toFixed(4) : value}</td></tr>`;
            });
            html += '</table>';
        }
        html += '</div>';
    }
    
    // Forecast Values
    if (data.forecast && data.forecast.length > 0) {
        html += '<div class="card">';
        html += '<h3>Forecast Values</h3>';
        html += '<table>';
        html += '<tr><th>Period</th><th>Predicted Value</th>';
        if (data.forecast[0].lower_bound !== undefined) {
            html += '<th>Lower Bound (95%)</th><th>Upper Bound (95%)</th>';
        }
        html += '</tr>';
        
        data.forecast.forEach((point, index) => {
            html += `<tr>`;
            html += `<td>T+${index + 1}</td>`;
            html += `<td>${point.value.toFixed(2)}</td>`;
            if (point.lower_bound !== undefined) {
                html += `<td>${point.lower_bound.toFixed(2)}</td>`;
                html += `<td>${point.upper_bound.toFixed(2)}</td>`;
            }
            html += `</tr>`;
        });
        
        html += '</table>';
        html += '</div>';
    }
    
    // Confidence Intervals
    if (data.confidence_intervals) {
        html += '<div class="alert alert-info">';
        html += '<strong>Confidence Intervals:</strong> ';
        html += 'The forecast includes 95% confidence intervals showing the range of likely values.';
        html += '</div>';
    }
    
    // Visualization Placeholder
    html += '<div class="alert alert-info">';
    html += '📊 Chart visualization would appear here with historical data and forecasted values.';
    html += '</div>';
    
    document.getElementById('forecastResults').innerHTML = html;
}
