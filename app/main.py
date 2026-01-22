from fastapi import FastAPI, UploadFile, HTTPException
import pandas as pd
import numpy as np
import uvicorn
import os
from db import DbConnection

MYSQL_HOST = os.getenv("MYSQL_HOST", 'localhost')
MYSQL_PORT = int(os.getenv("MYSQL_PORT", '3306'))
MYSQL_USER = os.getenv("MYSQL_USER", 'root')
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", '')
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", 'weapons_db')

app = FastAPI()
conn = DbConnection(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)


@app.on_event("startup")
def startup_event():
    conn.get_connection()


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
    result = conn.insert_weapon(df)

    return result

if __name__ == "__main__":
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
