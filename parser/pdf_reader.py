import pdfplumber


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF resume.
    """

    # Remove accidental quotes from the file path
    file_path = file_path.strip().strip('"').strip("'")

    text = ""

    try:

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text.strip()

    except Exception as e:

        print("Error while reading PDF:")
        print(e)

        return ""


if __name__ == "__main__":

    print("=" * 70)
    print("PDF TEXT EXTRACTION TEST")
    print("=" * 70)

    file_path = input(
        "\nEnter PDF file path: "
    )

    extracted_text = extract_text_from_pdf(
        file_path
    )

    if extracted_text:

        print(
            "\nPDF text extracted successfully!"
        )

        print("\n" + "=" * 70)
        print("EXTRACTED TEXT")
        print("=" * 70)

        print(
            extracted_text[:5000]
        )

    else:

        print(
            "\nNo text could be extracted from the PDF."
        )