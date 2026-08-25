from typing import List, Dict


SIGNAL_WEIGHTS = {
    "urgency": 20,
    "secrecy": 25,
    "financial_request": 25,
    "credential_request": 30,
    "threat_or_consequence": 20,
}


def calculate_risk(signals: List[Dict]) -> Dict:
    """
    Calculate a communication risk score based on
    the combination of detected signals.

    The current scoring model is transparent and deterministic.
    """

    score = 0

    for signal in signals:
        signal_type = signal["type"]
        score += SIGNAL_WEIGHTS.get(signal_type, 0)

    # Combination bonuses:
    # Certain combinations are more suspicious together
    signal_types = {signal["type"] for signal in signals}

    if {"urgency", "financial_request"}.issubset(signal_types):
        score += 10

    if {"secrecy", "financial_request"}.issubset(signal_types):
        score += 15

    if {"urgency", "credential_request"}.issubset(signal_types):
        score += 15

    # Keep score within 0–100
    score = min(score, 100)

    if score >= 75:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_score": score,
        "risk_level": risk_level,
    }
