from flask import Flask, request, session, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash
from app import bcrypt
import os
from app.db import get_db


main=Blueprint("main",__name__)

@main.route("/signup",methods=["GET","POST"])
def signup():
    db=get_db()
    cursor=db.cursor()
    
    data=request.get_json()
    
    username=data.get("username")
    email=data.get("email")
    password=data.get("password")
    
    sql="SELECT * FROM Users WHERE username=%s"
    cursor.execute(sql, (username,))   
    
    user_obj=cursor.fetchone()
     
    if user_obj:
        return{
            "message":"user already exists"
        }
        
    
    hashed_password=bcrypt.generate_password_hash(password).decode("utf-8")
    
    sql="INSERT INTO Users (username,email,password) VALUES (%s,%s,%s)"
    values=(username,email,hashed_password)
    
    cursor.execute(sql, values)
    db.commit()
    
    return{
        "message":"User craeted successfully"
    }
    
    
@main.route("/login",methods=["GET","POST"])
def login():
    print("DB HOST:", os.getenv("DB_HOST"))
    db=get_db()
    cursor=db.cursor()
    
    data=request.get_json()
    
    email=data.get("email")
    password=data.get("password")
    
    if not email or not password:
        return{
            "message":"email and password are required"
        }
        
    sql="SELECT email,password FROM Users WHERE email=%s"
    cursor.execute(sql,(email,))
    
    user_obj=cursor.fetchone()
    
    print(user_obj)
    print(type(user_obj))
    
    if not user_obj:
        return{
            "message":"Invalid email"
        }
        
    if not bcrypt.check_password_hash(user_obj[1], password):
        return{
            "message":"Invalid password"
        }
        
    token=create_access_token(identity=email)
    refresh_token=create_refresh_token(identity=email)
    
    
    return{
        "message":"login successfully",
        "token":token,
        "refresh_token":refresh_token
    }
        
        
@main.route("/dashboard",methods=["GET"])
@jwt_required()
def dashboard():
    
    current_user=get_jwt_identity()
    
    return{
        "message":f"welcome {current_user}"
    }
        