# Kaspi Cloud Computing Task_1

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
