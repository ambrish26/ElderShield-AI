import re
from typing import List, Dict


SIGNAL_PATTERNS = {
    "urgency": {
        "patterns": [
            r"\burgent\b",
            r"\burgently\b",
            r"\bimmediately\b",
            r"\bright now\b",
            r"\basap\b",
            r"\bquickly\b",
            r"\bhurry\b",
            r"\bact now\b",
            r"\bdon'?t wait\b",
        ],
        "description": (
            "The message creates pressure to act quickly or immediately."
        ),
    },

    "secrecy": {
        "patterns": [
            r"\bdon'?t tell\b",
            r"\bkeep this secret\b",
            r"\bbetween us\b",
            r"\bdon'?t tell anyone\b",
            r"\bdo not tell\b",
            r"\bkeep it confidential\b",
        ],
        "description": (
            "The message discourages the recipient from discussing the request "
            "with others."
        ),
    },

    "financial_request": {
        "patterns": [
            r"\bsend (?:me )?(?:money|cash)\b",
            r"\btransfer\b",
            r"\bwire\b",
            r"\bpay me\b",
            r"\bpayment\b",
            r"\bneed .{0,20}(?:money|cash|₹|\$|€|£)\b",
            r"[₹$€£]\s?\d+",
        ],
        "description": (
            "The message contains a possible request for money or payment."
        ),
    },

    "credential_request": {
        "patterns": [
            r"\bpassword\b",
            r"\botp\b",
            r"\bone[- ]time password\b",
            r"\bverification code\b",
            r"\bsecurity code\b",
            r"\bpin\b",
            r"\blogin details\b",
        ],
        "description": (
            "The message may be requesting sensitive account or authentication "
            "information."
        ),
    },

    "threat_or_consequence": {
        "patterns": [
            r"\baccount.{0,20}blocked\b",
            r"\baccount.{0,20}suspended\b",
            r"\baccount.{0,20}closed\b",
            r"\blegal action\b",
            r"\bpolice\b",
            r"\barrest\b",
            r"\bfine\b",
            r"\bpenalty\b",
            r"\bconsequences\b",
        ],
        "description": (
            "The message uses a possible threat, penalty, or negative consequence "
            "to pressure the recipient."
        ),
    },
}


def extract_signals(message: str) -> List[Dict]:
    """
    Detect potentially suspicious communication signals.

    This version uses transparent pattern matching so every
    detected signal can be traced back to evidence in the message.
    """

    normalized_message = message.lower()
    detected_signals = []

    for signal_type, config in SIGNAL_PATTERNS.items():
        evidence = []

        for pattern in config["patterns"]:
            matches = re.findall(
                pattern,
                normalized_message,
                flags=re.IGNORECASE
            )

            for match in matches:
                if isinstance(match, tuple):
                    match = " ".join(
                        part for part in match if part
                    )

                if match and match not in evidence:
                    evidence.append(match)

        if evidence:
            detected_signals.append(
                {
                    "type": signal_type,
                    "evidence": evidence,
                    "description": config["description"],
                }
            )

    return detected_signals
