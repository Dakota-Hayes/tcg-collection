from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/books/create', methods = ['POST'])
@token_required
def create_book(current_user_token):
    ISBN = request.json['ISBN']
    author_name = request.json['author_name']
    book_title = request.json['book_title']
    page_count = request.json['page_count']
    book_type = request.json['book_type']
    book = Book(ISBN, author_name, book_title, page_count, book_type)
    db.session.add(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/all', methods = ['GET'])
@token_required
def get_books(current_user_token):
    books = Book.query.filter_by().all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/ISBN/<book_type>', methods = ['GET'])
@token_required
def get_books_by_book_type(current_user_token,book_type):
    books = Book.query.filter_by(book_type = book_type).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/ISBN/<book_ISBN>', methods = ['GET'])
@token_required
def get_books_by_ISBN(current_user_token,book_ISBN):
    books = Book.query.filter_by(ISBN = book_ISBN).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/author_name/<book_author_name>', methods = ['GET'])
@token_required
def get_books_by_author_name(current_user_token,book_author_name):
    books = Book.query.filter_by(author_name = book_author_name).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/book_title/<book_book_title>', methods = ['GET'])
@token_required
def get_books_by_book_title(current_user_token,book_book_title):
    books = Book.query.filter_by(book_title = book_book_title).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/page_count/<book_page_count>', methods = ['GET'])
@token_required
def get_books_by_page_count(current_user_token,book_page_count):
    books = Book.query.filter_by(page_count = book_page_count).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/<book_id>', methods = ['GET'])
@token_required
def get_book(current_user_token, book_id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        book = Book.query.get(book_id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/books/<book_id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,book_id):
    book = Book.query.get(book_id) 
    book.ISBN = request.json['ISBN']
    book.author_name = request.json['author_name']
    book.book_title = request.json['book_title']
    book.page_count = request.json['page_count']

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<book_id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)