"""
Börsenwerk Backend - Flask API Server
Hauptserver für Fundamental-Analyse mit Claude AI
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from config import Config
from analyzer import (
    calculate_category_scores,
    determine_signal,
    generate_pros_cons,
    calculate_data_quality,
    get_simple_explanation,
    generate_simple_summary
)

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

def call_claude_api(prompt):
    """Ruft Claude API auf"""
    headers = {
        'x-api-key': Config.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    }
    
    data = {
        'model': 'claude-sonnet-4-20250514',
        'max_tokens': 4000,
        'messages': [{
            'role': 'user',
            'content': prompt
        }]
    }
    
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()['content'][0]['text']
    else:
        raise Exception(f"API Error: {response.status_code}")

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Hauptendpoint für Aktienanalyse"""
    try:
        data = request.json
        ticker = data.get('ticker', '').upper()
        
        if not ticker:
            return jsonify({'error': 'Ticker erforderlich'}), 400
        
        if not Config.ANTHROPIC_API_KEY:
            return jsonify({'error': 'API Key nicht konfiguriert'}), 500
        
        # Prompt für Claude
        prompt = f"""Du bist ein professioneller Finanzanalyst. Analysiere die Aktie {ticker}.

Gib die Analyse in folgendem EXAKTEN JSON-Format zurück (keine zusätzlichen Texte, nur JSON):

{{
  "ticker": "{ticker}",
  "company_name": "Vollständiger Firmenname",
  "sector": "Branche",
  "current_price": 123.45,
  "currency": "USD oder EUR",
  "fundamentals": {{
    "net_margin": 15.5,
    "gross_margin": 42.0,
    "roe": 18.5,
    "roic": 12.3,
    "revenue_growth_yoy": 8.5,
    "eps_growth": 10.2,
    "fcf_growth": 5.5,
    "debt_to_equity": 0.65,
    "interest_coverage": 8.2,
    "current_ratio": 1.8,
    "pe_ratio": 22.5,
    "peg_ratio": 1.2,
    "pb_ratio": 3.5,
    "ps_ratio": 2.1,
    "ev_ebitda": 14.5,
    "fcf": 5000,
    "payout_ratio": 35.0,
    "dividend_yield": 2.5
  }},
  "news": [
    {{
      "title": "Nachrichtentitel 1",
      "summary": "Kurze Zusammenfassung",
      "date": "2025-10-25",
      "sentiment": "positiv"
    }},
    {{
      "title": "Nachrichtentitel 2",
      "summary": "Kurze Zusammenfassung",
      "date": "2025-10-24",
      "sentiment": "neutral"
    }}
  ]
}}

WICHTIG:
- Alle Werte in fundamentals müssen numerisch sein (null wenn unbekannt)
- News nur aus den letzten 7 Tagen (heute ist {Config.CURRENT_DATE})
- Alle News auf Deutsch
- Sentiment: "positiv", "neutral" oder "negativ"
- Nur VALIDES JSON zurückgeben, keine Markdown-Code-Blöcke
"""
        
        # Claude API aufrufen
        response_text = call_claude_api(prompt)
        
        # JSON parsen (mit Fehlerbehandlung für Markdown)
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        analysis_data = json.loads(response_text)
        
        # Scores berechnen
        fundamentals = analysis_data['fundamentals']
        category_scores = calculate_category_scores(fundamentals)
        
        # Gesamtscore berechnen (gewichtet)
        total_score = sum(
            category_scores[cat] * (Config.CATEGORY_WEIGHTS[cat] / 100)
            for cat in category_scores
        )
        
        # Signal bestimmen
        signal = determine_signal(total_score)
        
        # Pro/Contra generieren
        pros, contras = generate_pros_cons(fundamentals, category_scores)
        
        # Datenqualität
        data_quality = calculate_data_quality(fundamentals)
        
        # Einfache Erklärungen hinzufügen
        simple_explanations = {}
        for cat in category_scores:
            simple_explanations[cat] = get_simple_explanation(
                cat, 
                category_scores[cat], 
                fundamentals
            )
        
        # Einfache Zusammenfassung
        simple_summary = generate_simple_summary(
            category_scores, 
            total_score, 
            fundamentals
        )
        
        # Finale Response
        result = {
            'ticker': analysis_data['ticker'],
            'company_name': analysis_data['company_name'],
            'sector': analysis_data['sector'],
            'current_price': analysis_data['current_price'],
            'currency': analysis_data['currency'],
            'total_score': round(total_score, 1),
            'signal': signal,
            'category_scores': {
                cat: {
                    'score': round(score, 1),
                    'weight': Config.CATEGORY_WEIGHTS[cat]
                }
                for cat, score in category_scores.items()
            },
            'simple_explanations': simple_explanations,
            'simple_summary': simple_summary,
            'fundamentals': fundamentals,
            'pros': pros[:5],
            'contras': contras[:5],
            'news': analysis_data.get('news', [])[:5],
            'data_quality': data_quality,
            'analysis_date': Config.CURRENT_DATE
        }
        
        return jsonify(result)
    
    except json.JSONDecodeError as e:
        return jsonify({
            'error': 'Fehler beim Parsen der Claude-Antwort',
            'details': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Analysefehler',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health Check Endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'Börsenwerk Backend',
        'api_configured': bool(Config.ANTHROPIC_API_KEY)
    })

if __name__ == '__main__':
    print("🚀 Börsenwerk Backend startet...")
    print(f"📡 Server läuft auf http://{Config.HOST}:{Config.PORT}")
    print(f"🔑 API Key konfiguriert: {'✅' if Config.ANTHROPIC_API_KEY else '❌'}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
