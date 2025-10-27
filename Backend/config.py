import os
from datetime import datetime

class Config:
    """Zentrale Konfiguration für Börsenwerk"""
    
    # API Keys
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-key-change-in-production')
    
    # App Settings
    DEBUG = True
    PORT = 5000
    HOST = '0.0.0.0'
    
    # Analysis Settings
    MAX_NEWS_AGE_DAYS = 7
    CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')
    
    # Ampel-Schwellenwerte
    THRESHOLDS = {
        'green_min': 67,
        'yellow_min': 34
    }
    
    # Gewichtung der 5 Kategorien
    CATEGORY_WEIGHTS = {
        'profitability': 25,
        'growth': 25,
        'stability': 20,
        'valuation': 20,
        'cashflow': 10
    }
