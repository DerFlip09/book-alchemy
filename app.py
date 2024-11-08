import os
from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book

app = Flask(__name__)

# Get the absolute path to the current directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Configure the database URI and tracking modifications
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
    """Render the home page with a list of books.

    Retrieves books from the database, allowing for sorting and searching.

    Returns:
        Rendered HTML page of the home view with books.
    """
    sort_by = request.args.get('sort_by', 'title')
    search = request.args.get('search')

    # Search functionality
    if search:
        books = Book.query.filter(Book.title.like(f'%{search}%')).order_by(Book.title).all()
        return render_template('home.html', books=books, success=bool(books))

    # Sorting functionality
    if sort_by == 'title':
        books = Book.query.order_by(Book.title).all()
    elif sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    elif sort_by == 'publication_year':
        books = Book.query.order_by(Book.publication_year).all()
    else:
        books = Book.query.all()  # Default case if no valid sort_by

    return render_template('home.html', books=books, success=True)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Add a new author to the database.

    Handles both GET and POST requests. On a POST request, it retrieves
    author details from the form and adds the author to the database.

    Returns:
        Redirects to the same page with a success flag if the author is added.
        Renders the add author form on a GET request.
    """
    if request.method == 'POST':
        author_name = request.form.get('name').strip()
        birth_date = request.form.get('birth_date').strip()
        death_date = request.form.get('death_date').strip()
        author = Author(name=author_name, birth_date=birth_date, death_date=death_date)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('add_author', success=True), 302)
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Add a new book to the database.

    Handles both GET and POST requests. On a POST request, it retrieves
    book details from the form and adds the book to the database.

    Returns:
        Redirects to the same page with a success flag if the book is added.
        Renders the add book form along with a list of authors on a GET request.
    """
    if request.method == 'POST':
        title = request.form.get('title').strip()
        author_id = request.form.get('author_id').strip()
        publication_year = request.form.get('publication_year').strip()
        isbn = request.form.get('isbn').strip()
        book = Book(title=title, author_id=author_id, publication_year=publication_year, isbn=isbn)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('add_book', success=True), 302)

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book from the database.

    Deletes a book identified by the book_id parameter.

    Args:
        book_id (int): The ID of the book to be deleted.

    Returns:
        Redirects to the home page after the book is deleted.
    """
    book = Book.query.get(book_id)
    if book:  # Ensure the book exists before attempting to delete
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('home', success_delete=True), 302)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
