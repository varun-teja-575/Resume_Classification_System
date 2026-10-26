import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from preprocessing.clean_text import clean_resume

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# STEP 1: LOAD DATASET
# ============================================================

print("=" * 70)
print("STEP 1: LOADING DATASET")
print("=" * 70)

df = pd.read_csv("dataset/UpdatedResumeDataSet.csv")

print("Dataset loaded successfully!")
print("Dataset Shape:", df.shape)


# ============================================================
# STEP 2: REMOVE MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("STEP 2: CHECKING DATA")
print("=" * 70)

print("\nMissing Values:")
print(df.isnull().sum())

df = df.dropna(subset=["Category", "Resume"])

print("\nDataset Shape after removing missing values:")
print(df.shape)


# ============================================================
# STEP 3: TEXT PREPROCESSING
# ============================================================

print("\n" + "=" * 70)
print("STEP 3: TEXT PREPROCESSING")
print("=" * 70)

print("Cleaning resumes...")

df["Cleaned_Resume"] = df["Resume"].apply(clean_resume)

print("Cleaning completed successfully!")


# ============================================================
# STEP 4: LABEL ENCODING
# ============================================================

print("\n" + "=" * 70)
print("STEP 4: LABEL ENCODING")
print("=" * 70)

label_encoder = LabelEncoder()

df["Category_Encoded"] = label_encoder.fit_transform(
    df["Category"]
)

print("Encoding completed successfully!")

print("\nCategory Mapping:")

for number, category in enumerate(label_encoder.classes_):
    print(f"{number:2d} --> {category}")


# ============================================================
# STEP 5: TF-IDF VECTORIZATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 5: TF-IDF VECTORIZATION")
print("=" * 70)

tfidf = TfidfVectorizer(
    max_features=5000,
    sublinear_tf=True
)

X = tfidf.fit_transform(
    df["Cleaned_Resume"]
)

y = df["Category_Encoded"]

print("TF-IDF vectorization completed successfully!")

print("\nTF-IDF Matrix Shape:")
print(X.shape)

print("\nTarget Shape:")
print(y.shape)


# ============================================================
# STEP 6: TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 70)
print("STEP 6: TRAIN / TEST SPLIT")
print("=" * 70)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", X_train.shape[0])
print("Testing samples :", X_test.shape[0])

print("\nTraining data shape:")
print(X_train.shape)

print("\nTesting data shape:")
print(X_test.shape)


# ============================================================
# STEP 7: TRAIN SVM MODEL
# ============================================================

print("\n" + "=" * 70)
print("STEP 7: TRAINING SVM MODEL")
print("=" * 70)

print("Training Support Vector Machine...")

svm_model = SVC(
    kernel="linear",
    probability=True,
    random_state=42
)

svm_model.fit(X_train, y_train)

print("SVM training completed successfully!")


# ============================================================
# STEP 8: MAKE PREDICTIONS
# ============================================================

print("\n" + "=" * 70)
print("STEP 8: MAKING PREDICTIONS")
print("=" * 70)

y_pred = svm_model.predict(X_test)

print("Predictions completed successfully!")


# ============================================================
# STEP 9: MODEL ACCURACY
# ============================================================

print("\n" + "=" * 70)
print("STEP 9: MODEL EVALUATION")
print("=" * 70)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nSVM Accuracy: {accuracy * 100:.2f}%")


# ============================================================
# STEP 10: CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

report = classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_,
    zero_division=0
)

print(report)


# ============================================================
# STEP 11: CONFUSION MATRIX
# ============================================================

print("\n" + "=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)


# ============================================================
# STEP 12: SAVE CONFUSION MATRIX IMAGE
# ============================================================

print("\nCreating confusion matrix visualization...")

plt.figure(figsize=(16, 12))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=label_encoder.classes_,
    yticklabels=label_encoder.classes_
)

plt.title("Resume Classification - SVM Confusion Matrix")
plt.xlabel("Predicted Category")
plt.ylabel("Actual Category")

plt.xticks(rotation=90)
plt.yticks(rotation=0)

plt.tight_layout()

os.makedirs("assets", exist_ok=True)

plt.savefig(
    "assets/confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Confusion matrix saved:")
print("assets/confusion_matrix.png")


# ============================================================
# STEP 13: SAVE TRAINED MODEL
# ============================================================

print("\n" + "=" * 70)
print("STEP 13: SAVING MODEL FILES")
print("=" * 70)

os.makedirs("model", exist_ok=True)

# Save SVM model
joblib.dump(
    svm_model,
    "model/svm_model.pkl"
)

# Save TF-IDF vectorizer
joblib.dump(
    tfidf,
    "model/tfidf.pkl"
)

# Save label encoder
joblib.dump(
    label_encoder,
    "model/label_encoder.pkl"
)

print("SVM model saved:")
print("model/svm_model.pkl")

print("\nTF-IDF vectorizer saved:")
print("model/tfidf.pkl")

print("\nLabel encoder saved:")
print("model/label_encoder.pkl")


# ============================================================
# STEP 14: SAVE CLEANED DATASET
# ============================================================

print("\n" + "=" * 70)
print("STEP 14: SAVING CLEANED DATASET")
print("=" * 70)

df.to_csv(
    "dataset/cleaned_resume_dataset.csv",
    index=False
)

print("Cleaned dataset saved successfully!")


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("MODEL TRAINING COMPLETED")
print("=" * 70)

print(f"""
Dataset Size       : {len(df)}
Number of Classes  : {len(label_encoder.classes_)}
TF-IDF Features    : {X.shape[1]}
Training Samples   : {X_train.shape[0]}
Testing Samples    : {X_test.shape[0]}
SVM Accuracy       : {accuracy * 100:.2f}%

Model Files:
    model/svm_model.pkl
    model/tfidf.pkl
    model/label_encoder.pkl

Confusion Matrix:
    assets/confusion_matrix.png
""")

print("=" * 70)
print("READY FOR RESUME PREDICTION!")
print("=" * 70)