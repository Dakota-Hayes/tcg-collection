from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Book(db.Model):
    id = db.Column(db.String, primary_key=True)
    author_name = db.Column(db.String(150), nullable=True, default='')
    book_title = db.Column(db.String(150), nullable = True, default = '')
    book_type = db.Column(db.String(150), nullable = True, default = '')
    ISBN = db.Column(db.Integer, nullable = True, default = 0)
    page_count = db.Column(db.Integer, nullable = True, default = 0)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, ISBN=0, author_name = '', book_title='',page_count=0, book_type=''):
        self.id = self.set_id()
        self.author_name = author_name
        self.book_title = book_title
        self.book_type = book_type
        self.ISBN = ISBN
        self.page_count = page_count

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_author_name(self, author_name):
        self.author_name = author_name

    def set_book_title(self, book_title):
        self.book_title = book_title

    def set_book_type(self, book_type):
        self.book_type
    
    def set_ISBN(self, ISBN):
        self.ISBN = ISBN

    def set_page_count(self, page_count):
        self.page_count = page_count

    def __repr__(self):
        return f'Book {self.author_name} {self.book_title} {self.book_type} {self.ISBN} {self.page_count} has been added to the database'

class BookSchema(ma.Schema):
    class Meta:
        fields = ['id', 'ISBN', 'author_name','book_title','page_count','book_type']

book_schema = BookSchema()
books_schema = BookSchema(many=True)