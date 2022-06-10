from email.mime import audio
from django.shortcuts import render
from sqlalchemy import join
import numpy as np
import joblib
from functools import wraps
from flask_login_multi.login_manager import LoginManager
from sqlalchemy import select
from chat import get_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, flash, redirect, url_for,Blueprint,session,jsonify
from flask_login import UserMixin, login_fresh, login_user,LoginManager, login_required, logout_user,current_user,AnonymousUserMixin
from wtforms import validators, PasswordField, SubmitField, EmailField, IntegerField, StringField, SelectField, BooleanField,DateTimeLocalField
from wtforms.validators import email_validator, DataRequired, ValidationError, EqualTo
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from wtforms.widgets import TextArea
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
from werkzeug.utils import secure_filename
import uuid as uuid
import os
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SECRET_KEY'] = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/ehr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mysql_db = SQLAlchemy(app)
db = SQLAlchemy(app)
migrate = Migrate(app, mysql_db, render_as_batch=True)
admin_app = Blueprint('docto', __name__, url_prefix="/doctor")  
user_app = Blueprint('patient', __name__, url_prefix="/patient")  

Upload_Folder='static/images_user'
audio_folder='static/audio_folder'
app.config['audio_folder']=audio_folder
app.config['Upload_Folder']=Upload_Folder
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/login/patient/home')
def home_patient():
    return render_template('index_patient.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    return render_template('predict.html')
@app.route('/login/patient/predict', methods=['GET', 'POST'])
def predict_patient():
    return render_template('predict_patient.html')


@app.errorhandler(404)
def error_file_handler(e):
    return render_template('404.html'), 404


@app.route('/predict/stroke', methods=['GET', 'POST'])
def stroke():
    return render_template('stroke.html')

# predicting stroke


@app.route('/predict/stroke/predict_stroke', methods=['GET', 'POST'])
def predict_stroke():
    model = pickle.load(open('predict/stroke/stroke.pkl', 'rb'))
    if request.method == 'POST':
        gender = request.form['gender']
        if gender == 'Male':
            gender = 1
        else:
            gender = 0
        Age = int(request.form['Age'])
        bp = request.form['bp']
        if bp == 'Yes':
            bp = 1
        else:
            bp = 0
        heart = request.form['heart']
        if heart == 'Yes':
            heart = 0
        else:
            heart = 1
        married = request.form['married']
        if married == 'Yes':
            married = 1
        else:
            married = 0
        work = request.form['work']
        if work == 'never wroked':
            work = 1
        elif work == 'private':
            work = 2
        elif work == 'self employed':
            work = 3
        elif work == 'childern':
            work = 4
        else:
            work = 0
        house = request.form['house']
        if house == 'Urban Housing':
            house = 1
        else:
            house = 0
        glucose = int(request.form['glucose'])
        bmi = int(request.form['bmi'])
        smoking = request.form['smoking']
        if smoking == 'Used to Smoke':
            smoking = 1
        elif smoking == 'Never Smoked':
            smoking = 2
        elif smoking == 'Smokes':
            smoking = 3
        else:
            smoking = 0
        pred = model.predict(
            [[gender, Age, bp, heart, married, work, house, glucose, bmi, smoking]])
        if pred == 0:
            return render_template('pred_stroke.html', text='You will never have a stroke in the near future,maintain good health and diet.')
        else:
            return render_template('pred_stroke.html', text='You may have stroke in the near future Please take precautions and lead a stress free life as possible.')
    else:
        return render_template('stroke.html')


def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if(size == 5):
        loaded_model = joblib.load(
            'C:\\Users\\kanch\\Desktop\\projects\\ehr\\predict\\breast_cancer\\cancer_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]
# predicting Heart attack


@app.route('/predict/heart', methods=['GET', 'POST'])
def heart():
    return render_template('heart.html')


@app.route('/predict/heart/predict_heart', methods=['GET', 'POST'])
def predict_heart():
    model = pickle.load(open('predict/heart attack/Heart.pkl', 'rb'))
    if request.method == 'POST':
        Age = int(request.form['Age'])
        gender = request.form['gender']
        if gender == "Male":
            gender = 0
        else:
            gender = 1
        cpain = request.form['cpain']
        if cpain == "Typical angina":
            cpain = 0
        elif cpain == 'Atypical Angina':
            cpain = 1
        elif cpain == 'Non-Anginal Pain':
            cpain = 2
        else:
            cpain = 3
        Bloodp = int(request.form['BP'])
        Cholestoral = int(request.form['Cholestoral'])
        sugar = request.form['sugar']
        if sugar == "Greater 120":
            sugar = 1
        else:
            sugar = 0
        ecg = request.form['ecg']
        if ecg == "Normal":
            ecg = 0
        elif ecg == "ST-T wave normality":
            ecg = 1
        else:
            ecg = 2
        heartrate = int(request.form['heartrate'])
        prev = float(request.form['prev'])
        slope = int(request.form['slope'])
        vessels = int(request.form['vessels'])
        stress = int(request.form['stress'])
        excercise = request.form['excercise']
        if excercise == 'yes':
            excercise = 1
        else:
            excercise = 0
        pred = model.predict([[Age, gender, cpain, Bloodp, Cholestoral,
                               sugar, ecg, heartrate, prev, slope, vessels, stress, excercise]])
        if pred == 0:
            return render_template('pred_heart.html', text='You will never have heart attack in near future,maintain proper diet and excercise')
        else:
            return render_template('pred_heart.html', text="You are predicted to have a Heart attack in near future, please consult doctor , take precautionary steps , take medications ")
    else:
        return render_template('heart.html')
# predicting diabetes


@app.route('/predict/diabetes', methods=['POST', 'GET'])
def diabetes():
    return render_template('diabetes.html')


@app.route('/predict/diabetes/predict_diabetes', methods=['POST', 'GET'])
def predict_diabetes():
    model = pickle.load(open('predict/diabetes/diabetes.pkl', 'rb'))
    if request.method == 'POST':
        Pregnancies = int(request.form['Pregnancies'])
        Glucose = int(request.form['Glucose'])
        BloodPressure = int(request.form['BloodPressure'])
        SkinThickness = int(request.form['SkinThickness'])
        Insulin = int(request.form['Insulin'])
        BMI = int(request.form['BMI'])
        DiabetesPedigreeFunction = float(
            request.form['DiabetesPedigreeFunction'])
        Age = int(request.form['Age'])
        prediction = model.predict(
            [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        if prediction == 0:
            return render_template('pred_diabetes.html', text='you dont have diabetes')
        else:
            return render_template('pred_diabetes.html', text='you have diabetes')
    else:
        return render_template('diabetes.html')
# predicting kidney disease


@app.route('/predict/kidney', methods=['POST', "GET"])
def kidney():
    return render_template('kidney.html')


@app.route('/predict/kidney/predict_kidney', methods=['POST', 'GET'])
def predict_kidney():
    model = pickle.load(open('predict/kidney/kidney.pkl', 'rb'))
    if request.method == 'POST':
        Age = int(request.form['Age'])
        Bp = int(request.form['BP'])
        gravity = int(request.form['gravity'])
        albumin = int(request.form['albumin'])
        glucose = int(request.form['glucose'])
        work = request.form['work']
        if work == 'Normal':
            work = 1
        else:
            work = 0
        pus = request.form['puss']
        if pus == 'Normal':
            pus = 1
        else:
            pus = 0
        clumps = request.form['clumps']
        if clumps == 'Not present':
            clumps = 1
        else:
            clumps = 0
        bacteria = request.form['bacteria']
        if bacteria == 'Not present':
            bacteria = 1
        else:
            bacteria = 0
        Blood = int(request.form['Blood'])
        urea = int(request.form['urea'])
        serum = int(request.form['serum'])
        sodium = int(request.form['sodium'])
        potassium = int(request.form['potassium'])
        hemo = int(request.form['hemo'])
        packed = int(request.form['packed'])
        wbc = int(request.form['wbc'])
        rbc = int(request.form['rbc'])
        hypertension = request.form['hypertension']
        if hypertension == 'No':
            hypertension = 0
        else:
            hypertension = 1
        diabetes = request.form['diabetes']
        if diabetes == 'No':
            diabetes = 0
        else:
            diabetes = 1
        coronary = request.form['coronary']
        if coronary == "No":
            coronary = 0
        else:
            coronary = 1
        appetite = request.form['appetite']
        if appetite == 'No':
            appetite = 0
        else:
            appetite = 1
        pedal = request.form['pedal']
        if pedal == 'No':
            pedal = 0
        else:
            pedal = 1
        anemia = request.form['anemia']
        if anemia == 'No':
            anemia = 0
        else:
            anemia = 1
        pred = model.predict([[Age, Bp, gravity, albumin, glucose, work, pus, clumps, bacteria, Blood, urea, serum,
                               sodium, potassium, hemo, packed, wbc, rbc, hypertension, diabetes, coronary, appetite, pedal, anemia]])
        if pred == 0:
            return render_template('pred_kidney.html', text="you dont have kindey failure")
        else:
            return render_template('pred_kidney.html', text='you will have kidney failure in the near future')
    else:
        return render_template('kidney.html')
# predicting Breast cancer


@app.route('/predict/breast', methods=["POST", "GET"])
def breast():
    return render_template('breast.html')


@app.route('/predict/breast/predict_breast', methods=['POST', 'GET'])
def predict_breast():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        # cancer
        if(len(to_predict_list) == 5):
            result = ValuePredictor(to_predict_list, 5)

    if(int(result) == 1):
        prediction = "Sorry you have  chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    return(render_template("pred_breast.html", text=prediction))


@app.route('/predict/hepatitis', methods=["POST", "GET"])
def hepatitis():
    return render_template('hepatitis.html')


@app.route('/predict/hepatitis/predict_hepatitis', methods=["POST", "GET"])
def predict_hepatitis():
    files = open('predict/hepatitsC/hepat.pkl', 'rb')
    classifier = pickle.load(files)
    files.close()
    if request.method == "POST":
        Age = int(request.form['Age'])
        gender = request.form['gender']
        if gender == 'Male':
            gender = 1
        else:
            gender = 0
        asp = int(request.form['asp'])
        bil = int(request.form['bil'])
        acety = int(request.form['acety'])
        Creatinine = int(request.form['cet'])
        gama = int(request.form['gama'])
        alkaline = int(request.form['alkaline'])
        cholesterol = int(request.form['cholesterol'])
        albumin = int(request.form['albumin'])
        proteins = int(request.form['proteins'])
        Transaminase = int(request.form['Transaminase'])
        pred = classifier.predict([[Age, gender, asp, bil, acety, Creatinine,
                                    gama, alkaline, cholesterol, albumin, proteins, Transaminase]])
        if pred == 0:
            return render_template('pred_hepatits.html', text="You are not infected with Hepatitis C")
        else:
            return render_template('pred_hepatits.html', text='You are infected with Hepatits C')
    else:
        return render_template('hepatitis.html')

'''

---------------------------------------------------------------------------------------------------------------------------|

---------------------------------------------||   login info       ||------------------------------------------------

---------------------------------------------------------------------------------------------------------------------------


'''
# login information
'''
@app.route('/login')
def login():
    return render_template("login.html")'''



''''
=================================================================================================================

                                        1.Register of Doctors

================================================================================================================
'''
@app.route('/login/register', methods=["POST", "GET"])
def register():
    username = None
    email = None
    aadhar=None
    dept=None
    password_hash = None
    form = UserForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = users( username=form.username.data,
                          email=form.email.data,aadhar=form.aadhar.data,dept=form.dept.data, password=form.password_hash.data)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.email.data = ""
        form.aadhar.data = ""
        form.password_hash.data =""
        form.dept.data=""
        flash("user added sucessfully")

    our_users = users.query.order_by(aadhar)
    return render_template("add_user.html", form=form, username=username, email=email,aadhar=aadhar,password_hash=password_hash, dept=dept,our_users=our_users)


'''class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    date_add = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify(self, password):
        return check_password_hash(self.password_hash, password)
'''

class UserForm(FlaskForm):
    
    username = StringField("UserName", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    aadhar= StringField("aadhar", validators=[DataRequired()])
    password_hash = PasswordField("password", validators=[DataRequired(), EqualTo(
        'password_hash2', message="password should match")])
    password_hash2 = PasswordField(
        "confirm password", validators=[DataRequired()])
    dept=StringField("department",validators=[DataRequired()])
    submit = SubmitField("submit")


@app.before_first_request
def create_tables():
    db.create_all()
    mysql_db.create_all()

''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                     2.deletion of prescription

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delte = users.query.get_or_404(id)
    username = None
    form = UserForm()
    try:
        mysql_db.session.delete(user_to_delte)
        mysql_db.session.commit()
        flash("Delete User Sucessfully")
        #our_users = users.query.order_by(users.aadhar)
        return render_template("add_user.html", form=form, username=username )
    except:
        flash("there was a problem deleting")
        return render_template("add_user.html", form=form,username=username)
''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                     3. prescription

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''

# doctor prescription module
class Doctor(mysql_db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    patient_id=db.Column(db.String(20),nullable=False)
    Bp = db.Column(db.Integer, nullable=False)
    Temp = db.Column(db.Integer, nullable=False)
    invest = db.Column(db.String(200), nullable=False)
    prescription = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(200))
    poster_id=mysql_db.Column(mysql_db.Integer,db.ForeignKey('users.id'))


class DocForm(FlaskForm):
    title = StringField("patient name", validators=[DataRequired()])
    patient_id=StringField("patient id",validators=[DataRequired()])
    Bp = IntegerField("Blood pressure", validators=[DataRequired()])
    Temp = IntegerField("Temperature", validators=[DataRequired()])
    invest = StringField("Symptoms and investigations", validators=[
                         DataRequired()], widget=TextArea())
    prescription = StringField("Prescription", validators=[
                               DataRequired()], widget=TextArea())
    slug = StringField("severity", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/prescribe', methods=["GET", "POST"])
def add_prescribe():
    form = DocForm()
    if form.validate_on_submit():
        use=session['username']
        user=users.query.filter_by(username=use).first()
        post = Doctor(title=form.title.data,patient_id=form.patient_id.data ,Bp=form.Bp.data, Temp=form.Temp.data,
                      invest=form.invest.data, prescription=form.prescription.data, slug=form.slug.data,poster_id=user.id)
        form.title.data = ""
        form.patient_id.data=""
        form.Bp.data = ""
        form.Temp.data = ""
        form.invest.data = ""
        form.prescription.data = ""
        form.slug.data = ""
        mysql_db.session.add(post)
        mysql_db.session.commit()
        flash("patient record success")
    return render_template("doctor_post.html", form=form)
# showing prescribe


@app.route('/login/patient/posts', methods=["GET", "POST"])
def doctor_posts():
    use=session["username"]
    user=users.query.filter_by(username=use).first()
    posts = Doctor.query.filter_by(poster_id=user.id)
    return render_template("doctor_posts.html", posts=posts)


@app.route('/posts/<int:id>')
def view_detail(id):
    
    post = Doctor.query.get_or_404(id)
    return render_template("detail_post.html", post=post)

@app.route('/login/doctor/dashboard/<int:id>')
def view_patient_prescriptions(id):
    post = Doctor.query.filter_by(patient_id=id).all()
    return render_template("older_prescriptions.html", posts=post)


# editing the posts


@app.route('/posts/edit/<int:id>', methods=['POST', 'GET'])
def edit_posts(id):
    post = Doctor.query.get_or_404(id)
    form = DocForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.patient_id=form.patient_id.data
        post.Bp = form.Bp.data
        post.Temp = form.Temp.data
        post.invest = form.invest.data
        post.prescription = form.prescription.data
        post.slug = form.slug.data
        mysql_db.session.add(post)
        mysql_db.session.commit()
        flash("posts has been updated")
        return redirect(url_for('doctor_posts',id=post.id))
    form.title.data = post.title
    form.Bp.data = post.Bp
    form.patient_id.data=post.patient_id
    form.Temp.data = post.Temp
    form.invest.data = post.invest
    form.prescription.data = post.prescription
    form.slug.data = post.slug
    return render_template("edit_doc.html", form=form)

# delete the posts


@app.route('/posts/delete<int:id>')
def delete_post(id):
    post_to_delete = Doctor.query.get_or_404(id)
    try:
        mysql_db.session.delete(post_to_delete)
        mysql_db.session.commit()

        flash("Record deleted")
        posts = Doctor.query.order_by(Doctor.date)
        return render_template("doctor_posts.html", posts=posts)

    except:
        flash("Unable to delete the Record")
        posts = Doctor.query.order_by(Doctor.date)
        return render_template("doctor_posts.html", posts=posts)
''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                    4.Login of Doctors

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("submit")
class users(mysql_db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    aadhar = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    dept=db.Column(db.String(20),nullable=False)
    posts=db.relationship('Doctor',backref='poster')
   

    def __init__(self, username, email, aadhar, password,dept):
        self.username = username
        self.email = email
        self.aadhar = aadhar
        self.dept=dept
        self.password = password
    def get_id(self):
            return self.id
    def is_active(self):
            return self.is_active
    def activate_user(self):
            self.is_active = True         
    def get_username(self):
            return self.username
    def get_urole(self):
            return self.urole
   
@app.route('/login', methods=['POST', 'GET'])
def login_users():
    return render_template('login_user.html')

''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


                                    Doctor login Function

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=+

'''
'''
@app.route('/login/doctor',methods=["POST",'GET'])
def login_doctor():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        session['username']=request.form['username']
        session['password']=request.form['password']
        user=users.query.filter_by(username=username).first()
        if user:
            if password==user.password:
                login_user(user)
                flash("login sucessfull")
                #posts = Doctor.query.filter_by(poster_id=user.id)
                return redirect(url_for('user_dash'))
                #return render_template('user_dash.html',user=user,posts=posts)
            else:
                flash("username or password is invalid")
                return render_template("login_user.html")
        else:
            flash("user not found") 
            return render_template("login_user.html")
    return render_template("login_user.html")

'''


@app.route('/login/users',methods=["POST","GET"])
def login_pro():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        role=request.form['role']
        session['username']=request.form['username']
        session['password']=request.form['password']
        session['role']=request.form['role']
        if role=="Doctor":
            user=users.query.filter_by(username=username).first()
            if user:
                if password==user.password:
                    login_user(user)
                    flash("login sucessfull")
                    #posts = Doctor.query.filter_by(poster_id=user.id)
                    return redirect(url_for('user_dash'))
                    #return render_template('user_dash.html',user=user,posts=posts)
                else:
                    flash("username or password is invalid")
                    return render_template("login_user.html")
            else:
                flash("user not found") 
                return render_template("login_user.html")
        else:
            patient_i=patient.query.filter_by(username=username).first()
            if patient_i:
                if password==patient_i.password:
                    login_user(patient_i)
                    flash("login sucessfull")
                            #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==current_user.patient_id).distinct()
                            #appo=appoint.query.filter_by(patient_id=current_user.patient_id).all()             
                    
                        #posts=mysql_db.session.query(Doctor).join(patient).filter(Doctor.patient_id==current_user.patient_id).unique().all()
                    return redirect(url_for('patient_dashboard'))
                else:
                    flash("username or password is invalid")
                    return render_template("login_user.html")
            
            else:
                flash("user not found")    
                return render_template('login_user.html')
    return render_template('login_user.html')




''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                     Patient Login function

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
'''
@app.route('/login/patient',methods=["POST",'GET'])
def login_patient():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        user=patient.query.filter_by(username=username).first()
        if user:
            if password==users.password:
                login_user(user)
                flash("login sucessfull")
                        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==current_user.patient_id).distinct()
                        #appo=appoint.query.filter_by(patient_id=current_user.patient_id).all()             
                
                    #posts=mysql_db.session.query(Doctor).join(patient).filter(Doctor.patient_id==current_user.patient_id).unique().all()
                return redirect(url_for('patient_dashboard'))
            else:
                flash("username or password is invalid")
                return render_template("login_patient.html")
        
        else:
            flash("user not found")    
            return render_template('login_patient.html')
    return render_template('login_patient.html')
'''
@app.route('/logout',methods=["POST","GET"])
@login_required
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for('login_pro'))
'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                                            doctor dashboard


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
@app.route('/login/doctor/dashboard', methods=['POST', 'GET'])
@login_required
def user_dash():
    use=session["username"]
    user=users.query.filter_by(username=use).first()
    #user_1=users.query.filter_by(username=use)
    posts = Doctor.query.filter_by(poster_id=user.id).all()
    appointments=appoint.query.filter_by(doctor_id=user.aadhar)

    appo=appoint.query.filter_by(doctor_id=user.aadhar).first()
    #pat=Doctor.query.filter_by(patient_id=appointments.patient_id).first()
    #second=patient.query.filter_by(patient_id=appo.patient_id)

    date=datetime.now()

    #return render_template("user_dash.html",user=user,posts=posts,appointments=appointments,appoin=appo,boo=pat,sec=sec)
    return render_template("user_dash.html",appointments=appointments,user=user,posts=posts,date=date,appo=appo)
'''===anonymus class==='''
class AnonymousUser(AnonymousUserMixin):
    id=None
'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                                            Login views


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.anonymous_user=AnonymousUser
login_manager.login_view = 'login_pro'
@login_manager.user_loader
def user_loader(id):
        if patient.query.get(id):
            return patient.query.get(id)
            
        elif users.query.get(id):
           return users.query.get(id)
        else:
            pass
 

''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                     patient Registeration

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
@app.route('/login/patient/patient_register',methods=["POST","GET"])
def register_patient():
    if request.method == 'POST':
        name=request.form['name']
        username=request.form['username']
        id=request.form['validid']
        gender=request.form['gender']
        email=request.form['email']
        password=request.form['pswd']
        cr_password=request.form['pswd1']
        if password==cr_password:
            flash("matched password")
            post=patient(name=name,username=username,gender=gender,email=email,patient_id=id,password=password)
            mysql_db.session.add(post)
            mysql_db.session.commit()
            #=patient_dashboard(username)
            return render_template("patient_dashboard.html")
        else:
            flash("entered password doesn't match with confirm password")
            return render_template("patient_register.html")
    return render_template("patient_register.html")
''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                    Patient Database

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''  
class patient(mysql_db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    username=db.Column(db.String(20),nullable=False,unique=True)
    patient_id=db.Column(db.String(20),nullable=False,unique=True)
    gender=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(30),nullable=False,unique=True)
    password=db.Column(db.String(20),nullable=False)
   
    def __init__(self, name,username, email,patient_id, gender,password):
        self.username = username
        self.name=name
        self.email = email
        self.patient_id= patient_id
        self.gender=gender
        self.password = password
    def get_id(self):
            return self.id
    def is_active(self):
            return self.is_active
    def activate_user(self):
            self.is_active = True         
    def get_username(self):
            return self.username
    def get_urole(self):
            return self.urole

'''
@app.route('/login/patient',methods=['POST','GET'])
def login_patient():
    return render_template('login_patient.html')

@app.route('/login//dashboard',methods=["POST","GET"])
@login_required
def after_login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        user=patient.query.filter_by(username=username).first()
        if user:
            if password==user.password:
                login_user(user)
                flash("login sucessfull")
                posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==current_user.patient_id).distinct()
                appo=appoint.query.filter_by(patient_id=current_user.patient_id).all()             
               
                #posts=mysql_db.session.query(Doctor).join(patient).filter(Doctor.patient_id==current_user.patient_id).unique().all()
                return render_template('patient_dashboard.html',posts=posts,appoint=appo)
            else:
                flash("username or password is invalid")
                return render_template("login_patient.html")
    
        else:
            flash("user not found")    
    return render_template('login.html')
'''
@app.route('/login/register')
def home_user():
    return render_template('register.html')
#creating a database for appointments storage

''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=

                                       Appointment Database
                                    
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
class appoint(mysql_db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id=db.Column(db.String(20),nullable=False)
    patient_id=db.Column(db.String(20),nullable=False)
    dept=db.Column(db.String(20),nullable=False)
    doctor_name=db.Column(db.String(30),nullable=False)
    time=db.Column(db.DateTime)
    patient_name=db.Column(db.String(20),nullable=False)
    file_name=db.Column(db.String(100),nullable=True)
    audio=db.Column(db.String(100),nullable=True)

#  patient dashboard development
''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                     Appoints according to Department

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''

@app.route('/login/patient/cardio',methods=["POST","GET"])
def heart_appointment():
    if request.method == 'POST':
       
        doctor_id=request.form['doctor_id']
        date_time=request.form['date']
        doctor_name=users.query.filter_by(aadhar=doctor_id).first()
        patient_id=current_user.patient_id
        dept=doctor_name.dept
        patient_name=current_user.name
        audio_file=request.form['invest']
        file_name=request.files['imageinfected']

        pic_filename=secure_filename(file_name.filename)
        pic_name=str(uuid.uuid1())+"-"+pic_filename
        saver=request.files['imageinfected']
        file_name=pic_name

        saver.save(os.path.join(app.config['Upload_Folder'],pic_name))
        entry=appoint(doctor_id=doctor_id,file_name=file_name,audio=audio_file,patient_id=patient_id,doctor_name=doctor_name.username,dept=dept,time=date_time,patient_name=patient_name)
        mysql_db.session.add(entry)
        mysql_db.session.commit()
        user="ok"
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==current_user.patient_id).distinct()
        #appo=appoint.query.filter_by(patient_id=current_user.patient_id).all()
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==patient_id).distinct()
        flash(" appointment Booked sucessfully")
        
       
    return render_template('heart_appointment.html')


@app.route('/login/patient/neuro',methods=["POST","GET"])
def neuro_appointment():
    if request.method=="POST":
        doctor_id=request.form['doctor_id']
        date_time=request.form['date']
        doctor_name=users.query.filter_by(aadhar=doctor_id).first()
        patient_id=current_user.patient_id
        patient_name=current_user.name
        deptartment="Nuerology"
        name=doctor_name.username
        audio_file=request.form['invest']
        file_name=request.files['imageinfected']
        
        pic_filename=secure_filename(file_name.filename)
        pic_name=str(uuid.uuid1())+"-"+pic_filename
        saver=request.files['imageinfected']
        file_name=pic_name
        saver.save(os.path.join(app.config['Upload_Folder'],pic_name))
       


        

        
        entrys=appoint(doctor_id=doctor_id,patient_id=patient_id,file_name=file_name,audio=audio_file,doctor_name=name,dept=deptartment,time=date_time,patient_name=patient_name)
        mysql_db.session.add(entrys)
        mysql_db.session.commit()
       
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==current_user.patient_id).distinct()
        #appo=appoint.query.filter_by(patient_id=current_user.patient_id).all()
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==patient_id).distinct()
        flash(" appointment Booked sucessfully")
        
    return render_template('neuro_appointment.html',user="ok") 

    
@app.route('/login/patient/general',methods=["POST","GET"])
def general_appointment():
    if request.method=="POST":
        doctor_id=request.form['doctor_id']
        date_time=request.form['date']
        doctor_name=users.query.filter_by(aadhar=doctor_id).first()
        patient_id=current_user.patient_id
        patient_name=current_user.patient_name
        dept=doctor_name.dept
        name=doctor_name.username
        audio_file=request.form['invest']
        pic_filename=secure_filename(file_name.filename)
        pic_name=str(uuid.uuid1())+"-"+pic_filename
        saver=request.files['imageinfected']
        file_name=pic_name

        saver.save(os.path.join(app.config['Upload_Folder'],pic_name))
        entrys=appoint(doctor_id=doctor_id,patient_id=patient_id,audio=audio_file,file_name=file_name,doctor_name=name,dept=dept,time=date_time,patient_name=patient_name)
        mysql_db.session.add(entrys)
        mysql_db.session.commit()
        user="ok"
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==current_user.patient_id).distinct()
        #appo=appoint.query.filter_by(patient_id=current_user.patient_id).all()
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==patient_id).distinct()
        flash(" appointment Booked sucessfully")
    return render_template('gen_appointment.html') 
@app.route('/login/patient/eye',methods=["POST","GET"])
def eye_appointment():
    if request.method=="POST":
        doctor_id=request.form['doctor_id']
        date_time=request.form['date']
        doctor_name=users.query.filter_by(aadhar=doctor_id).first()
        patient_id=current_user.patient_id
        patient_name=current_user.patient_name
        dept=doctor_name.dept
        name=doctor_name.username
        audio_file=request.form['invest']
        pic_filename=secure_filename(file_name.filename)
        pic_name=str(uuid.uuid1())+"-"+pic_filename
        saver=request.files['imageinfected']
        file_name=pic_name

        saver.save(os.path.join(app.config['Upload_Folder'],pic_name))
        entrys=appoint(doctor_id=doctor_id,patient_id=patient_id,audio=audio_file,file_name=file_name,doctor_name=name,dept=dept,time=date_time,patient_name=patient_name)
        mysql_db.session.add(entrys)
        mysql_db.session.commit()
        user="ok"
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==current_user.patient_id).distinct()
        #appo=appoint.query.filter_by(patient_id=current_user.patient_id).all()
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==patient_id).distinct()
        flash(" appointment Booked sucessfully")
    return render_template('opth_appointment.html')
@app.route('/login/patient/child',methods=["POST","GET"])
def child_appointment():
    if request.method=="POST":
        doctor_id=request.form['doctor_id']
        date_time=request.form['date']
        doctor_name=users.query.filter_by(aadhar=doctor_id).first()
        patient_id=current_user.patient_id
        patient_name=current_user.patient_name
        dept=doctor_name.dept
        name=doctor_name.username
        audio_file=request.form['invest']
        pic_filename=secure_filename(file_name.filename)
        pic_name=str(uuid.uuid1())+"-"+pic_filename
        saver=request.files['imageinfected']
        file_name=pic_name

        saver.save(os.path.join(app.config['Upload_Folder'],pic_name))
        entrys=appoint(doctor_id=doctor_id,patient_id=patient_id,audio=audio_file,file_name=file_name,doctor_name=name,dept=dept,time=date_time,patient_name=patient_name)
        mysql_db.session.add(entrys)
        mysql_db.session.commit()
        user="ok"
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==current_user.patient_id).distinct()
        #appo=appoint.query.filter_by(patient_id=current_user.patient_id).all()
        #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==patient_id).distinct()
        flash(" appointment Booked sucessfully")
    return render_template('pedia_appointment.html')
 
''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                     2.deletion of appointment

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
@app.route('/login/patient/delete/<int:id>')
def delete_appointment(id):
    user_to_delte = appoint.query.get_or_404(id)
    try:
        mysql_db.session.delete(user_to_delte)
        mysql_db.session.commit()
        flash("Deleted the appointmnet")
        #our_users = users.query.order_by(users.aadhar)
        return redirect(url_for('patient_dashboard'))
    except:
        flash("there was a problem  while deleting appointment")
        return redirect(url_for('patient_dashboard'))
@app.route('/login/doctor/delete/<int:id>')
def delete_appointment_doctor(id):
    user_to_delte = appoint.query.get_or_404(id)
    try:
        mysql_db.session.delete(user_to_delte)
        mysql_db.session.commit()
        flash("Deleted the appointmnet")
        #our_users = users.query.order_by(users.aadhar)
        return redirect(url_for('user_dash'))
    except:
        flash("there was a problem  while deleting appointment")
        return redirect(url_for('user_dash'))
@app.route('/login/doctor/dashboard/prescription/<int:id>',methods=["POST","GET"])
def write_doctor_prescription(id):
    #ashboard/prescription/123?id2=3
    patients_list=patient.query.filter_by(patient_id=id).all()
   
    id2=request.args.get('id2',type=str,default='')
    id3=request.args.get('id3',type=str,default='')
    ap_table=appoint.query.filter_by(id=id3)
    appo=appoint.query.filter_by(file_name=id2)


   
    
    return render_template('write_doc_prescription.html',elem=patients_list,photo=appo,symp=ap_table)
'''
sample for two id from same url


@app.route('/createcm')
def createcm():
    summary  = request.args.get('summary', type=str ,default='')
    change  = request.args.get('change',type=str , default='')

'''
@app.route('/login/doctor/dashboard/prescription/doctor/<int:id>',methods=["POST","GET"])
def prescriptions_short(id):
    ids=patient.query.filter_by(patient_id=id).all()
    us="ok";
    if request.method=="POST":
        temp=request.form['temp']
        bp=request.form['bp']
        invest=request.form['invest']
        prescription=request.form['prescription']
        
        use=session["username"]
        slug=use
        user=users.query.filter_by(username=use).first()
        
        for i in ids:
            name=i.name
            patient_id=i.patient_id
        details=Doctor(title=name,patient_id=patient_id,Bp=bp, Temp=temp,
                      invest=invest, prescription=prescription, slug=slug,poster_id=user.id)
        mysql_db.session.add(details)
        mysql_db.session.commit()
    return render_template('write_doc_prescription.html')


@app.route('/login/doctor/dashboard/prescription/doctor/view_photo_detail/<string:id4>',methods=["POST","GET"])
def view_photo_detail(id4):
    appo=appoint.query.filter_by(file_name=id4)
    return render_template("view_photo_detail.html",photo=appo)

''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                     3.Patient Dashboard

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
@app.route('/login/patient/dashboard',methods=["POST","GET"])
@login_required
def patient_dashboard():
    #posts=mysql_db.session.query(Doctor,patient).filter(Doctor.patient_id==current_user.patient_id).distinct()
    posts=Doctor.query.filter_by(patient_id=current_user.patient_id)
    appo=appoint.query.filter_by(patient_id=current_user.patient_id).all()
    return render_template('patient_dashboard.html',posts=posts,appoint=appo)
   

@app.route('/login/patient/dashbord/<int:id>',methods=["POST","GET"])
def view_doctor_details(id):
    use=users.query.filter_by(id=id)
    return render_template("doctor_details.html",use=use)
"""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                                        chatbot


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

limiter = Limiter(app, key_func = get_remote_address)
# Comment out @app.get and index_get() if you are using CORS(app) for standalone frontend and uncomment all other commented lines
@app.route("/login/patient/dashboard/predicts",methods=["POST","GET"])
def predict_chatbot():
    if request.method=="POST":
        text = request.form['input_text']
        if len(text) > 100:
             message = {"answer": "I'm sorry, your query has too many characters for me to process. If you would like to speak to a live agent, say 'I would like to speak to a live agent'"}
             return jsonify(message)
        response = get_response(text)
        message = {"answer": response}
        return jsonify(message)
    return render_template('base_chatbot.html')

''''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


                                    main
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''

if __name__ == '__main__':
    
    app.run(debug=True)
