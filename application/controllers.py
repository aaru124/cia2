from flask import jsonify, render_template, request, session, redirect
from flask import current_app as app
import razorpay
import stripe
from application.models import User, db, Product, Purchase, Order, Cart
import re
import json


@app.route('/')
def welcome():
    
    if "user" not in session:
        session["guest"]="yes"
        return render_template("main.html",var="Login",var1="/user-login")
    if "user" in session:
        print("hey in session")
        return render_template("main.html",var="Logout" ,var1="/logout")
    return render_template("main.html",var="Login",var1="/user-login")
    



@app.route('/sneakers', methods=["GET","POST"])
def sneaker():
    
    prod=Product.query.filter_by(category_name = "sneakers")
    max=0
    for i in prod:
        if int(i.price)>max:
            max=i.price
    if request.method=="GET":
        prod= Product.query.filter_by(category_name = "sneakers")
        
        
        if "user" not in session:
            return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login")
        if "user" in session:
            return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout")
           
        
    
    if request.method=="POST":

        if "product" in request.form :
           
            product_id= request.form["product"]
            count = request.form["quantity"]
            size = request.form["size"]
            product = Product.query.filter_by(id = int(product_id)).first()
            u=User.query.filter_by(name=session["user"]).first()
            cart = Cart.query.filter_by(user_id=u.id)
            flag=1
            for i in cart:
                
                if i.product_id==int(product_id) and i.size==int(size):
                    
                    flag=0
                    if size=="36":
                        if product.size_36<int(count):
                            render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                            
                    if size=="37":
                        if product.size_37<int(count):
                            render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="38":
                        if product.size_38<int(count):
                            render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="39":
                        if product.size_39<int(count):
                            render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="40":
                        if product.size_40<int(count):
                            render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="41":
                        if product.size_41<int(count):
                            render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="42":
                        if product.size_42<int(count):
                            render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
            if flag==1:
                c = Cart(product_id=product.id, user_id=u.id, quantity=int(count), price=product.price ,size=int(size))
                db.session.add(c)
                db.session.commit()

            return redirect("/sneakers")
        if "min_price" in request.form:

            p_new=[]
            p=Product.query.filter_by(category_name="sneakers").first()
            for i in p:
                if int(i.price)>=int(request.form["min_price"]) and int(i.price)<=int(request.form["max_price"]):
                    p_new.append(i) 
            print(p_new)
            return render_template('home.html',prod=p_new)
                
        elif "user" not in session:
            return render_template("home.html", error="You are not logged in.",prod=prod,  max=max)
        return redirect("/sneakers")
    
@app.route('/slides', methods=["GET","POST"])
def slide():
    
    prod=Product.query.filter_by(category_name = "slides")
    max=0
    for i in prod:
        if int(i.price)>max:
            max=i.price
    if request.method=="GET":
        prod= Product.query.filter_by(category_name = "slides")
        
        if "user" not in session:
            return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login")
        if "user" in session:
            return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout")
           
        
    
    if request.method=="POST":

        if "product" in request.form :
           
            product_id= request.form["product"]
            count = request.form["quantity"]
            size = request.form["size"]
            product = Product.query.filter_by(id = product_id).first()
        
            cart = json.loads(session["cart"])
            if size=="36":
                if product.size_36<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_36):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_36):
                            cart[product_id] = count
            if size=="37":
                if product.size_37<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_37):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_37):
                            cart[product_id] = count
            if size=="38":
                if product.size_38<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_38):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_38):
                            cart[product_id] = count
            if size=="39":
                if product.size_39<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_39):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_39):
                            cart[product_id] = count
            
            if size=="40":
                if product.size_40<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_40):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_40):
                            cart[product_id] = count
            
            if size=="41":
                if product.size_41<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_41):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_41):
                            cart[product_id] = count
            
            if size=="42":
                if product.size_42<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_42):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_42):
                            cart[product_id] = count

            session["cart"] = json.dumps(cart)
            return redirect("/slides")
        if "min_price" in request.form:

            p_new=[]
            p=Product.query.filter_by(category_name="slides").first()
            for i in p:
                if int(i.price)>=int(request.form["min_price"]) and int(i.price)<=int(request.form["max_price"]):
                    p_new.append(i) 
            print(p_new)
            return render_template('home.html',prod=p_new)
                
        elif "user" not in session:
            return render_template("home.html", error="You are not logged in.",prod=prod,  max=max)
        return redirect("/slides")


    
@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
        session.pop("cart")
    return redirect("/")

@app.route('/admin-register', methods=["GET","POST"])
def admin_register():
    errors={}
    if request.method=='GET':
        if "user" not in session:
            return render_template("admin_register.html",var="Login",var1="/user-login",error="")
        if "user" in session:
            return render_template("admin_register.html",var="Logout" ,var1="/logout",error="")
    
    elif request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']
        store = request.form['store_name']

        user_pattern = r'^[A-Za-z0-9]+$'  
        pass_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$'
        
        user = User.query.filter_by(name = username).first()        
        if user is not None and user.admin==True:
            errors['login']="An account has been found in your name."
        
        if not re.match(pass_pattern,password):
            errors['pass']="The minimum length of the password should be 8 characters including an uppercase, lowercase and special character and a number"
        if not re.match(user_pattern,username):  
            errors['user']="The username should only be alphanumeric"
        
        if errors:
            return render_template("admin_register.html",error=errors)
        else:
            user = User(name = username, password = password, admin=True, contact_no=phone, email=email,store_name=store)
            db.session.add(user)
            db.session.commit()
            session["admin"] = username
            session["cart"]=json.dumps(dict())
            return redirect("/store-manager/product")
    
@app.route('/user-register', methods=["GET","POST"])
def user_register():
    errors={}
    if request.method=='GET':
        return render_template("user_register.html",error=errors)
    
    elif request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        postal_code = request.form['zip']

        
        user_pattern = r'^[A-Za-z0-9]+$'  
        pass_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$'
        
        user = User.query.filter_by(name = username).first()        
        if user is not None and user.admin==False:
            errors['login']="An account has been found in your name."
        
        if not re.match(pass_pattern,password):
            errors['pass']="The minimum length of the password should be 8 characters including an uppercase, lowercase and special character and a number"
        if not re.match(user_pattern,username):  
            errors['user']="The username should only be alphanumeric"
        
        if errors:
            return render_template("user_register.html",error=errors)
        else:
            user = User(name = username, password = password,contact_no = phone, address=address, postal_code=postal_code,email=email)
            db.session.add(user)
            db.session.commit()
            session["user"] = username
            session["cart"]=json.dumps(dict())
            return redirect("/")
        
                
               
@app.route('/user-login', methods=["GET","POST"])
def user_login():
    errors={}
    if request.method=='GET':
        if "user" not in session:
            return render_template("user_login.html",error=errors,var="Login" ,var1="/user-login")
        if "user" in session:
            return render_template("user_login.html",error=errors,var="Logout" ,var1="/logout")
    
    elif request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name = username).first()       
        if user is not None and user.admin==False and password==user.password:
            session["user"]=username
            session["cart"]=json.dumps(dict())
            return redirect("/")
        
        elif user is None or user.admin:
            errors['no_user']="User is not present in the system."
            errors['register']='yes'
        elif password!=user.password:  
            errors['no_user']="The password is wrong."
            errors['register']='no'
        
        if errors:
            return render_template("user_login.html",error=errors)

@app.route('/admin-login', methods=["GET","POST"])
def admin_login():
    errors={}
    if request.method=='GET':
        if "user" not in session:
            return render_template("admin_login.html",error="",var="Login",var1="/user-login")
        if "user" in session:
            return render_template("admin_login.html",error="",var="Logout" ,var1="/logout")
        
    
    elif request.method=='POST':
        username = request.form['username']
        password = request.form['password']


        user = User.query.filter_by(name = username).first()        
        if user is not None and user.admin==True and password==user.password:
            session["admin"]=username
            session["cart"]=json.dumps(dict())
            return redirect('/store-manager/product')
        
        elif user is None or not user.admin:
            errors['no_user']="User is not present in the system."
            errors['register']='yes'
        elif password!=user.password:  
            errors['no_user']="The password is wrong."
            errors['register']='no'
        
        if errors:
            return render_template("admin_login.html",error=errors)




@app.route("/store-manager/product",methods=["GET","POST"])
def product():
    if request.method=="GET":
        prod = Product.query.all()
        order = Order.query.all()
        return render_template("product.html",prod=prod,order=order)
    if request.method=="POST":
        print("hey")
        if "process" in request.form:
            o=Order.query.filter_by(id=int(request.form["process"])).first()
            o.status="In Process"
            db.session.commit()
        if "shipped" in request.form:
            print(request.form["shipped"])
            o=Order.query.filter_by(id=int(request.form["shipped"])).first()
            o.status="Shipped"
            db.session.commit()
        if "delivered" in request.form:
            o=Order.query.filter_by(id=int(request.form["delivered"])).first()
            o.status="Delivered"
            db.session.commit()
        return redirect("/store-manager/product")
        


@app.route("/store-manager/product/add", methods=["GET","POST"])
def add_product():
    if request.method=="GET" and "user" in session:
        user=User.query.filter_by(admin = True)
        
        prod=Product.query.all()
        
        
        return render_template("add_product.html")
     
        
    if request.method=="POST" and "user" in session:
        user = User.query.filter_by(name=session["user"]).first()      
        if user.admin:                  
            if request.method == "POST":
                name = request.form["product_name"]
                description = request.form["description"]
                brand = request.form["brand"]
                gender = request.form["gender"]
                discount = request.form["discount"]
                s36 = request.form["size_36"]
                s37 = request.form["size_37"]
                s38 = request.form["size_38"]
                s39 = request.form["size_39"]
                s40 = request.form["size_40"]
                s41 = request.form["size_41"]
                s42 = request.form["size_42"]
                rate = request.form["price"]
                category = request.form["category"]
                man_date = request.form["date_added"]
                img = request.files["img"]
                product = Product(name = name, description = description, brand=brand, price = rate, date_added=man_date, category_name=category, size_36=s36, size_37=s37, size_38=s38,size_39=s39,size_40=s40,size_41=s41,size_42=s42,gender=gender,discount=discount)
                db.session.add(product)
                db.session.commit()
                img.save("./static/products/" + str(product.id) + ".png")
                return redirect("/store-manager/product")
    return redirect("/store-manager/product")
    
@app.route("/store-manager/product/delete_<product_id>", methods=["GET","POST"])
def delete_product(product_id):
    p=int(product_id)
    prod = Product.query.all()
    user=session["user"]
    user = User.query.filter_by(name = user).first()
    if request.method=="GET":
        return render_template("product.html",prod=prod,delete="yes",edit="no")
    prod_del = Product.query.filter_by(id = p).first()

    if request.method=="POST" and user.admin:
        if "yes" in request.form: 
            db.session.delete(prod_del)
            db.session.commit()
            
            return redirect("/store-manager/product")
        
        if "no" in request.form:
            return redirect("/store-manager/product")
    else:
        return render_template("product.html",error="You cannot delete this product",error_id=prod_del.id)

@app.route("/store-manager/product/edit_<product_id>", methods=["GET","POST"])
def edit_product(product_id):
    p=int(product_id)
    if request.method=="GET" and "user" in session:
        user=User.query.filter_by(admin = True)
        
        prod=Product.query.filter_by(id=product_id)
        return render_template("edit_product.html",prod=prod)
    

    if request.method=="POST" and "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        prod = Product.query.filter_by(id = p).first()      
        
        if user.admin:                
            
            name = request.form["product_name"]
            description = request.form["description"]
            brand = request.form["brand"]
            gender = request.form["gender"]
            discount = request.form["discount"]
            s36 = request.form["size_36"]
            s37 = request.form["size_37"]
            s38 = request.form["size_38"]
            s39 = request.form["size_39"]
            s40 = request.form["size_40"]
            s41 = request.form["size_41"]
            s42 = request.form["size_42"]
            rate = request.form["price"]
            category = request.form["category"]
            man_date = request.form["date_added"]
            img = request.files["img"]
            rate = request.form['price']
                
                
            if name:
                prod.name=name
            if description:
                prod.description = description
            if brand:
                prod.brand = brand
            if rate:
                prod.price = rate
            if gender:
                prod.gender = gender
            if discount:
                prod.discount = discount
            if category:
                prod.category_name = category
            if man_date:
                prod.date_added = man_date
            if s36:
                prod.size_36 = s36
            if s37:
                prod.size_37 = s37
            if s38:
                prod.size_38 = s38
            if s39:
                prod.size_39 = s39
            if s40:
                prod.size_40 = s40
            if s41:
                prod.size_41 = s41
            if s42:
                prod.size_42 = s42
                
                
            db.session.commit()
            if img:
                img.save("./static/products/" + str(prod.id) + ".png")

                return redirect("/store-manager/product")
        else:
            return render_template("product.html", error="You cannot delete this product",error_id=prod.id)
    return redirect("/store-manager/product")

@app.route("/cart", methods=["GET","POST"])
def cart():
    if "user" in session: 
        user = User.query.filter_by(name=session["user"]).first() 
        cart = Cart.query.filter_by(user_id=user.id)
        products=[]
        rate_list=[]
        for i in cart:
            
            el=[]
            p=Product.query.filter_by(id = i.product_id).first()
            r=int(i.price*i.quantity)
            c=i.quantity
            s=i.size
            el.append(p)
            el.append(c)
            el.append(r)
            el.append(i)
            rate_list.append(r)
            products.append(el)

        total = sum(rate_list)
        if request.method=="GET":
          
            if "user" not in session:
                
                return render_template("cart.html",error="",var="Login",var1="/user-login",products = products, total = total)
            if "user" in session:
                return render_template("cart.html",error="",var="Logout" ,var1="/logout",products = products, total = total)
            
        else:
            if "remove" in request.form:
                id = request.form['remove']
                cart_del=Cart.query.filter_by(id = int(id)).first()
                db.session.delete(cart_del)
                db.session.commit()
                return redirect("/cart")
            else:
                for product, count, rate in products:
                    product.stock -= int(count)
                    purhcase=Purchase(product=product.id,owner_store=product.owner,customer_user=user.id,quantity=count,price=rate)
                    db.session.add(purhcase)
                    db.session.commit()   
                order=Order(total_price=total,payment_method=request.form["paymentOption"])
                db.session.add(order)
                db.session.commit() 
                session["cart"] = json.dumps(dict())
                return redirect("/thank-you")
    elif "guest" in session:
        if request.method=="GET":
            return render_template("cart.html",error="",var="Login",var1="/user-login")
           
    return redirect("/")

@app.route("/thank-you")
def final():
    
    return render_template("final_page.html")

@app.route("/product_page/<val>", methods=["GET","POST"])
def product_page(val):
    if request.method=="GET": 
        p = Product.query.filter_by(name=val).first()
        new_price=p.price
        if p.discount:
            new_price=p.price-(p.price*(p.discount/100))
        if "user" not in session:
            return render_template("product_page.html",prod=p,var="Login",var1="/user-login",error="",p=new_price)
        if "user" in session:
            return render_template("product_page.html",prod=p,var="Logout" ,var1="/logout",error="",p=new_price)
        
        

   
        

@app.route("/sneakers/search/<val>", methods=["GET","POST"])  
def search(val):
    
    if request.method=="GET":    
        prod= Product.query.all()
        max=0
        for i in prod:
            if int(i.price)>max:
                max=i.price
        
        p=Product.query.all()
      
        p_new=[]
        for i in p:
            if val in i.name or val in str(int(i.price)) or val in i.date_added or val in i.category_name:
                p_new.append(i)
        
        if "user" not in session:
            return render_template("home.html",var="Login",var1="/user-login",prod=p_new,max=max,search_name=val)
        if "user" in session:
            return render_template("home.html",var="Logout" ,var1="/logout",prod=p_new,max=max,search_name=val)
    if request.method=="POST":
        '''if "category" in request.form:
            if request.form["category"]!=" ":
                filter= Product.query.filter_by(category_name = request.form["category"])
                return render_template('home.html',prod=filter,filter_name=request.form["category"])
        elif "product" in request.form:
            product_id= request.form["product"]
            count = request.form["count"]
            product = Product.query.filter_by(id = product_id).first()
        
            cart = json.loads(session["cart"])

            if product_id in cart:
                current = int(count) + int(cart[product_id])
                if current <= int(product.size_36):
                    cart[product_id] = str(int(cart[product_id]) + int(count))
            else:
                current = int(count)
                if current <= int(product.size_36):
                    cart[product_id] = count

            session["cart"] = json.dumps(cart)
            return redirect("/home/search/"+val)'''
        if "product" in request.form:
            product_id= request.form["product"]
            count = request.form["quantity"]
            size = request.form["size"]
            product = Product.query.filter_by(id = product_id).first()
        
            cart = json.loads(session["cart"])
            if size=="36":
                if product.size_36<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_36):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_36):
                            cart[product_id] = count
            if size=="37":
                if product.size_37<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_37):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_37):
                            cart[product_id] = count
            if size=="38":
                if product.size_38<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_38):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_38):
                            cart[product_id] = count
            if size=="39":
                if product.size_39<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_39):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_39):
                            cart[product_id] = count
            
            if size=="40":
                if product.size_40<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_40):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_40):
                            cart[product_id] = count
            
            if size=="41":
                if product.size_41<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_41):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_41):
                            cart[product_id] = count
            
            if size=="42":
                if product.size_42<int(count):
                    return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod,max=max)
                elif product_id in cart:
                    current = int(count) + int(cart[product_id])
                    if current <= int(product.size_42):
                        cart[product_id] = str(int(cart[product_id]) + int(count))
                    else:
                        current = int(count)
                        if current <= int(product.size_42):
                            cart[product_id] = count

            session["cart"] = json.dumps(cart)
            return redirect("/sneakers")
        elif not prod:
            return render_template("home.html", error="no products",prod=prod,  max=max)
        return redirect("/sneakers/search/<val>")

    return render_template("home.html")  

@app.route('/account', methods=["GET","POST"])
def account():

    if request.method=="GET":
        a=User.query.filter_by(name=session['user']).first()
        order=Order.query.filter_by(user_id=a.id)
        purchase=Purchase.query.filter_by(customer_user=a.id)
        main=[]
        lst=[]
        prod=[]
        for i in order:
            lst.append(i.id)
            lst.append(i.date_added)
            lst.append(i.total_price)
            lst.append(i.status)
            for j in purchase:
                if i.id==j.order_id:
                    b=Product.query.filter_by(id=j.product).first()
                    prod.append([b.id,b.brand,b.name,b.price])
            lst.append(prod)
            main.append(lst)
        print(lst)

        return render_template("account_page.html",var="Logout" ,var1="/logout",u=a,main=main)

@app.route('/wishlist', methods=["GET","POST"])
def wishlist():

    if request.method=="GET":
        if "user" in session:
            a=User.query.filter_by(name=session['user']).first()
            return render_template("wishlist.html",var="Logout" ,var1="/logout",u=a)
        if "guest" in session:
            
            return render_template("wishlist.html",var="Login" ,var1="/user-login")


