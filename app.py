from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# URL for each microservice
SERVICES = {
    "guest_service": os.getenv("GUEST_SERVICE_URL", "http://guest_service:5001"),
    "reservation_service": os.getenv("RESERVATION_SERVICE_URL", "http://reservations_service:5002"),
    "review_service": os.getenv("REVIEW_SERVICE_URL", "http://hotel_reviews:5003"),
    "room_service": os.getenv("ROOM_SERVICE_URL", "http://room_services:5004"),
}

# Hjælpe function to forward the request
def forward_request(service, endpoint, method="GET", data=None):
    url = f"{SERVICES[service]}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:  # GET
            response = requests.get(url)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

############  Define routes for each service  ############

# Guests Service routes
@app.route("/api/guests", methods=["GET", "POST"])
def guests():
    if request.method == "POST":
        return forward_request("guest_service", "/guests", method="POST", data=request.json)
    return forward_request("guest_service", "/guests")

@app.route("/api/guests/<int:guest_id>", methods=["GET", "PUT", "DELETE"])
def guest(guest_id):
    if request.method == "PUT":
        return forward_request("guest_service", f"/guests/{guest_id}", method="PUT", data=request.json)
    elif request.method == "DELETE":
        return forward_request("guest_service", f"/guests/{guest_id}", method="DELETE")
    return forward_request("guest_service", f"/guests/{guest_id}")

# Reservations Service routes
@app.route("/api/reservations", methods=["GET", "POST"])
def reservations():
    if request.method == "POST":
        return forward_request("reservation_service", "/reservations", method="POST", data=request.json)
    return forward_request("reservation_service", "/reservations")

@app.route("/api/reservations/<int:reservation_id>", methods=["GET", "PUT", "DELETE"])
def reservation(reservation_id):
    if request.method == "PUT":
        return forward_request("reservation_service", f"/reservations/{reservation_id}", method="PUT", data=request.json)
    elif request.method == "DELETE":
        return forward_request("reservation_service", f"/reservations/{reservation_id}", method="DELETE")
    return forward_request("reservation_service", f"/reservations/{reservation_id}")

# Reviews Service routes
@app.route("/api/reviews", methods=["GET", "POST"])
def reviews():
    if request.method == "POST":
        return forward_request("review_service", "/reviews", method="POST", data=request.json)
    return forward_request("review_service", "/reviews")

@app.route("/api/reviews/<int:review_id>", methods=["GET", "PUT", "DELETE"])
def review(review_id):
    if request.method == "PUT":
        return forward_request("review_service", f"/reviews/{review_id}", method="PUT", data=request.json)
    elif request.method == "DELETE":
        return forward_request("review_service", f"/reviews/{review_id}", method="DELETE")
    return forward_request("review_service", f"/reviews/{review_id}")

# Rooms Service routes
@app.route("/api/rooms", methods=["GET", "POST"])
def rooms():
    if request.method == "POST":
        return forward_request("room_service", "/rooms", method="POST", data=request.json)
    return forward_request("room_service", "/rooms")

@app.route("/api/rooms/<int:room_id>", methods=["GET", "PUT", "DELETE"])
def room(room_id):
    if request.method == "PUT":
        return forward_request("room_service", f"/rooms/{room_id}", method="PUT", data=request.json)
    elif request.method == "DELETE":
        return forward_request("room_service", f"/rooms/{room_id}", method="DELETE")
    return forward_request("room_service", f"/rooms/{room_id}")

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
