from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
import redis

path = sys.path.append(os.path.join(sys.path[0]))

load_dotenv()

# Данные для email рассылки

sender_email = os.environ.get("EMAIL")
server_email = os.environ.get("MAIL_SERVER")

# Подключение к MSSQL

username = os.environ.get("USER")
password = os.environ.get("PASS")
hostname = os.environ.get("HOST")
database = os.environ.get("DBNAME")


# Подключение к Redis

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PASS = os.environ.get("REDIS_PASS")

# Создание подключения к базе данных
engine = create_engine(
    f"mssql+pyodbc://{username}:{password}@{hostname}/{database}?driver=ODBC+Driver+18+for+SQL+Server"
    f"&TrustServerCertificate=yes"
)

# Созда
Session = sessionmaker(bind=engine)
session = Session()

redis_conn = redis.Redis(host=REDIS_HOST, port=6379, db=0, password=REDIS_PASS, decode_responses=True)
redis_celery = redis.Redis(host=REDIS_HOST, port=6379, db=1, password=REDIS_PASS)
