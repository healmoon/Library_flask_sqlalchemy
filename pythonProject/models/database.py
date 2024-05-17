from sqlalchemy import Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Genre(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    books = relationship("Book", back_populates="genre")

    def __repr__(self):
        return self.name


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=True)
    genre_id: Mapped[int] = mapped_column(Integer, ForeignKey('genre.id', ondelete="SET NULL"))
    genre = relationship("Genre", back_populates="books")
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    cover_url: Mapped[str] = mapped_column(String(200),
                                           default="https://w7.pngwing.com"
                                                   "/pngs/15/881/png-transparent-drawing-book"
                                                   "-cover-shy-town-girls-book.png")
    text_url: Mapped[str] = mapped_column(String,
                                          default="жили были, он надеялся, она была противной, сверху упал ящер, конец"
                                          + "мяумяу\n" * 800)

    def __repr__(self):
        return f'Book(name={self.name!r})'
