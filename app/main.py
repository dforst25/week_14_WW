from fastapi import FastAPI, UploadFile, HTTPException
import pandas as pd
import numpy as np
import uvicorn

app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile | None = None):
    if file is None:
        raise HTTPException(status_code=400, detail="no file uploaded")
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=422, detail="a csv file required")
    df = pd.read_csv(file.file)
    df['risk_level'] = pd.cut(x=df['range_km'], bins=[-np.inf, 20, 100, 300, np.inf], labels=['low', 'medium',
                                                                                              'high', 'extreme'])
    df.fillna('Unknown', inplace=True)
    print(df)
    print(df.dtypes)
    return {"filename": file.filename}


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
