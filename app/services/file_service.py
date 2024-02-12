import json
import fitz  # PyMuPDF
from fastapi import UploadFile

async def read_json_file(file: UploadFile) -> dict:
    """
    Reads a JSON file and returns its content as a dictionary.
    """
    content = await file.read()
    return json.loads(content)

async def read_pdf_file(file: UploadFile) -> str:
    """
    Reads a PDF file and extracts its text content.
    """
    content = await file.read()
    with fitz.open(stream=content, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

async def read_file(file: UploadFile, file_type: str) -> str:
    """
    Reads a file and returns its content. The file can be either JSON or PDF.
    """
    if file_type == "application/json":
        return await read_json_file(file)
    elif file_type == "application/pdf":
        return await read_pdf_file(file)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
