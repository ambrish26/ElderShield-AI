from typing import List
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """
    The message submitted by the user for analysis.
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The communication message to analyze."
    )


class Signal(BaseModel):
    """
    A potentially suspicious signal detected in a message.
    """

    type: str
    evidence: List[str]
    description: str


class AnalyzeResponse(BaseModel):
    """
    Structured result returned after message analysis.
    """

    risk_score: int = Field(
        ...,
        ge=0,
        le=100
    )

    risk_level: str

    signals: List[Signal]

    explanation: str

    recommended_action: str
