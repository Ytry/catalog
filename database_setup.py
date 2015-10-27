# import SQL Alchemy dependencies
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()




engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
