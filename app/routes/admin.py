import random
import string
from functools import wraps
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.models import db, Course, Enrollment, User, ClassSlot, Payment
from datetime import date, timedelta

admin_bp = Blueprint("admin", __name__)


# Only lets logged-in users with role == "admin" through.
# Use this on every route that creates/edits/deletes data.
def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            return jsonify({"error": "Admins only"}), 403
        return f(*args, **kwargs)
    return wrapper


# =========================
# ADMIN PAGE (FRONTEND)
# =========================
@admin_bp.route("/admin")
@admin_required
def admin_page():
    return render_template("admin.html")


# =========================
# CREATE COURSE
# =========================
@admin_bp.route("/admin/course", methods=["POST"])
@admin_required
def create_course():
    data = request.get_json()

    new_course = Course(
        title=data.get("title"),
        description=data.get("description"),
        price=data.get("price"),
        video_url=data.get("video_url"),
        is_published=data.get("is_published", False)
    )

    db.session.add(new_course)
    db.session.commit()

    return jsonify({
        "message": "Course created successfully",
        "course_id": new_course.id
    })


# =========================
# GET ALL COURSES
# =========================
@admin_bp.route("/admin/courses", methods=["GET"])
@admin_required
def get_all_courses():
    courses = Course.query.all()

    return jsonify([
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "price": c.price,
            "video_url": c.video_url,
            "is_published": c.is_published
        }
        for c in courses
    ])


# =========================
# UPDATE COURSE
# =========================
@admin_bp.route("/admin/course/<int:id>", methods=["PUT"])
@admin_required
def update_course(id):
    course = Course.query.get(id)

    if not course:
        return jsonify({"error": "Course not found"}), 404

    data = request.get_json() or {}

    course.title = data.get("title", course.title)
    course.description = data.get("description", course.description)
    course.price = data.get("price", course.price)
    course.video_url = data.get("video_url", course.video_url)

    db.session.commit()

    return jsonify({"message": "Course updated"})


# =========================
# DELETE COURSE
# =========================
@admin_bp.route("/admin/course/<int:id>", methods=["DELETE"])
@admin_required
def delete_course(id):
    course = Course.query.get(id)

    if not course:
        return jsonify({"error": "Course not found"}), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({"message": "Course deleted"})
@admin_bp.route("/admin/payments", methods=["GET"])
@admin_required
def view_all_payments():
    enrollments = Enrollment.query.all()
    result = []
    for e in enrollments:
        student = User.query.get(e.user_id)
        course = Course.query.get(e.course_id)
        result.append({
            "enrollment_id": e.id,
            "student_name": student.name if student else "Unknown",
            "student_email": student.email if student else "Unknown",
            "course_title": course.title if course else "Unknown",
            "paid": e.paid
        })
    return jsonify(result)

@admin_bp.route("/admin/mark-paid/<int:enrollment_id>", methods=["POST"])
@admin_required
def mark_paid(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404

    enrollment.paid = True
    enrollment.paid_until = date.today() + timedelta(days=30)
    db.session.commit()
    return jsonify({"message": "Marked as paid"})

@admin_bp.route("/admin/course/<int:course_id>/slots", methods=["GET"])
@admin_required
def get_slots(course_id):
    slots = ClassSlot.query.filter_by(course_id=course_id).all()
    return jsonify([{
        "id": s.id,
        "day": s.day,
        "time": s.time,
        "meeting_link": s.meeting_link
    } for s in slots])


@admin_bp.route("/admin/course/<int:course_id>/slots", methods=["POST"])
@admin_required
def add_slot(course_id):
    data = request.get_json()

    slot = ClassSlot(
        course_id=course_id,
        day=data.get("day"),
        time=data.get("time"),
        meeting_link=data.get("meeting_link"),
        max_students=data.get("max_students", 20)
    )

    db.session.add(slot)
    db.session.commit()

    return jsonify({"message": "Class slot added"})


@admin_bp.route("/admin/slot/<int:slot_id>", methods=["DELETE"])
@admin_required
def delete_slot(slot_id):
    slot = ClassSlot.query.get(slot_id)
    if not slot:
        return jsonify({"error": "Slot not found"}), 404

    db.session.delete(slot)
    db.session.commit()
    return jsonify({"message": "Slot removed"})

@admin_bp.route("/admin/enrollment/<int:enrollment_id>/generate-code", methods=["POST"])
@admin_required
def generate_code(enrollment_id):

    enrollment = db.session.get(
        Enrollment,
        enrollment_id
    )

    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404

    code = "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )

    enrollment.access_code = code

    db.session.commit()

    return jsonify({
        "message": "Code generated",
        "code": code
    })
@admin_bp.route("/admin/enrollments")
@admin_required
def admin_enrollments():

    enrollments = Enrollment.query.order_by(
        Enrollment.enrolled_at.desc()
    ).all()

    return render_template(
        "admin_enrollments.html",
        enrollments=enrollments
    )
@admin_bp.route("/admin/course-requests", methods=["GET"])
@admin_required
def get_course_requests():
    users = User.query.filter(User.requested_course.isnot(None)).all()

    return jsonify([{
        "name": u.name,
        "email": u.email,
        "phone": u.phone,
        "child_name": u.child_name,
        "requested_course": u.requested_course
    } for u in users])

@admin_bp.route("/admin/users")
@login_required
def users():

    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    return render_template(
        "admin_users.html",
        users=users
    )
