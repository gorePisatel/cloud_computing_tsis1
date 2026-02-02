from pathlib import Path
from datetime import datetime


def write(path: Path, text: str):
      path.write_text(text, encoding="utf-8")

def main():
    out_dir = Path("out")
    out_dir.mkdir(parents=True, exist_ok=True)

    a1 = (out_dir / "analysis_kaspi_20f_2024.txt")
    a2 = (out_dir / "analysis_kaspi_fy2024_fs.txt")

    analysis_text = ""
    if a1.exists():
        analysis_text += "\n\n## 20-F 2024 (snippets)\n\n" + a1.read_text(encoding="utf-8", errors="ignore")
    if a2.exists():
        analysis_text += "\n\n## FY 2024 Financial Statements (snippets)\n\n" + a2.read_text(encoding="utf-8", errors="ignore")


    write(
        out_dir / "audit-results.md",
        f"""# Kaspi Audit Results (Text Evidence) 
Generated: {datetime.now().isoformat(timespec="seconds")}

{analysis_text if analysis_text.strip() else "No analysis files found in out/ . Run analyze_text.py first."}
""")

    write(
        out_dir / "phase_2_jtbd_setup.md",
        """# Phase 2 — JTBD Setup (Kaspi)

## Target “job”
A user wants to pay/buy/transfer money fast and safely, inside one app, with minimal friction.

## Forces (example)
- Push: need to complete purchase/payment quickly
- Pull: convenience of ecosystem (services in one place)
- Anxiety: fraud, account blocks, support issues
- Habit: using Kaspi daily for payments/marketplace
""")

    write(
        out_dir / "phase2_results.md",
        """# Phase 2 — Findings (Kaspi)

## Likely bottlenecks to check in evidence
- Risk/compliance vs user experience (blocks, AML/KYC)
- Scale/infrastructure availability vs incidents
- Governance/approvals slowing iteration
- Product execution: feature delivery vs improvements/quality
""")

    write(
        out_dir / "ROI.md",
        """# ROI Notes (Kaspi)

## What ROI could mean here (examples)
- Lower fraud losses vs higher false-positives (blocked good users)
- Faster checkout -> higher GMV conversion
- Better uptime -> more transactions
- Better support -> retention / NPS
""")

    write(
        out_dir / "README.md",
        """# Kaspi Cloud Computing Task

## Files (final order)
1. [ROI.md](./ROI.md)
2. [audit-results.md](./audit-results.md)
3. [phase2_results.md](./phase2_results.md)
4. [phase_2_jtbd_setup.md](./phase_2_jtbd_setup.md)

## How to run
```bash
pip install -r requirements.txt

python extract_pdf.py data/kaspi_20f_2024.pdf out/kaspi_20f_2024.txt
python analyze_text.py out/kaspi_20f_2024.txt out/analysis_kaspi_20f_2024.txt

python extract_pdf.py data/kaspi_fy2024_fs.pdf out/kaspi_fy2024_fs.txt
python analyze_text.py out/kaspi_fy2024_fs.txt out/analysis_kaspi_fy2024_fs.txt

python build_report.py
""")
    print("Generated: ROI.md, audit-results.md, phase2_results.md, phase_2_jtbd_setup.md, README.md")


if __name__ == "__main__":
    main()