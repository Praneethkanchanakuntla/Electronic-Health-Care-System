
from flask import Flask,render_template,request
import pickle
model=pickle.load(open('Heart.pkl','rb'))
app=Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    return render_template('heart.html')
@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=='POST':
        Age=int(request.form['Age'])
        gender=request.form['gender']
        if gender=="Male":
            gender=0
        else:
            gender=1
        cpain=request.form['cpain']
        if cpain=="Typical angina":
            cpain=0
        elif cpain=='Atypical Angina':
            cpain=1
        elif cpain=='Non-Anginal Pain':
            cpain=2
        else:
            cpain=3
        Bloodp=int(request.form['BP'])
        Cholestoral=int(request.form['Cholestoral'])
        sugar=request.form['sugar']
        if sugar=="Greater 120":
            sugar=1
        else:
            sugar=0
        ecg=request.form['ecg']
        if ecg=="Normal":
            ecg=0
        elif ecg=="ST-T wave normality":
            ecg=1
        else:
            ecg=2
        heartrate=int(request.form['heartrate'])
        prev=float(request.form['prev'])
        slope=int(request.form['slope'])
        vessels=int(request.form['vessels'])
        stress=int(request.form['stress'])
        excercise=request.form['excercise']
        if excercise=='yes':
            excercise=1
        else:
            excercise=0
        pred=model.predict([[Age,gender,cpain,Bloodp,Cholestoral,sugar,ecg,heartrate,prev,slope,vessels,stress,excercise]])
        if pred==0:
            return render_template('pred.html',text='You will never have heart attack in near future,maintain proper diet and excercise')
        else:
            return render_template('pred.html',text="You are predicted to have a Heart attack in near future, please consult doctor , take precautionary steps , take medications ")
    else:
        return render_template('heart.html')
if __name__=='__main__':
    app.run(debug=True)



