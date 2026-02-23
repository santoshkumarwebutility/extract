from fastapi import FastAPI, UploadFile, File
import pdfplumber
import shutil
import os

app = FastAPI()

@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):

    temp_file = f"temp_{file.filename}"

    # Save uploaded file temporarily
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    tables_data = []

    try:
        with pdfplumber.open(temp_file) as pdf:
            for page_number, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                for table in tables:
                    tables_data.append({
                        "page": page_number + 1,
                        "data": table
                    })
    except Exception as e:
        return {"error": str(e)}

    os.remove(temp_file)

    return {
        "status": "success",
        "tables": tables_data
    }
