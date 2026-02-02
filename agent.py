import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as agent


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def build_context() -> str:
    parts = []

    # итоговые md
    for p in [
        Path("audit-results.md"),
        Path("ROI.md"),
        Path("phase2_results.md"),
        Path("phase_2_jtbd_setup.md"),
        Path("README.md")
    ]:
        t = read_text(p)
        if t:
            parts.append(f"\n\n===== FILE:{p.name} =====\n{t}\n")

    # analysis из out/
    for p in [
        Path("out/analysis_kaspi_20f_2024.txt"),
        Path("out/analysis_kaspi_fy2024_fs.txt")
    ]:
        t = read_text(p)
        if t:
            parts.append(f"\n\n ===== FILE: {p.as_posix()} =====\n")

    return "\n".join(parts).strip()
    


def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("No API key. Put GOOGLE_API_KEY in .env")
        return
    
    agent.configure(api_key=api_key)

    model = agent.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "You are an assistant for a Cloud Computing for Big Data assignment.\n"
            "Use ONLY the provided project files as your evidence.\n"
            "If evidence is missing, say so and suggest what file to generate.\n"
            "Answer concisely and structure outputs in bullet points.\n"
        ),
    )

    context = build_context()
    if not context:
        print("No context files found. Generate results/audit-results.md and out/analysis_*.txt first")
        return
    
    chat = model.start_chat(history=[
        {"role": "user", "parts": [f"PROJECT CONTEXT (FILES DUMP):\n{context}"]}
    ])

    print("AI agent is ready. Ask questions. Type 'exit' to stop.\n")

    while True:
        q = input("> ").strip()
        if not q:
            continue
        if q.lower() in {"exit", "quit"}:
            break

        r = chat.send_message(q)
        print("\n" + (r.text or "").strip() + "\n")


if __name__ == "__main__":
    main()