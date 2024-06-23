from datetime import datetime
from pydantic import BaseModel


class HistoryStock(BaseModel):

    accion_id: int
    fecha: datetime
    precio: float


    class Config:
        populate_by_name = True
        from_attributes = True