import re


INTENT_PATTERNS = {
    "financial_request": [
        r"\bsend\s+(me\s+)?money\b",
        r"\btransfer\b",
        r"\bwire\b",
        r"\bpay\s+me\b",
        r"\bi\s+need\s+\$?\d+\b",
        r"\bneed\s+money\b",
        r"\bneed\s+\$?\d+\b",
        r"\bloan\b",
    ],

    "information_request": [
        r"\bcan\s+you\s+(give|tell|provide)\b",
        r"\bi\s+need\s+info\b",
        r"\bneed\s+information\b",
        r"\btell\s+me\s+about\b",
        r"\bwhat\s+is\b",
        r"\bhow\s+does\b",
        r"\binfo\b",
    ],

    "credential_request": [
        r"\bpassword\b",
        r"\botp\b",
        r"\bverification\s+code\b",
        r"\bsecurity\s+code\b",
        r"\bpin\b",
        r"\blogin\s+details\b",
        r"\baccount\s+details\b",
    ],

    "emergency_claim": [
        r"\bemergency\b",
        r"\bi'?m\s+stuck\b",
        r"\bhelp\s+me\b",
        r"\baccident\b",
        r"\bhospital\b",
        r"\barrested\b",
        r"\bstranded\b",
    ],

    "normal_conversation": [
        r"\bhey\b",
        r"\bhello\b",
        r"\bhow\s+are\s+you\b",
        r"\bwhat'?s\s+up\b",
        r"\bwassup\b",
        r"\bthank\s+you\b",
    ],
}


def analyze_intent(message: str):
    """
    Performs lightweight intent detection using
    interpretable language patterns.

    This MVP intentionally does not use an external LLM.
    """

    normalized_message = message.lower().strip()

    detected_intents = []

    for intent, patterns in INTENT_PATTERNS.items():

        evidence = []

        for pattern in patterns:

            matches = re.findall(
                pattern,
                normalized_message
            )

            if matches:
                evidence.append(pattern)

        if evidence:
            detected_intents.append(
                {
                    "intent": intent,
                    "evidence": evidence
                }
            )

    # If nothing specific was detected,
    # classify it as unknown.
    if not detected_intents:
        detected_intents.append(
            {
                "intent": "unknown",
                "evidence": []
            }
        )

    return detected_intents