import re
from pathlib import Path
import sys


KEYWORDS = {
    "Strategy/Product/Ecosystem": [
        r"strategy", r"strategic", r"ecosystem", r"super\s*app", r"platform", r"product",
        r"marketplace", r"payments?", r"fintech", r"merchant"
    ],
    "Org/Process/Execution": [
        r"process", r"governance", r"committee", r"approval", r"roadmap", r"delivery",
        r"agile", r"sprint", r"waterfall", r"cross[\s-]?functional", r"OKR"
    ],
    "Tech/Cloud/Data": [
        r"cloud", r"AWS|Azure|GCP|Google Cloud", r"data", r"analytics", r"machine learning",
        r"AI\b", r"architecture", r"infrastructure", r"availability", r"scalab"
    ],
    "Risk/Regulation/Security": [
        r"risk", r"regulat", r"compliance", r"cyber", r"security", r"fraud",
        r"AML|KYC", r"sanction", r"privacy", r"personal data"
    ],
    "Business/Metrics": [
        r"revenue", r"net income", r"profit", r"GMV", r"TPV", r"MAU", r"DAU",
        r"loan", r"credit", r"deposit", r"customers?", r"merchants?"
    ],
}


def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def analyze(text: str, window: int = 220, max_hits_per_pattern: int = 5) -> str:
    out = []
    for category, patterns in KEYWORDS.items():
        out.append(f"\n=== {category} ===\n")
        found = False
        for pat in patterns:
            matches = list(re.finditer(pat, text, flags=re.IGNORECASE))
            if not matches:
                continue
            found = True
            for m in matches[:max_hits_per_pattern]:
                a = max(0, m.start() - window)
                b = min(len(text), m.end() + window)
                snippet = normalize_space(text[a:b])
                out.append(f"Match '{pat}': ...{snippet}...\n---\n")
        if not found:
            out.append("No matches found.\n")
    return "".join(out)


def main():
    if len(sys.argv) < 3:
        print("Usage: python analyze_text.py out/input.txt out/analysis_results.txt")
        return
    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    text = in_path.read_text(encoding="utf-8", errors="ignore")
    result = analyze(text)
    out_path.write_text(result, encoding="utf-8")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
