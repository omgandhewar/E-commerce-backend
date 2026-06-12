from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.services.order_service import create_order, userview_order, adminupdate_status



order_bp=Blueprint("order",__name__)


@order_bp.route("/orders",methods=["POST"])
@jwt_required()
def orders():
    return create_order()


@order_bp.route("/vieworder",methods=["GET"])
@jwt_required()
def view_order():
    return userview_order()


@order_bp.route("/updatestatus/<int:id>",methods=["PUT"])
@jwt_required()
def update_status(id):
    return adminupdate_status(request.get_json(),id)