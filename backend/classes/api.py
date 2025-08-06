from flask import Flask,request,jsonify
from datetime import datetime
from database_central_system import Databasecentralsystem
from BookingManager import BookingManager
from confirmation import confirmation_number
from mysql.connector import Error

app=Flask(__name__)

db=Databasecentralsystem()
conn=db.connect()
cursor=conn.cursor(dictionary=True)
booking_manager=BookingManager()


@app.route('/rooms', methods=['GET'])
def get_all_rooms():
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from rooms")
        rooms=cursor.fetchall()
        return jsonify(rooms)
    except Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()
    
    

@app.route('/rooms/search', methods=['GET'])
def search_rooms():
    check_in=request.args.get('check_in')
    check_out=request.args.get('check_out')
    query="""select * from rooms where room_id NOT IN(select room_id from reservations where not (%s >= check_out OR %s <= check_in))"""
    cursor.execute(query,(check_in,check_out))
    available_rooms=cursor.fetchall()
    return jsonify(available_rooms)


@app.route('/booking', methods=['POST'])
def create_booking():
    data=request.json
    name=data["name"]
    email=data["email"]
    room_id=data["room_id"]
    check_in=data["check_in"]
    check_out=data["check_out"]
    
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("select id from users where email = %s",(email,))
        user=cursor.fetchone()
        if user:
            user_id=user['id']
        else:
            cursor.execute("insert into users(name,email) values (%s,%s)", (name,email))
            user_id=cursor.lastrowid
            cursor.execute(" INSERT INTO bookings (user_id, room_id, check_in, check_out)VALUES (%s, %s, %s, %s)", (user_id, room_id, check_in, check_out))
            booking_id = cursor.lastrowid
            cursor.execute("UPDATE rooms SET available = 0 WHERE id = %s", (room_id,))
            confirmation=confirmation_number()
            cursor.execute("insert into reservations(booking_id,status,confirmationnumber) values (%s,%s,%s)",(booking_id,'confirmed',confirmation))
            conn.commit()
        
        return jsonify({'message': 'Booking created', 'booking_id': booking_id,"confirmation_number":confirmation,"room_id":room_id,"check_in":check_in,"check_out":check_out})
    except Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()



@app.route('/booking/cancel', methods=['POST'])
def cancel_booking():
    data=request.json
    confirmation=data.get('confirmation_number')
    
    try:
        conn=db
        cursor=conn.cursor(dictionary=True)
        cursor.execute("select * from reservations where confirmationnumber = %s",(confirmation,))
        reservation=cursor.fetchone()
        if not reservation:
            return jsonify({'error':'wrong number'})
        
        booking_id=reservation['booking_id']
        cursor.execute("update reservations set status='cancelled' where confirmationnumber=%s",(confirmation,))
        cursor.execute("select room_id from bookings where id=%s",(booking_id,))
        booking=cursor.fetchone()
        if booking:
            room_id=booking['room_id']
            cursor.execute("update rooms set available=1 where id=%s",(room_id,))
            conn.commit()
            return jsonify({'message':'booking cancel'})
    except Error as e:
        return jsonify({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
    
    
@app.route('/booking/<confirmation_number>', methods=['GET'])
def get_confirmation(confirmation_number):
    try:
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT b.user_id, b.room_id, b.check_in, b.check_out, r.confirmationnumber
            FROM bookings b
            JOIN reservations r ON b.id = r.booking_id
            WHERE r.confirmationnumber = %s
        """, (confirmation_number,))
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
        

if __name__ == '__main__':
    app.run(debug=True)
        
