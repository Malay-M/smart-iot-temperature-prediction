from flask import Flask, request, jsonify
import pickle
import datetime
import pandas as pd
import numpy as np


with open("temperature_predictor.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

def predict_next_n_hours(temp, humidity, n=6):
    values = []
    now = datetime.datetime.now()

    for i in range(1, n+1):
        future_time = now + datetime.timedelta(hours=i)
        
        features = {
            "temperature": temp,
            "humidity": humidity,
            "month": future_time.month,
            "day": future_time.day,
            "hour": future_time.hour,
            "minute": future_time.minute,
            "second": future_time.second,
            "day_of_week": future_time.weekday()
        }
        
        X = pd.DataFrame([features])
        pred = model.predict(X)[0]
        pred_rounded = round(float(pred), 1) 
        values.append(pred_rounded)
        temp = pred  
    
    return np.array(values)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    temp = float(data["temp"])
    humidity = float(data["humidity"])
    n = int(data["n"])

    predictions = predict_next_n_hours(temp, humidity, n)

    return jsonify({
        "success": True,
        "predictions": predictions.tolist()
    })

if __name__ == "__main__":
    app.run(debug=True)
