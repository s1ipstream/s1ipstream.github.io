import pandas as pd
import sys
from pathlib import Path

# Force UTF-8 output encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def load_index(filename="archive_index.jsonl"):
    return pd.read_json(filename, lines=True)

# Load the data
df = load_index()

# Create both console output and file output
with open('dsm_analysis.txt', 'w', encoding='utf-8') as f:
    def dual_print(text):
        print(text)
        f.write(text + '\n')

    dual_print("DSM-5 RELATED CONTENT ANALYSIS")
    dual_print("=" * 60)

    # Find diagnostic/pathology content
    diagnostic_files = df[
        (df['filename'].str.contains('patholog|diagnos|dsm', case=False, na=False, regex=True)) |
        (df['first_500_chars'].str.contains('patholog|diagnos|dsm', case=False, na=False, regex=True))
    ]

    if len(diagnostic_files) > 0:
        dual_print(f"\nFound {len(diagnostic_files)} files with DSM/diagnostic content:")
        for _, row in diagnostic_files.iterrows():
            dual_print(f"\nFILE: {row['filename']}")
            dual_print(f"Words: {row['wordcount']:,}")
            if isinstance(row['all_tags'], list):
                dual_print(f"Tags: {', '.join(row['all_tags'])}")
            if 'first_500_chars' in row:
                dual_print(f"Preview:\n{row['first_500_chars'][:200]}...")
            dual_print("-" * 60)
    else:
        dual_print("\nNo DSM/diagnostic files found")

    dual_print("\nANALYSIS GUIDELINES:")
    dual_print("• Look for critiques of traditional diagnostic models")
    dual_print("• Identify alternative frameworks proposed")
    dual_print("• Note examples of reframing 'disorders'")
    dual_print("• Compare debugging vs diagnostic approaches")