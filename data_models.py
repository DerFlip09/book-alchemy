from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Author(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True, autoincrement=True)
    name: db.Mapped[str] = db.mapped_column(nullable=False)
    birth_date: db.Mapped[str] = db.mapped_column()
    death_date: db.Mapped[str] = db.mapped_column()

    def __repr__(self):
        return f"Author(id = {self.id}, name = {self.name}"

    def __str__(self):
        birth = self.birth_date if self.birth_date else ""
        death = self.death_date if self.death_date else ""

        if birth or death:
            return f"{self.id}. {self.name} ({birth} - {death})".strip(" -")
        else:
            return f"{self.id}. {self.name}"


class Book(db.Model):
    id: db.Mapped[int] = db.mapped_column(primary_key=True, autoincrement=True)
    author_id: db.Mapped[int] = db.mapped_column(db.ForeignKey('author.id'))
    title: db.Mapped[str] = db.mapped_column(nullable=False)
    publication_year: db.Mapped[str] = db.mapped_column()
    isbn: db.Mapped[int] = db.mapped_column()

    def __repr__(self):
        return f"Book(id = {self.id}, title = {self.title}"

    def __str__(self):
        pub_year = self.publication_year if self.publication_year else ""

        if pub_year:
            return f"{self.id}. {self.title} ({pub_year})"
        else:
            return f"{self.id}. {self.title}"
