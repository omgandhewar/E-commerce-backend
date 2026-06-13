from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, set_access_cookies
from app.services.auth_service import signup_user, login_user, user_refreshtoken, user_logout


auth_bp=Blueprint("auth",__name__)


@auth_bp.route("/signup",methods=["GEt","POST"])
def signup():
    return signup_user(request.get_json())


@auth_bp.route("/login",methods=["GET","POST"])
def login():
    
    result=login_user(request.get_json())

    if "token" not in result:
        return jsonify(result)
    
    response=jsonify({
        "mesage":result["message"]
    })
    
    response.set_cookie(
        "access_token",
        result["token"],
        httponly=True,
        secure=True
    )
    
    return response

@auth_bp.route("/refresh",methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    return user_refreshtoken()


@auth_bp.route("/logout",methods=["POST"])
@jwt_required(refresh=True)
def logout():
    return user_logout()

