from app.db.database import get_db
from flask_jwt_extended import get_jwt_identity


def useradd_to_cart(data,id):
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt_identity()
    
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
    

def userview_cart():
    db=get_db()
    cursor=db.cursor()
    
    current_user=get_jwt_identity()
    
    sql="SELECT c.Cartproduct_id,p.Product_name,p.Price,c.quantity,(p.Price*c.quantity) as amount FROM addcart c JOIN products p ON c.Product_id=p.Product_id WHERE id=%s"
    cursor.execute(sql,(current_user,))
    
    products=cursor.fetchall()
    
    return{
        "products":products
    }
    
    
def userupdate_cart(data,id):
        db=get_db()
        cursor=db.cursor()
        
        current_user=get_jwt_identity()
        
        
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