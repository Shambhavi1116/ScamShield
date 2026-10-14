# ============================================
# SCAMSHIELD - TEST NEW MESSAGE
# ============================================


import joblib
from risk_engine import calculate_risk
from scam_categories import detect_scam_categories


# Load trained model and TF-IDF vectorizer

model = joblib.load("../models/scam_classifier.pkl")
vectorizer = joblib.load("../models/tfidf_vectorizer.pkl")

print("Model and vectorizer loaded successfully!")


# Take message from user

message = input("\nEnter a message to analyze: ")


# Convert message into TF-IDF features

message_tfidf = vectorizer.transform([message])


# Get ML prediction

prediction = model.predict(message_tfidf)[0]

probability = model.predict_proba(message_tfidf)[0]


# Get probability of spam

ml_probability = probability[1]


# Send ML probability to Risk Engine

risk_result = calculate_risk(
    message,
    ml_probability
)

# Detect possible scam categories

category_result = detect_scam_categories(message)


# Display final result

print("\n========== SCAMSHIELD RESULT ==========")

print("Message:", message)

print(f"ML Spam Probability: {ml_probability * 100:.2f}%")

print(f"Risk Score: {risk_result['risk_score']}/100")

print("Classification:", risk_result["classification"])

print("\nScam Categories:")

if category_result["categories"]:
    for category in category_result["categories"]:
        print("-", category)
else:
    print("No specific scam category detected.")


print("\nSuspicious Indicators:")

if risk_result["indicators"]:
    for indicator in risk_result["indicators"]:
        print("⚠", indicator)
else:
    print("No suspicious indicators detected.")

