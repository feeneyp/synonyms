import datetime
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine
from flask.ext.login import UserMixin


word_association_table = Table('word_association', Base.metadata,
    Column('left_node_id', Integer, ForeignKey('words.id'), primary_key=True),
    Column('right_node_id', Integer, ForeignKey('words.id'), primary_key=True)
)

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    content = Column(Text)
    category = Column(String(128))
    level = Column(String(128))
    datetime = Column(DateTime, default=datetime.datetime.now)
    right_nodes = relationship("Word", 
                            secondary="word_association",
                            primaryjoin = id==word_association_table.c.left_node_id,
                            secondaryjoin = id==word_association_table.c.right_node_id,
                            backref="left_nodes")
    contributor_id = Column(Integer, ForeignKey('users.id'))

    
class User(Base, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    posts = relationship("Word", backref="author")
  
    

Base.metadata.create_all(engine)