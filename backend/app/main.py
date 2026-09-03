from fastapi import FastAPI
from .intent_engine import analyze_intent
from .schemas import AnalyzeRequest, AnalyzeResponse
from .analyzer import extract_signals
from .risk_engine import calculate_risk


app = FastAPI(
    title="ElderShield AI",
    description="An explainable communication-risk analysis prototype.",
    version="0.1.0",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none"
    }
)


@app.get("/",include_in_schema=False)
def health_check():
    return {
        "status": "online",
        "service": "ElderShield AI"
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_message(request: AnalyzeRequest):
    """
    Analyze a message for potentially suspicious
    communication patterns.
    """

    # Step 1: Extract observable signals
    signals = extract_signals(request.message)

    intents = analyze_intent(request.message)
    
    # Step 2: Calculate risk
    risk_result = calculate_risk(signals)

    # Step 3: Build explanation
    if signals:
        signal_names = [
            signal["type"].replace("_", " ")
            for signal in signals
        ]

        explanation = (
            "The analysis detected the following communication "
            f"risk signals: {', '.join(signal_names)}."
        )
    else:
        explanation = (
            "The prototype did not detect any predefined "
            "communication-risk signals."
        )

    # Step 4: Recommend an action
    if risk_result["risk_level"] == "HIGH":
        recommended_action = (
            "Do not act immediately. Verify the sender through "
            "a separate trusted channel before sending money, "
            "sharing credentials, or taking further action."
        )

    elif risk_result["risk_level"] == "MEDIUM":
        recommended_action = (
            "Proceed cautiously and independently verify the "
            "request before taking action."
        )

    else:
        recommended_action = (
            "No major predefined risk signals were detected. "
            "However, remain cautious with unexpected requests."
        )

    return {
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"],
        "signals": signals,
        "explanation": explanation,
        "recommended_action": recommended_action,
    }
