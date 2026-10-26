import os

from parser.pdf_reader import extract_text_from_pdf
from parser.docx_reader import extract_text_from_docx
from model.predict import predict_resume


def extract_resume_text(file_path):

    # Remove accidental quotes
    file_path = file_path.strip().strip('"').strip("'")

    if not os.path.exists(file_path):
        print("\nERROR: File does not exist.")
        return ""

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        print("\nReading PDF resume...")

        text = extract_text_from_pdf(
            file_path
        )

    elif extension == ".docx":

        print("\nReading DOCX resume...")

        text = extract_text_from_docx(
            file_path
        )

    else:

        print(
            "\nERROR: Only PDF and DOCX files are supported."
        )

        return ""

    return text


if __name__ == "__main__":

    print("=" * 70)
    print("RESUME FILE CLASSIFICATION")
    print("=" * 70)

    file_path = input(
        "\nEnter PDF/DOCX file path: "
    )

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    resume_text = extract_resume_text(
        file_path
    )

    if not resume_text:

        print(
            "\nNo text could be extracted from the resume."
        )

        exit()


    print(
        "\nResume text extracted successfully!"
    )

    print(
        "\nExtracted characters:",
        len(resume_text)
    )


    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    print(
        "\nAnalyzing resume..."
    )

    predicted_category, confidence = predict_resume(
        resume_text
    )


    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RESUME ANALYSIS RESULT")
    print("=" * 70)

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
    print("ANALYSIS COMPLETED")
    print("=" * 70)