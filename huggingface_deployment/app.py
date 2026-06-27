import pickle
import datetime
import pandas as pd
import numpy as np
import gradio as gr

# Load trained model
with open("temperature_predictor.pkl", "rb") as f:
    model = pickle.load(f)

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
        temp = pred  # recursive

    return values

# Gradio interface
def api(temp, humidity, n):
    predictions = predict_next_n_hours(temp, humidity, int(n))
    return {"predictions": predictions}

demo = gr.Interface(
    fn=api,
    inputs=[
        gr.Number(label="Current Temperature"),
        gr.Number(label="Current Humidity"),
        gr.Number(label="N Hours Ahead")
    ],
    outputs="json",
    title="Temperature Predictor",
    description="Predict future temperature for next N hours."
)

if __name__ == "__main__":
    demo.launch()
