from flask import Flask,render_template,request
import pickle

from sympy import re
model=pickle.load(open('stroke.pkl','rb'))
app=Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    return render_template('stroke.html')
@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=='POST':
        gender=request.form['gender']
        if gender=='Male':
            gender=1
        else:
            gender=0
        Age=int(request.form['Age'])
        bp=request.form['bp']
        if bp=='Yes':
            bp=1
        else:
            bp=0
        heart=request.form['heart']
        if heart=='Yes':
            heart=0
        else:
            heart=1
        married=request.form['married']
        if married=='Yes':
            married=1
        else:
            married=0
        work=request.form['work']
        if work=='never wroked':
            work=1
        elif work=='private':
            work=2
        elif work=='self employed':
            work=3
        elif work=='childern':
            work=4
        else:
            work=0
        house=request.form['house']
        if house=='Urban Housing':
            house=1
        else:
            house=0
        glucose=int(request.form['glucose'])
        bmi=int(request.form['bmi'])
        smoking=request.form['smoking']
        if smoking=='Used to Smoke':
            smoking=1
        elif smoking=='Never Smoked':
            smoking=2
        elif smoking=='Smokes':
            smoking=3
        else:
            smoking=0
        pred=model.predict([[gender,Age,bp,heart,married,work,house,glucose,bmi,smoking]])
        if pred==0:
            return render_template('pred.html',text='You will never have a stroke in the near future,maintain good health and diet.')
        else:
            return render_template('pred.html',text='You may have stroke in the near future Please take precautions and lead a stress free life as possible.')
    else:
        return render_template('stroke.html')
if __name__=='__main__':
    app.run(debug=True)

