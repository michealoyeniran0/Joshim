from flask import Blueprint, request, jsonify, redirect, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import db, User
import secrets
from datetime import datetime, timedelta
from app.services.email_services import send_password_reset_email
from app import limiter
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/')
def home():
    return render_template('landing.html')
# -------------------------
# REGISTER
# -------------------------
@auth_bp.route("/register-page")
def register_page():
    # This renders the HTML file from your /templates folder
    return render_template("register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    child_name = data.get("child_name")
    child_class_level = data.get("child_class_level")
    course_id = data.get("course_id")
    requested_course = data.get("requested_course")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name,
        email=email,
        phone=phone,
        password_hash=hashed_password,
        child_name=child_name,
        child_class_level=child_class_level,
        requested_course=requested_course
    )

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    if course_id:
        from app.models import Enrollment
        enrollment = Enrollment(user_id=new_user.id, course_id=course_id, paid=False)
        db.session.add(enrollment)
        db.session.commit()

    return jsonify({"message": "Account created successfully"})
# -------------------------
# LOGIN
# -------------------------
@auth_bp.route("/login-page")
def login_page():
    return render_template("login.html")
@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user)

    return jsonify({"message": "Login successful", "role": user.role})
# -------------------------
# LOGOUT
# -------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
@auth_bp.route("/legal")
def legal_page():
    return render_template("legal.html")

#-----------------
#forget password
#------------------
@auth_bp.route("/forgot-password")
def forgot_password_page():
    return render_template("forgot_password.html")

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "If the email exists, a reset link has been sent."
        })

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)

    db.session.commit()

    reset_link = url_for(
        "auth.reset_password",
        token=token,
        _external=True
    )

    send_password_reset_email(
        user.email,
        user.name,
        reset_link
    )

    return jsonify({
        "message": "Password reset link sent."
    })

@auth_bp.route("/reset-password/<token>")
def reset_password(token):

    user = User.query.filter_by(
        reset_token=token
    ).first()

    if not user:
        return "Invalid reset link", 400

    if user.reset_token_expiry < datetime.utcnow():
        return "Reset link expired", 400

    return render_template(
        "reset_password.html",
        token=token
    )

@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password_submit(token):

    data = request.get_json()

    password = data.get("password")

    user = User.query.filter_by(
        reset_token=token
    ).first()

    if not user:
        return jsonify({
            "error":"Invalid reset link"
        }),400

    if user.reset_token_expiry < datetime.utcnow():
        return jsonify({
            "error":"Reset link expired"
        }),400

    user.password_hash = generate_password_hash(password)

    user.reset_token = None
    user.reset_token_expiry = None

    db.session.commit()

    return jsonify({
        "message":"Password changed successfully"
    })
