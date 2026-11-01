
from src.pdf_reader import extract_pdf_text


def main():
    pdf_path = input("Enter the PDF path: ")

    try:
        result = extract_pdf_text(pdf_path)

        print("\nPDF Processing Successful!")
        print("--------------------------")
        print("File:", result["file_name"])
        print("Total pages:", result["total_pages"])
        print("Total characters:", result["total_characters"])
        print("Pages without text:", result["pages_without_text"])

        print("\nExtracted Text:")
        print(result["full_text"])

    except (FileNotFoundError, ValueError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
