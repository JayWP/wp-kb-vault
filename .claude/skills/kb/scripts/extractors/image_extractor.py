"""OCR text from images using pytesseract."""
import pytesseract
from PIL import Image
import os


def extract(image_path: str, output_dir: str) -> str:
    """OCR image, return text file path."""
    basename = os.path.splitext(os.path.basename(image_path))[0]
    txt_path = os.path.join(output_dir, f"{basename}.txt")

    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang="chi_sim+eng")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    chars = len(text.strip())
    print(f"  Image OCR: {chars} characters extracted")
    return txt_path
