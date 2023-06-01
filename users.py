from DBMS import users_db, forgot_password_db
from flask import request, render_template, url_for, redirect, session
from main import app

@app.route("/change-details", methods=["GET", "POST"])
def change_details():
    if session.get("change_details"):
        session["change_details"] = False
        if request.method == "POST":
            details = request.get_json()
            if details is not None:
                method = details.get("method")
                broker = details.get("broker")
                users_db.update_user(session["uid"],method=method,broker=broker)
                return "", 200
        return "No JSON payload received", 400
    else:
        return "Access denied", 403
@app.route("/dashboard")
def dashboard() -> str:
    """Handle the dashboard route."""
    data=users_db.read_user(session["uid"])
    if "uid" in session and "user" in session:
        return '''this is dashboard <button onclick="window.location='/logout'">Logout</button><p>'''+data[6]+" "+data[7]+"</p>"
    else:
        return redirect(url_for("login"))