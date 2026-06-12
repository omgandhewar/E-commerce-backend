from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.services.cart_service import useradd_to_cart, userview_cart, userupdate_cart


cart_bp=Blueprint("cart",__name__)

@cart_bp.route("/addtocart/<int:id>",methods=["POST"])
@jwt_required()
def add_to_cart(id):
    return useradd_to_cart(request.get_json(),id)


@cart_bp.route("/viewcart",methods=["GET"])
@jwt_required()
def view_cart():
    return userview_cart()


@cart_bp.route("/updatecart/<int:id>",methods=["PUT"])
@jwt_required()
def update_cart(id):
    return userupdate_cart(request.get_json(),id)