#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Book, Author, Publisher

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

# AUTHORS

@app.get('/authors/<int:id>')
def get_author_by_id(id):
    author = db.session.get(Author, id)
    if not author:
        return {'error': 'Author could not be found'}, 404
    
    return author.to_dict(), 200

@app.delete('/authors/<int:id>')
def remove_author(id):
    author = db.session.get(Author, id)

    if not author:
        return {'error', 'Author could not be found'}, 404
    
    db.session.delete(author)
    db.session.commit()

    return {}, 204

# BOOKS

@app.get('/books')
def get_books():
    books = Book.query.all()
    books_list = []

    for b in books:
        books_list.append(b.to_dict(rules = ['publisher.name', 'author.name']))
    
    return books_list, 200

@app.post('/books')
def add_book():
    try:
        data = request.json
        book = Book(name = data.get('name'), page_count = data.get('page_count'), author_name = data.get('author_name'), publisher_name = data.get('publisher_name'))
        db.session.add(book)
        db.session.commit()
        return book.to_dict(), 200
    
    except Exception:
        return {'errors': ['validation erros']}, 404
    

# PUBLISHER
    
@app.get('/publishers/<int:id>')
def get_publisher_by_id(id):
    publisher = db.session.get(Publisher, id)

    if not publisher:
        return {'error': 'Publisher could not be found'}, 404
    
    return publisher.to_dict()



if __name__ == '__main__':
    app.run(port=5555, debug=True)
