from flask import Flask,request,jsonify
from database_central_system import Databasecentralsystem
from confirmation import Confirmation
from mysql.connector import Error
#from login import loginapi
#from registration import reservationapi

#app.register_blueprint(login_form)
#app.register_blueprint(registration_form)//


app=Flask(__name__)

db=Databasecentralsystem()
conn=db.get_connection()
cursor=conn.cursor(dictionary=True)


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
    try:
        conn=db.get_connection()
        cursor=conn.cursor(dictionary=True)
        query="""select r.* from rooms r where r.id NOT IN(select b.room_id from bookings b JOIN reservations res ON b.id=res.booking_id where res.status='confirmed' AND (%s<b.check_out AND %s > b.check_in))"""
        cursor.execute(query,(check_in,check_out))
        available_rooms=cursor.fetchall()
        return jsonify(available_rooms)
    except Error as e:
        return jsonify({'error':str(e)})
    finally:
        cursor.close()
        conn.close()



@app.route('/booking', methods=['POST'])
def create_booking():
    data=request.json
    name=data.get["name"]
    email=data.get["email"]
    room_id=data.get["room_id"]
    check_in=data.get["check_in"]
    check_out=data.get["check_out"]
    payment=data.get("payment")
    card_number=payment.get("card_number")
    expiry_date=payment.get("expiry_date")
    cvv=payment.get("cvv")
    
    if not payment:
        return jsonify({"error":"payment info"})
    
    try:
        conn=db.get_connection()
        cursor=conn.cursor(dictionary=True)
        
        query="""select b.id from bookings b JOIN reservations r ON b.id = r.booking_id where b.room_id=%s AND r.status='confirmed' AND (%s < b.check_out AND %s > b.check_in)"""
        cursor.execute(query,(room_id,check_out,check_in))
        if cursor.fetchone():
            return jsonify({"error":"Room not available"})
        
        cursor.execute("select id from users where email = %s",(email,))
        user=cursor.fetchone()
        user_id=user['id']
        cursor.execute("insert into users(name,email) values (%s,%s)", (name,email))
        user_id=cursor.lastrowid
        
        cursor.execute("INSERT INTO bookings (name,email,user_id, room_id, check_in, check_out)VALUES (%s,%s,%s, %s, %s, %s)", (name,email,user_id, room_id, check_in, check_out))
        booking_id = cursor.lastrowid
        
        cursor.execute("insert into payments(booking_id,card_number,expiry_date,cvv) values(%s,%s,%s,%s)",(booking_id,card_number,expiry_date,cvv))
        confirmation=Confirmation.gen_confirmation_number()

    
        cursor.execute("insert into reservations(booking_id,status,confirmation_number) values (%s,%s,%s)",(booking_id,'confirmed',confirmation))
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
        conn=db.get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("select booking_id from reservations where confirmation_number = %s AND status='confirmed'",(confirmation,))
        reservation=cursor.fetchone()
        if not reservation:
            return jsonify({'error':'wrong number'})

        cursor.execute("update reservations set status='cancelled' where confirmation_number=%s",(confirmation,))
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
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query="""
            SELECT u.name,u.email, b.room_id, b.check_in, b.check_out,r.status, r.confirmation_number
            FROM bookings b
            JOIN reservations r ON b.id = r.booking_id
            JOIN users u ON b.user_id = u.id
            WHERE r.confirmation_number = %s
        """
        cursor.execute(query,(confirmation_number,))
        booking=cursor.fetchone()
        
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
        
