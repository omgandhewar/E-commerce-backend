from flask import Flask
from app.flaskextension import bcrypt, jwt
from datetime import timedelta
from flask_cors import CORS
from app.routes.auth_routes import auth_bp
from app.routes.order_routes import order_bp
from app.routes.cart_routes import cart_bp
from app.routes.product_routes import product_bp


def create_app():
    app=Flask(__name__)
    
    app.config["SECRET_KEY"]="abc"
    app.config["JWT_SECRET_KEY"]="abc"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(minutes=20)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"]=timedelta(days=30)
    
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    

    app.register_blueprint(auth_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(product_bp)
    
    print(app.url_map)
    
   
    return app