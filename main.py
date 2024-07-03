from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, func, DateTime, Float, ForeignKey,desc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel,Field
from datetime import datetime, date
from typing import List
from fastapi.middleware.cors import CORSMiddleware

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, index=True, nullable=False)
    balance = Column(Float, index=True, nullable=False)


class Transaction(Base):
    __tablename__ = "transacciones"

    transaccion_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'), index=True, nullable=False)
    accion_id = Column(Integer,ForeignKey('acciones.accion_id'), index=True, nullable=False)
    tipo_transaccion = Column(String, index=True, nullable=False)
    cantidad = Column(Integer, index=True, nullable=False)
    precio = Column(Float, index=True, nullable=False)
    TransactionDate = Column(DateTime, default=func.now())

class Accion(Base):
    __tablename__ = "acciones"

    accion_id = Column(Integer, primary_key=True, index=True)
    nombre_accion = Column(String, index=True, nullable=False)
    nombre_abreviado = Column(String, index=True, nullable=False)

class Historia_accion(Base):
    __tablename__ = "historia_acciones"

    transaccion_id = Column(Integer,primary_key=True,index=True, nullable=False)
    accion_id = Column(Integer,ForeignKey('acciones.accion_id'), nullable=False)
    fecha = Column(DateTime, index=True, nullable=False)
    precio = Column(Float, index=True, nullable=False)


class UserBase(BaseModel):
    nombre_usuario: str

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    usuario_id: int
    balance: float

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    pass


class TransactionBase(BaseModel):
    usuario_id: int
    accion_id: int
    tipo_transaccion: str
    cantidad: int
    TransactionDate: datetime = Field(default_factory=datetime.now)
    precio: float

    class Config:
        orm_mode = True

class TransactionInDB(TransactionBase):
    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    nombre_usuario: str
    cantidad: int
    tipo_transaccion: str
    nombre_abreviado: str
    precio: float
    pass

class AccionBase(BaseModel):
    nombre_accion: str
    nombre_abreviado: str

class AccionInDB(AccionBase):
    accion_id: int

    class Config:
        orm_mode = True

class AccionCreate(AccionBase):
    pass

class Historia_AccionBase(BaseModel):
    accion_id: int

class Historia_AccionBaseInDB(Historia_AccionBase):
    accion_id: int
    transaccion_id: int
    fecha: datetime
    precio: float

    class Config:
        orm_mode = True

class PrecioAccion(BaseModel):
    accion_id: int
    nombre_accion: str
    nombre_abreviado: str
    precio: float

    class Config:
        orm_mode = True

class AccionID(BaseModel):
    accion_id: int

    class Config:
        orm_mode = True

class TransactionResponse(BaseModel):
    TransactionDate: datetime
    tipo_transaccion: str
    cantidad: int
    precio: float
    nombre_accion: str



Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Crear un usuario
@app.post("/users/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica si el usuario ya existe en la base de datos
    existing_user = db.query(User).filter(User.nombre_usuario == user.nombre_usuario).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nombre de usuario ya existe")

    db_user = User(**user.dict())
    db_user.balance = 1000000
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Obtener informacion del usuario
@app.get("/users/{nombre_usuario}", response_model=UserInDB)
def get_users(nombre_usuario: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nombre_usuario == nombre_usuario).first()
    if not user:
        raise HTTPException(status_code=404, detail="No usuarios con este nombre")
    return user


#Compra y venta de acciones
@app.post("/transactions/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    accion_id = db.query(Accion).filter(Accion.nombre_abreviado == transaction.nombre_abreviado).first().accion_id
    precio= db.query(Historia_accion).filter(Historia_accion.accion_id == accion_id).first().precio
    usuario_id = db.query(User).filter(User.nombre_usuario == transaction.nombre_usuario).first().usuario_id
    usuario = db.query(User).filter(User.nombre_usuario == transaction.nombre_usuario).first()

    if transaction.tipo_transaccion == 'Compra':
        total_cost = transaction.cantidad * precio
        if usuario.balance < total_cost:
            raise HTTPException(status_code=400, detail="Balance insuficiente para realizar la compra")
        
        usuario.balance -= total_cost
        
        # Actualizar el balance del usuario
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        # Crear la transacción
        crear_transaccion = TransactionInDB(
            accion_id=accion_id,
            usuario_id=usuario.usuario_id,
            tipo_transaccion=transaction.tipo_transaccion,
            cantidad=transaction.cantidad,
            precio=precio
        )
        
        db_transaccion = Transaction(**crear_transaccion.model_dump())
        db.add(db_transaccion)
        db.commit()
        db.refresh(db_transaccion)
    
    elif transaction.tipo_transaccion == 'Venta':
        # Verificar si el usuario tiene suficientes acciones para vender
        total_cantidad_compras = db.query(func.sum(Transaction.cantidad)).filter(
            Transaction.usuario_id == usuario.usuario_id,
            Transaction.accion_id == accion_id,
            Transaction.tipo_transaccion == 'Compra'
        ).scalar() or 0
        
        total_cantidad_ventas = db.query(func.sum(Transaction.cantidad)).filter(
            Transaction.usuario_id == usuario.usuario_id,
            Transaction.accion_id == accion_id,
            Transaction.tipo_transaccion == 'Venta'
        ).scalar() or 0
        
        total_cantidad = total_cantidad_compras - total_cantidad_ventas
        
        if total_cantidad < transaction.cantidad:
            raise HTTPException(status_code=400, detail="Cantidad insuficiente de acciones para vender")
        
        total_income = transaction.cantidad * precio
        usuario.balance += total_income
        
        # Actualizar el balance del usuario
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        # Crear la transacción
        crear_transaccion = TransactionInDB(
            accion_id=accion_id,
            usuario_id=usuario.usuario_id,
            tipo_transaccion=transaction.tipo_transaccion,
            cantidad=transaction.cantidad,
            precio=precio
        )
        
        db_transaccion = Transaction(**crear_transaccion.model_dump())
        db.add(db_transaccion)
        db.commit()
        db.refresh(db_transaccion)

    return db_transaccion


@app.get("/transactions/{usuario_id}", response_model=List[TransactionResponse])
def get_transactions(usuario_id: int, db: Session = Depends(get_db)):
    transactions = db.query(
        Transaction.TransactionDate,
        Transaction.tipo_transaccion,
        Transaction.cantidad,
        Transaction.precio,
        Accion.nombre_abreviado.label("nombre_accion")
    ).join(Accion, Transaction.accion_id == Accion.accion_id).filter(Transaction.usuario_id == usuario_id).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No hay transacciones del usuario")
    
    return transactions


#Crear una accion
@app.post("/acciones/", response_model=AccionInDB)
def create_accion(accion: AccionCreate, db: Session = Depends(get_db)):
    db_accion = Accion(**accion.dict())
    db.add(db_accion)
    db.commit()
    db.refresh(db_accion)
    return db_accion


#Obtener precio de una a
@app.get("/acciones/{accion_id}", response_model=PrecioAccion)
def get_precion_accion(accion_id: int, db: Session = Depends(get_db)):
    # Realiza el join entre Historia_accion y Accion
    resultado = db.query(
        Historia_accion.accion_id,
        Accion.nombre_accion,
        Accion.nombre_abreviado,
        Historia_accion.fecha,
        Historia_accion.precio
    ).join(
        Accion, Historia_accion.accion_id == Accion.accion_id
    ).filter(
        Historia_accion.accion_id == accion_id
    ).order_by(desc(Historia_accion.fecha)
    ).first()


    if not resultado:
        raise HTTPException(status_code=404, detail="No hay precios para esta acción")

    return resultado


# Obtener información de la acción por nombre abreviado
@app.get("/acciones_id/{nombre_abreviado}", response_model=AccionID)
def get_accion(nombre_abreviado: str, db: Session = Depends(get_db)):
    accion = db.query(Accion).filter(Accion.nombre_abreviado == nombre_abreviado).first()
    if not accion:
        raise HTTPException(status_code=404, detail="No hay acción con este nombre abreviado")
    return accion
