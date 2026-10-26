import os
import joblib

from preprocessing.clean_text import clean_resume


# ============================================================
# FILE PATHS
# ============================================================

MODEL_PATH = "model/svm_model.pkl"
TFIDF_PATH = "model/tfidf.pkl"
ENCODER_PATH = "model/label_encoder.pkl"


# ============================================================
# LOAD TRAINED FILES
# ============================================================

print("=" * 70)
print("LOADING TRAINED MODEL")
print("=" * 70)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

if not os.path.exists(TFIDF_PATH):
    raise FileNotFoundError(
        f"TF-IDF vectorizer not found: {TFIDF_PATH}"
    )

if not os.path.exists(ENCODER_PATH):
    raise FileNotFoundError(
        f"Label encoder not found: {ENCODER_PATH}"
    )


svm_model = joblib.load(MODEL_PATH)

tfidf = joblib.load(TFIDF_PATH)

label_encoder = joblib.load(ENCODER_PATH)


print("SVM model loaded successfully!")
print("TF-IDF vectorizer loaded successfully!")
print("Label encoder loaded successfully!")


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_resume(resume_text):

    # --------------------------------------------------------
    # Check input
    # --------------------------------------------------------

    if not resume_text:
        return None, 0.0

    if not resume_text.strip():
        return None, 0.0


    # --------------------------------------------------------
    # TEXT PREPROCESSING
    # --------------------------------------------------------

    cleaned_text = clean_resume(
        resume_text
    )


    # --------------------------------------------------------
    # TF-IDF TRANSFORMATION
    # --------------------------------------------------------

    resume_vector = tfidf.transform(
        [cleaned_text]
    )


    # --------------------------------------------------------
    # PREDICT CATEGORY
    # --------------------------------------------------------

    prediction = svm_model.predict(
        resume_vector
    )


    # --------------------------------------------------------
    # CONVERT NUMBER TO CATEGORY
    # --------------------------------------------------------

    predicted_category = label_encoder.inverse_transform(
        prediction
    )[0]


    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = 0.0

    if hasattr(svm_model, "predict_proba"):

        probabilities = svm_model.predict_proba(
            resume_vector
        )

        confidence = probabilities.max() * 100


    return predicted_category, confidence


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("RESUME CLASSIFICATION")
    print("=" * 70)

    print("\nEnter resume text below.")
    print("Type END on a new line when finished.\n")


    resume_lines = []

    while True:

        line = input()

        if line.strip().upper() == "END":
            break

        resume_lines.append(line)


    resume_text = "\n".join(
        resume_lines
    )


    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    predicted_category, confidence = predict_resume(
        resume_text
    )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("PREDICTION RESULT")
    print("=" * 70)

    if predicted_category is None:

        print("\nNo resume text was provided.")

    else:

        print(
            "\nPredicted Job Category:"
        )

        print(
            predicted_category
        )

        print(
            f"\nPrediction Confidence: {confidence:.2f}%"
        )

    print("\n" + "=" * 70)
    print("PREDICTION COMPLETED")
    print("=" * 70)