from flask import Flask, request, jsonify
from database_central_system import Databasecentralsystem
from mysql.connector import Error
from confirmation import Confirmation
from loginapi import loginform  # Import login blueprint
# Import registration blueprint
from registerapi import registration_form

app = Flask(__name__)

app.register_blueprint(loginform)  # Register login routes
app.register_blueprint(registration_form)  # Register registration routes

db = Databasecentralsystem()


@app.route('/rooms', methods=['GET'])
def get_all_rooms():
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from rooms")
        rooms = cursor.fetchall()
        return jsonify(rooms)
    except Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/rooms/search', methods=['GET'])
def search_rooms():
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select r.*
                   from rooms r
                   where r.id NOT IN (select b.room_id
                                      from bookings b
                                               JOIN reservations res ON b.id = res.booking_id
                                      where res.status = 'confirmed'
                                        AND (%s < b.check_out AND %s > b.check_in))"""
        cursor.execute(query, (check_in, check_out))
        available_rooms = cursor.fetchall()
        return jsonify(available_rooms)
    except Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/booking', methods=['POST'])
def create_booking():
    data = request.json
    user_id = data.get("user_id")
    room_id = data.get("room_id")
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    payment = data.get("payment", {})
    card_number = payment.get("card_number")
    expiry_date = payment.get("expiry_date")
    card_type = payment.get("card_type")
    amount = payment.get("amount")
    cvv = payment.get("cvv")

    if not payment:
        return jsonify({"error": "payment info"})

    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select b.id
                   from bookings b
                            JOIN reservations r ON b.id = r.booking_id
                   where b.room_id = %s
                     AND r.status = 'confirmed'
                     AND (%s < b.check_out AND %s > b.check_in)"""
        cursor.execute(query, (room_id, check_out, check_in))
        if cursor.fetchone():
            return jsonify({"error": "Room not available"})

        cursor.execute(
            "SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        cursor.execute(
            "INSERT INTO bookings (user_id, room_id, check_in, check_out)VALUES (%s, %s, %s, %s)",
            (user_id, room_id, check_in, check_out))
        booking_id = cursor.lastrowid

        # Correctly insert payment details into the payments table
        cursor.execute("INSERT INTO payments(booking_id, amount, cvv, method) VALUES (%s, %s, %s, %s)",
                       (booking_id, amount, cvv, card_type))
        confirmation = Confirmation.gen_confirmation_number()

        cursor.execute("insert into reservations(booking_id,status,confirmation_number) values (%s,%s,%s)",
                       (booking_id, 'confirmed', confirmation))
        conn.commit()

        return jsonify({'message': 'Booking created', 'booking_id': booking_id, "confirmation_number": confirmation,
                        "room_id": room_id, "check_in": check_in, "check_out": check_out})
    except Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/booking/cancel', methods=['POST'])
def cancel_booking():
    data = request.json
    confirmation = data.get('confirmation_number')

    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select booking_id from reservations where confirmation_number = %s AND status='confirmed'",
                       (confirmation,))
        reservation = cursor.fetchone()
        if not reservation:
            return jsonify({'error': 'wrong number'})

        cursor.execute(
            "update reservations set status='cancelled' where confirmation_number=%s", (confirmation,))
        conn.commit()

        return jsonify({'message': 'booking cancel'})
    except Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/booking/<confirmation_number>', methods=['GET'])
def get_confirmation(confirmation_number):
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT u.name, u.email, b.room_id, b.check_in, b.check_out, r.status, r.confirmation_number
                FROM bookings b
                         JOIN reservations r ON b.id = r.booking_id
                         JOIN users u ON b.user_id = u.id
                WHERE r.confirmation_number = %s \
                """
        cursor.execute(query, (confirmation_number,))
        booking = cursor.fetchone()

        if booking:
            return jsonify(booking)
        else:
            return jsonify({'error': 'Booking not found'})
    except Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/bookings/user/<user_id>', methods=['GET'])
def get_user_bookings(user_id):
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get all bookings for the user with room details
        query = """
            SELECT b.*, r.room_type, r.price, res.status, res.confirmation_number
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            JOIN reservations res ON b.id = res.booking_id
            WHERE b.user_id = %s
            ORDER BY b.check_in DESC
        """
        cursor.execute(query, (user_id,))
        bookings = cursor.fetchall()

        # Format dates and calculate total price
        result = []
        for booking in bookings:
            result.append({
                'id': booking['id'],
                'room_id': booking['room_id'],
                'room_type': booking['room_type'],
                'check_in': booking['check_in'].isoformat(),
                'check_out': booking['check_out'].isoformat(),
                'price_per_night': float(booking['price']) if booking['price'] else 0.0,
                'status': booking['status'],
                'confirmation_number': booking['confirmation_number']
            })

        return jsonify(result)

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/booking/modify', methods=['POST'])
def modify_booking():
    data = request.json
    confirmation_number = data.get('confirmation_number')
    new_check_in = data.get('new_check_in')
    new_check_out = data.get('new_check_out')
    new_room_type = data.get('new_room_type')  # New field

    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Find the original booking ID
        cursor.execute("""
            SELECT b.id FROM bookings b 
            JOIN reservations r ON b.id = r.booking_id 
            WHERE r.confirmation_number = %s
        """, (confirmation_number,))
        booking = cursor.fetchone()

        if not booking:
            return jsonify({'error': 'Booking not found.'}), 404
        booking_id = booking['id']

        # Find an available room of the new type for the new dates
        cursor.execute("""
            SELECT id FROM rooms
            WHERE room_type = %s AND id NOT IN (
                SELECT room_id FROM bookings
                WHERE id != %s AND (%s < check_out AND %s > check_in)
            )
            LIMIT 1
        """, (new_room_type, booking_id, new_check_in, new_check_out))

        available_room = cursor.fetchone()

        if not available_room:
            return jsonify({'error': f'No available "{new_room_type}" for the selected dates.'}), 409

        new_room_id = available_room['id']

        # Update the booking with the new room and dates
        cursor.execute("""
            UPDATE bookings 
            SET room_id = %s, check_in = %s, check_out = %s 
            WHERE id = %s
        """, (new_room_id, new_check_in, new_check_out, booking_id))

        conn.commit()
        return jsonify({'message': 'Booking modified successfully.'})

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# --- NEW FUNCTION ---


@app.route('/reports/all_bookings', methods=['GET'])
def get_all_bookings_report():
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT
                r.confirmation_number,
                u.name AS user_name,
                u.email AS user_email,
                rm.room_number,
                rm.room_type,
                b.check_in,
                b.check_out,
                r.status
            FROM reservations r
            JOIN bookings b ON r.booking_id = b.id
            JOIN users u ON b.user_id = u.id
            JOIN rooms rm ON b.room_id = rm.id
            ORDER BY b.check_in DESC;
        """
        cursor.execute(query)
        report_data = cursor.fetchall()

        # Convert date objects to strings for JSON serialization
        for row in report_data:
            row['check_in'] = row['check_in'].isoformat()
            row['check_out'] = row['check_out'].isoformat()

        return jsonify(report_data)

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
# --- END OF NEW FUNCTION ---


if __name__ == '__main__':
    app.run(debug=True)
