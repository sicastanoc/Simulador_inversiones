from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, func
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
    nombre_usuario = Column(String, index=True)


class Transaction(Base):
    __tablename__ = "transacciones"

    transaccion_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, index=True)
    accion_id = Column(Integer, index=True)
    tipo_transaccion = Column(String, index=True)
    cantidad = Column(Integer, index=True)
    TransactionDate = Column(default=datetime.now().strftime("%Y-%m-%d"))

class Accion(Base):
    __tablename__ = "acciones"

    accion_id = Column(Integer, primary_key=True, index=True)
    nombre_accion = Column(String, index=True)
    nombre_abreviado = Column(String, index=True)

Base.metadata.create_all(bind=engine)

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
