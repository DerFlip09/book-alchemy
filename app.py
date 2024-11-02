import os
from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book

app = Flask(__name__)

# Get the absolute path to the current directory
base_dir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "data", "library.sqlite3")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create the tables
# with app.app_context():
#     print("Creating tables...")
#     db.create_all()  # Create all tables based on the defined models
#     print("Tables created.")


@app.route('/', methods=['GET'])
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        author_name = request.form.get('name').strip()
        birth_date = request.form.get('birth_date').strip()
        death_date = request.form.get('death_date').strip()
        author = Author(name=author_name, birth_date=birth_date, death_date=death_date)
        db.session.add(author)
        db.session.commit()
        return redirect('/add_author', 302)
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        author_id = request.form.get('author_id').strip()
        publication_year = request.form.get('publication_year').strip()
        isbn = request.form.get('isbn').strip()
        book = Book(title=title, author_id=author_id, publication_year=publication_year, isbn=isbn)
        db.session.add(book)
        db.session.commit()
        return redirect('/add_book', 302)
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
