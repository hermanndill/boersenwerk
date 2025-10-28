"""
Fundamental-Analyse Engine für Börsenwerk - VEREINFACHTE VERSION
Einfache Erklärungen statt Fachbegriffe
"""

from config import Config

def calculate_category_scores(fundamentals):
    """Berechnet Scores für jede der 5 Kategorien"""
    scores = {}
    
    # 1. Profitabilität (25%)
    prof_score = 0
    prof_count = 0
    
    if fundamentals.get('net_margin') is not None:
        nm = fundamentals['net_margin']
        prof_score += 100 if nm > 15 else (50 if nm > 10 else 25)
        prof_count += 1
    
    if fundamentals.get('gross_margin') is not None:
        gm = fundamentals['gross_margin']
        prof_score += 100 if gm > 40 else (50 if gm > 30 else 25)
        prof_count += 1
    
    if fundamentals.get('roe') is not None:
        roe = fundamentals['roe']
        prof_score += 100 if roe > 20 else (75 if roe > 15 else 25)
        prof_count += 1
    
    if fundamentals.get('roic') is not None:
        roic = fundamentals['roic']
        prof_score += 100 if roic > 15 else (50 if roic > 10 else 25)
        prof_count += 1
    
    scores['profitability'] = prof_score / prof_count if prof_count > 0 else 50
    
    # 2. Wachstum (25%)
    growth_score = 0
    growth_count = 0
    
    if fundamentals.get('revenue_growth_yoy') is not None:
        rg = fundamentals['revenue_growth_yoy']
        growth_score += 100 if rg > 15 else (75 if rg > 10 else (50 if rg > 5 else 25))
        growth_count += 1
    
    if fundamentals.get('eps_growth') is not None:
        eg = fundamentals['eps_growth']
        growth_score += 100 if eg > 15 else (50 if eg > 10 else 25)
        growth_count += 1
    
    if fundamentals.get('fcf_growth') is not None:
        fcfg = fundamentals['fcf_growth']
        growth_score += 100 if fcfg > 10 else (50 if fcfg > 0 else 25)
        growth_count += 1
    
    scores['growth'] = growth_score / growth_count if growth_count > 0 else 50
    
    # 3. Stabilität (20%)
    stab_score = 0
    stab_count = 0
    
    if fundamentals.get('debt_to_equity') is not None:
        dte = fundamentals['debt_to_equity']
        stab_score += 100 if dte < 0.5 else (75 if dte < 1 else (50 if dte < 2 else 25))
        stab_count += 1
    
    if fundamentals.get('interest_coverage') is not None:
        ic = fundamentals['interest_coverage']
        stab_score += 100 if ic > 10 else (75 if ic > 5 else 25)
        stab_count += 1
    
    if fundamentals.get('current_ratio') is not None:
        cr = fundamentals['current_ratio']
        stab_score += 100 if 1.5 <= cr <= 2.5 else (50 if cr > 1 else 25)
        stab_count += 1
    
    scores['stability'] = stab_score / stab_count if stab_count > 0 else 50
    
    # 4. Bewertung (20%)
    val_score = 0
    val_count = 0
    
    if fundamentals.get('pe_ratio') is not None:
        pe = fundamentals['pe_ratio']
        val_score += 100 if pe < 15 else (50 if pe < 25 else 25)
        val_count += 1
    
    if fundamentals.get('peg_ratio') is not None:
        peg = fundamentals['peg_ratio']
        val_score += 100 if peg < 1 else (50 if peg < 2 else 25)
        val_count += 1
    
    if fundamentals.get('pb_ratio') is not None:
        pb = fundamentals['pb_ratio']
        val_score += 100 if pb < 2 else (50 if pb < 5 else 25)
        val_count += 1
    
    scores['valuation'] = val_score / val_count if val_count > 0 else 50
    
    # 5. Cashflow (10%)
    cf_score = 0
    cf_count = 0
    
    if fundamentals.get('fcf') is not None:
        fcf = fundamentals['fcf']
        cf_score += 100 if fcf > 0 else 25
        cf_count += 1
    
    if fundamentals.get('dividend_yield') is not None:
        dy = fundamentals['dividend_yield']
        cf_score += 100 if dy > 3 else (50 if dy > 1 else 25)
        cf_count += 1
    
    scores['cashflow'] = cf_score / cf_count if cf_count > 0 else 50
    
    return scores

def get_simple_explanation(category, score, fundamentals):
    """Gibt einfache Erklärung für Laien zurück"""
    
    explanations = {
        'profitability': {
            'title': 'Verdient die Firma gut Geld?',
            'high': 'Die Firma macht SEHR GUTEN Gewinn! Bei jedem verkauften Produkt bleibt viel Geld übrig.',
            'medium': 'Die Firma verdient okay Geld, aber könnte effizienter arbeiten.',
            'low': 'Die Firma verdient wenig oder macht sogar Verluste. Das ist riskant!'
        },
        'growth': {
            'title': 'Wächst die Firma?',
            'high': 'Die Firma wächst SCHNELL! Immer mehr Umsatz und Gewinn.',
            'medium': 'Die Firma wächst langsam aber stetig. Normales Wachstum.',
            'low': 'Die Firma wächst kaum oder schrumpft sogar. Reifes/altes Unternehmen.'
        },
        'stability': {
            'title': 'Ist die Firma finanziell stabil?',
            'high': 'Die Firma hat wenig Schulden und steht sehr stabil da. Kein Risiko!',
            'medium': 'Die Firma hat etwas Schulden, aber nichts Gefährliches.',
            'low': 'Die Firma hat VIELE Schulden! Könnte in Schwierigkeiten geraten.'
        },
        'valuation': {
            'title': 'Ist der Aktienkurs fair?',
            'high': 'Die Aktie ist GÜNSTIG! Der Preis ist niedriger als der wahre Wert.',
            'medium': 'Der Preis ist okay - nicht teuer, nicht billig.',
            'low': 'Die Aktie ist TEUER! Jeder zahlt gerade viel zu viel für diese Aktie.'
        },
        'cashflow': {
            'title': 'Hat die Firma genug Geld?',
            'high': 'Die Firma hat viel Bargeld und zahlt gute Dividenden!',
            'medium': 'Die Firma hat genug Geld für den Betrieb.',
            'low': 'Die Firma hat Geldprobleme. Wenig freies Bargeld verfügbar.'
        }
    }
    
    cat_data = explanations[category]
    
    if score >= 67:
        level = 'high'
        emoji = '🟢'
        rating = 'SEHR GUT'
    elif score >= 34:
        level = 'medium'
        emoji = '🟡'
        rating = 'OKAY'
    else:
        level = 'low'
        emoji = '🔴'
        rating = 'SCHWACH'
    
    return {
        'title': cat_data['title'],
        'explanation': cat_data[level],
        'emoji': emoji,
        'rating': rating,
        'score': round(score, 1)
    }

def generate_simple_summary(category_scores, total_score, fundamentals):
    """Erstellt eine einfache Zusammenfassung für Laien"""
    
    # Bewerte die einzelnen Kategorien
    prof = category_scores['profitability']
    growth = category_scores['growth']
    stab = category_scores['stability']
    val = category_scores['valuation']
    cf = category_scores['cashflow']
    
    # Bestimme Hauptproblem/Hauptvorteil
    best_cat = max(category_scores, key=category_scores.get)
    worst_cat = min(category_scores, key=category_scores.get)
    
    cat_names = {
        'profitability': 'beim Geldverdienen',
        'growth': 'beim Wachstum',
        'stability': 'bei der Stabilität',
        'valuation': 'beim Preis',
        'cashflow': 'beim Cashflow'
    }
    
    # Haupt-Zusammenfassung
    if total_score >= 67:
        summary = f"✅ **GUTE INVESTITION**\n\nDiese Firma ist stark {cat_names[best_cat]}."
    elif total_score >= 50:
        summary = f"🟡 **VORSICHTIG**\n\nDie Firma ist okay, aber hat Schwächen {cat_names[worst_cat]}."
    elif total_score >= 34:
        summary = f"⚠️ **NUR FÜR ERFAHRENE**\n\nDie Firma hat Probleme {cat_names[worst_cat]}."
    else:
        summary = f"❌ **BESSER NICHT**\n\nDie Firma hat große Schwächen {cat_names[worst_cat]}."
    
    # Spezielle Hinweise
    hints = []
    
    if prof > 75 and val < 40:
        hints.append("Die Firma ist exzellent, aber die Aktie ist zu teuer. Warten Sie auf einen besseren Preis!")
    
    if growth < 40:
        hints.append("Die Firma wächst kaum noch. Gut für Stabilität, schlecht für schnelle Gewinne.")
    
    if stab < 40:
        hints.append("ACHTUNG: Viele Schulden! Nur für risikobereite Anleger.")
    
    if val > 70:
        hints.append("SCHNÄPPCHEN! Die Aktie ist günstig bewertet. Guter Einstiegszeitpunkt.")
    
    if cf > 70 and fundamentals.get('dividend_yield', 0) > 3:
        hints.append("Gute Dividende! Perfekt für regelmäßige Einkünfte.")
    
    return {
        'summary': summary,
        'hints': hints[:3]  # Max 3 Hinweise
    }

def determine_signal(score):
    """Bestimmt Ampel-Signal"""
    if score >= 67:
        return {'color': 'green', 'text': 'KAUFEN', 'emoji': '🟢'}
    elif score >= 34:
        return {'color': 'yellow', 'text': 'HALTEN', 'emoji': '🟡'}
    else:
        return {'color': 'red', 'text': 'VERKAUFEN', 'emoji': '🔴'}

def generate_pros_cons(fundamentals, category_scores):
    """Erstellt Pro/Contra Listen"""
    pros = []
    contras = []
    
    # Profitabilität
    if fundamentals.get('net_margin', 0) > 15:
        pros.append(f"Verdient sehr gut: {fundamentals['net_margin']:.1f}% Gewinnmarge")
    elif fundamentals.get('net_margin', 0) < 5:
        contras.append(f"Verdient wenig: Nur {fundamentals['net_margin']:.1f}% Gewinnmarge")
    
    if fundamentals.get('roe', 0) > 20:
        pros.append(f"Sehr profitabel: {fundamentals['roe']:.1f}% Eigenkapitalrendite")
    elif fundamentals.get('roe', 0) < 10:
        contras.append(f"Schwach profitabel: Nur {fundamentals['roe']:.1f}% Eigenkapitalrendite")
    
    # Wachstum
    if fundamentals.get('revenue_growth_yoy', 0) > 15:
        pros.append(f"Starkes Wachstum: +{fundamentals['revenue_growth_yoy']:.1f}% Umsatz pro Jahr")
    elif fundamentals.get('revenue_growth_yoy', 0) < 3:
        contras.append(f"Kaum Wachstum: Nur +{fundamentals['revenue_growth_yoy']:.1f}% Umsatz pro Jahr")
    
    # Verschuldung
    if fundamentals.get('debt_to_equity', 999) < 1:
        pros.append(f"Wenig Schulden: Verhältnis von {fundamentals['debt_to_equity']:.2f}")
    elif fundamentals.get('debt_to_equity', 0) > 2:
        contras.append(f"Viele Schulden: Verhältnis von {fundamentals['debt_to_equity']:.2f}")
    
    # Bewertung
    if fundamentals.get('pe_ratio', 999) < 15:
        pros.append(f"Günstig bewertet: KGV von {fundamentals['pe_ratio']:.1f}")
    elif fundamentals.get('pe_ratio', 0) > 30:
        contras.append(f"Teuer bewertet: KGV von {fundamentals['pe_ratio']:.1f}")
    
    if fundamentals.get('peg_ratio', 999) < 1:
        pros.append(f"Sehr günstig fürs Wachstum: PEG {fundamentals['peg_ratio']:.2f}")
    
    # Cashflow
    if fundamentals.get('fcf', 0) > 0:
        pros.append(f"Hat freies Geld: {fundamentals['fcf']:,.0f} Millionen")
    else:
        contras.append("Kein freies Geld übrig")
    
    if fundamentals.get('dividend_yield', 0) > 3:
        pros.append(f"Hohe Dividende: {fundamentals['dividend_yield']:.2f}% pro Jahr")
    elif fundamentals.get('dividend_yield', 0) < 1 and fundamentals.get('dividend_yield', 0) > 0:
        contras.append(f"Niedrige Dividende: Nur {fundamentals['dividend_yield']:.2f}%")
    
    # Kategorien
    for cat, score in category_scores.items():
        cat_names = {
            'profitability': 'Gewinn',
            'growth': 'Wachstum',
            'stability': 'Stabilität',
            'valuation': 'Bewertung',
            'cashflow': 'Cashflow'
        }
        if score > 75:
            pros.append(f"Starker {cat_names[cat]} ({score:.0f}/100)")
        elif score < 40:
            contras.append(f"Schwacher {cat_names[cat]} ({score:.0f}/100)")
    
    return pros, contras

def calculate_data_quality(fundamentals):
    """Berechnet Datenqualität"""
    total = 18
    available = sum(1 for v in fundamentals.values() if v is not None)
    quality_pct = (available / total) * 100
    
    return {
        'score': round(quality_pct, 0),
        'available': available,
        'total': total,
        'text': f"{available} von {total} Kennzahlen verfügbar"
    }
