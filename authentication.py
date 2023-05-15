import re
from DBMS import users_db
from flask import request, render_template,url_for,redirect,session
from main import app



def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def validate_mobile(mobile):
    pattern = r'^\d{10}$'
    return re.match(pattern, mobile)

def check_password_strength(password):
    if len(password) < 6:
        return False
        
    return True

def check_existing_user(email, mobile):
    users = users_db.read_user()  
    
    for user in users:
        if user[2] == email or user[3] == mobile:
            return True  
    
    return False  

def check_cred(email, password):
    users = users_db.read_user()
    
    for user in users:
        if (user[2] == email or user[3] == email) and user[4] == password:
            return True, user[0], user[1]
    
    return False, None, None


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        business_name = request.form.get("businessName")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")
        
        if not validate_email(email):
            return "Invalid email format",400
        
        if not validate_mobile(mobile):
            return "Invalid mobile number format",400
        
        if check_existing_user(email, mobile):
            return "Email or mobile number already exists",409
        
        if not check_password_strength(password):
            return "Password is not strong enough",400
        
        if password != confirm_password:
            return "Passwords do not match",400
        

        session["uid"]=users_db.insert_user(business_name,email,mobile,password)
        session["verified"]=0
        #send otp here
        return "User registered successfully"
    
    return render_template("signup.html")

@app.route("/otp",methods=["GET","POST"])
def otp():
    if ("verified" in session ):
        if request.method=="POST":
            otp=request.form.get('otp')
            if str(otp)=="123456":
                users_db.update_user(uid=session["uid"],verified=1)
                session['verified']=1
                data=users_db.read_user(uid=session["uid"])
                session["user"]=data[1]
                return "Success!OTP Verified",200
            else:
                return "OTP Invalid!",405
        elif session["verified"]==0:
            return render_template("otp.html")
        else:
            return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("dashboard"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="POST":
        users = users_db.read_user()  
        email = request.form.get('email')
        password = request.form.get('password')
        authen,uid,name=check_cred(email,password) 
        if authen:
            session["uid"]=uid
            session["user"]=name
            return redirect(url_for("dashboard"))
        else:
            return "Credentials Invalid Or Mismatch!",405
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if ("uid" in session) and ("user" in session):
        return "this is dashboard"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))