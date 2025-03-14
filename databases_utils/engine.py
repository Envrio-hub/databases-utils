__version__='1.0.8'
__author__=['Ioannis Tsakmakis']
__date_created__='2023-10-20'
__last_updated__='2024-01-16'

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import json

with open('local_paths.json','r') as f:
    local_paths = json.load(f)

with open(local_paths['mysql'],'r') as f:
    config = json.load(f)

# sqlalchemy logging path
logging_path = local_paths['sqlalchemy_logging_path']

# Creating sqlalchemy engine
engine = create_engine(url=f'{config["DBAPI"]}://{config["username"]}:{config['password']}@{config["host-ip"]}/{config["database"]}',
                         pool_size=30, max_overflow=5, pool_recycle=7200)


SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
