#!/usr/bin/env python3
from random import randint, choice as rc
from app import app
from models import db, Author, Publisher, Book
from faker import Faker

fake = Faker()

def create_authors():
    authors = []
    for _ in range(10):
        a = Author(
            name= fake.name(),
            pen_name= fake.first_name(),
        )
        authors.append(a)

    return authors


def create_publishers():
    publishers = []
    for _ in range(10):
        p = Publisher(
            name= fake.sentence(nb_words=2),
            founding_year = int(randint(1600, 2023))
        )
        publishers.append(p)

    return publishers


def create_books(authors, publishers):
    books = []
    for _ in range(10):
        b = Book(
            title=fake.sentence(nb_words=3),
            page_count = int(randint(0, 500)),
            author_id=rc(authors).id,
            publisher_id=rc(publishers).id,
        )
        books.append(b)
    return books


if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        # write your seeds here!
        Author.query.delete()
        Publisher.query.delete()
        Book.query.delete()

        print('Seeding authors...')
        authors = create_authors()
        db.session.add_all(authors)
        db.session.commit()

        print('Seeding publishers...')
        publishers = create_publishers()
        db.session.add_all(publishers)
        db.session.commit()

        print('Seeding books...')
        books = create_books(authors, publishers)
        db.session.add_all(books)
        db.session.commit()


        print("Seeding complete!")
