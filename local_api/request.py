import requests

API_URL = "https://YOUR_USERNAME-temperature-predictor.hf.space/gradio_api/call/predict/"

# Input data: [temperature, humidity, n_hours]
data = {"data": [25.0, 70.0, 6]}

# Some requests get blocked without a User-Agent header
headers = {
    "User-Agent": "python-requests/2.31.0"
}

response = requests.post(API_URL, headers=headers, json=data)

# Check response status first
print("Status code:", response.status_code)
print("Response text:", response.text)

# Only attempt to parse JSON if status code is 200
if response.status_code == 200:
    print(response.json())
else:
    print("Request failed. See response text above.")
