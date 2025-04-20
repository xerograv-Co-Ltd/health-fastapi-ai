# test_request.py
import requests

url = "https://fastapi-analyze-api-production.up.railway.app/analyze"
data = {
    "heart_rate": 84,
    "skin_temp": 33.2,
    "uv_index": 6.5,
    "pm25": 58,
    "humidity": 71
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
