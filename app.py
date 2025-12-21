
from flask import Flask,render_template,request,jsonify
import joblib,numpy as np
app=Flask(__name__)
model=joblib.load('model/aqi_model.pkl')
def cat(a):
 return('Good','Healthy') if a<=50 else ('Moderate','Acceptable') if a<=100 else ('Poor','Unhealthy')
@app.route('/')
def h(): return render_template('index.html')
@app.route('/predict',methods=['POST'])
def p():
 d = request.json
 features = [float(d['pm25']), float(d['pm10']), float(d['no2']), float(d['so2']), float(d['co'])]
 a=model.predict([features])[0]
 c,h=cat(a)
 return jsonify(aqi=round(a,2),category=c,health=h)
app.run(debug=True)
