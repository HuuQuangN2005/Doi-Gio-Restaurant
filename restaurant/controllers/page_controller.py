from flask import render_template, redirect


def landing():
    return render_template("pages/landing/index.html")
