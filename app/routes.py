from flask import Flask, Blueprint
from db import get_db


main=Blueprint("main",__name__)

@main.route("/users",methods=["GET"])
def users():
    db=get_db()
    
    cursor=db.cursor()
    
    cursor.execute("SELECT * FROM users")