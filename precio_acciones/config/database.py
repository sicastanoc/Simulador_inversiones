import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = 'C:/Users/simon/Downloads/yahoo-finance-request-main/database.db'
base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f'sqlite:///{os.path.join(base_dir, sqlite_file_name)}'

engine = create_engine(database_url, echo=False)

Session = sessionmaker(bind=engine)

Base = declarative_base()