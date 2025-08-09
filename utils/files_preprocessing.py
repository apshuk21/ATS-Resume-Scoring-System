from PyPDF2 import PdfReader
from pathlib import Path


class FilePreprocessing:
    def __init__(self, file_path: Path):
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if file_path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a PDF file, got: {file_path.suffix}")

        self.file_path = file_path
        self.pdf_reader = PdfReader(str(self.file_path))  # Ensure it's a string path

    def extract_text_from_pdf(self) -> str:
        return "\n".join(
            page.extract_text() or ""  # Handle pages with no extractable text
            for page in self.pdf_reader.pages
        )


if __name__ == "__main__":
    pdf_file_path = Path("data") / "sample.pdf"

    pdf_text = FilePreprocessing(file_path=pdf_file_path).extract_text_from_pdf()

    print(pdf_text[:10000])
