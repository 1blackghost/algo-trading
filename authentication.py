import re
from DBMS import users_db,forgot_password_db
from flask import request, render_template,url_for,redirect,session
from main import app
from utils.forgot_password import send_otp


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

def get_cred(email):
    users = users_db.read_user()

    for user in users:
        if (user[2] == email or user[3] == email) and user[5]==1:
            return True, user[0], user[1],user[2],user[3]

    return False, None, None,None,None

def check_cred(email, password):
    users = users_db.read_user()

    for user in users:
        if (user[2] == email or user[3] == email) and user[4] == password and user[5]==1:
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
        if "forgot" in session:
            session.pop("forgot")
        #send otp here
        return "User registered successfully"

    return render_template("signup.html")

@app.route("/otp",methods=["GET","POST"])
def otp():
    if request.method=="POST":
        if ("verified" in session ):
                if session["verified"]==0:
                    otp=request.form.get('otp')
                    if str(otp)=="123456":
                        users_db.update_user(uid=session["uid"],verified=1)
                        session['verified']=1
                        data=users_db.read_user(uid=session["uid"])
                        session["user"]=data[1]
                        return "Success!OTP Verified",200
                    else:
                        return "OTP Invalid!",400
        if "forgot" in session:
            if session["forgot"]==1:
                otp=request.form.get("otp")
                data=forgot_password_db.read_user(session["uid"])
                true_otp=data[4]
                if str(otp)==str(true_otp):
                    session["able"]=1
                    return "ok",200
                else:
                    return "OTP Invalid!",400
    elif ("verified" in session or "forgot" in session):
        return render_template("otp.html")
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
            return "Succcess!",200
        else:
            return "Credentials Invalid Or Mismatch!",400
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if ("uid" in session) and ("user" in session):
        return '''this is dashboard <button onclick="window.location='/logout'">Logout</button>'''
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/forgot_password",methods=["GET","POST"])
def forgot_password():
    if request.method=="POST":
        user = request.form.get('email')
        exists,uid,name,email,mobile=get_cred(user)
        if exists:
            otp=send_otp(email)

            forgot_password_db.insert_user(uid,name,email,mobile,otp)


            session["forgot"]=1
            session["uid"]=uid
            if "verified" in session:
                session.pop("verified")
            return "OTP Sent!"
        else:
            return "User Doesn't Exists Or Unverfied!"

    return render_template("forgot_password.html")

@app.route("/reset_password",methods=["GET","POST"])
def reset_password():
    if request.method=="POST":
        if "able" in session:
            if session["able"]==1:
                    password = request.form.get("password")
                    confirm_password = request.form.get("confirmPassword")
                    if not check_password_strength(password):
                        return "Password is not strong enough",400

                    elif password != confirm_password:
                        return "Passwords do not match",400
                    users_db.update_user(session["uid"],password=password)
                    session.pop("able")
                    return "Success!Password Changed",200


    elif "able" in session:
        return render_template("reset_password.html")
    else:
        return redirect(url_for("dashboard"))
