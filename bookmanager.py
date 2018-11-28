#v1.1
import os

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    #########
    author = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    num_of_pages = db.Column(db.Integer)
    #########

    def __repr__(self):
        return "<Title: {}>".format(self.title)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    nationality = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return "<Author: {}>".format(self.name)

@app.route('/', methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"), \
                        author=request.form.get("author"), \
                        genre=request.form.get("genre"), \
                        num_of_pages=request.form.get("pages"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route('/author', methods=["GET", "POST"])
def author():
    authors = None
    if request.form:
        try:
            author = Author(name=request.form.get("name"), \
                            nationality=request.form.get("nationality"), \
                            age=request.form.get("age"))
            db.session.add(author)
            db.session.commit()
        except Exception as e:
            print("Failed to add author")
            print(e)
    authors = Author.query.all()
    return render_template("authors.html", authors=authors)


@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
