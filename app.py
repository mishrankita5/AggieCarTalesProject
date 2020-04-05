from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "randomstring123"

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
    email = db.Column(db.VARCHAR(length=100), unique=True)
    password = db.Column(db.VARCHAR(length=20))
    yearOfGraduation = db.Column(db.Integer)

    def __init__(self, firstName, lastName, email, password, yearOfGraduation):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.yearOfGraduation = yearOfGraduation


class Review(db.Model):
    __tablename__ = 'Review'
    review_id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    review = db.Column(db.VARCHAR(length=2000))
    carName = db.Column(db.VARCHAR(length=100))
    carModel= db.Column(db.VARCHAR(length=100))
    carCategory = db.Column(db.VARCHAR(length=100))
    yearOfManufacturing = db.Column(db.Integer)
    carImage = db.Column(db.VARCHAR(length=100), nullable= True)
  
    

    def __init__(self, user_id, review, carName, carModel, carCategory,yearOfManufacturing,carImage):
        self.user_id = user_id
        self.review = review
        self.carName = carName
        self.carModel = carModel
        self.carCategory = carCategory
        self.yearOfManufacturing = yearOfManufacturing
        self.carImage = carImage




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
            return render_template ('login.html', message='You have registered successfully! Please log in to continue')
        return render_template('register.html', message='User already exists. Kindly login.')


# working login method
# @app.route('/login' , methods =['POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['emailId']
#         password = request.form['password']
#         if db.session.query(User).filter(User.email == email).count() > 0:
#             records = db.session.query(User).filter(User.email == email).all()
#             for record in records:
#                 # recordObject = {'id': record.user_id,
#                 #                 'user_firstName': record.firstName,
#                 #                 'user_lastName': record.lastName,
#                 #                 'user_email': record.email,
#                 #                 'user_password': record.password,
#                 #                 'user_yearOfGraduation': record.yearOfGraduation
#                 #                 }
#                 dbPassword = record.password
#                 if dbPassword == password:
#                     return render_template ('index.html', message='Welcome to Aggie Car Tales!')
#                 return render_template ('login.html', message='Invalid Password. Please try again')
#         return render_template ('register.html', message='User does not exist. Please sign up')

@app.route('/login' , methods =['POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailId']
        password = request.form['password']
        form = request.form
        records = db.session.query(User).filter(User.email == email).all()
        for record in records:
            if record:
                db_password =  record.password
                if(password == db_password): # if password correct
                    session['username'] = record.firstName
                    session['user_id'] = record.user_id
                    # firstName = record.firstName
                    # print(firstName)
                    return redirect('index.html')
                 # and if password is not correct
                return render_template ('login.html', message='Invalid Password. Please try again')
               # flash("Incorrect password, please try again or register") 
        return render_template ('register.html', message='User does not exist. Please sign up')
    return render_template('index.html')
        

@app.route('/ad-listing', methods = ['POST'])
def adlisting():
    if request.method == 'POST':
        user_id = session['user_id']
        review = request.form['review']
        carName = request.form['carName']
        carModel = request.form['carModel']
        carCategory = request.form['carCategory']
        yearOfManufacturing = request.form['yearOfManufacturing']
        carImage = request.form['carImage']

        if review == '' or carName == '' or carModel == '' or carCategory == '' or yearOfManufacturing == '':
            return render_template('ad-listing.html', message='Please enter all required fields')
        
        
        data = Review(user_id, review, carName, carModel, carCategory,yearOfManufacturing,carImage)  
        db.session.add(data)
        db.session.commit()
        return render_template ('ad-listing.html', message='Thank you for your review!')
     
@app.route('/logout')
def logout():
    session.clear()
    return redirect('login.html')


if __name__ == '__main__':
    
    app.run()