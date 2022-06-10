from django.shortcuts import render
from flask import Flask,render_template,request
import requests
import pickle
app=Flask(__name__)
model=pickle.load(open('diabetes.pkl','rb'))
@app.route('/')
def home():
    return render_template('diabetes.html')
@app.route('/predict',methods=['POST','GET'])
def predict():
    #Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome
    if request.method=='POST':
        Pregnancies=int(request.form['Pregnancies'])
        Glucose=int(request.form['Glucose'])
        BloodPressure=int(request.form['BloodPressure'])
        SkinThickness=int(request.form['SkinThickness'])
        Insulin=int(request.form['Insulin'])
        BMI=int(request.form['BMI'])
        DiabetesPedigreeFunction=float(request.form['DiabetesPedigreeFunction'])
        Age=int(request.form['Age'])
        prediction=model.predict([[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]])
        if prediction==0:
            return render_template('pred.html',text='you dont have diabetes')
        else:
            return render_template('pred.html',text='you have diabetes')
    else:
        pass
if __name__=='__main__':
    app.run(debug=True)

        



