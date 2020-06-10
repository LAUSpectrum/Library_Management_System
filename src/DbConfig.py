import multiprocessing
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()  # ModuleNotFoundError: No module named 'MySQLdb'


db_url = "mysql+{}://{}:{}@{}:{}/{}?{}".format(
	"mysqldb",        # driver_lib,
	"root",      # username
	"mysql",         # password
	"localhost",        # host
	"3306",    # port
	"LIBRARY",      # database
	"charset=utf8" # params
)

pool_size = multiprocessing.cpu_count() * 2 + 1
engine = create_engine(db_url, pool_size=10, max_overflow=15, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
