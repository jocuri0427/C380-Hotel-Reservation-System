from flask import Blueprint,request,jsonify
from database_central_system import Databasecentralsystem
import bcrypt
from mysql.connector import Error

registration_form=Blueprint('registration',__name__)
db=Databasecentralsystem()

@registration_form.route('/register', methods=['POST'])
def register_user():
    data=request.json
    name=data.get("name")
    email=data.get("email")
    password=data.get("password")
    user_type=data.get("user_type","user")
    
    hash_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    
    try:
        conn=db.get_connection()
        cursor=conn.cursor()
        
        cursor.execute("select id from users where email=%s",(email,))
        if cursor.fetchone():
            return jsonify({"error":"email registered"})
        
        query="""insert into users(name,email,hash_password,user_type) values (%s,%s,%s,%s)"""
        cursor.execute(query,(name,email,hash_password,user_type))
        return jsonify({"message":"user created"})
    except Error as e:
        conn.rollback()
        return jsonify({"error":str(e)})
    finally:
        cursor.close()
        conn.close()