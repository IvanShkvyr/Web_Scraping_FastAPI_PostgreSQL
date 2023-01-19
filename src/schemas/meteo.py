from datetime import datetime

from pydantic import BaseModel, Field


class MeteoBase(BaseModel):
    created_by: str = Field()
    odesa_air_temp: float
    odesa_wind_spd: float
    odesa__prc: float
    rivne_air_temp: float
    rivne_wind_spd: float
    rivne__prc: float
    baryshivka_air_temp: float
    baryshivka_wind_spd: float
    baryshivka_prc: float


class MeteoUpdate(MeteoBase):
    odesa_air_temp: float
    odesa_wind_spd: float
    odesa__prc: float
    rivne_air_temp: float
    rivne_wind_spd: float
    rivne__prc: float
    baryshivka_air_temp: float
    baryshivka_wind_spd: float
    baryshivka_prc: float
    is_verify: bool


class MeteoStatus(BaseModel):
    is_verify: bool


class MeteoResponse(MeteoBase):
    id: int
    create_data: datetime
    odesa_air_temp: float
    odesa_wind_spd: float
    odesa__prc: float
    rivne_air_temp: float
    rivne_wind_spd: float
    rivne__prc: float
    baryshivka_air_temp: float
    baryshivka_wind_spd: float
    baryshivka_prc: float
    is_verify: bool


    class Config:
        orm_mode = True
