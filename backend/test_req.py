import requests
data = {"intersection_id": "int_1", "lanes": {"N": 10, "S": 5, "E": 2, "W": 8}, "pedestrian": False}
res = requests.post("http://127.0.0.1:8000/traffic/", json=data)
print(res.status_code)
print(res.json())
