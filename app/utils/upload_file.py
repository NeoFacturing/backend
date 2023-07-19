# upload_files.py
import os
from fastapi import UploadFile

file_path = "docs"


async def upload_file(file: UploadFile):
    contents = await file.read()

    # Ensure 'docs' directory exists
    os.makedirs('docs', exist_ok=True)

    # Prepend the 'docs' directory to the filename
    filepath = os.path.join('docs', file.filename)

    # Check if the file already exists
    if os.path.exists(filepath):
        return {"error": f"A file with the name {file.filename} already exists."}

    # Check the file format
    _, ext = os.path.splitext(filepath)
    if ext.lower() not in ['.step', '.stp']:
        return {"error": "Invalid file format. Please upload a STEP file."}

    # Save the file
    with open(filepath, 'wb') as f:
        f.write(contents)

    return {"filename": file.filename}