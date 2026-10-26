import os
import pandas as pd
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
print("FAIR MODEL EVALUATION")
print("=" * 70)

df = pd.read_csv("dataset/UpdatedResumeDataSet.csv")

print("\nOriginal Dataset Shape:", df.shape)


# ============================================================
# STEP 2: CHECK MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("CHECKING DATA")
print("=" * 70)

print("\nMissing Values:")
print(df.isnull().sum())

df = df.dropna(
    subset=["Category", "Resume"]
).reset_index(drop=True)

print("\nDataset Shape after removing missing values:")
print(df.shape)


# ============================================================
# STEP 3: REMOVE DUPLICATES
# ============================================================

print("\n" + "=" * 70)
print("REMOVING DUPLICATES FOR FAIR EVALUATION")
print("=" * 70)

duplicate_count = df.duplicated(
    subset=["Category", "Resume"]
).sum()

print("Duplicate Resume Records:", duplicate_count)

df = df.drop_duplicates(
    subset=["Category", "Resume"]
).reset_index(drop=True)

print("Unique Dataset Shape:", df.shape)


# ============================================================
# STEP 4: CATEGORY INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("JOB CATEGORY INFORMATION")
print("=" * 70)

total_categories = df["Category"].nunique()

print("\nTotal Categories:", total_categories)

print("\nCategory Distribution:")
print(df["Category"].value_counts())


# ============================================================
# STEP 5: TEXT PREPROCESSING
# ============================================================

print("\n" + "=" * 70)
print("TEXT PREPROCESSING")
print("=" * 70)

print("\nCleaning all resumes...")

df["Cleaned_Resume"] = df["Resume"].apply(
    clean_resume
)

print("Cleaning completed successfully!")


# ============================================================
# STEP 6: LABEL ENCODING
# ============================================================

print("\n" + "=" * 70)
print("LABEL ENCODING")
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
# STEP 7: TF-IDF VECTORIZATION
# ============================================================

print("\n" + "=" * 70)
print("TF-IDF VECTORIZATION")
print("=" * 70)

tfidf = TfidfVectorizer(
    max_features=5000,
    sublinear_tf=True
)

X = tfidf.fit_transform(
    df["Cleaned_Resume"]
)

y = df["Category_Encoded"]

print("TF-IDF completed!")

print("\nTF-IDF Matrix Shape:")
print(X.shape)

print("\nTarget Shape:")
print(y.shape)


# ============================================================
# STEP 8: TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 70)
print("TRAIN / TEST SPLIT")
print("=" * 70)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# IMPORTANT:
# X_train and X_test are sparse matrices.
# Use shape[0], NOT len().

training_samples = X_train.shape[0]
testing_samples = X_test.shape[0]

print("\nTraining Samples:", training_samples)
print("Testing Samples :", testing_samples)


# ============================================================
# STEP 9: TRAIN SVM MODEL
# ============================================================

print("\n" + "=" * 70)
print("TRAINING SVM MODEL")
print("=" * 70)

print("\nTraining Support Vector Machine...")

svm_model = SVC(
    kernel="linear",
    probability=True,
    random_state=42
)

svm_model.fit(
    X_train,
    y_train
)

print("SVM training completed!")


# ============================================================
# STEP 10: MAKE PREDICTIONS
# ============================================================

print("\n" + "=" * 70)
print("MAKING PREDICTIONS")
print("=" * 70)

y_pred = svm_model.predict(
    X_test
)

print("Prediction completed!")


# ============================================================
# STEP 11: MODEL ACCURACY
# ============================================================

print("\n" + "=" * 70)
print("MODEL ACCURACY")
print("=" * 70)

accuracy = accuracy_score(
    y_test,
    y_pred
)

accuracy_percentage = accuracy * 100

print(
    "\nFair SVM Accuracy: "
    + format(accuracy_percentage, ".2f")
    + "%"
)


# ============================================================
# STEP 12: CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

classification_rep = classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_,
    zero_division=0
)

print(classification_rep)


# ============================================================
# STEP 13: CONFUSION MATRIX
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
# STEP 14: SAVE CONFUSION MATRIX
# ============================================================

print("\n" + "=" * 70)
print("CREATING CONFUSION MATRIX VISUALIZATION")
print("=" * 70)

os.makedirs(
    "assets",
    exist_ok=True
)

plt.figure(
    figsize=(16, 12)
)

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=label_encoder.classes_,
    yticklabels=label_encoder.classes_
)

plt.title(
    "Resume Classification - SVM Fair Evaluation"
)

plt.xlabel(
    "Predicted Category"
)

plt.ylabel(
    "Actual Category"
)

plt.xticks(
    rotation=90
)

plt.yticks(
    rotation=0
)

plt.tight_layout()

confusion_matrix_path = "assets/fair_confusion_matrix.png"

plt.savefig(
    confusion_matrix_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "\nConfusion matrix saved successfully!"
)

print(
    "Location:",
    confusion_matrix_path
)


# ============================================================
# STEP 15: SAVE EVALUATION RESULTS
# ============================================================

print("\n" + "=" * 70)
print("SAVING EVALUATION RESULTS")
print("=" * 70)

actual_categories = label_encoder.inverse_transform(
    y_test
)

predicted_categories = label_encoder.inverse_transform(
    y_pred
)

evaluation_results = pd.DataFrame({
    "Actual": actual_categories,
    "Predicted": predicted_categories
})

evaluation_results_path = (
    "dataset/evaluation_results.csv"
)

evaluation_results.to_csv(
    evaluation_results_path,
    index=False
)

print(
    "Evaluation results saved successfully!"
)

print(
    "Location:",
    evaluation_results_path
)


# ============================================================
# STEP 16: SAVE EVALUATION SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SAVING EVALUATION SUMMARY")
print("=" * 70)

summary = pd.DataFrame({
    "Metric": [
        "Original Dataset",
        "Duplicate Records",
        "Unique Resumes",
        "Total Categories",
        "Training Samples",
        "Testing Samples",
        "TF-IDF Features",
        "SVM Accuracy"
    ],
    "Value": [
        962,
        duplicate_count,
        df.shape[0],
        total_categories,
        training_samples,
        testing_samples,
        X.shape[1],
        format(accuracy_percentage, ".2f") + "%"
    ]
})

summary_path = "dataset/evaluation_summary.csv"

summary.to_csv(
    summary_path,
    index=False
)

print(
    "Evaluation summary saved successfully!"
)

print(
    "Location:",
    summary_path
)


# ============================================================
# STEP 17: FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FAIR EVALUATION COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nOriginal Dataset       :", 962)
print("Duplicate Records      :", duplicate_count)
print("Unique Resumes         :", df.shape[0])
print("Total Categories       :", total_categories)
print("Training Samples       :", training_samples)
print("Testing Samples        :", testing_samples)
print("TF-IDF Features        :", X.shape[1])
print(
    "Fair SVM Accuracy      :",
    format(accuracy_percentage, ".2f") + "%"
)

print("\nOutput Files:")

print(
    "1. assets/fair_confusion_matrix.png"
)

print(
    "2. dataset/evaluation_results.csv"
)

print(
    "3. dataset/evaluation_summary.csv"
)

print("\n" + "=" * 70)
print("EVALUATION FINISHED")
print("=" * 70)