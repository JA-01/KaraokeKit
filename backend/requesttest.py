import requests
import json

url = 'http://localhost:5000/lyrics'
data = {
    "text": "audio.mp3"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
