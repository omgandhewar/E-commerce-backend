from app.db.database import get_db
from flask_jwt_extended import get_jwt, get_jwt_identity



def create_order():
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
    
    
def userview_order():
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt_identity()
    
    sql="SELECT o.order_id,o.status,p.product_name,p.Price,Oi.quantity,o.amount FROM order1 o JOIN Order_Items Oi ON o.order_id=Oi.order_id JOIN products p ON Oi.Product_id=p.Product_id WHERE o.id=%s "
    cursor.execute(sql,(current_user,))
    
    products=cursor.fetchall()
    
    return{
        "products":products
    }
    
    
def adminupdate_status(data,id):
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt()
    
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