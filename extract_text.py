import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import json
import os
import sys

def extract_text_from_pdf(pdf_path: str, output_json: str):
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Файл PDF не найден: {pdf_path}")

        print("📄 Конвертация PDF в изображения...")
        images = convert_from_path(pdf_path, dpi=300)

        print(f"🔍 Распознавание текста с {len(images)} страниц...")
        extracted_data = {}

        for i, image in enumerate(images):
            try:
                text = pytesseract.image_to_string(image, lang='eng')
                extracted_data[f"page_{i + 1}"] = text
            except Exception as ocr_error:
                extracted_data[f"page_{i + 1}"] = f"Ошибка OCR: {str(ocr_error)}"

        # Сохраняем результат
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Готово! Текст сохранён в '{output_json}'")

    except Exception as e:
        print(f"❌ Общая ошибка: {str(e)}")

if __name__ == "__main__":
    # Замените на ваш файл, например: 'sample.pdf'
    input_pdf = "sample.pdf"
    output_json = "output_text.json"

    extract_text_from_pdf(input_pdf, output_json)