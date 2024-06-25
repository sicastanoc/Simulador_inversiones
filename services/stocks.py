from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models import Stocks, HistoryStocks
from schemas import HistoryStock as HistoryStockSchema


class StockServices:

    def __init__(self, db: Session) -> None:
        
        self.db = db
        self.model = Stocks

    def get_all_values(self, skip: int = 0, limit: int = 100):

        return self.db.query(self.model).offset(skip).limit(limit).all()
    

class HistoryStocksServices:

    def __init__(self, db: Session) -> None:
        
        self.db = db
        self.model = HistoryStocks

    def create_value(self, value: HistoryStockSchema):

        new_value = self.model(**value.model_dump())
        self.db.add(new_value)
        self.db.commit()
        self.db.refresh(new_value)

        return new_value
    
    def get_value(self, stock_id: int):

        try:

            value = self.db.query(self.model).filter_by(accion_id=stock_id).order_by(desc(self.model.fecha)).limit(1).one()
            return value
        
        except NoResultFound:

            return None
