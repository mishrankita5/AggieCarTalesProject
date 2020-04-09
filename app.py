from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from base64 import b64encode
from datetime import datetime

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
    carImage = db.Column(db.LargeBinary)
    reviewDate = db.Column(db.Date)
  
    

    def __init__(self, user_id, review, carName, carModel, carCategory, yearOfManufacturing, carImage,reviewDate):
        self.user_id = user_id
        self.review = review
        self.carName = carName
        self.carModel = carModel
        self.carCategory = carCategory
        self.yearOfManufacturing = yearOfManufacturing
        self.carImage = carImage
        self.reviewDate=reviewDate




@app.route('/')
def index():
    records = db.session.query(Review).join(User,Review.user_id==User.user_id).add_columns(User.firstName,Review.carName,Review.carModel,Review.carCategory,Review.review,Review.review_id,Review.yearOfManufacturing, Review.carImage, Review.reviewDate, Review.carCategory).order_by(Review.review_id.desc()).all()
    reviewVar = ["" for x in range(len(records))]
    adminVar = ["" for x in range(len(records))]
    carNameVar = ["" for x in range(len(records))]
    carModelVar = ["" for x in range(len(records))]
    reviewIdVar = ["" for x in range(len(records))]
    carImageVar = ["" for x in range(len(records))]
    reviewDateVar = ["" for x in range(len(records))]
    carCategoryVar = ["" for x in range(len(records))]
    i=0
    for record in records:
        reviewVar[i] = record.review 
        adminVar[i] = record.firstName
        carNameVar[i] = record.carName
        carModelVar[i] = record.carModel
        reviewIdVar[i] = record.review_id
        carImageVar[i] = b64encode(record.carImage).decode("utf-8")
        reviewDateVar[i] = record.reviewDate
        carCategoryVar[i] =record.carCategory

        i=i+1
    return render_template('index.html',len = len(records),reviewVar=reviewVar,adminVar=adminVar,carNameVar=carNameVar,carModelVar=carModelVar,reviewIdVar=reviewIdVar, carImageVar = carImageVar, reviewDateVar=reviewDateVar,carCategoryVar=carCategoryVar)
    #return render_template('index.html')

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
    records = db.session.query(Review).join(User,Review.user_id==User.user_id).add_columns(User.firstName,Review.carName,Review.carModel,Review.carCategory,Review.review,Review.review_id,Review.yearOfManufacturing, Review.carImage, Review.reviewDate, Review.carCategory).order_by(Review.review_id.desc()).all()
    reviewVar = ["" for x in range(len(records))]
    adminVar = ["" for x in range(len(records))]
    carNameVar = ["" for x in range(len(records))]
    carModelVar = ["" for x in range(len(records))]
    reviewIdVar = ["" for x in range(len(records))]
    carImageVar = ["" for x in range(len(records))]
    reviewDateVar = ["" for x in range(len(records))]
    carCategoryVar = ["" for x in range(len(records))]
    i=0
    for record in records:
        reviewVar[i] = record.review 
        adminVar[i] = record.firstName
        carNameVar[i] = record.carName
        carModelVar[i] = record.carModel
        reviewIdVar[i] = record.review_id
        carImageVar[i] = b64encode(record.carImage).decode("utf-8")
        reviewDateVar[i] = record.reviewDate
        carCategoryVar[i] =record.carCategory

        i=i+1
    return render_template('index.html',len = len(records),reviewVar=reviewVar,adminVar=adminVar,carNameVar=carNameVar,carModelVar=carModelVar,reviewIdVar=reviewIdVar, carImageVar = carImageVar, reviewDateVar=reviewDateVar,carCategoryVar=carCategoryVar)
  

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
        records = db.session.query(Review).join(User,Review.user_id==User.user_id).add_columns(User.firstName,Review.carName,Review.carModel,Review.carCategory,Review.review,Review.review_id,Review.yearOfManufacturing, Review.carImage, Review.reviewDate).order_by(Review.review_id.desc()).all()
        session['carName'] = 'blogClick'
        reviewVar = ["" for x in range(len(records))]
        adminVar = ["" for x in range(len(records))]
        carNameVar = ["" for x in range(len(records))]
        carModelVar = ["" for x in range(len(records))]
        reviewIdVar = ["" for x in range(len(records))]
        carImageVar = ["" for x in range(len(records))]
        reviewDateVar = ["" for x in range(len(records))]
        i=0
        for record in records:
            reviewVar[i] = record.review 
            adminVar[i] = record.firstName
            carNameVar[i] = record.carName
            carModelVar[i] = record.carModel
            reviewIdVar[i] = record.review_id
            carImageVar[i] = b64encode(record.carImage).decode("utf-8")
            reviewDateVar[i] = record.reviewDate

            i=i+1
        return render_template('blog.html',len = len(records),reviewVar=reviewVar,adminVar=adminVar,carNameVar=carNameVar,carModelVar=carModelVar,reviewIdVar=reviewIdVar, carImageVar = carImageVar, reviewDateVar=reviewDateVar)

@app.route('/database.html')
def routeDatabase():
    return render_template('database.html')

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
            return render_template ('register_success.html')
        return render_template('register.html', message='User already exists. Kindly login.')



@app.route('/login' , methods =['POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailId']
        password = request.form['password']
        if email == '' or password == '':
            return render_template('login.html', message='Please enter all required fields')
        form = request.form
        records = db.session.query(User).filter(User.email == email).all()
        for record in records:
            if record:
                db_password =  record.password
                if(password == db_password): # if password correct
                    session['username'] = record.firstName
                    session['user_id'] = record.user_id
                    return redirect('index.html')
                 # and if password is not correct
                return render_template ('login.html', message='Invalid Password. Please try again')
               # flash("Incorrect password, please try again or register") 
        return render_template ('register.html', message='User does not exist. Please sign up')
    return render_template('index.html')
        

@app.route('/ad-listing', methods = ['POST'])
def adlisting():
    now = datetime.today()
    print (now)
    if request.method == 'POST':
        user_id = session['user_id']
        review = request.form['review']
        carName = request.form['carName']
        carModel = request.form['carModel']
        carCategory = request.form['carCategory']
        yearOfManufacturing = request.form['yearOfManufacturing']
        carImage = request.files['fileimg'].read()
        reviewDate = datetime.strftime(now, "%Y-%m-%d")
        print(reviewDate)

        if review == '' or carName == '' or carModel == '' or carCategory == '' or yearOfManufacturing == '':
            return render_template('ad-listing.html', message='Please enter all required fields')
        
        
        data = Review(user_id, review, carName, carModel, carCategory,yearOfManufacturing,carImage,reviewDate)  
        db.session.add(data)
        db.session.commit()
        return render_template ('ad-listing.html', message='Thank you for your review!')
     

@app.route('/search', methods =['POST'])
def search():
    if request.method == 'POST':
        search = request.form['searchText']
        search = search.lower()
        records = db.session.query(Review).join(User,Review.user_id==User.user_id).add_columns(User.firstName,Review.carName,Review.carModel,Review.carCategory,Review.review,Review.review_id,Review.yearOfManufacturing, Review.carImage, Review.reviewDate).filter(func.lower(Review.carName).ilike('%'+search+'%')).order_by(Review.review_id.desc()).all()
        reviewVar = ["" for x in range(len(records))]
        adminVar = ["" for x in range(len(records))]
        carNameVar = ["" for x in range(len(records))]
        carModelVar = ["" for x in range(len(records))]
        reviewIdVar = ["" for x in range(len(records))]
        carImageVar = ["" for x in range(len(records))]
        reviewDateVar = ["" for x in range(len(records))]
        i=0
        for record in records:
            session['carName'] = record.carName
            reviewVar[i] = record.review 
            adminVar[i] = record.firstName
            carNameVar[i] = record.carName
            carModelVar[i] = record.carModel
            reviewIdVar[i] = record.review_id
            carImageVar[i] = b64encode(record.carImage).decode("utf-8")
            reviewDateVar[i] = record.reviewDate
            i=i+1
            
        return render_template("blog.html", len = len(records),reviewVar=reviewVar,adminVar=adminVar,carNameVar=carNameVar,carModelVar=carModelVar,reviewIdVar=reviewIdVar,carImageVar=carImageVar, reviewDateVar=reviewDateVar) 
        


@app.route('/readMore', methods =['POST'])
def readMore():
    if request.method == 'POST':
        reviewId = request.form['tag']
        records = db.session.query(Review).join(User,Review.user_id==User.user_id).add_columns(User.firstName,Review.carName,Review.carModel,Review.carCategory,Review.review,Review.review_id,Review.yearOfManufacturing, Review.carImage, Review.reviewDate).filter(Review.review_id==reviewId).order_by(Review.review_id.desc()).all()
        reviewVar=""
        adminVar = ""
        carNameVar = ""
        carModelVar = ""
        carCategoryVar = ""
        carYearOfManufacturingVar=""
        carImageVar = ""
        reviewDateVar =""
        i=0
        for record in records:
            session['carName'] = record.carName
            
            
            reviewVar = record.review 
            adminVar= record.firstName
            carNameVar = record.carName
            carModelVar = record.carModel
            carCategoryVar=record.carCategory
            carYearOfManufacturingVar=record.yearOfManufacturing
            carImageVar = b64encode(record.carImage).decode("utf-8")
            reviewDateVar=record.reviewDate
            i=i+1
         
           
        return render_template("single-blog.html", len = len(records),reviewVar=reviewVar,adminVar=adminVar,carNameVar=carNameVar,carModelVar=carModelVar,carCategoryVar=carCategoryVar,carYearOfManufacturingVar=carYearOfManufacturingVar, carImageVar=carImageVar,reviewDateVar=reviewDateVar) 



@app.route('/showDatabase', methods=['POST'])
def showDatabase():
    if request.method == 'POST':
        userRecords = db.session.query(User).all()
        reviewRecords = db.session.query(Review).all()     
    return render_template("database.html", reviewRecords=reviewRecords, userRecords=userRecords)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('login.html')


if __name__ == '__main__':
    
    app.run()