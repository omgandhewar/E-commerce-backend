from flask import request
from app.db.database import get_db
from flask_jwt_extended import get_jwt


def adminadd_product(data):
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt()
    
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
    
def adminupdate_product(data,id):
    print("UPDATE ROUTE HIT")
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt()
    
    print(current_user)
    
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
    
    
def userget_product(id):
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

def userview_product():
    db=get_db()
    cursor=db.cursor()
    
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    offset = (page - 1) * limit
    
    name=request.args.get("name")
    
    sql="SELECT Product_name,Price FROM products WHERE Product_name LIKE %s LIMIT %s OFFSET %s"
    cursor.execute(sql,(f"%{name}%",limit,offset))
    
    products=cursor.fetchall()
    
    return{
        "message":products
    }