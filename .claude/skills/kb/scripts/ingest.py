#!/usr/bin/env python3
"""Scan raw/ for new files, extract text, print summary for LLM to parse."""
import importlib
import os
import sys

# Add scripts dir to path so extractors can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

EXTRACTORS = {
    ".pdf": "extractors.pdf_extractor",
    ".xlsx": "extractors.excel_extractor",
    ".xls": "extractors.excel_extractor",
    ".csv": "extractors.excel_extractor",
    ".png": "extractors.image_extractor",
    ".jpg": "extractors.image_extractor",
    ".jpeg": "extractors.image_extractor",
    ".docx": "extractors.docx_extractor",
}
SKIP_EXT = {".md", ".txt"}
SKIP_DIRS = {".extracted"}


def scan_raw(raw_dir, registry_path):
    """Find files in raw/ not yet in RAW-REGISTRY.md."""
    registered = set()
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("| raw/") or line.startswith("| ./raw/"):
                    path = line.split("|")[1].strip()
                    registered.add(path)

    new_files = []
    for root, dirs, files in os.walk(raw_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, os.path.dirname(raw_dir))
            if rel not in registered:
                new_files.append(fpath)
    return new_files


def process_file(fpath):
    """Extract text from a single file. Returns (txt_path, file_type) or (None, file_type)."""
    ext = os.path.splitext(fpath)[1].lower()
    extracted_dir = os.path.join(os.path.dirname(fpath), ".extracted")
    os.makedirs(extracted_dir, exist_ok=True)

    if ext in SKIP_EXT:
        return None, ext

    mod_name = EXTRACTORS.get(ext)
    if not mod_name:
        print(f"  SKIP (unsupported): {os.path.basename(fpath)}")
        return None, ext

    try:
        extractor = importlib.import_module(mod_name)
        txt_path = extractor.extract(fpath, extracted_dir)
        return txt_path, ext
    except ImportError as e:
        print(f"  ERROR (missing dependency): {e}")
        return None, ext
    except Exception as e:
        print(f"  ERROR: {e}")
        return None, ext


def main():
    kb_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    raw_dir = os.path.join(kb_root, "raw")
    registry = os.path.join(kb_root, "index", "RAW-REGISTRY.md")

    if not os.path.isdir(raw_dir):
        print(f"ERROR: {raw_dir} not found")
        sys.exit(1)

    new_files = scan_raw(raw_dir, registry)
    if not new_files:
        print("No new files in raw/")
        return

    print(f"Found {len(new_files)} new file(s) in raw/:\n")
    results = []
    for fpath in sorted(new_files):
        print(f"Processing: {os.path.basename(fpath)}")
        txt_path, ext = process_file(fpath)
        results.append((fpath, txt_path, ext))

    # Output summary for LLM to parse and update RAW-REGISTRY.md
    print(f"\n--- INGEST SUMMARY ---")
    print(f"Processed: {len(results)} files")
    for fpath, txt_path, ext in results:
        rel = os.path.relpath(fpath, kb_root)
        status = "extracted" if txt_path else "ready"
        print(f"  {rel} [{ext}] -> {status}")


if __name__ == "__main__":
    main()
