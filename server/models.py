from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# write your models here!

class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False, unique = True)
    page_count = db.Column(db.Integer, nullable = False)

    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    publisher = db.relationship('Publisher', back_populates = 'books')
    author = db.relationship('Author', back_populates = 'books')

    serialize_rules = ['-publisher.books', '-author.books']


    #Create Validat: page caount must be greater than 0
    @validates('page_count')
    def validate_page_count(self, key, page_count):
        if not 0 < page_count:
            raise ValueError('Page count must be greater than 0')
        
        return page_count



class Publisher(db.Model, SerializerMixin):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    founding_year = db.Column(db.Integer, nullable = False)

    books = db.relationship('Book', back_populates = 'publisher')

    serialize_rules = ['-books.publisher']


    #Create Validate: founding_year must be between 1600 and current year
    @validates('founding_year')
    def validate_year(self, key, founding_year):

        if not 1600 <= founding_year <= 2024:
            raise ValueError('Year must be between 1600 and current year')
            
        return founding_year


class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    pen_name = db.Column(db.String)

    books = db.relationship('Book', back_populates = 'author')

    serialize_rules = ['-books.author']