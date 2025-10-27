"""
Fundamental-Analyse Engine für Börsenwerk
Berechnet Scores basierend auf 18 Kennzahlen in 5 Kategorien
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

def determine_signal(score):
    """Bestimmt Ampel-Signal"""
    if score >= Config.THRESHOLDS['green_min']:
        return {'color': 'green', 'text': 'KAUFEN', 'emoji': '🟢'}
    elif score >= Config.THRESHOLDS['yellow_min']:
        return {'color': 'yellow', 'text': 'HALTEN', 'emoji': '🟡'}
    else:
        return {'color': 'red', 'text': 'VERKAUFEN', 'emoji': '🔴'}

def generate_pros_cons(fundamentals, category_scores):
    """Erstellt Pro/Contra Listen"""
    pros = []
    contras = []
    
    # Profitabilität
    if fundamentals.get('net_margin', 0) > 15:
        pros.append(f"Starke Nettomarge von {fundamentals['net_margin']:.1f}%")
    elif fundamentals.get('net_margin', 0) < 5:
        contras.append(f"Schwache Nettomarge von {fundamentals['net_margin']:.1f}%")
    
    if fundamentals.get('roe', 0) > 20:
        pros.append(f"Exzellente ROE von {fundamentals['roe']:.1f}%")
    elif fundamentals.get('roe', 0) < 10:
        contras.append(f"Niedrige ROE von {fundamentals['roe']:.1f}%")
    
    # Wachstum
    if fundamentals.get('revenue_growth_yoy', 0) > 15:
        pros.append(f"Starkes Wachstum von {fundamentals['revenue_growth_yoy']:.1f}% YoY")
    elif fundamentals.get('revenue_growth_yoy', 0) < 3:
        contras.append(f"Schwaches Wachstum von {fundamentals['revenue_growth_yoy']:.1f}% YoY")
    
    # Verschuldung
    if fundamentals.get('debt_to_equity', 999) < 1:
        pros.append(f"Solide Bilanz (D/E: {fundamentals['debt_to_equity']:.2f})")
    elif fundamentals.get('debt_to_equity', 0) > 2:
        contras.append(f"Hohe Verschuldung (D/E: {fundamentals['debt_to_equity']:.2f})")
    
    # Bewertung
    if fundamentals.get('pe_ratio', 999) < 15:
        pros.append(f"Günstige Bewertung (KGV: {fundamentals['pe_ratio']:.1f})")
    elif fundamentals.get('pe_ratio', 0) > 30:
        contras.append(f"Teure Bewertung (KGV: {fundamentals['pe_ratio']:.1f})")
    
    if fundamentals.get('peg_ratio', 999) < 1:
        pros.append(f"Attraktive PEG-Ratio von {fundamentals['peg_ratio']:.2f}")
    
    # Cashflow
    if fundamentals.get('fcf', 0) > 0:
        pros.append(f"Positiver FCF: {fundamentals['fcf']:,.0f} Mio.")
    else:
        contras.append("Negativer Free Cashflow")
    
    if fundamentals.get('dividend_yield', 0) > 3:
        pros.append(f"Hohe Dividende: {fundamentals['dividend_yield']:.2f}%")
    
    # Kategorien
    for cat, score in category_scores.items():
        cat_names = {
            'profitability': 'Profitabilität',
            'growth': 'Wachstum',
            'stability': 'Stabilität',
            'valuation': 'Bewertung',
            'cashflow': 'Cashflow'
        }
        if score > 75:
            pros.append(f"Starke {cat_names[cat]} ({score:.0f}/100)")
        elif score < 40:
            contras.append(f"Schwache {cat_names[cat]} ({score:.0f}/100)")
    
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
