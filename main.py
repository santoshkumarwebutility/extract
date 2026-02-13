from fastapi import FastAPI, UploadFile, File
import camelot
import os
import uvicorn

app = FastAPI()

@app.post("/extract")
async def extract_table(file: UploadFile = File(...)):
    file_path = "temp_file.pdf"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        # 'stream' mode text alignment ke liye, 'lattice' borders ke liye
        tables = camelot.read_pdf(file_path, pages='all', flavor='stream')
        
        if len(tables) == 0:
            return {"status": "success", "data": [], "message": "No tables found"}

        all_tables_data = []
        for table in tables:
            # Table ko clean karke JSON compatible banana
            all_tables_data.append(table.df.to_dict(orient='records'))

        return {"status": "success", "count": len(tables), "data": all_tables_data}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
