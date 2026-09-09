import re


# 1. Define suspicious keyword groups

URGENCY_KEYWORDS = [
    "urgent",
    "immediately",
    "act now",
    "asap",
    "last chance",
    "expires",
    "account blocked",
    "account suspended",
]

FINANCIAL_KEYWORDS = [
    "bank",
    "payment",
    "transfer",
    "refund",
    "money",
    "upi",
    "transaction",
    "credit card",
    "debit card",
]

CREDENTIAL_KEYWORDS = [
    "otp",
    "pin",
    "password",
    "cvv",
    "passcode",
    "verify",
    "login",
]

PRIZE_KEYWORDS = [
    "won",
    "winner",
    "prize",
    "reward",
    "lottery",
    "cash prize",
    "claim",
]


# 2. Detect URLs

def contains_url(message):
    url_pattern = r"https?://\S+|www\.\S+"
    return bool(re.search(url_pattern, message.lower()))


# 3. Main risk analysis function

def calculate_risk(message, ml_probability):

    message_lower = message.lower()

    indicators = []
    rule_score = 0

    # Urgency detection
    if any(keyword in message_lower for keyword in URGENCY_KEYWORDS):
        indicators.append("Urgency or threat detected")
        rule_score += 15

    # Financial detection
    if any(keyword in message_lower for keyword in FINANCIAL_KEYWORDS):
        indicators.append("Financial request detected")
        rule_score += 15

    # Credential detection
    if any(keyword in message_lower for keyword in CREDENTIAL_KEYWORDS):
        indicators.append("Credential or sensitive information request detected")
        rule_score += 20

    # Prize detection
    if any(keyword in message_lower for keyword in PRIZE_KEYWORDS):
        indicators.append("Prize or reward language detected")
        rule_score += 15

    # URL detection
    if contains_url(message):
        indicators.append("URL/link detected")
        rule_score += 20

    # Combine ML probability with rule-based signals
    ml_score = ml_probability * 60

    risk_score = ml_score + rule_score

    # Maximum risk score = 100
    risk_score = min(risk_score, 100)

    # Final classification
    if risk_score >= 70:
        classification = "Scam"

    elif risk_score >= 30:
        classification = "Suspicious"

    else:
        classification = "Safe"

    return {
        "risk_score": round(risk_score, 2),
        "classification": classification,
        "indicators": indicators,
        "ml_probability": round(ml_probability, 4)
    }