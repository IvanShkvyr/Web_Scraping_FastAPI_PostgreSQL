from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db.connect import get_db
from src.router import meteo

app = FastAPI()


@app.get("/api/healthchecker")
async def healthchecker(db: Session = Depends(get_db)):
    try:
        r = db.execute('SELECT 1').fetchone()
        if r is None:
            raise HTTPException(status_code=500, detail='Database is not configured correctly')
        return {'massage': 'Good!'}
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail='Error connection to database')


@app.get('/')
def root():
    return {'massege': 'APP'}


app.include_router(meteo.router)


# uvicorn main:app --reload

