from flask import Flask,request,jsonify
from datetime import datetime
from database_central_system import DatabaseCentralSystem
from BookingManager import BookingManager
from user import user
from confirmation import Reservations
from PaymentMethod import Payment
from confirmation_number import confirmation_number

app=Flask(__name__)

db=DatabaseCentralSystem(host='localhost',user='root',password='jaypatel',database='hotel')

@app.route('/rooms', methods=['GET'])
def get_all_rooms():
    conn=db.get_connection()
    if not conn:
       return None
    try:
        cursor=conn.cursor(dictionary=True)
        cursor,execute("select * from rooms")
        rooms=cursor.fetchall()
        return jsonify(rooms)
  finally:
      cursor.close()
      conn.close()

@app.route('/rooms/available', methods=['GET'])
def is_available():
    conn=db.get_connection()
    if not conn:
       return None
    try:
        cursor=conn.cursor(dictionary=True)
        cursor,execute("select * from rooms where available = 1")
        rooms=cursor.fetchall()
        return jsonify(rooms)
    finally:
       cursor.close()
       conn.close()

@app.route('/booking', methods=['POST'])
def create_booking():
    data=request.json
    required = ['name', 'email', 'room_id', 'start_date', 'end_date']

    conn = db_system.get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        user = user(conn)
        user_id = user.create_user(data['name'], data['email'])
        cursor.execute("SELECT * FROM rooms WHERE id = %s", (data['room_id'],))
        room_data = cursor.fetchone()
        if not room_data:
            return jsonify({'error': 'Room not found'})
        room = Room(
            room_number=room_data['id'],
            room_type=room_data['room_type'],
            price_per_night=room_data['price_per_night']
        )
        booking_manager = BookingManager()
        booking_manager.rooms = [room]
        booking_manager.users = [{'user_id': user_id}]  
        start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()

        success = booking_manager.create_booking(user_id, room.room_number, start_date, end_date)
        if not success:
            return jsonify({'error': 'Booking failed'})

        number_of_nights = (end_date - start_date).days
        total_price = number_of_nights * room.price_per_night
        cursor.execute("""
            INSERT INTO bookings (user_id, room_id, start_date, end_date)
            VALUES (%s, %s, %s, %s)
        """, (user_id, room.room_number, start_date, end_date))
        booking_id = cursor.lastrowid

        cursor.execute("UPDATE rooms SET available = 0 WHERE id = %s", (room.room_number,))

        reservation_manager = ReservationManager(conn)
        confirmation_number = generate_confirmation_number()
        reservation_manager.create_reservation(booking_id, confirmation_number)

        conn.commit()
        return jsonify({
            'message': 'Booking successful',
            'booking_id': booking_id,
            'confirmation_number': confirmation_number
        })

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/booking/cancel', methods=['POST'])
def cancel_booking():
    data = request.json
    if 'booking_id' not in data:
        return jsonify({'error': 'Missing booking_id'})

    booking_id = data['booking_id']
    conn = db_system.get_connection()
    if not conn:
        return None

    try:
        reservation_manager = ReservationManager(conn)
        reservation_manager.cancel_reservation(booking_id)
        conn.commit()
        return jsonify({'message': f'Booking {booking_id} cancelled successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})
    finally:
        conn.close()

@app.route('/rooms/search', methods=['GET'])
def search_rooms():
    room_type = request.args.get('type')
    max_price = request.args.get('max_price')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = db_system.get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM rooms WHERE available = 1"
        conditions = []
        params = []

        if room_type:
            conditions.append("room_type = %s")
            params.append(room_type)
        if max_price:
            conditions.append("price_per_night <= %s")
            params.append(float(max_price))
        if start_date and end_date:
            conditions.append("""
                id NOT IN (
                    SELECT room_id FROM bookings
                    WHERE (start_date < %s AND end_date > %s)
                )
            """)
            params.extend([end_date, start_date])

        if conditions:
            query += " AND " + " AND ".join(conditions)

        cursor.execute(query, params)
        results = cursor.fetchall()
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True)
        
