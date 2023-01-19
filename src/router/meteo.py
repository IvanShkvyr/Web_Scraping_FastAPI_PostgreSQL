from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.connect import get_db
from src.schemas.meteo import MeteoBase, MeteoUpdate, MeteoStatus, MeteoResponse
from src.repository import meteo as repository_meteo

router = APIRouter(prefix="/meteo", tags=['meteo'])


@router.get("/", response_model=List[MeteoResponse])
async def get_meteo_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    all_meteo = await repository_meteo.get_all_records(skip, limit, db)
    return all_meteo


@router.get("/{meteo_record_id}", response_model=MeteoResponse)
async def get_meteo_record(meteo_record_id: int, db: Session = Depends(get_db)):
    meteo = await repository_meteo.get_record(meteo_record_id, db)
    if meteo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return meteo


@router.post("/", response_model=MeteoResponse, status_code=status.HTTP_201_CREATED)
async def create_meteo_record(meteo_record: MeteoBase, db: Session = Depends(get_db)):
    meteo = await repository_meteo.create_record(meteo_record, db)
    return meteo


@router.put("/{meteo_record_id}", response_model=MeteoResponse)
async def update_meteo_record(meteo_record_id: int, meteo_record: MeteoUpdate, db: Session = Depends(get_db)):
    meteo = await repository_meteo.update_record(meteo_record_id, meteo_record, db)
    if meteo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return meteo


@router.patch("/{meteo_record_id}", response_model=MeteoResponse)
async def update_meteo_status(meteo_record_id: int, meteo_record: MeteoStatus, db: Session = Depends(get_db)):
    meteo = await repository_meteo.update_status(meteo_record_id, meteo_record, db)
    if meteo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return meteo


@router.delete("/{meteo_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meteo_record(meteo_record_id: int, db: Session = Depends(get_db)):
    meteo = await repository_meteo.delete_records(meteo_record_id, db)
    if meteo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return meteo
