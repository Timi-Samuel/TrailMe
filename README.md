# TrailMe

TrailMe is a lightweight location–tracking and navigation assistant designed for scenarios where you need to remember a physical location — such as a parking spot, a hidden trail point, or any place you want to return to later.
The system lets you **capture your coordinates**, **label the location**, **store an image of the surroundings**, and **later navigate back to it** using step-by-step walking directions powered by Google Maps.

---

## 🚀 Features
### Core Checkpoint Management
* **Add a Checkpoint**
Store a location with label, image, latitude, and longitude.
* **Update a Checkpoint**
Modify existing checkpoints with new data
* **Delete a Checkpoint**
Remove unwanted checkpoints permanently.
* **View all Checkpoints**
Retrieve a list of all stored checkpoint records.

### Navigation + Routing
* Uses Google Maps Routes API.
* Returns:
  * Estimated distance
  * Estimated duration
  * Step-by-step navigation instructions
* Supported travel mode: **Walking**, **Driving**

### Simulated Frontend
A `simulated_frontend.py` script is included to sent requests to all backend routes, acting as a mock client.

---

## 🏗️ Project Structure

```graphql
TrailMe/
│── .git
│── src/
│   ├── database/
│── |    └── checkpoints.db
│   ├── models/
│   │   └── model.py
│   ├── services/
│   │   ├── check_service.py
│   │   ├── custom_exceptions.py
│   │   └── maps_service.py
│   └── main.py
│── tests/
│   └── simulated_frontend.py
│── .env
│── .gitignore
│── LICENSE
│── sample_google_api_response.txt # Used postman to get a json doc just to see what keys and values the google api response gave back
```

---

## 🛠️ Technologies Used
* **Python 3**
* **Flask** - API framework
* **SQLALchemy** - ORM for SQLite database
* **Google Maps Routes API** - for directions and route calculations
* **Postman** – Used to inspect the Google Directions API JSON responses

### Python Libraries
* `requests`
* `os`
* `abc`
* `flask`

---

## 🔌 API Endpoints
### Checkpoint Management
```graphql
| Method | Endpoint             | Description                   |
| ------ | -------------------- | ----------------------------- |
| POST   | `/checkpoint/add`    | Add a new checkpoint          |
| PUT    | `/checkpoint/update` | Update an existing checkpoint |
| DELETE | `/checkpoint/<id>`   | Delete a checkpoint           |
| GET    | `/checkpoint`        | Get all checkpoints           |
```
### Navigation
```graphql
| Method | Endpoint                       | Description                            |
| ------ | ------------------------------ | -------------------------------------- |
| POST   | `/checkpoint/get-trip-details` | Get walking directions to a checkpoint |
```

Example request body:
```python
{
  "id": 1,
  "olat": -33.9150,
  "olong": 18.5200,
  "travel_mode": "WALK" # Or "DRIVE"
}
```

---

## 🧪 Simulated Frontend
Use:
```nginx
python simulated_frontend.py
```

---

## 🔧 Setup Instructions
### 1. Install dependencies
```nginx
pip install -r requirements.txt
```
### 2. Set your Google API key
Create a `.env` file:
```ini
GOOGLE_API_KEY=your_api_key_here
```
### 3. Run the backend
```css
python main.py
```
Backend will start on:
```adruino
http://127.0.0.1:5050

---

## 🌍 Choosing a Frontend (To Be Decided)
TrailMe backend is fully built and ready for any frontend. Possible options include:
* Flutter
* React Native
* Android Studio (Java)

---

## 🛠️ Troubleshooting & Common Pitfalls
### 1. `__init__() takes 1 positional argument but 6 were given`
This happened because the SQLAlchemy `Checkpoint` model was instantiated using **positional arguments**:
```python
checkpoint = Checkpoint(self.__id, self.__label, self.__image, self.__latitude, self.__longitude)
```
SQLAlchemy only worked with keyword arguments and not positional ones.

#### Solution:
```python
checkpoint = Checkpoint(
    id=self.__id,
    label=self.__label,
    image=self.__image,
    latitude=self.__latitude,
    longitude=self.__longitude
)
```

### 2. `'CheckService' object has no attribute 'id'`
This happened because I wrote:
```python
match = session.query(Checkpoint).get(self.id)
```
The issue with this is that I had set `self.__id` to **None** as a default value, and sonce the `/add` endpoint did not send an ID, the query would not be successful.

#### Solution:
```python
match = session.query(Checkpoint).filter_by(
    label=self.__label,
    latitude=self.__latitude,
    longitude=self.__longitude
).first()
```

### 3. Image stored as string instead of bytes
Initially it seemed like the image needed to be converted to bytes by using a helper class.

I later found this unnecessary because images are sent in requests as byes anyway, so I did not need to convert it.

### 4. Google Maps Directions API — Missing `navigationInstruction`
Some steps returned:
```python
i["navigationInstruction"]["instructions"]
```
The issue here was that not all steps have a 'navigationInstruction` value, which caused the program to break.

#### Solution:
```python
instruction = i.get("navigationInstruction", {}).get("instructions", {})
```

