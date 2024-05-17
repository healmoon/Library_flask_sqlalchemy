from flask import Flask, render_template, request, redirect

from models.database import db, Book, Genre

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


with app.app_context():
    db.drop_all()
    db.create_all()

    novel = Genre(name="Роман")
    db.session.add(novel)

    fantasy = Genre(name="Фэнтези")
    db.session.add(fantasy)

    Harry_potter = Book(
            id=1,
            name="Гарри Поттер",
            author="Дж. К. Роулинг",
            genre=fantasy,
        )
    db.session.add(Harry_potter)
    db.session.add(
        Book(
            id=2,
            name="Властелин колец",
            author="Дж. Р. Р. Толкина",
            genre=fantasy
        )
    )
    Great_Expectations = Book(
            id=3,
            name="Большие Надежды",
            author="Чарльз Диккенс",
            genre=novel,
            cover_url="https://img4.labirint.ru"
                      "/rc/cf0d0bed48aa3f120ff85b793aff8a32/363x561q80/books54/530788/cover.jpg?1612697178"
    )
    db.session.add(Great_Expectations)
    db.session.commit()


@app.route("/")
def all_books():
    books = Book.query.order_by(Book.id.desc()).limit(15).all()
    return render_template("Books.html", books=books)


@app.route("/genre/<int:genre_id>")
def books_by_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template(
        "books_by_genre.html",
        genre_name=genre.name,
        books=genre.books,
    )


@app.route("/save_book_status", methods=["POST"])
def save_book_status():
    book_id = request.form.get('book_id')
    is_read = True if request.form.get("is_read") else False

    book = Book.query.get(book_id)
    book.is_read = is_read
    db.session.commit()

    return redirect("/")


@app.route('/read_books')
def read_books():
    is_read_books = Book.query.filter_by(is_read=True).all()
    return render_template("read_books.html", books=is_read_books)


@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = Book.query.get(book_id)
    return render_template('book_details.html', book=book)


if __name__ == "__main__":
    app.run(debug=True)