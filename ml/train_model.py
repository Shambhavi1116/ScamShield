import kagglehub
import pandas as pd
import os

# ============================================
# 1. DOWNLOAD DATASET
# ============================================

path = kagglehub.dataset_download(
    "uciml/sms-spam-collection-dataset"
)

print("Dataset path:", path)


# ============================================
# 2. LOAD DATASET
# ============================================

csv_path = os.path.join(path, "spam.csv")

df = pd.read_csv(
    csv_path,
    encoding="latin-1"
)

print("\nOriginal shape:", df.shape)


# ============================================
# 3. REMOVE UNNECESSARY COLUMNS
# ============================================

df = df.iloc[:, :2]

print("After removing unnecessary columns:", df.shape)


# ============================================
# 4. RENAME COLUMNS
# ============================================

df.columns = ["label", "message"]

print("\nColumns after renaming:")
print(df.columns.tolist())


# ============================================
# 5. REMOVE DUPLICATE MESSAGES
# ============================================

df = df.drop_duplicates()

print("\nShape after removing duplicates:", df.shape)


# ============================================
# 6. CHECK MISSING VALUES
# ============================================

print("\nMissing values:")
print(df.isnull().sum())


# ============================================
# 7. DISPLAY CLEAN DATA
# ============================================

print("\nClean dataset:")
print(df.head())

print("\nLabel distribution:")
print(df["label"].value_counts())

# ============================================
# 8. BASIC EDA
# ============================================

print("\nDataset information:")
print(df.info())

print("\nLabel distribution:")
print(df["label"].value_counts())

print("\nLabel percentages:")
print(df["label"].value_counts(normalize=True) * 100)


# ============================================
# 9. CONVERT LABELS TO NUMBERS
# ============================================

df["label_encoded"] = df["label"].map({
    "ham": 0,
    "spam": 1
})

print("\nEncoded labels:")
print(df[["label", "label_encoded"]].head())

# ============================================
# 10. SEPARATE FEATURES AND TARGET
# ============================================

X = df["message"]
y = df["label_encoded"]

print("\nFeatures (X) shape:", X.shape)
print("Target (y) shape:", y.shape)


# ============================================
# 11. TRAIN-TEST SPLIT
# ============================================

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# ============================================
# 12. TF-IDF VECTORIZATION
# ============================================

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_features=5000
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("\nTF-IDF vectorization completed!")

print("X_train TF-IDF shape:", X_train_tfidf.shape)
print("X_test TF-IDF shape:", X_test_tfidf.shape)

# ============================================
# 13. TRAIN LOGISTIC REGRESSION MODEL
# ============================================

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_tfidf, y_train)

print("\nLogistic Regression model trained successfully!")

# ============================================
# 14. MAKE PREDICTIONS ON TEST DATA
# ============================================

y_pred = model.predict(X_test_tfidf)

print("\nPredictions completed!")

print("First 20 predictions:")
print(y_pred[:20])

print("\nActual labels:")
print(y_test.values[:20])

# ============================================
# 15. MODEL EVALUATION
# ============================================

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n========== MODEL EVALUATION ==========")

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")


# Detailed classification report
print("\n========== CLASSIFICATION REPORT ==========")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Ham", "Spam"]
    )
)


# Confusion matrix
print("\n========== CONFUSION MATRIX ==========")

cm = confusion_matrix(y_test, y_pred)

print(cm)

# ============================================
# 16. SAVE MODEL AND TF-IDF VECTORIZER
# ============================================

import joblib
import os

# Create models folder
os.makedirs("../models", exist_ok=True)

# Save trained model
joblib.dump(
    model,
    "../models/scam_classifier.pkl"
)

# Save TF-IDF vectorizer
joblib.dump(
    vectorizer,
    "../models/tfidf_vectorizer.pkl"
)

print("\nModel and vectorizer saved successfully!")