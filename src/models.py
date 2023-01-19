from sqlalchemy import Column, Float, func, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import DateTime

from db.connect import Base


class MeteoData(Base):
    __tablename__ = "meteodatas"
    id = Column(Integer, primary_key=True)
    create_data = Column("created_at", DateTime, default=func.now())
    created_by = Column(String(50))
    odesa_air_temp = Column(Float)
    odesa_wind_spd = Column(Float)
    odesa__prc = Column(Float)
    rivne_air_temp = Column(Float)
    rivne_wind_spd = Column(Float)
    rivne__prc = Column(Float)
    baryshivka_air_temp = Column(Float)
    baryshivka_wind_spd = Column(Float)
    baryshivka_prc = Column(Float)
    is_verify = Column(Boolean, default=False)



# alembic init migrations

# змінити файл env.py
# 
# alembic revision --autogenerate -m 'add created_by field'
#
# alembic upgrade head