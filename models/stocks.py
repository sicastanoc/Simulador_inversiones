from config import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Relationship


class Stocks(Base):
    __tablename__ = 'acciones'

    accion_id = Column(Integer, primary_key=True)
    nombre_accion = Column(String)
    nombre_abreviado = Column(String)

    def __init__(self, *args, **kwargs):
        """initializes Clients"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"Nombre accion: {self.nombre_accion}, abreviatura: {self.nombre_abreviado}"
    
    def __repr__(self):
        return f"Nombre accion: {self.nombre_accion}, abreviatura: {self.nombre_abreviado}"


class HistoryStocks(Base):
    __tablename__ = 'historia_acciones'

    transaccion_id = Column(Integer, primary_key=True)
    accion_id = Column(Integer, ForeignKey('acciones.accion_id'))
    fecha = Column(DateTime)
    precio = Column(Float)

    stocks = Relationship(
        Stocks
    )

    def __init__(self, *args, **kwargs):
        """initializes Clients"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"Nombre accion: {self.stocks.nombre_accion}, abreviatura: {self.precio}, fecha: {self.fecha}"
    
    def __repr__(self):
        return f"Nombre accion: {self.stocks.nombre_accion}, abreviatura: {self.precio}, fecha: {self.fecha}"
