__version__='1.2.0'
__author__=['Ioannis Tsakmakis']
__date_created__='2023-10-20'
__last_updated__='2024-10-02'

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from .aws_utils import SecretsManager
# from aws_utils import SecretsManager
from dotenv import load_dotenv
from .logger import alchemy
# from logger import alchemy
import os

# Load variables from the .env file
load_dotenv()

# Access database configuration info
db_conf = SecretsManager().get_secret(secret_name=os.getenv('db_name'))

# Creating sqlalchemy engine
try:
    engine = create_engine(url=f'{db_conf["DBAPI"]}://{db_conf["username"]}:{db_conf['password']}@{db_conf["host-ip"]}/{os.getenv('db_name')}',
                        pool_size=30, max_overflow=5, pool_recycle=7200)
except Exception as e:
    alchemy.error(f"Error occurred during engine creation: {str(e)}")
    
SessionLocal = scoped_session(sessionmaker(bind=engine))

class Base(DeclarativeBase):
    pass
