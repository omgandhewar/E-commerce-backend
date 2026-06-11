from flask import Flask, request, session, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash
from app import bcrypt, jwt
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
        "role": user_obj[2]
    }
)
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
        
        
@main.route("/logout",methods=["POST"])
@jwt_required(refresh=True)
def logout():
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
    
@main.route("/refresh",methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user=get_jwt_identity()
    
    new_access_token=create_access_token(identity=current_user)
    
    return{
        "new_access_token":new_access_token
    }
    

@main.route("/checktoken")
@jwt.token_in_blocklist_loader
def check_in_blocklist_token(jwt_header,jwt_payload):
    db=get_db()
    cursor=db.cursor()
    
    jti=jwt_payload["jti"]
    
    sql="SELECT jti FROM token_id WHERE jti=%s"
    cursor.execute(sql,(jti,))
    
    user_obj=cursor.fetchone()
    
    return user_obj is not None


@main.route("/addproducts",methods=["GET","POST"])
@jwt_required()
def add_product():
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt()

    data=request.get_json()
    
    Product_name=data.get("Product_name")
    Price=data.get("Price")
    quantity=data.get("quantity")
    
    
    if current_user["role"]!="admin":
         return{
            "message":"Invalid User"
        }

    sql="INSERT INTO Products(Product_name,Price,quantity) VALUES(%s,%s,%s)"
    values=(Product_name,Price,quantity)
        
    cursor.execute(sql,values)
    db.commit()
    
    return{
        "message":"product added successfully"
    }
    
    
@main.route("/updateproducts/<int:id>",methods=["PUT"])
@jwt_required()
def update_product(id):
    print("UPDATE ROUTE HIT")
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt()
    
    data=request.get_json()
    
    Product_name=data.get("Product_name")
    Price=data.get("Price")
    
    if current_user["role"]!="admin":
        return{
            "message":"Invalid User"
        }
        
    sql="UPDATE Products SET Product_name=%s,Price=%s WHERE Product_id=%s"
    values=(Product_name,Price,id)
    
    cursor.execute(sql,values)
    db.commit()
    
    return{
        "message":"update successfully"
    }


@main.route("/products/<int:id>",methods=["GET"])
def get_product(id):
    db=get_db()
    cursor=db.cursor()
    
    sql="SELECT * FROM Products WHERE Product_id=%s"
    cursor.execute(sql,(id,))
    
    product=cursor.fetchone()
    
    if not product:
        return{
            "message":"product is not found"
        }
        
    return{
        "product":product
    }

@main.route("/addtocart/<int:id>",methods=["POST"])
@jwt_required()
def add_to_cart(id):
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt_identity()
    
    data=request.get_json()
    
    quantity=data.get("quantity")
    
    sql="SELECT * FROM Products WHERE Product_id=%s"
    cursor.execute(sql,(id,))
    
    user_obj=cursor.fetchone()
    
    if not user_obj:
        return{
            "message":"product are not available"
        }
        
    sql="INSERT INTO addcart(id,product_id,quantity) VALUES(%s,%s,%s)"
    values=(current_user,id,quantity)
    
    cursor.execute(sql,values)
    db.commit()
        
    return{
        "message":"product added successfully"
    }
    
@main.route("/orders",methods=["POST"])
@jwt_required()
def orders():
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt_identity()
    
    sql="SELECT * FROM addcart WHERE id=%s"
    cursor.execute(sql,(current_user,))
    
    products=cursor.fetchall()
    
    sql="SELECT SUM(c.quantity * p.Price) AS amount FROM addcart c JOIN Products p ON c.Product_id = p.Product_id WHERE c.id=%s   "
    cursor.execute(sql,(current_user,))
    
    product=cursor.fetchone()
    amount=product[0]
    
    if not products:
        return{
            "message":"product not in cart"
        }

    sql="INSERT INTO order1(id,amount) VALUES(%s,%s)"
    values=(current_user,amount)
    
    cursor.execute(sql,values)
    db.commit()
    
    order_id=cursor.lastrowid
    
    sql="SELECT Product_id,quantity FROM addcart WHERE id=%s"
    cursor.execute(sql,(current_user,))
    
    Products=cursor.fetchall()
    
    for product in products:
        sql="INSERT INTO Order_Items(order_id,Product_id,quantity) VALUES(%s,%s,%s)"
        values=(order_id,product[2],product[3])
    
        cursor.execute(sql,values)
        db.commit()
        
    sql="SELECT Product_id,quantity FROM Order_Items Where order_id=%s"
    cursor.execute(sql,(order_id,))
    
    product=cursor.fetchall()
    print(product)
    
    for products in product:
        sql="UPDATE Products SET quantity=quantity-%s WHERE Product_id=%s"
        values=(products[1],products[0])
        
        cursor.execute(sql,values)
        db.commit()
    
    sql="DELETE FROM addcart WHERE id=%s"
    cursor.execute(sql,(current_user,))
    
    db.commit()
    
    
    return{
        "message":"order is added successfully"
    }
    
 
@main.route("/viewcart",methods=["GET"])
@jwt_required()
def view_cart():
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt_identity()
    
    sql="SELECT c.Cartproduct_id,p.Product_name,p.Price,c.quantity,(p.Price*c.quantity) as amount FROM addcart c JOIN products p ON c.Product_id=p.Product_id WHERE id=%s"
    cursor.execute(sql,(current_user,))
    
    products=cursor.fetchall()
    
    return{
        "products":products
    }
    
    
@main.route("/vieworder",methods=["GET"])
@jwt_required()
def view_order():
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt_identity()
    
    sql="SELECT o.order_id,o.status,p.product_name,p.Price,Oi.quantity,o.amount FROM order1 o JOIN Order_Items Oi ON o.order_id=Oi.order_id JOIN products p ON Oi.Product_id=p.Product_id WHERE o.id=%s "
    cursor.execute(sql,(current_user,))
    
    products=cursor.fetchall()
    
    return{
        "products":products
    }
  
    
@main.route("/updatecart/<int:id>",methods=["PUT"])
@jwt_required()
def update_cart(id):
        db=get_db()
        cursor=db.cursor()
        
        current_user=get_jwt_identity()
        
        data=request.get_json()
        
        quantity=data.get("quantity")
        
        sql="SELECT * FROM addcart WHERE Cartproduct_id=%s AND id=%s"
        cursor.execute(sql,(id,current_user))
        
        products=cursor.fetchall()
        
        if not products:
            return{
                "message":"product not in cart"
            }
            
        sql="UPDATE addcart SET quantity=%s WHERE Cartproduct_id=%s AND id=%s"
        cursor.execute(sql,(quantity,id,current_user))
        
        db.commit()
        
        return{
            "message":"Cart updated succesfully"
        }
        
@main.route("/updatestatus/<int:id>",methods=["PUT"])
@jwt_required()
def update_status(id):
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt()
    
    data=request.get_json()
    
    status=data.get("status")
    
    if current_user["role"]!="admin":
        return{
            "mesasge":"Invalid user"
        }
            
    sql="UPDATE order1 SET status=%s WHERE order_id=%s"
    cursor.execute(sql,(status,id))
    
    db.commit()
    
    return{
        "message":"status update successfully"
    }
    

    
            