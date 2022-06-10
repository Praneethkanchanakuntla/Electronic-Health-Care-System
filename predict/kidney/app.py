from flask import Flask,render_template,request
import pickle
model=pickle.load(open('kidney.pkl','rb'))
app=Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    return render_template('kidney.html')
@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=='POST':
        Age=int(request.form['Age'])
        Bp=int(request.form['BP'])
        gravity=int(request.form['gravity'])
        albumin=int(request.form['albumin'])
        glucose=int(request.form['glucose'])
        work=request.form['work']
        if work=='Normal':
            work=1
        else:
            work=0
        pus=request.form['puss']
        if pus=='Normal':
            pus=1
        else:
            pus=0
        clumps=request.form['clumps']
        if clumps=='Not present':
            clumps=1
        else:
            clumps=0
        bacteria=request.form['bacteria']
        if bacteria=='Not present':
            bacteria=1
        else:
            bacteria=0
        Blood=int(request.form['Blood'])
        urea=int(request.form['urea'])
        serum=int(request.form['serum'])
        sodium=int(request.form['sodium'])
        potassium=int(request.form['potassium'])
        hemo=int(request.form['hemo'])
        packed=int(request.form['packed'])
        wbc=int(request.form['wbc'])
        rbc=int(request.form['rbc'])
        hypertension=request.form['hypertension']
        if hypertension=='No':
            hypertension=0
        else:
            hypertension=1
        diabetes=request.form['diabetes']
        if diabetes=='No':
            diabetes=0
        else:
            diabetes=1
        coronary=request.form['coronary']
        if coronary=="No":
            coronary=0
        else:
            coronary=1
        appetite=request.form['appetite']
        if appetite=='No':
            appetite=0
        else:
            appetite=1
        pedal=request.form['pedal']
        if pedal=='No':
            pedal=0
        else:
            pedal=1
        anemia=request.form['anemia']
        if anemia=='No':
            anemia=0
        else:
            anemia=1
        pred=model.predict([[Age,Bp,gravity,albumin,glucose,work,pus,clumps,bacteria,Blood,urea,serum,sodium,potassium,hemo,packed,wbc,rbc,hypertension,diabetes,coronary,appetite,pedal,anemia]])
        if pred==0:
            return render_template('pred.html',text="you dont have kindey failure")
        else:
            return render_template('pred.html',text='you will have kidney failure in the near future')
if __name__=='__main__':
    app.run(debug=True)
        