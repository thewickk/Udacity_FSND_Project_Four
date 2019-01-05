import sys

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Create our user table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


# Create our category table
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="category")

    # Create category data for our JSON endpoint
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
        }


# Create our category item table
class CategoryItem(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(255))
    creation_date = Column(DateTime())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, backref=('item'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="item")

    # Create category item data for our JSON endpoint
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creation_date': self.creation_date,
            'category_id': self.category_id,
            'user_id': self.user_id
        }


engine = create_engine('postgresql://catalog:grader@localhost/catalog')
#engine = create_engine('sqlite:///database.db')

Base.metadata.create_all(engine)
