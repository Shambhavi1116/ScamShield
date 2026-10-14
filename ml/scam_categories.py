# ============================================
# SCAMSHIELD - SCAM CATEGORY DETECTOR
# ============================================

import re


# Keywords associated with different scam categories

SCAM_CATEGORIES = {

    "Prize / Reward Scam": [
        "you won",
        "won a prize",
        "cash prize",
        "lucky winner",
        "lottery",
        "reward",
        "claim your prize",
        "congratulations",
        "gift card",
        "free gift"
    ],

    "OTP / Credential Phishing": [
        "otp",
        "one time password",
        "verification code",
        "verify your account",
        "verify your identity",
        "password",
        "login",
        "credentials",
        "pin",
        "cvv"
    ],

    "Banking / UPI Scam": [
        "bank account",
        "upi",
        "upi payment",
        "bank",
        "account blocked",
        "account suspended",
        "transaction",
        "debit",
        "credit",
        "ifsc"
    ],

    "Payment / Refund Scam": [
        "refund",
        "payment failed",
        "payment pending",
        "pay now",
        "make payment",
        "refund amount",
        "cashback",
        "fee",
        "processing fee"
    ],

    "Job / Recruitment Scam": [
        "job offer",
        "work from home",
        "part time job",
        "earn money",
        "salary",
        "hiring",
        "recruitment",
        "vacancy",
        "registration fee",
        "job opportunity"
    ],

    "Delivery Scam": [
        "delivery",
        "parcel",
        "package",
        "courier",
        "shipment",
        "delivery failed",
        "delivery attempt",
        "track your package",
        "customs"
    ],

    "Impersonation Scam": [
        "this is police",
        "police",
        "income tax",
        "government",
        "official notice",
        "your account will be blocked",
        "legal action",
        "arrest",
        "court",
        "officer"
    ],

    "Phishing / Malicious Link": [
        "click here",
        "click the link",
        "open this link",
        "visit this link",
        "verify at",
        "http://",
        "https://",
        "bit.ly",
        "tinyurl"
    ]
}


def detect_scam_categories(message):

    """
    Detect possible scam categories based on
    suspicious keywords and patterns.
    """

    message_lower = message.lower()

    detected_categories = []
    matched_keywords = {}

    for category, keywords in SCAM_CATEGORIES.items():

        matches = []

        for keyword in keywords:

            # Use normal substring matching for phrases
            if keyword in message_lower:
                matches.append(keyword)

        if matches:
            detected_categories.append(category)
            matched_keywords[category] = matches

    # Check for URLs even if they are not common URL keywords
    url_pattern = r"https?://\S+|www\.\S+"

    if re.search(url_pattern, message_lower):

        if "Phishing / Malicious Link" not in detected_categories:
            detected_categories.append("Phishing / Malicious Link")

        matched_keywords.setdefault(
            "Phishing / Malicious Link",
            []
        )

        if "URL detected" not in matched_keywords[
            "Phishing / Malicious Link"
        ]:
            matched_keywords[
                "Phishing / Malicious Link"
            ].append("URL detected")

    return {
        "categories": detected_categories,
        "matched_keywords": matched_keywords
    }