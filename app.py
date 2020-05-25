import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from joblib import load
app = Flask(__name__)
model = pickle.load(open('modelmep.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[int(x) for x in request.form.values()]]
    print(x_test)
    if(x_test[0][12] == 0):
        x_test[0][12]=1
        x_test[0].insert(13,0)
    elif(x_test[0][12] == 1):
        x_test[0][12]=0
        x_test[0].insert(13,1)
    else:
        x_test[0][12]=0
        x_test[0].insert(13,0)
        
    if(x_test[0][14] == 0):
        x_test[0][14]=1
        x_test[0].insert(15,0)
    elif(x_test[0][14] == 1):
        x_test[0][14]=0
        x_test[0].insert(15,1)
    else:
        x_test[0][14]=0
        x_test[0].insert(15,0)
    print(x_test)
    prediction = model.predict(x_test)
    print(prediction)
    output=prediction[0]
    if(output==0):
        s="Non Hazardous State. You are Safe!!"
    else:
        s="Hazardous State. Red Alert!!"
        
    return render_template('index.html', prediction_text='{}'.format(s))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run()
