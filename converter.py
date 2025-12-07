import os
from pdf2docx import Converter
from PIL import Image
from docx2pdf import convert
import threading

class FileConverter:
    def __init__(self):
        pass

    def pdf_to_word(self, pdf_path, word_path, callback=None):
        try:
            cv = Converter(pdf_path)
            cv.convert(word_path, start=0, end=None)
            cv.close()
            if callback:
                callback(True, "Conversion successful!")
        except Exception as e:
            if callback:
                callback(False, str(e))

    def images_to_pdf(self, image_paths, pdf_path, callback=None):
        try:
            images = []
            for path in image_paths:
                img = Image.open(path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
            
            if images:
                images[0].save(
                    pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
                )
                if callback:
                    callback(True, "Conversion successful!")
            else:
                if callback:
                    callback(False, "No images selected.")
        except Exception as e:
            if callback:
                callback(False, str(e))
    
    def word_to_pdf(self, word_path, pdf_path, callback=None):
        try:
            convert(word_path, pdf_path)
            if callback:
                callback(True, "Conversion successful!")
        except Exception as e:
            if callback:
                callback(False, str(e))
