from flask import jsonify, render_template, request, session, redirect
from flask import current_app as app
import razorpay
import stripe
from application.models import User, db, Product, Purchase, Order, Cart, WishList, Payments, Issue, Review
import re
import json
from sqlalchemy import or_
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime, timedelta


@app.route('/')
def welcome():
    purch=Purchase.query.all()
    p={}
    for i in purch:
        if i.product not in p:
            p[i.product]=i.quantity
        else:
            p[i.product]+=i.quantity
    lst=list(p.values())
    lst.sort(reverse=True)
    final=[]
    ctr=0
    no_pop="false"
    for i in p:
        if p[i] in lst and ctr<2:
            final.append(i)
            ctr+=1
    if len(final)<2:
        no_pop="true"
        p1=Product.query.all()
        p2=Product.query.all()
    else:
        p1=Product.query.filter_by(id=final[0]).first()
        p2=Product.query.filter_by(id=final[1]).first()

    if "user" not in session:
        session["guest"]="yes"
        return render_template("main.html",var="Login",var1="/user-login",p1=p1,p2=p2,no_pop=no_pop)
    if "user" in session:
        print("hey in session")
        return render_template("main.html",var="Logout" ,var1="/logout",p1=p1,p2=p2,no_pop=no_pop)
    return render_template("main.html",var="Login",var1="/user-login")
    



@app.route('/sneakers', methods=["GET","POST"])
def sneaker():
    
    prod=Product.query.filter_by(category_name = "sneakers")
    if "user" in session: 
        u=User.query.filter_by(name=session["user"]).first()
        w=WishList.query.filter_by(user_id=u.id)
        heart=[]
        for i in prod:
            for j in w:
                if j.product_id==i.id:
                    heart.append(i.id)

    max=0
    for i in prod:
        if int(i.price)>max:
            max=i.price
    
    p=Product.query.all()
    brand=[]
    for i in p:
        if i.brand not in brand:
            brand.append(i.brand)
    
    if request.method=="GET":
        prod= Product.query.filter_by(category_name = "sneakers")
        
        
        if "user" not in session:
            return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login",b=brand)
        if "user" in session:
            return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout",heart=heart,b=brand)
           
        
    
    if request.method=="POST":
        print(request.form)

        if "filter" in request.form:
                print("in filter")
                d={}
                
                if "Men" in request.form:
                    if 'gender' not in d:
                        d['gender']=['Men']
                    else:
                        d['gender'].append('Men')

                    
                if "Women" in request.form:
                    if 'gender' not in d:
                        d['gender']=['Women']
                    else:
                        d['gender'].append('Women')
                
                if "Child" in request.form:
                    if 'gender' not in d:
                        d['gender']=['Child']
                    else:
                        d['gender'].append('Child')
                
                if "Unisex" in request.form:
                    if 'gender' not in d:
                        d['gender']=['Unisex']
                    else:
                        d['gender'].append('Unisex')
                
                
                if '36' in request.form:
                    if 'size' not in d:
                        d['size']=['36']
                    else:
                        d['size'].append('36')
                
                if '37' in request.form:
                    if 'size' not in d:
                        d['size']=['37']
                    else:
                        d['size'].append('37')
                
                if '38' in request.form:
                    if 'size' not in d:
                        d['size']=['38']
                    else:
                        d['size'].append('38')
                
                if '39' in request.form:
                    if 'size' not in d:
                        d['size']=['39']
                    else:
                        d['size'].append('39')
                
                if '40' in request.form:
                    if 'size' not in d:
                        d['size']=['40']
                    else:
                        d['size'].append('40')
                
                if '41' in request.form:
                    if 'size' not in d:
                        d['size']=['41']
                    else:
                        d['size'].append('41')
                
                if '42' in request.form:
                    if 'size' not in d:
                        d['size']=['42']
                    else:
                        d['size'].append('42')
            
            
                for i in brand:
                    if i in request.form:
                        if 'brand' not in d:
                            d['brand']=[i]
                        else:
                            d['brand'].append(i)

            

                p=Product.query.filter_by(category_name='sneakers')
                filtered=[]
                for i in p:
                    if 'gender' in d:
                        if i.gender in d['gender']:
                            filtered.append(i)
                    if 'brand' in d:
                        if i in filtered:
                            if i.brand in d['brand']:
                                pass
                            else:
                                filtered.remove(i)
                        else:
                            if i.brand in d['brand']:
                                filtered.append(i)
                    if 'size' in d:
                        if i in filtered:
                            if "36" in d['size']:
                                if i.size_36>0:
                                    pass
                                else:
                                    filtered.remove(i)
                            if "37" in d['size']:
                                if i.size_37>0:
                                    pass
                                else:
                                    filtered.remove(i)
                            if "38" in d['size']:
                                if i.size_38>0:
                                    pass
                                else:
                                    filtered.remove(i)
                            if "39" in d['size']:
                                if i.size_39>0:
                                    pass
                                else:
                                    filtered.remove(i)
                            if "40" in d['size']:
                                if i.size_40>0:
                                    pass
                                else:
                                    filtered.remove(i)
                            if "41" in d['size']:
                                if i.size_41>0:
                                    pass
                                else:
                                    filtered.remove(i)
                            if "42" in d['size']:
                                if i.size_42>0:
                                    pass
                                else:
                                    filtered.remove(i)                           

                        else:
                            if "36" in d['size']:
                                if i.size_36>0:
                                    filtered.append(i)   
                            if "37" in d['size']:
                                if i.size_37>0 and i not in filtered:
                                    filtered.append(i)   
                            if "38" in d['size']:
                                if i.size_38>0 and i not in filtered:
                                    filtered.append(i)   

                            if "39" in d['size']:
                                if i.size_39>0 and i not in filtered:
                                    filtered.append(i)   
                            if "40" in d['size']:
                                if i.size_40>0 and i not in filtered:
                                    filtered.append(i)   
                            if "41" in d['size']:
                                if i.size_41>0 and i not in filtered:
                                    filtered.append(i)   

                            if "42" in d['size']:
                                if i.size_42>0 and i not in filtered:
                                    filtered.append(i)

                            if "min" in request.form:
                                min=request.form['min']
                                max=request.form['max']
                                if i in filtered:
                                    if int(i.price)>=int(min) and int(i.price)<=int(max):  
                                        pass
                                    else:
                                        filtered.remove(i)
                                else:
                                    if int(i.price)>=int(min) and int(i.price)<=int(max):
                                        filtered.append(i)


                            
            

                if "user" not in session:
                    return render_template('home.html',prod=filtered, max=max, var="Login" ,var1="/user-login",b=brand)
                if "user" in session:
                    return render_template('home.html',prod=filtered, max=max, user=session["user"],var="Logout" ,var1="/logout",heart=heart,b=brand)

                return redirect('/sneakers')

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
        

        '''if "min_price" in request.form:

            p_new=[]
            p=Product.query.filter_by(category_name="sneakers").first()
            for i in p:
                if int(i.price)>=int(request.form["min_price"]) and int(i.price)<=int(request.form["max_price"]):
                    p_new.append(i) 
            print(p_new)
            return render_template('home.html',prod=p_new)'''
        
        if "wishlist" in request.form and "user" in session:
            id=int(request.form['wishlist'])
            p=Product.query.filter_by(id=id).first()
            u=User.query.filter_by(name=session['user']).first()
            w_check=WishList.query.filter_by(user_id=u.id)
            flag=0
            for i in w:
                if i.product_id==id:
                    flag=1
            if flag==0:
                w=WishList(product_id=p.id,user_id=u.id,price=p.price)
                db.session.add(w)
                db.session.commit()
        
        if "wishlist_remove" in request.form and "user" in session:
            id=int(request.form['wishlist_remove'])
            w_check=WishList.query.filter_by(user_id=u.id)
            for i in w_check:
                if i.product_id==id:
                    flag=i
            db.session.delete(flag)
            db.session.commit()
        
        if "sort" in request.form:
            purch=Purchase.query.all()
            p={}
            for i in purch:
                
                if i.product not in p:
                    p[i.product]=i.quantity
                else:
                    p[i.product]+=i.quantity
            p_sort = dict(sorted(p.items(), key=lambda item: item[1], reverse=True))
            prod=[]
            for i in p_sort:
                p=Product.query.filter_by(id=int(i)).first()
                if p.category_name=="sneakers":
                    prod.append(p)
            if request.form["sort"]=="popularity":
                if "user" not in session:
                    return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login",sort_name="popularity")
                if "user" in session:
                    return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout",heart=heart,sort_name="popularity")
            
            if request.form["sort"]=="price_l_h":
                prod = (Product.query.filter(or_(Product.category_name.contains("sneakers"))).order_by(Product.price).all())
                if "user" not in session:
                    return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login",sort_name="Price(Low to High)")
                if "user" in session:
                    return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout",heart=heart,sort_name="Price(Low to High)")
            
            if request.form["sort"]=="price_h_l":
                prod = (Product.query.filter(or_(Product.category_name.contains("sneakers"))).order_by(Product.price.desc()).all())
                if "user" not in session:
                    return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login",sort_name="Price(High to Low)")
                if "user" in session:
                    return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout",heart=heart,sort_name="Price(High to Low)")

            
            
                    
                    
                
                


            
        elif "user" not in session:
            return render_template("home.html", error="You are not logged in.",prod=prod,  max=max)
        return redirect("/sneakers")
    
@app.route('/slides', methods=["GET","POST"])
def slide():
    
    prod=Product.query.filter_by(category_name = "slides")
    if "user" in session: 
        u=User.query.filter_by(name=session["user"]).first()
        w=WishList.query.filter_by(user_id=u.id)
        heart=[]
        for i in prod:
            for j in w:
                if j.product_id==i.id:
                    heart.append(i.id)
    max=0
    for i in prod:
        if int(i.price)>max:
            max=i.price
    
    p=Product.query.all()
    brand=[]
    for i in p:
        if i.brand not in brand:
            brand.append(i.brand)
    if request.method=="GET":
        prod= Product.query.filter_by(category_name = "slides")
        
        if "user" not in session:
            return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login",b=brand)
        if "user" in session:
            return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout",heart=heart,b=brand)
           
        
    
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

            return redirect("/slides")
        if "min_price" in request.form:

            p_new=[]
            p=Product.query.filter_by(category_name="slides").first()
            for i in p:
                if int(i.price)>=int(request.form["min_price"]) and int(i.price)<=int(request.form["max_price"]):
                    p_new.append(i) 
            print(p_new)
            return render_template('home.html',prod=p_new)
        
        if "wishlist" in request.form and "user" in session:
            id=int(request.form['wishlist'])
            p=Product.query.filter_by(id=id).first()
            u=User.query.filter_by(name=session['user']).first()
            w_check=WishList.query.filter_by(user_id=u.id)
            flag=0
            for i in w_check:
                if i.product_id==id:
                    flag=1
            if flag==0:
                w=WishList(product_id=p.id,user_id=u.id,price=p.price)
                db.session.add(w)
                db.session.commit()
        
        if "wishlist_remove" in request.form and "user" in session:
            id=int(request.form['wishlist_remove'])
            w_check=WishList.query.filter_by(user_id=u.id)
            for i in w_check:
                if i.product_id==id:
                    flag=i
            db.session.delete(flag)
            db.session.commit()
        if "sort" in request.form:
            purch=Purchase.query.all()
            p={}
            for i in purch:
                
                if i.product not in p:
                    p[i.product]=i.quantity
                else:
                    p[i.product]+=i.quantity
            p_sort = dict(sorted(p.items(), key=lambda item: item[1], reverse=True))
            prod=[]
            for i in p_sort:
                p=Product.query.filter_by(id=int(i)).first()
                if p.category_name=="slides":
                    prod.append(p)
            if request.form["sort"]=="popularity":
                if "user" not in session:
                    return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login",sort_name="popularity")
                if "user" in session:
                    return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout",heart=heart,sort_name="popularity")
            
            if request.form["sort"]=="price_l_h":
                prod = (Product.query.filter(or_(Product.category_name.contains("slides"))).order_by(Product.price).all())
                if "user" not in session:
                    return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login",sort_name="Price(Low to High)")
                if "user" in session:
                    return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout",heart=heart,sort_name="Price(Low to High)")
            
            if request.form["sort"]=="price_h_l":
                prod = (Product.query.filter(or_(Product.category_name.contains("slides"))).order_by(Product.price.desc()).all())
                if "user" not in session:
                    return render_template('home.html',prod=prod, max=max, var="Login" ,var1="/user-login",sort_name="Price(High to Low)")
                if "user" in session:
                    return render_template('home.html',prod=prod, max=max, user=session["user"],var="Logout" ,var1="/logout",heart=heart,sort_name="Price(High to Low)")
                
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
    current_date = datetime.now()
    six_months_ago_date = current_date - timedelta(days=6*30) 
    date_string = six_months_ago_date.strftime('%Y-%m-%d')
    p=Product.query.filter(Product.date_added<=date_string).all()
    min=0
    min_quant=100000
    for i in p:
        total_q = db.session.query(db.func.sum(Purchase.quantity)).filter(Purchase.product == i.id).scalar()
        if total_q:
            if total_q<min_quant:
                min_quant=total_q
                min=i.id

    if request.method=="GET":
        prod = Product.query.all()
        order = Order.query.all()
        return render_template("product.html",prod=prod,order=order,min=min)
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
     
        
    if "user" in session:
        user = User.query.filter_by(name=session["admin"]).first()      
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
    user=session["admin"]
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
    

    if request.method=="POST" and "admin" in session:
        user = User.query.filter_by(name=session["admin"]).first()
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
    total = 0
    
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
        
        if len(rate_list)!=0:
            total = sum(rate_list)
        if request.method=="GET":
            print("hey")
            if "user" not in session:
                print(rate_list,total)
                return render_template("cart.html",error="",var="Login",var1="/user-login",products = products, total = total)
            if "user" in session:
                return render_template("cart.html",error="",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward)
            
        else:
            if "reward" in request.form:
                a = User.query.filter_by(name=session["user"]).first()
                r=a.reward
                a.reward=0
                db.session.commit()
                print(a.reward)
                return render_template("cart.html",error="",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward,r=r)
            if "discount" in request.form:
                a = User.query.filter_by(name=session["user"]).first()
                coup=request.form['disc_coup']
                if coup=="SNEAKER200":
                    d="200"
                if coup=="SLIDE10":
                    d="10"
                print(a.reward)
                return render_template("cart.html",error="",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward,r=r,d=d)
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
            return render_template("cart.html",error="",var="Login",var1="/user-login",total=total)
           
    return redirect("/")

@app.route("/thank-you")
def final():
    
    return render_template("final_page.html")

@app.route("/product_page/<val>", methods=["GET","POST"])
def product_page(val):
    if request.method=="GET": 
        if "user" in session: 
            u=User.query.filter_by(name=session["user"]).first()
            w=WishList.query.filter_by(user_id=u.id)
            heart="false"
            for j in w:
                if j.product_id==int(val):
                    heart="true"
        p = Product.query.filter_by(id=int(val)).first()
        new_price=p.price
        u=User.query.filter_by(name=session["user"]).first()
        r=Review.query.filter((Review.user_id == u.id) & (Review.prod_id == int(val))).all()
        r_count=Review.query.filter((Review.user_id == u.id) & (Review.prod_id == int(val))).count()
        print(r_count)
        if p.discount:
            new_price=p.price-(p.price*(p.discount/100))
        if "user" not in session:
            return render_template("product_page.html",prod=p,var="Login",var1="/user-login",error="",p=new_price)
        if "user" in session:
            return render_template("product_page.html",prod=p,var="Logout" ,var1="/logout",error="",p=new_price,heart=heart,rev=r,c=r_count)
    
    if request.method=="POST":
        id=int(val)
        if "wishlist" in request.form and "user" in session:
            id=int(request.form['wishlist'])
            p=Product.query.filter_by(id=id).first()
            u=User.query.filter_by(name=session['user']).first()
            w_check=WishList.query.filter_by(user_id=u.id)
            flag=0
            for i in w_check:
                if i.product_id==id:
                    flag=1
            if flag==0:
                w=WishList(product_id=p.id,user_id=u.id,price=p.price)
                db.session.add(w)
                db.session.commit()
            return redirect("/product_page/"+str(id))

        if "wishlist_remove" in request.form and "user" in session:
            id=int(request.form['wishlist_remove'])
            u=User.query.filter_by(name=session['user']).first()
            w_check=WishList.query.filter_by(user_id=u.id)
            for i in w_check:
                if i.product_id==id:
                    flag=i
            db.session.delete(flag)
            db.session.commit()
            return redirect("/product_page/"+str(id))
        
        if "review" in request.form and "user" in session:
            rev=request.form['review']
            rate=request.form["rating"]
            u=User.query.filter_by(name=session["user"]).first()
            r=Review(content=rev,rating=rate,user_id=u.id,prod_id=id)
            db.session.add(r)
            db.session.commit()
        
        if "product" in request.form :
           
            product_id= request.form["product"]
            size = request.form["size"]
            count = request.form["quantity"]
            
            u=User.query.filter_by(name=session['user']).first()
            w_check=WishList.query.filter_by(user_id=u.id)
            for i in w_check:
                if i.product_id==int(product_id):
                    flag=i
                    db.session.delete(flag)
                    db.session.commit()

            product = Product.query.filter_by(id = int(product_id)).first()
            u=User.query.filter_by(name=session["user"]).first()
            cart = Cart.query.filter_by(user_id=u.id)
            prod=Product.query.all()
            flag=1
            for i in cart:
                
                if i.product_id==int(product_id) and i.size==int(size):
                    
                    flag=0
                    if size=="36":
                        if product.size_36<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                            
                    if size=="37":
                        if product.size_37<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="38":
                        if product.size_38<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="39":
                        if product.size_39<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="40":
                        if product.size_40<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="41":
                        if product.size_41<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="42":
                        if product.size_42<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
            if flag==1:
                c = Cart(product_id=product.id, user_id=u.id, quantity=int(count), price=product.price ,size=int(size))
                db.session.add(c)
                db.session.commit()

            return redirect("/product_page/"+str(id))
        return redirect("/product_page/"+str(id))



        
        

   
        

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
            if i.category_name=="sneakers" and val in i.name or val in str(int(i.price)) or val in i.date_added:
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
    a=User.query.filter_by(name=session['user']).first()
    if request.method=="GET":
        a=User.query.filter_by(name=session['user']).first()
        order=Order.query.filter_by(user_id=a.id)
        o_id=[]
        prod=[]
        lst=[]
        main=[]
        prod=[]

        for i in order:
            lst=[]
            print(i.id)
            lst.append(i.id)
            lst.append(i.date_added)
            lst.append(i.total_price)
            lst.append(i.status)
            p=Purchase.query.filter_by(order_id=i.id)
            
            prod=[]
            for i in p:  
                print(i.id)             
                p1=Product.query.filter_by(id=i.id).first()
                prod.append([i.product,p1.brand,p1.name,p1.price,i.size])
            lst.append(prod)

            main.append(lst)
        print(len(main))
        print(main[0])
        reward=a.reward

        
        db.session.commit()


        return render_template("account_page.html",var="Logout" ,var1="/logout",u=a,main=main)
    
    if request.method=="POST":
        if "help" in request.form:
            email=request.form['email']
            message=request.form['msg']
            user=User.query.filter_by(name=session['user']).first()
            id=request.form['help']
            i=Issue(order_id=int(id),content=message,user_id=user.id)
            db.session.add(i)
            db.session.commit()
            send_email(email, message)
            return redirect("/account")
        
        if "return" in request.form:
            user=User.query.filter_by(name=session['user']).first()
            id=request.form['return']
            o=Order.query.filter((Order.user_id == user.id) & (Order.id == int(id))).first()
            o.returned="yes"
            o.status="In return process"
            db.session.commit()

            t=Payments.query.filter_by(order_id=int(id)).first()
            t.refund="yes"
            db.session.commit()

            return redirect("/account")
        
        if "cancel" in request.form:
            user=User.query.filter_by(name=session['user']).first()
            id=request.form['cancel']
            o=Order.query.filter((Order.user_id == user.id) & (Order.id == int(id))).first()
            o.cancelled="yes"
            o.status="Cancelled"
            db.session.commit()

            t=Payments.query.filter_by(order_id=int(id)).first()
            t.refund="yes"
            db.session.commit()

            return redirect("/account")
      





@app.route('/wishlist', methods=["GET","POST"])
def wishlist():
    if "user" in session:
        id= User.query.filter_by(name=session['user']).first()
        w=WishList.query.filter_by(user_id=id.id)
        lst=[]
        for i in w:
            p=Product.query.filter_by(id=i.product_id).first()
            lst.append(p)
    if "user" not in session:
        return render_template("wishlist.html",var="Login" ,var1="/user-login",err="You have to Login.")
    if request.method=="GET":
        if "user" in session:
            a=User.query.filter_by(name=session['user']).first()
            return render_template("wishlist.html",var="Logout" ,var1="/logout",u=a,w=lst)
        if "guest" in session:
            
            return render_template("wishlist.html",var="Login" ,var1="/user-login")

    if request.method=="POST":

        if "wishlist_remove" in request.form and "user" in session:
            id=int(request.form['wishlist_remove'])
            u=User.query.filter_by(name=session['user']).first()
            w_check=WishList.query.filter_by(user_id=u.id)
            for i in w_check:
                if i.product_id==id:
                    flag=i
            db.session.delete(flag)
            db.session.commit()
            return redirect("/wishlist")
        
        if "product" in request.form :
           
            product_id= request.form["product"]
            count = request.form["quantity"]
            size = request.form["size"]
            u=User.query.filter_by(name=session['user']).first()
            w_check=WishList.query.filter_by(user_id=u.id)
            for i in w_check:
                if i.product_id==int(product_id):
                    flag=i
                    db.session.delete(flag)
                    db.session.commit()

            product = Product.query.filter_by(id = int(product_id)).first()
            u=User.query.filter_by(name=session["user"]).first()
            cart = Cart.query.filter_by(user_id=u.id)
            prod=Product.query.all()
            flag=1
            for i in cart:
                
                if i.product_id==int(product_id) and i.size==int(size):
                    
                    flag=0
                    if size=="36":
                        if product.size_36<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                            
                    if size=="37":
                        if product.size_37<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="38":
                        if product.size_38<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="39":
                        if product.size_39<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="40":
                        if product.size_40<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="41":
                        if product.size_41<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
                    if size=="42":
                        if product.size_42<int(count):
                            render_template("wishlist.html", error1="Quantity added is more than the stock available.",prod=prod,max=max,var="Logout")
                        else:
                            i.quantity=i.quantity+int(count)
                            db.session.commit()
            if flag==1:
                c = Cart(product_id=product.id, user_id=u.id, quantity=int(count), price=product.price ,size=int(size))
                db.session.add(c)
                db.session.commit()

            return redirect("/wishlist")

@app.route("/about")
def about():
    if "user" not in session:
        return render_template("about.html",var="Login",var1="/user-login")
    if "user" in session:
        print("hey in session")
        return render_template("about.html",var="Logout" ,var1="/logout")
    
@app.route('/save_payment', methods=['POST'])
def save_payment():
    total = 0
    user = User.query.filter_by(name=session["user"]).first() 
    if "user" in session: 
        user = User.query.filter_by(name=session["user"]).first() 
        cart = Cart.query.filter_by(user_id=user.id)
        order = Order.query.filter_by(user_id=user.id)
        

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
        
        if len(rate_list)!=0:
            total = sum(rate_list)
    
    payment_data = request.json  
    p_id = payment_data.get('paymentId')
    client = razorpay.Client(auth=("rzp_test_XOy0arNBRKuF4z", "eGVaXmXbQbQWygImcrjIaQ8i"))
    a=client.payment.fetch(p_id)
    order=Order(total_price=a['amount']/100,payment_method=a['method'],user_id=user.id)
    db.session.add(order)
    db.session.commit() 

    for product, count, rate,size in products:
        size=size.size
        print(size, product.id)
        if size==36:
            if count<=product.size_36:
                product.size_36-= int(count)
                db.session.commit()
            else:                 
                return render_template("cart.html",error="Quantity added more than stock available.",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward)

            
        if size==37:
            if count<=product.size_37:
                product.size_37-= int(count)
                db.session.commit()
            else:                 
                return render_template("cart.html",error="Quantity added more than stock available.",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward)

        if size==38:
            if count<=product.size_38:
                product.size_38-= int(count)
                db.session.commit()
            else:                 
                return render_template("cart.html",error="Quantity added more than stock available.",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward)
        if size==39:
            if count<=product.size_39:
                product.size_39-= int(count)
                db.session.commit()
            else:                 
                return render_template("cart.html",error="Quantity added more than stock available.",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward)
        if size==40:
            if count<=product.size_40:
                product.size_40-= int(count)
                db.session.commit()
            else:                 
                return render_template("cart.html",error="Quantity added more than stock available.",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward)
        if size==41:
            if count<=product.size_41:
                product.size_41-= int(count)
                db.session.commit()
            else:                 
                return render_template("cart.html",error="Quantity added more than stock available.",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward)
        if size==42:
            if count<=product.size_42:
                product.size_42-= int(count)
                db.session.commit()
            else:                 
                return render_template("cart.html",error="Quantity added more than stock available.",var="Logout" ,var1="/logout",products = products, total = total,reward=user.reward)
        purhcase=Purchase(product=product.id,customer_user=user.id,quantity=count,price=rate,order_id=order.id,size=size)
        db.session.add(purhcase)
        db.session.commit()   

    

    for i in cart:
        db.session.delete(i)
        db.session.commit()
    
    
    
    t1=Payments(payment_id=p_id,payment_method=a['method'],order_id=order.id,total_price=a['amount']/100)
    db.session.add(t1)
    db.session.commit()

    r=user.reward
    r+=round(order.total_price*0.01)
    user.reward=r
    db.session.commit()


    return 'Payment details saved'

mail = Mail(app)
def send_email(sender_email, message):
    recipient1 = 'annitjacob@gmail.com'
    recipient2 = 'paridaaarushi124@gmail.com'
    subject = 'Message from User'
    msg = Message(subject, recipients=[recipient1,recipient2], sender='aerostride222@gmail.com')
    msg.body = f"Sender's Email: {sender_email}\n\nMessage:\n{message}"
    mail.send(msg)
