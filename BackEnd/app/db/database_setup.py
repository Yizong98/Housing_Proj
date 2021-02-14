import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, FLOAT, DateTime, \
    Boolean

sys.path.insert(0, os.path.dirname(__file__))

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)
    phone = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    school_year = Column(String(20), nullable=False)
    major = Column(String(250))
    description = Column(String(1000), nullable=False)
    room = relationship("Room", backref="user")
    bookmark = relationship("Bookmark", backref="user")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'name': self.name,
            'description': self.description
        }


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    room_type = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    negotiable = Column(Boolean, nullable=False)
    description = Column(String(1000), nullable=False)
    move_in_id = Column(Integer, ForeignKey("move_in.id"))
    address_id = Column(Integer, ForeignKey("address.id"))
    stay_period_id = Column(Integer, ForeignKey("stay_period.id"))
    no_rooms = Column(Integer, nullable=False)
    no_bathrooms = Column(FLOAT, nullable=False)
    house_attribute = relationship("House_Attribute", backref="room")
    move_in = relationship("Move_In", backref="room")
    bookmark = relationship("Bookmark", backref="room")
    address = relationship("Address", backref="room")
    stay_period = relationship("Stay_Period", backref="room")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'room_type': self.room_type,
            'price': self.price,
            'negotiable': self.negotiable,
            'description': self.description,
            'no_rooms': self.no_rooms,
            'no_bathrooms': self.no_bathrooms
        }


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    distance = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'distance': self.distance,
            'address': self.address,
        }


class Stay_Period(Base):
    __tablename__ = 'stay_period'
    id = Column(Integer, primary_key=True)
    from_month = Column(DateTime, nullable=False)
    to_month = Column(DateTime, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'from_month': self.from_month,
            'to_month': self.to_month,
        }


class Move_In(Base):
    __tablename__ = 'move_in'

    id = Column(Integer, primary_key=True)
    early_date = Column(DateTime, nullable=False)
    late_date = Column(DateTime, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'early_date': self.early_date,
            'late_date': self.late_date,
        }


class House_Attribute(Base):
    __tablename__ = 'house_attribute'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'))
    attribute_name = Column(String(250), ForeignKey(
        'attribute.name'), nullable=False)
    house_attribute = relationship("Attribute", backref="house_attribute")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'room_id': self.room_id,
            'attribute_name': self.attribute_name
        }


class Attribute(Base):
    __tablename__ = 'attribute'

    name = Column(String(250), primary_key=True)
    category = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'category': self.category
        }


class Bookmark(Base):
    __tablename__ = 'bookmark'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'room_id': self.room_id,
            'user_id': self.user_id
        }


def createDB(db_path):
    """
    create a DB given the database schema
    return True if the db is created successfully
    """
    try:
        engine = create_engine(db_path)
        Base.metadata.create_all(engine)
        return True
    except:
        return False


if __name__ == '__main__':
    print(createDB('sqlite:///housing.db'))
