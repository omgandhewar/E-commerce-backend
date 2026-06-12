from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.services.product_service import adminadd_product, adminupdate_product, userget_product, userview_product


product_bp=Blueprint("product",__name__)

@product_bp.route("/addproducts",methods=["GET","POST"])
@jwt_required()
def add_product():
    return adminadd_product(request.get_json())

@product_bp.route("/updateproducts/<int:id>",methods=["PUT"])
@jwt_required()
def update_product(id):
    return adminupdate_product(request.get_json(),id)

@product_bp.route("/products/<int:id>",methods=["GET"])
def get_product(id):
    return userget_product(id)

@product_bp.route("/viewproduct",methods=["GET"])
def view_product():
    return userview_product()
