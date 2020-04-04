from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/AggieCarTalesDB'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key = True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    # TODO - Make Email Unique
    email = db.Column(db.VARCHAR(length=100))
    password = db.Column(db.VARCHAR(length=20))
    yearOfGraduation = db.Column(db.Integer)

    def __init__(self, firstName, lastName, email, password, yearOfGraduation):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.yearOfGraduation = yearOfGraduation


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register.html')
def routeRegister():
    return render_template('register.html')

@app.route('/login.html')
def routeLogin():
    return render_template('login.html')

@app.route('/about-us.html')
def routeAbout():
    return render_template('about-us.html')

@app.route('/index.html')
def routeHome():
    return render_template('index.html')

@app.route('/ad-listing.html')
def routeAddListing():
    return render_template('ad-listing.html')

@app.route('/user-profile.html')
def routeUserProfile():
    return render_template('user-profile.html')

@app.route('/single-blog.html')
def routeSingleBlog():
    return render_template('single-blog.html')

@app.route('/blog.html')
def routeBlog():
    return render_template('blog.html')

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        yearOfGraduation = request.form['yearOfGraduation']

        if firstName == '' or lastName == '' or email == '' or password == '' or yearOfGraduation == '':
            return render_template('register.html', message='Please enter all required fields')
        
        if db.session.query(User).filter(User.email == email).count() == 0:
            data = User(firstName, lastName, email, password, yearOfGraduation)  
            db.session.add(data)
            db.session.commit()
            return render_template ('index.html', message='Welcome to Aggie Car Tales!')
        return render_template('register.html', message='User already exists. Kindly login.')

@app.route('/login' , methods =['POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailId']
        password = request.form['password']
        print(password)
        records = db.session.query(User).filter(User.email == email).all()
        for record in records:
            # recordObject = {'id': record.user_id,
            #                 'user_firstName': record.firstName,
            #                 'user_lastName': record.lastName,
            #                 'user_email': record.email,
            #                 'user_password': record.password,
            #                 'user_yearOfGraduation': record.yearOfGraduation
            #                 }
            dbPassword = record.password
            # print(record.password)
            if dbPassword == password:
               print("password match")
            print("password don't match")

        
        # if db.session.query(User).filter(User.email == email).count() > 0:
    return render_template ('index.html', message='Welcome to Aggie Car Tales!')
        

if __name__ == '__main__':
    
    app.run()