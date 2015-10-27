# import SQL Alchemy dependencies
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """Create table to hold User data"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Category(Base):
    """Create table to hold Category data"""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return{
            'id': self.id,
            'name': self.name,
        }


class Item(Base):
    """Create table to hold Item data"""
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)



engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
