from sqlalchemy import case
from restaurant.services import *
from restaurant.models.sql import UserRole, Employee
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from restaurant import app
from flask import render_template, redirect, request

import math

from restaurant.admin import *

login = LoginManager(app)
login.login_view = "login"

@login.user_loader
def load_user(uuid):
    user = Employee.query.filter_by(uuid=uuid).first()
    return user


@app.route("/", methods=["get"])
def index():
    foods = product_service.get_foods()

    page = request.args.get("page")
    if not page:
        page = 1
    page = int(page)
    page_size = app.config["PAGE_SIZE_AT_MAINMENU"]
    page_quatity = int(math.ceil(len(foods) / app.config["PAGE_SIZE_AT_MAINMENU"]))
    foods = foods[page_size * (page - 1) : page_size * (page - 1) + page_size]
    return render_template(
        "pages/landing/index.html",
        foods=foods,
        page=page,
        page_size=page_size,
        page_quatity=page_quatity,
    )


def my_redict(user):
    
    match user.role:
        case UserRole.ADMIN | UserRole.MANAGER:
            return redirect("/admin")
        case _:
            return redirect("/website/" + str(user.uuid))


@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return my_redict(current_user)

    err_msg = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = user_service.authenticate(username=username, password=password)

        if user:
            login_user(user)
            return my_redict(user)

        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template("pages/login/index.html", err_msg=err_msg)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect("/")


@app.route("/website", methods=["GET"])
def allias():
    return redirect("/login")


@app.route("/website/<uuid>/profile", methods=["GET"])
@login_required
def profile(uuid):

    return render_template("pages/website/profile/profile.html", user=current_user)

@app.route("/website/<uuid>", methods=["GET"])
@login_required
def website(uuid):

    return redirect(f"/website/{uuid}/profile")

@app.route("/website/<uuid>/order", methods=["GET"])
@login_required
def order(uuid):
    page = request.args.get("page", 1, type=int)
    
    tables_all = user_service.get_tables()
    page_size = int(app.config["PAGE_SIZE_OF_CHOOSE_TABLE"])
    
    number_of_pages = int(math.ceil(len(tables_all) / page_size))
    
    start = (page - 1) * page_size
    end = start + page_size
    tables_paginated = tables_all[start:end]
    
    return render_template(
        "pages/website/order/tables.html",
        user=current_user,
        page=page, 
        tables=tables_paginated,
        number_of_pages=number_of_pages
    )

@app.route("/order/<int:table_id>")
@login_required
def ChonMonAn(table_id):
    if current_user.role != UserRole.WAITER:
        return redirect("/login")
    cate = request.args.get("cate")
    return render_template("pages/website/order/order.html",
                           categories=product_service.get_all_categories(),
                           foods=product_service.get_food_by_category(cate),
                           table_id=table_id)