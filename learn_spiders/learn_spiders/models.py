# from decimal import Clamped
from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Date, DateTime, Float, Boolean, Text
from scrapy.utils.project import get_project_settings

Base = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py
    Change CONNECTION_STRING in settings.py to connect to different datatbase system i.e MySQL, etc
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    Base.metadata.create_all(engine)


# Association Table for Many-to-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
quote_tag = Table('quote_tag', Base.metadata,
    Column('quote_id', Integer, ForeignKey('quote.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

# Creating Many-to-Many relationship between Quote and Tag (one quote can one or more tags and tag can associate with one or more quotes)
# Creating One-to-Many relationship between Author and Quote (one author can have one or more quotes but one quote belongs to only one author)
class Quote(Base):
    """
    Creating an empty table for data from the Quote field 
    """
    
    __tablename__ = "quote"

    id = Column(Integer, primary_key=True)
    quote_content = Column('quote_content', Text())
    author_id = Column(Integer, ForeignKey('author.id')) # Many quotes to one author
    tags = relationship('Tag', secondary='quote_tag',
        lazy='dynamic', backref="quote") # Many-to-Many for quote and tag

class Author(Base):
    """
    Creating an empty table for data from the Author field
    """

    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    birthday = Column('birthday', DateTime)
    bornlocation = Column('bornlocation', String(150))
    bio = Column('bio', Text())
    quotes = relationship('Quote', backref='author') # One author to many Quotes


class Tag(Base):
    """
    Creating an empty table for data from the Tag field
    """

    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True)
    quotes = relationship('Quote', secondary='quote_tag',
        lazy='dynamic', backref="tag") # Many-to-Many for quote and tag
