import os
from pathlib import Path
import google.generativeai as agent

BASE = Path("results")
OUT = BASE / "generated"
OUT.mkdir(parents=True, exist_ok=True)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")


def write(p: Path, s: str):
    p.write_text(s, encoding="utf-8")


def model():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Set GOOGLE_API_KEY env var first")
        raise SystemExit(1)
    agent.configure(api_key=api_key)
    return agent.GenerativeModel("gemini-1.5-flash")


def generate(system_rules: str, task: str, evidence: str) -> str:
    m = model()
    prompt = f"""SYSTEM RULES:
{system_rules}

TASK:
{task}

EVIDENCE (ONLY SOURCE OF FACTS):
{evidence}
"""
    
    r = m.generate_content(prompt)
    return (r.text or "").strip()


def main():
    audit = read(BASE / "audit-results.md")
    phase2 = read(BASE / "phase2_results.md")
    roi = read(BASE / "ROI.md")

    evidence = "\n\n".join([
        "=== audit-results.md ===\n" + audit,
        "=== phase2_results.md ===\n" + phase2,
        "=== ROI.md ===\n" + roi,
    ])

    rules = """- Do NOT invent numbers, dates, metrics, product names, or quotes.
- If a claim is not supported by EVIDENCE, write: "Not found in evidence".
- Use short, clear sentences. No fluff.
- When you reference evidence, paste a short quote (max 20 words) from it.
"""
    board_task = """Write a board-level memo:
- TO, FROM, DATE, SUBJECT
- Executive summary (5-7 lines)
- 5-8 evidence-backed findings (each with a short quote)
- 3-5 risks (each tied to evidence)
- 5 recommendations (actionable)
Keep it strict and professional."""

    phase2_task = """Write Phase 2: From symptoms to root causes:
- 5 Whys interview transcript (Auditor vs Arman) grounded in evidence themes
- Root causes list (6-10)
- Constraints & tradeoffs
- What to measure next (metrics list)
No made-up financial numbers."""

    roi_task = """Write ROI reasoning:
- Define 4 ROI levers relevant here
- For each lever: what improves, what evidence hints at it, and what metric to track
No invented numbers."""

    write(OUT / "board_memo.md", generate(rules, board_task, evidence))
    write(OUT / "phase2_expanded.md", generate(rules, phase2_task, evidence))
    write(OUT / "roi_expanded.md", generate(rules, roi_task, evidence))


if __name__ == "__main__":
    main()