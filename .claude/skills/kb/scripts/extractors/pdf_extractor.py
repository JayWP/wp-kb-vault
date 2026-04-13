"""Extract text and images from PDF files using PyMuPDF."""
import fitz  # PyMuPDF
import os


def extract(pdf_path: str, output_dir: str) -> str:
    """Extract text from PDF, save images, return text file path."""
    doc = fitz.open(pdf_path)
    text_parts = []
    img_count = 0

    for page_num, page in enumerate(doc):
        text_parts.append(f"--- Page {page_num + 1} ---")
        text_parts.append(page.get_text())

        for img_idx, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n > 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            img_path = os.path.join(output_dir, f"page{page_num+1}_img{img_idx+1}.png")
            pix.save(img_path)
            img_count += 1
            pix = None

    doc.close()

    basename = os.path.splitext(os.path.basename(pdf_path))[0]
    txt_path = os.path.join(output_dir, f"{basename}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(text_parts))

    print(f"  PDF: {len(text_parts)//2} pages, {img_count} images extracted")
    return txt_path
