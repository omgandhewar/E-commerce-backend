from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from datetime import timedelta


jwt=JWTManager()
bcrypt=Bcrypt()
def create_app():
    app=Flask(__name__)
    
    app.config["SECRET_KEY"]="abc"
    app.config["JWT_SECRET_KEY"]="abc"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(minutes=20)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"]=timedelta(days=30)
    
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
   
    return app