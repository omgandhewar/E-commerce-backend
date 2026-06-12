from app.db.database import get_db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash
from app.flaskextension import bcrypt, jwt
import os


def signup_user(data):
    db=get_db()
    cursor=db.cursor()
    
    username=data.get("username")
    email=data.get("email")
    password=data.get("password")
    role=data.get("role")
    
    sql="SELECT * FROM Users WHERE username=%s"
    cursor.execute(sql, (username,))   
    
    user_obj=cursor.fetchone()
     
    if user_obj:
        return{
            "message":"user already exists"
        }
        
    
    hashed_password=bcrypt.generate_password_hash(password).decode("utf-8")
    
    sql="INSERT INTO Users (username,email,password,role) VALUES (%s,%s,%s,%s)"
    values=(username,email,hashed_password,role)
    
    cursor.execute(sql, values)
    db.commit()
    
    return{
        "message":"User craeted successfully"
    }


def login_user(data):
    print("DB HOST:", os.getenv("DB_HOST"))
    db=get_db()
    cursor=db.cursor()
    
    email=data.get("email")
    password=data.get("password")
    
    if not email or not password:
        return{
            "message":"email and password are required"
        }
        
    sql="SELECT id,email,password,role FROM Users WHERE email=%s"
    cursor.execute(sql,(email,))
    
    user_obj=cursor.fetchone()
    
    print(user_obj)
    print(type(user_obj))
    
    if not user_obj:
        return{
            "message":"Invalid email"
        }
        
    if not bcrypt.check_password_hash(user_obj[2], password):
        return{
            "message":"Invalid password"
        }
        
    token=token = create_access_token(
    identity=str(user_obj[0]),
    additional_claims={
        "role": user_obj[3]
    }
)
    refresh_token=create_refresh_token(identity=email)
    
    
    return{
        "message":"login successfully",
        "token":token,
        "refresh_token":refresh_token
    }
    
    
def user_refreshtoken():
    current_user=get_jwt_identity()
    
    new_access_token=create_access_token(identity=current_user)
    
    return{
        "new_access_token":new_access_token
    }
    
    
@jwt.token_in_blocklist_loader 
def check_in_blocklist_token(jwt_header,jwt_payload):
    db=get_db()
    cursor=db.cursor()
    
    jti=jwt_payload["jti"]
    
    sql="SELECT jti FROM token_id WHERE jti=%s"
    cursor.execute(sql,(jti,))
    
    user_obj=cursor.fetchone()
    
    return user_obj is not None
    
    
def user_logout():
    db=get_db()
    cursor=db.cursor()
    
    jti=get_jwt()["jti"]
    
    sql="INSERT INTO token_id(jti) VALUES (%s)"
    values=(jti,)
    
    cursor.execute(sql,values)
    db.commit()
    
    return{
        "messages":"logout successfully"
    }