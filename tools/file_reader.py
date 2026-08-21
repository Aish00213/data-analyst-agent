import pandas as pd
import os

DATA_DIR = "data"

def read_file(filename: str) -> str:
    filepath = os.path.join(DATA_DIR, filename)

    if not os.path.exists(filepath):
        return f"ERROR: File '{filename}' not found in the data/ folder."

    ext = filename.lower().split(".")[-1]
    try:
        if ext == "csv":
            df = pd.read_csv(filepath)
        elif ext in ("xlsx", "xls"):
            df = pd.read_excel(filepath)
        else:
            return f"ERROR: Unsupported file type '.{ext}'."
    except Exception as e:
        return f"ERROR loading file: {str(e)}"

    lines = []
    lines.append(f"File: {filename}")
    lines.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    lines.append("")

    lines.append("Columns and data types:")
    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_note = f"  ({null_count} nulls)" if null_count > 0 else ""
        lines.append(f"  - {col}: {df[col].dtype}{null_note}")
        
    lines.append("Sample unique values per column (up to 5, first 15 text columns only):")
    text_cols = [c for c in df.columns if df[c].dtype == object]
    for col in text_cols[:15]:
        unique_vals = df[col].dropna().unique()[:5].tolist()
        lines.append(f"  - {col}: {unique_vals}")
    if len(text_cols) > 15:
        lines.append(f"  ...and {len(text_cols) - 15} more text columns omitted.")
        
    lines.append("")
    lines.append("First 3 rows (sample):")
    lines.append(df.head(3).to_string(index=False, max_cols=15))
    return "\n".join(lines)
