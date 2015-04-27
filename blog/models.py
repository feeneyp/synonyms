import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine
from flask.ext.login import UserMixin


word_association_table = Table('word_association', Base.metadata,
    Column('word_id', Integer, ForeignKey('word.id')),
    Column('related_word_id', Integer, ForeignKey('word.id'))
)

class Word(Base):
    __tablename__ = "word"
    id = Column(Integer, primary_key=True)
    content = Column(String(128))
    synonyms = relationship("Word", secondary="word_association_table",
                            backref="synonyms")
#    contributor_id = Column(Integer, ForeignKey('users.id'))
    
    
# class User(Base, UserMixin):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String(128))
#     email = Column(String(128), unique=True)
#     password = Column(String(128))
#     posts = relationship("Post", backref="author")
  
    

Base.metadata.create_all(engine)