from sqlalchemy.orm import Session

from src.models import MeteoData
from src.schemas.meteo import MeteoBase, MeteoUpdate, MeteoStatus
from src import get_meteo_data 


async def get_all_records(skip, limit, db: Session):
    records = db.query(MeteoData).offset(skip).limit(limit).all()
    return records


async def get_record(meteo_record_id: int,  db: Session):
    record = db.query(MeteoData).filter(MeteoData.id == meteo_record_id).first()
    return record


async def create_record(body: MeteoBase,  db: Session):
    meteo_data = get_meteo_data.main()
    print(meteo_data['odesa_air_temp'])
    new_record = MeteoData(
                            created_by=body.created_by,
                            odesa_air_temp=meteo_data['odesa_air_temp'],
                            odesa_wind_spd=meteo_data['odesa_wind_spd'],
                            odesa__prc=meteo_data['odesa__prc'],
                            rivne_air_temp=meteo_data['rivne_air_temp'],
                            rivne_wind_spd=meteo_data['rivne_wind_spd'],
                            rivne__prc=meteo_data['rivne__prc'],
                            baryshivka_air_temp=meteo_data['baryshivka_air_temp'],
                            baryshivka_wind_spd=meteo_data['baryshivka_wind_spd'],
                            baryshivka_prc=meteo_data['baryshivka_prc']
                        )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


async def update_record(meteo_record_id: int, body: MeteoUpdate,  db: Session):
    record = db.query(MeteoData).filter(MeteoData.id == meteo_record_id).first()
    if record:
        record.created_by = body.created_by
        record.odesa_air_temp = body.odesa_air_temp
        record.odesa_wind_spd = body.odesa_wind_spd
        record.odesa__prc = body.odesa__prc
        record.rivne_air_temp = body.rivne_air_temp
        record.rivne_wind_spd = body.rivne_wind_spd
        record.rivne__prc = body.rivne__prc
        record.baryshivka_air_temp = body.baryshivka_air_temp
        record.baryshivka_wind_spd = body.baryshivka_wind_spd
        record.baryshivka_prc = body.baryshivka_prc
        record.is_verify = body.is_verify
        db.commit()
    return record


async def update_status(meteo_record_id: int, body: MeteoStatus,  db: Session):
    record = db.query(MeteoData).filter(MeteoData.id == meteo_record_id).first()
    if record:
        record.is_verify = body.is_verify
        db.commit()
    return record


async def delete_records(meteo_record_id: int,  db: Session):
    record = db.query(MeteoData).filter(MeteoData.id == meteo_record_id).first()
    if record:
        db.delete(record)
        db.commit()
    return record
