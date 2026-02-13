from fastapi import FastAPI, UploadFile, File
import pandas as pd
import camelot
import os
import uvicorn

app = FastAPI()

@app.post("/extract")
async def extract_table(file: UploadFile = File(...)):
    # File ko temporary save karein
    with open("temp.pdf", "wb") as buffer:
        buffer.write(await file.read())

    try:
        # PDF se table nikalna (flavor='stream' basic tables ke liye best hai)
        tables = camelot.read_pdf("temp.pdf", pages='all', flavor='stream')
        
        all_tables_data = []
        for table in tables:
            # Dataframe ko list of dicts mein convert karein
            all_tables_data.append(table.df.to_dict(orient='records'))

        os.remove("temp.pdf") # File delete karein
        return {"status": "success", "data": all_tables_data}

    except Exception as e:
        if os.path.exists("temp.pdf"):
            os.remove("temp.pdf")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
