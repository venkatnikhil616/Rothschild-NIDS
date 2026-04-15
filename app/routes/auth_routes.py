from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, logout_user, login_required
from database.db import SessionLocal
from database.models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    db = SessionLocal()

    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = db.query(User).filter(User.username == username).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect("/dashboard/")
            else:
                error = "❌ Invalid username or password"

        return render_template("login.html", error=error)

    finally:
        db.close()


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
