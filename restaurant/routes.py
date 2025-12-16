from restaurant import app
from restaurant.controllers import user_controller

from flask import render_template, request, redirect, session, jsonify
from flask_login import current_user, login_user, logout_user

from restaurant.database.sql.models.user import UserRole

@app.route('/', methods = ["get"])
def index():
    return render_template('pages/landing/index.html')

@app.route('/admin', methods=["GET","POST","DELETE","PUT","PATCH"])
def dashboard():
    
    return render_template("admin/dashboard/index.html")


@app.route("/login", methods=["get", "post"])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    err_msg = None
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("password")

        user = user_controller.authenticate(username=username, password=password)

        if user:
            login_user(user)
            
            if user.user_role  == UserRole.ADMIN or user.user_role == UserRole.MANAGER:
                return redirect("/admin")
            else:
                return redirect("/")
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template("pages/login/index.html", err_msg=err_msg)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")