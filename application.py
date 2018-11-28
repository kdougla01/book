import os

from sqlalchemy.ext.associationproxy import association_proxy


from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "demo.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))

    # access all authors of that book
    authors = association_proxy('bookauthor', 'author', creator=lambda author: BookAuthor(author=author))

    def __init__(self, title):
        self.title = title

    def __unicode__(self):
        return '<Book {0}>'.format(self.id)


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    # access all books w/ this author
    books = association_proxy('bookauthor', 'book', creator=lambda book: BookAuthor(book=book))

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return '<Author {0}>'.format(self.id)


class BookAuthor(db.Model):
    """ This is an association table for the Book<->Author Many to Many relationship. """
    __tablename__ = 'book_author'

    id = db.Column(db.Integer, primary_key=True)

    id_book = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    id_author = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)

    # you can also access these objects of books and authors respectively
    book = db.relationship(Book, backref='bookauthor')
    author = db.relationship(Author, backref='bookauthor')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
