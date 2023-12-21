#!/usr/bin/python3
"""This module defines a class to manage DB Storage for hbnb clone"""
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.user import User
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
import sqlalchemy as db

# Dictionary mapping class names to their corresponding classes
classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Manages DB Storage for hbnb clone"""

    # Database engine & Database session
    __engine = None
    __session = None

    def __init__(self):
        """Initialize a DBStorage object"""

    def __init__(self):
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'. format(
                HBNB_MYSQL_USER,
                HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST,
                HBNB_MYSQL_DB),
            pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Reload data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def all(self, cls=None):
        """Query on the current database session"""
        result_dict = {}
        if cls is None:
            for class_name, class_type in classes.items():
                instances = self.session.query(class_type).all()
                for instance in instances:
                    key = instance.__class__.__name__ + '.' + instance.id
                    result_dict[key] = instance
        else:
            instances = self.__db_session.query(cls).all()
            for instance in instances:
                key = instance.__class__.__name__ + '.' + instance.id
                result_dict[key] = instance
        return result_dict

    def delete(self, obj=None):
        """Delete from the current database session if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()
