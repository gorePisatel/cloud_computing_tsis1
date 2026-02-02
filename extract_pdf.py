from pypdf import PdfReader
from pathlib import Path
import sys


def extract_with_pypdf(pdf_path: Path) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()


def extract_with_pymupdf(pdf_path: Path) -> str:
    import fitz
    doc = fitz.open(str(pdf_path))
    parts = []
    for page in doc:
        parts.append(page.get_text("text") or "")
    return "\n".join(parts).strip()


def extract(pdf_path: Path) -> str:
    text = extract_with_pypdf(pdf_path)
    if len(text) >= 500:
        print("Extractor: pypdf")
        return text
    print("Extractor: pymupdf")
    return extract_with_pymupdf(pdf_path)


def main():
    if len(sys.argv) < 3:
        print("Usage: python extra_pdf.py data/input.pdf out/output.txt")
        return
    pdf_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    text = extract(pdf_path)
    out_path.write_text(text, encoding="utf-8")
    print(f"Saved: {out_path} (chars: {len(text)})")


if __name__ == "__main__":
    main()
