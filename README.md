# Universal File Converter Tool

A modern GUI-based tool to convert files between different formats.

## Features
- **PDF to Word**: Convert PDF documents to editable `.docx` files.
- **Images to PDF**: Combine multiple images into a single PDF.
- **Word to PDF**: Convert Word documents to PDF (Requires Microsoft Word installed).

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application**:
    ```bash
    python main.py
    ```

## Technologies Used
- **CustomTkinter**: For a modern, dark-themed GUI.
- **pdf2docx**: For extracting text and layout from PDFs.
- **Pillow (PIL)**: For image processing.
- **docx2pdf**: For Microsoft Word automation.
