"""Extract text summary from Excel files."""
import pandas as pd
import os


def extract(excel_path: str, output_dir: str) -> str:
    """Read all sheets, output text summary."""
    basename = os.path.splitext(os.path.basename(excel_path))[0]
    txt_path = os.path.join(output_dir, f"{basename}.txt")

    ext = os.path.splitext(excel_path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(excel_path)
        parts = [f"--- CSV ({len(df)} rows x {len(df.columns)} cols) ---"]
        parts.append(f"Columns: {', '.join(df.columns.astype(str))}")
        parts.append(df.head(50).to_string(index=False))
        if len(df) > 50:
            parts.append(f"... ({len(df) - 50} more rows)")
    else:
        xls = pd.ExcelFile(excel_path)
        parts = []
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            parts.append(f"--- Sheet: {sheet} ({len(df)} rows x {len(df.columns)} cols) ---")
            parts.append(f"Columns: {', '.join(df.columns.astype(str))}")
            parts.append(df.head(50).to_string(index=False))
            if len(df) > 50:
                parts.append(f"... ({len(df) - 50} more rows)")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(parts))

    print(f"  Excel: extracted to {basename}.txt")
    return txt_path
