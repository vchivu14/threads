import sqlite3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    @property
    def serialize(self):
        return {
            'name': self.name,
            'email': self.email,
            'id': self.id,
            'picture': self.picture,
        }


class Cause(Base):
    __tablename__ = 'cause'
    name = Column(
        String(80), nullable=False)
    id = Column(
        Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class EffectAnswer(Base):
    __tablename__ = 'answer_item'
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    area = Column(String(40))
    solution = Column(String(400))
    importance = Column(String(20))
    cause_id = Column(
        Integer, ForeignKey('cause.id'))
    cause = relationship(Cause)
    user_id = Column(
        Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        return {
            'name': self.name,
            'solution': self.solution,
            'id': self.id,
            'importance': self.importance,
            'area': self.area,
        }


engine = create_engine('sqlite:///causeandeffectwithusers.db')
Base.metadata.create_all(engine)
