from flask import Flask, session, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import hashlib
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "J*j!(#)_(!U?TU*_T(#N-?FA*-_JND-UN*"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:debugaccountpassword@localhost/cms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
salt = "J7:k*a8:-I2gmw"

_A = "Lorem ipsum dalar tarem"


# Database cinfiguration
db = SQLAlchemy(app)


# class Text_element(db.Model):
#     element_id = db.Column(db.Integer, primary_key=True, auto_increment=True, nullable=False)
#     name = db.Column(db.String, nullable=False)
#     content = db.Column(db.String, nullable=False)
#     client_id = db.Column(db.Integer, db.ForeignKey('cleint.client_id'),
#         nullable=False)
#     client = db.relationship('client',
#         backref=db.backref('text_element', lazy=True))

# class Image_element(db.Model):
#     element_id = db.Column(db.Integer, primary_key=True, auto_increment=True, nullable=False)
#     name = db.Column(db.String, nullable=False)
#     content = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
#     client_id = db.Column(db.Integer, db.ForeignKey('cleint.client_id'),
#         nullable=False)
#     client = db.relationship('client',
#         backref=db.backref('image_element', lazy=True))

class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True, auto_increment=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)



# Routings
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password') + salt
        hash = hashlib.md5(password.encode()).hexdigest()
        result = Client.query.filter_by(email=email, passwordHash=hash).first()
        message = ""
        if result is not None:
            # logged in
            session['logged_in'] = True
            session['client_id'] = result.client_id
            message = "Logget inn."
            return redirect("home")
        else:
            # not logged in
            message = "Feil epost/passord."
            pass
    
    return render_template('index.html', message=message)

@app.route('/home')
def home():
    if session.get("logged_in"):
        try:
            session.pop("article")
            session.pop("page")
            session.pop("element")
        except:
            pass
        return render_template("home.html")
    else:
        return redirect("index")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/apps')
def apps():
    if session.get("logged_in"):
        test_applications = {
            "a": "Wacker Features",
            "b": "Del Tattoo",
            "c": "Blogg"
        }
        
        return test_applications
    else:
        return "Invalid Login."


@app.route('/pages', methods=['GET'])
def page():
    if session.get("logged_in"):
        test_pages = {
                "a": "Forside",
                "b": "Om oss",
                "c": "Kontakt"
            }
        return test_pages
    else:
        return "Invalid Login."


@app.route('/elements')
def elements():
    if session.get("logged_in"):
        test_elements = {
            "a": "First paragraph",
            "b": "Second paragraph",
            "c": "Bottom paragraph"
        }
        return test_elements
    else:
        return "Invalid Login."

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    
    if session.get("logged_in"):
        if request.method == "GET":
            # Get data from database based on arguments in the request
            # data = dataFromDb

            ### DEBUG
            session['article'] = 1
            session['page'] = 2
            session['element'] = 4
            print(request.args.get('application'))
            print(request.args.get('page'))
            print(request.args.get('element'))
            
            try:
                a = session.get("A")
            except:
                a = "Lorem ipsum dalar tarem dasam"
            ### DEBUG
            return render_template("edit.html", data=a)
        elif request.method == "POST":
            ### DEGUB
            nyData = request.form.get("data")
            session['A'] = nyData
            message = "Dine endringer ble lagret."
            ### DEGUB
            return url_for('home')
    else:
        return "Invalid Login."