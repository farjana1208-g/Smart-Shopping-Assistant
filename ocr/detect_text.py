import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image):
    """Extract raw OCR text"""
    return pytesseract.image_to_string(image).strip()


def extract_text_with_boxes(image):
    """
    Extract OCR words with position + confidence
    """
    width, height = image.size

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT
    )

    boxes = []
    n = len(data["text"])

    for i in range(n):
        word = data["text"][i].strip()

        try:
            conf = float(data["conf"][i])
        except:
            conf = -1

        if not word or conf < 40:
            continue

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        # remove top UI bar text (status bar + search bar)
        if y < height * 0.12:
            continue

        boxes.append({
            "text": word,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "line_num": data["line_num"][i],
            "block_num": data["block_num"][i],
            "par_num": data["par_num"][i],
        })

    return boxes