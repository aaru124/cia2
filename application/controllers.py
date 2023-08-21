from flask import jsonify, render_template, request, session, redirect
from flask import current_app as app
import razorpay
import stripe
from application.models import User, db, Product, Purchase, Order
import re
import json


@app.route('/')
def welcome():
    
    if "user" not in session:
        return render_template("main.html",var="Sign in / Sign up",var1="/user-login")
    if "user" in session:
        print("hey in session")
        return render_template("main.html",var="Logout" ,var1="/logout")
    return render_template("main.html",var="Sign in / Sign up",var1="/user-login")
    



@app.route('/home', methods=["GET","POST"])
def home():
    
    prod=Product.query.all()
    max=0
    for i in prod:
        if int(i.rate)>max:
            max=i.rate
    if request.method=="GET":
        prod= Product.query.all()
        
        
        return render_template('home.html',prod=prod, cat=cat, max=max, user=session["user"])
    
    if request.method=="POST":

        if "product" in request.form and "user" in session:
           
            product_id= request.form["product"]
            count = request.form["count"]
            product = Product.query.filter_by(id = product_id).first()
        
            cart = json.loads(session["cart"])
            if product.stock<int(count):
                return render_template("home.html", error1="Quantity added is more than the stock available.",prod=prod, cat=cat, max=max)
            elif product_id in cart:
                current = int(count) + int(cart[product_id])
                if current <= int(product.stock):
                    cart[product_id] = str(int(cart[product_id]) + int(count))
            else:
                current = int(count)
                if current <= int(product.stock):
                    cart[product_id] = count

            session["cart"] = json.dumps(cart)
            return redirect("/home")
        if "min_price" in request.form:

            p_new=[]
            p=Product.query.all()
            for i in p:
                if int(i.rate)>=int(request.form["min_price"]) and int(i.rate)<=int(request.form["max_price"]):
                    p_new.append(i) 
            print(p_new)
            return render_template('home.html',prod=p_new, cat=cat)
                
        elif "user" not in session:
            return render_template("home.html", error="You are not logged in.",prod=prod, cat=cat, max=max)
        return redirect("/home")

    
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
        return render_template("admin_register.html",error=errors)
    
    elif request.method=='POST':
        username = request.form['username']
        password = request.form['password']

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
            user = User(name = username, password = password, admin=True)
            db.session.add(user)
            db.session.commit()
            session["user"] = username
            session["cart"]=json.dumps(dict())
            return redirect("/store-manager")
    
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
        return render_template("user_login.html",error=errors)
    
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
        return render_template("admin_login.html",error=errors)
    
    elif request.method=='POST':
        username = request.form['username']
        password = request.form['password']


        user = User.query.filter_by(name = username).first()        
        if user is not None and user.admin==True and password==user.password:
            session["user"]=username
            session["cart"]=json.dumps(dict())
            return redirect('/store-manager')
        
        elif user is None or not user.admin:
            errors['no_user']="User is not present in the system."
            errors['register']='yes'
        elif password!=user.password:  
            errors['no_user']="The password is wrong."
            errors['register']='no'
        
        if errors:
            return render_template("admin_login.html",error=errors)

@app.route("/store-manager")
def store_manager():
    return render_template("store_manager.html")


@app.route("/store-manager/product")
def product():
    prod = Product.query.all()
    return render_template("product.html",prod=prod)


@app.route("/store-manager/product/add", methods=["GET","POST"])
def add_product():
    if request.method=="GET" and "user" in session:
        user=User.query.filter_by(admin = True)
        
        prod=Product.query.all()
        cat_n=[]
        for i in cat:
            cat_n.append(i)
        if cat_n:
            return render_template("add_product.html",cat=cat)
        else:
            return render_template("product.html",prod=prod,error1="No categories present.")
        
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

    if request.method=="POST" and user.admin and user.id==int(prod_del.owner):
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
        return render_template("edit_product.html",cat=cat,prod=prod)
    

    if request.method=="POST" and "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        prod = Product.query.filter_by(id = p).first()      
        print(user.id==int(prod.owner))
        if user.admin:                
            if int(prod.owner)==user.id:
                name = request.form["product_name"]
                description = request.form["description"]
                stock = request.form["stock"]
                rate = request.form["rate"]
                unit = request.form["unit"]
                category = request.form["category"]
                man_date = request.form["manufacturing_date"]
                img = request.files["img"]
                
                
                if name:
                    prod.name=name
                if description:
                    prod.description = description
                if stock:
                    prod.stock = stock
                if rate:
                    prod.rate = rate
                if unit:
                    prod.unit = unit
                if category:
                    prod.category_name = category
                if man_date:
                    prod.manufacturing_date = man_date
                
                db.session.commit()
                if img:
                    img.save("./static/products/" + str(prod.id) + ".png")

                return redirect("/store-manager/product")
            else:
                return render_template("product.html", error="You cannot delete this product",error_id=prod.id)
    return redirect("/store-manager/product")

@app.route("/cart", methods=["GET","POST"])
def cart():
    if "user" in session: user = User.query.filter_by(name=session["user"]).first() 
    if "user" in session and user.admin==False:
        cart = json.loads(session["cart"])
        print(cart)
        products=[]
        rate_list=[]
        for product_id in cart.keys():
            el=[]
            p=Product.query.filter_by(id = product_id).first()
            r=int(Product.query.filter_by(id = product_id).first().rate)*int(cart[product_id])
            c=cart[product_id]
            el.append(p)
            el.append(c)
            el.append(r)
            rate_list.append(r)
            products.append(el)

       
        total = sum(rate_list)
        if request.method == "GET":
            return render_template("cart.html", products = products, total = total)
        else:
            if "remove" in request.form:
                cart.pop(request.form["remove"])
                session["cart"] = json.dumps(cart)
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
    elif user.admin!=False:
        return render_template("cart.html", error="You are not a user")
    return redirect("/home")

@app.route("/thank-you")
def final():
    
    return render_template("final_page.html")


@app.route("/home/<category>",methods=["GET","POST"])  
def cat(category):
    if request.method=="GET":
        p= Product.query.all()
        max=0
        for i in p:
            if int(i.rate)>max:
                max=i.rate

        p=Product.query.filter_by(category_name=category)
        p_new=[]
        for i in p:
            p_new.append(i)
       

        return render_template("home.html",prod=p_new,cat=cat,max=max,user=session["user"])
        

   
        

@app.route("/home/search/<val>", methods=["GET","POST"])  
def search(val):
    
    if request.method=="GET":    
        prod= Product.query.all()
        max=0
        for i in prod:
            if int(i.rate)>max:
                max=i.rate
        
        p=Product.query.all()
      
        p_new=[]
        for i in p:
            if i.name==val or str(int(i.rate))==val or i.manufacturing_date==val or i.category_name==val:
                p_new.append(i)

        return render_template("home.html",prod=p_new,cat=cat,max=max,search_name=val)
    if request.method=="POST":
        if "category" in request.form:
            if request.form["category"]!=" ":
                filter= Product.query.filter_by(category_name = request.form["category"])
                return render_template('home.html',prod=filter, cat=cat, filter_name=request.form["category"])
        elif "product" in request.form and "user" in session:
            product_id= request.form["product"]
            count = request.form["count"]
            product = Product.query.filter_by(id = product_id).first()
        
            cart = json.loads(session["cart"])

            if product_id in cart:
                current = int(count) + int(cart[product_id])
                if current <= int(product.stock):
                    cart[product_id] = str(int(cart[product_id]) + int(count))
            else:
                current = int(count)
                if current <= int(product.stock):
                    cart[product_id] = count

            session["cart"] = json.dumps(cart)
            return redirect("/home/search/"+val)
        elif "user" not in session:
            return render_template("home.html", error="you are not logged in.",prod=prod, cat=cat, max=max)
        return redirect("/home/search/<val>")

    return render_template("home.html")  

razorpay_client = razorpay.Client(auth=("rzp_test_XOy0arNBRKuF4z", "eGVaXmXbQbQWygImcrjIaQ8i"))
@app.route('/create_order', methods=['POST'])
def create_order():
    # Get the order amount from the frontend
    order_amount = int(request.form['order_amount']) * 100  # Convert to paise

    # Create a Razorpay order
    order = razorpay_client.order.create({
        'amount': order_amount,
        'currency': 'INR',
        'payment_capture': '1'  # Auto-capture payment
    })
    print('success')
    print(order)