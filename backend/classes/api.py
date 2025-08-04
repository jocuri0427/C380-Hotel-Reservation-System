from flask import flask, request, jsonify
from datetime import date, datetime
from BookingManager import BookingManager
from user import User
from database_central_system import Databasecentralsystem
app = flask(Bookly)
booking_manager=BookingManager()
db=Databasecentralsystem(host="localhost", user="root", password="jaypatel", database="hotel")

def parse_date(date_str):
  return datetime.strptime(date_str, "%Y-%m-%d").date()

app.route("/rooms/available", methods=["GET"])
def available_rooms():
  try:
    rooms=db.rooms_available()
    return jsonify(rooms)
  except Exception as e:
    data=request.json
    try:
      user_Id=int(data["user_id"])
      room_id=int(data["room_id"])
      start_date=parse_date(data["start_date"])
      end_date=parse_date(data["end_date"])
      Booking = booking_manager.create_booking(user_id, room_id, start_date, end_date)
      if Booking:
        return jsonify({"message":"Booking confirmed"})
      else:
        return jsonify({"error": "Booking failed"})
    except Exception as e:
      return jsonify ({"error":str(e)})

app.route("/cancel", methods=["POST"])
def cancel_booking():
  data=request.json
  booking_id=int(data["booking_id"])
  if booking_manager.cancel_booking(booking_id):
    return jsonify({"message: "booking cancelled"})
    else:
    return jsonify({"error": "booking not found"})

    app.route("/reservation", methods=["GET"])
    def reservations():
    try:
    reservations=db.All_reservation()
    return jsonify(reservations)
    except Exception as e:
    return jsonify({"error": str(e)})

    if Bookly=="__main__":
    app.run(debug=True)
