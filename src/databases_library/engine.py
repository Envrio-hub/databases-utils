__version__='1.0.6'
__author__='Ioannis Tsakmakis'
__date_created__='2023-10-20'
__last_updated__='2023-11-28'

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os, json

local_directory = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(local_directory, 'mysql_config.json')

with open(config_path,'r') as f:
    config = json.load(f)

engine = create_engine(url=f'{config["DBAPI"]}://{config["username"]}:{config['password']}@{config["host-ip"]}/{config["database"]}',
                         pool_pre_ping=True)

Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass
