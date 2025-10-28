// Börsenwerk Frontend - Main JavaScript

const API_URL = window.location.origin;

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const tickerInput = document.getElementById('tickerInput');
    
    analyzeBtn.addEventListener('click', handleAnalyze);
    
    tickerInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleAnalyze();
        }
    });
});

// Hauptfunktion für Analyse
async function handleAnalyze() {
    const tickerInput = document.getElementById('tickerInput');
    const ticker = tickerInput.value.trim().toUpperCase();
    
    if (!ticker) {
        showError('Bitte geben Sie ein Börsenkürzel ein');
        return;
    }
    
    // UI Updates
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');
    
    analyzeBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    
    hideError();
    hideResults();
    
    try {
        const response = await fetch(`${API_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ticker })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysefehler');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        showError(`Fehler bei der Analyse: ${error.message}`);
    } finally {
        analyzeBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Ergebnisse anzeigen
function displayResults(data) {
    const container = document.getElementById('resultsContainer');
    container.style.display = 'block';
    
    // Company Header
    document.getElementById('companyName').textContent = data.company_name;
    document.getElementById('companyDetails').textContent = `${data.ticker} | ${data.sector}`;
    document.getElementById('currentPrice').textContent = data.current_price.toFixed(2);
    document.getElementById('currency').textContent = data.currency;
    
    // Signal
    const signalCard = document.getElementById('signalCard');
    const signal = data.signal;
    
    signalCard.className = `signal-card ${signal.color}`;
    document.getElementById('signalIcon').textContent = signal.emoji;
    document.getElementById('signalTitle').textContent = signal.text;
    document.getElementById('totalScore').textContent = data.total_score;
    
    // NEUE EINFACHE ZUSAMMENFASSUNG
    if (data.simple_summary) {
        const summaryDiv = document.getElementById('simpleSummary');
        summaryDiv.innerHTML = data.simple_summary.summary.replace(/\n/g, '<br>');
        
        const hintsDiv = document.getElementById('simpleHints');
        if (data.simple_summary.hints && data.simple_summary.hints.length > 0) {
            hintsDiv.innerHTML = data.simple_summary.hints
                .map(hint => `<div class="hint-item">💡 ${hint}</div>`)
                .join('');
        } else {
            hintsDiv.innerHTML = '';
        }
    }
    
    // Kategorien MIT ERKLÄRUNGEN
    const categoriesGrid = document.getElementById('categoriesGrid');
    categoriesGrid.innerHTML = '';
    
    const categoryOrder = ['profitability', 'growth', 'stability', 'valuation', 'cashflow'];
    
    for (const key of categoryOrder) {
        const value = data.category_scores[key];
        const explanation = data.simple_explanations[key];
        
        const card = document.createElement('div');
        card.className = 'category-card';
        
        let barColor = 'green';
        if (value.score < 67) barColor = 'yellow';
        if (value.score < 34) barColor = 'red';
        
        let ratingClass = 'sehr-gut';
        if (value.score < 67) ratingClass = 'okay';
        if (value.score < 34) ratingClass = 'schwach';
        
        card.innerHTML = `
            <div class="category-name">${explanation.emoji} ${explanation.title}</div>
            <div class="category-score">${value.score}</div>
            <div class="category-weight">Gewichtung: ${value.weight}%</div>
            <div class="category-bar">
                <div class="category-fill ${barColor}" style="width: ${value.score}%"></div>
            </div>
            <div class="category-explanation">
                <div class="category-rating ${ratingClass}">${explanation.rating}</div>
                <p>${explanation.explanation}</p>
            </div>
        `;
        
        categoriesGrid.appendChild(card);
    }
    
    // Pro & Contra
    const prosList = document.getElementById('prosList');
    const contrasList = document.getElementById('contrasList');
    
    prosList.innerHTML = data.pros.map(pro => `<li>✓ ${pro}</li>`).join('');
    contrasList.innerHTML = data.contras.map(contra => `<li>✗ ${contra}</li>`).join('');
    
    // News
    const newsList = document.getElementById('newsList');
    
    if (data.news && data.news.length > 0) {
        newsList.innerHTML = data.news.map(news => `
            <div class="news-card">
                <div class="news-header">
                    <div class="news-title">${news.title}</div>
                    <div class="news-date">${formatDate(news.date)}</div>
                </div>
                <div class="news-summary">${news.summary}</div>
                <span class="news-sentiment ${news.sentiment}">${news.sentiment}</span>
            </div>
        `).join('');
    } else {
        newsList.innerHTML = '<div class="news-card"><p>Keine aktuellen Nachrichten verfügbar</p></div>';
    }
    
    // Datenqualität
    const qualityFill = document.getElementById('qualityFill');
    const qualityText = document.getElementById('qualityText');
    
    qualityFill.style.width = `${data.data_quality.score}%`;
    qualityText.textContent = data.data_quality.text;
    
    // Analysedatum
    document.getElementById('analysisDate').textContent = formatDate(data.analysis_date);
    
    // Scroll to results
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Error anzeigen
function showError(message) {
    const errorDisplay = document.getElementById('errorDisplay');
    errorDisplay.textContent = `⚠️ ${message}`;
    errorDisplay.style.display = 'block';
}

// Error verstecken
function hideError() {
    const errorDisplay = document.getElementById('errorDisplay');
    errorDisplay.style.display = 'none';
}

// Results verstecken
function hideResults() {
    const container = document.getElementById('resultsContainer');
    container.style.display = 'none';
}

// Datum formatieren
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('de-DE', options);
}
