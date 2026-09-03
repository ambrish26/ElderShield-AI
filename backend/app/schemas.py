from typing import List
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    message: str


class Signal(BaseModel):
    type: str
    evidence: List[str]
    description: str


class Intent(BaseModel):
    intent: str
    evidence: List[str]


class AnalyzeResponse(BaseModel):
    risk_score: int
    risk_level: str
    signals: List[Signal]
    intents: List[Intent]
    explanation: str
    recommended_action: str