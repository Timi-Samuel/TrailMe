import requests

BASE_URL = "http://127.0.0.1:5050"  # localhost
id = 1  # Set to whichever checkpoint id you want

# 1. Home
response = requests.get(f"{BASE_URL}/home")
print("Home endpoint:", response.status_code, response.json())

# 2. Add checkpoint
checkpoint_payload = {
    "label": "My Home",
    "image": None,  # If you want to store an image, it should be put here in bytes
    "latitude": -33.9142607,
    "longitude": 18.5191269
}

response = requests.post(f"{BASE_URL}/checkpoint/add", json=checkpoint_payload)
print("Add checkpoint:", response.status_code, response.json())


# 3. Update checkpoint
update_payload = {
    "id": id,
    "label": "My Updated Home",
    "image": None,
    "latitude": -33.9142607,
    "longitude": 18.5191269
}

response = requests.put(f"{BASE_URL}/checkpoint/update", json=update_payload)
print("Update checkpoint:", response.status_code, response.json())

# 4. Get all checkpoints
response = requests.get(f"{BASE_URL}/checkpoint")
print("Get checkpoints:", response.status_code, response.json())

# 5. Get trip details
trip_payload = {
    "id": id,
    "olat": -33.8933,
    "olong": 18.5111,
    "travel_mode": "walk"
}

response = requests.post(
    f"{BASE_URL}/checkpoint/get-trip-details", json=trip_payload)
print("Trip details:", response.status_code, response.json())

# 6. Delete checkpoint
response = requests.delete(f"{BASE_URL}/checkpoint/{id}")
print("Delete checkpoint:", response.status_code, response.json())
