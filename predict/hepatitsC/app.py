from distutils.log import debug
from flask import Flask,render_template,request
import pickle
files=open('hepat.pkl', 'rb')
classifier=pickle.load(files)
files.close();
app=Flask(__name__)
@app.route('/')
def home():
    return  render_template('hepatitis.html')
@app.route('/predict',methods=["POST",'GET'])
def predict():
    if request.method=="POST":
        Age=int(request.form['Age'])
        gender=request.form['gender']
        if gender=='Male':
            gender=1
        else:
            gender=0
        asp=int(request.form['asp'])
        bil=int(request.form['bil'])
        acety=int(request.form['acety'])
        Creatinine=int(request.form['cet'])
        gama=int(request.form['gama'])
        alkaline=int(request.form['alkaline'])
        cholesterol=int(request.form['cholesterol'])
        albumin=int(request.form['albumin'])
        proteins=int(request.form['proteins'])
        Transaminase=int(request.form['Transaminase'])
        pred=classifier.predict([[Age,gender,asp,bil,acety,Creatinine,gama,alkaline,cholesterol,albumin,proteins,Transaminase]])
        if pred==0:
            return render_template('pred.html',text="You are not infected with Hepatitis C")
        else:
            return render_template('pred.html',text='You are infected with Hepatits C')
    else:
        return render_template('hepatitis.html')
if __name__=='__main__':
    app.run(debug=True)