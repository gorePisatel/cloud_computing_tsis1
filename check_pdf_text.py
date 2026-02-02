from pathlib import Path
import fitz

def main():
    pdf_path = Path("data/kaspi_fy2024_fs.pdf")
    doc = fitz.open(str(pdf_path))

    total = 0
    for i, page in enumerate(doc[:5]):  # проверим первые 5 страниц
        t = page.get_text("text") or ""
        total += len(t)
        print(i + 1, "chars:", len(t))

    print("Total first 5 pages chars:", total)

if __name__ == "__main__":
    main()