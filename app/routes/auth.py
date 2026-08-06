from flask import Blueprint, request, jsonify, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import db, User
from flask import render_template
from app import limiter

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