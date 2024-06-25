from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, func, DateTime, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, index=True, nullable=False)


class Transaction(Base):
    __tablename__ = "transacciones"

    transaccion_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, index=True, nullable=False)
    accion_id = Column(Integer, index=True, nullable=False)
    tipo_transaccion = Column(String, index=True, nullable=False)
    cantidad = Column(Integer, index=True, nullable=False)
    TransactionDate = Column(default=datetime.now().strftime("%Y-%m-%d"))

class Accion(Base):
    __tablename__ = "acciones"

    accion_id = Column(Integer, primary_key=True, index=True)
    nombre_accion = Column(String, index=True, nullable=False)
    nombre_abreviado = Column(String, index=True, nullable=False)

class Historia_accion(Base):
    __tablename__ = "historia_acciones"

    transaccion_id = Column(Integer,primary_key=True,index=True, nullable=False)
    accion_id = Column(Integer, nullable=False)
    fecha = Column(DateTime, index=True, nullable=False)
    precio = Column(Float, index=True, nullable=False)


class UserBase(BaseModel):
    nombre_usuario: str

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    usuario_id: int

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    pass

class TransactionBase(BaseModel):
    usuario_id: int
    accion_id: int
    tipo_transaccion: str
    cantidad: int

class TransactionInDB(TransactionBase):
    transaccion_id: int

    class Config:
        orm_mode = True

class TransactionCreate(TransactionBase):
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

@app.post("/users/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica si el usuario ya existe en la base de datos
    existing_user = db.query(User).filter(User.nombre_usuario == user.nombre_usuario).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nombre de usuario ya existe")

    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{nombre_usuario}", response_model=List[UserInDB])
def get_users(nombre_usuario: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nombre_usuario == nombre_usuario).all()
    if not user:
        raise HTTPException(status_code=404, detail="No usuarios con este nombre")
    return user


@app.post("/transactions/", response_model=TransactionInDB)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/{usuario_id}", response_model=List[TransactionInDB])
def get_transactions(usuario_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.usuario_id == usuario_id).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No hay transacciones del usuario")
    return transactions

@app.post("/acciones/", response_model=AccionInDB)
def create_accion(accion: AccionCreate, db: Session = Depends(get_db)):
    db_accion = Accion(**accion.dict())
    db.add(db_accion)
    db.commit()
    db.refresh(db_accion)
    return db_accion

@app.get("/acciones/{accion_id}", response_model=List[Historia_AccionBaseInDB])
def get_precion_accion(accion_id: int, db: Session = Depends(get_db)):
    precio_accion = db.query(Historia_accion,Accion).filter(Historia_accion.accion_id == accion_id).filter(Accion.accion_id == accion_id).all()
    if not precio_accion:
        raise HTTPException(status_code=404, detail="No hay transacciones del usuario")
    return precio_accion

