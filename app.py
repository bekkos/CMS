from flask import Flask, session, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import hashlib
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "J*j!(#)_(!U?TU*_T(#N-?FA*-_JND-UN*"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cmsUser:_Disp446Disp_@62.210.219.84:3306/CMS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
salt = "J7:k*a8:-I2gmw"

_A = "Lorem ipsum dalar tarem"


# Database cinfiguration
db = SQLAlchemy(app)




class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    
    applications = db.relationship('Application', backref='client', lazy=True)

class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    pages = db.relationship('Page', backref='pages', lazy=True)

class Page(db.Model):
    page_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    application_id = db.Column(db.Integer, db.ForeignKey('application.application_id'), nullable=False)
    textelements = db.relationship('Textelement', backref='textelements', lazy=True)
    imageelements = db.relationship('Imageelement', backref='imageelements', lazy=True)


class Textelement(db.Model):
    element_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    
    page_id = db.Column(db.Integer, db.ForeignKey('page.page_id'), nullable=False)


class Imageelement(db.Model):
    element_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    page_id = db.Column(db.Integer, db.ForeignKey('page.page_id'), nullable=False)



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
        id = session.get('client_id')
        c = Client.query.filter_by(client_id=id).first()
        applications = {}
        for i in range(len(c.applications)):
            applications[i] = c.applications[i].name
        return applications
    else:
        return "Invalid Login."


@app.route('/pages', methods=['GET'])
def page():
    if session.get("logged_in"):
        id = session.get('client_id')
        c = Client.query.filter_by(client_id=id).first()
        app_id = int(request.args.get('id'))-1
        session['application_id'] = app_id
        pages = {}
        for i in range(len(c.applications[app_id-1].pages)):
            pages[i] = c.applications[app_id-1].pages[i].name
        return pages
    else:
        return "Invalid Login."


@app.route('/elements')
def elements():
    if session.get("logged_in"):
        id = session.get('client_id')
        c = Client.query.filter_by(client_id=id).first()
        app_id = session.get('application_id')
        page_id = int(request.args.get('id'))-1
        session['page_id'] = page_id
        elements = {}
        i = 0
        x = 0
        while i < len(c.applications[app_id].pages[page_id].textelements):
            elements[i] = c.applications[app_id].pages[page_id].textelements[i].name
            i += 1
        while x < len(c.applications[app_id].pages[page_id].imageelements):
            elements[i] = c.applications[app_id].pages[page_id].imageelements[x].name
            i += 1
            x += 1
        return elements
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