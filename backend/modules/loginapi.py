from flask import Blueprint, request, jsonify
import bcrypt
from mysql.connector import Error

from database_central_system import Databasecentralsystem

loginform = Blueprint('login', __name__)
db = Databasecentralsystem()


@loginform.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "select id,name,email,hash_password,user_type from users where email=%s", (email,))
        user = cursor.fetchone()

        # First, check if a user was found with that email
        if user and bcrypt.checkpw(password.encode('utf-8'), user['hash_password'].encode('utf-8')):
            return jsonify({
                "message": "login done",
                "user_id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "user_type": user['user_type']
            })
        else:
            # This will now handle both "user not found" and "wrong password" cases
            return jsonify({"error": "wrong enteries try again"})

    except Error as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()
