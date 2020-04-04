from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/AggieCarTalesDB'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model)
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key = True, serial = True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.Varchar(100))
    password = db.Column(db.Varchar(20))
    yearOfGraduation = db.Column(db.Integer)

    def __init__(firstName,lastName,email,password,yearOfGraduation):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.yearOfGraduation = yearOfGraduation


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/about-us.html')
def about():
    return render_template('about-us.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/ad-listing.html')
def addListing():
    return render_template('ad-listing.html')

@app.route('/user-profile.html')
def userProfile():
    return render_template('user-profile.html')

@app.route('/single-blog.html')
def singleBlog():
    return render_template('single-blog.html')

@app.route('/blog.html')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    
    app.run()