import os
from datetime import date
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request, render_template, current_app
from app.models import Course, Enrollment, User, ClassSlot, db
from flask_login import login_required, current_user
from app.services.email_services import send_renewal_reminder

student_bp = Blueprint("student", __name__)


@student_bp.route("/student")
@login_required
def student_page():
    return render_template("student.html")


@student_bp.route("/courses-page")
def courses_page():
    return render_template("courses.html")


@student_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()

    result = []
    for course in courses:
        result.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "price": course.price
        })

    return jsonify(result)


@student_bp.route("/my-courses")
@login_required
def my_courses():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()

    result = []

    for e in enrollments:
        course = Course.query.get(e.course_id)

        # send a reminder 3 days before expiry, once only
        if e.paid and e.paid_until:
            days_left = (e.paid_until - date.today()).days

            if 0 <= days_left <= 3 and not e.reminder_sent:
                send_renewal_reminder(
                    current_user.email,
                    current_user.name,
                    course.title,
                    e.paid_until.strftime("%B %d, %Y")
                )
                e.reminder_sent = True
                db.session.commit()

        # auto-expire access if the 30-day period has passed
        if e.paid and e.paid_until and e.paid_until < date.today():
            e.paid = False
            e.reminder_sent = False
            db.session.commit()

        result.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "paid": e.paid,
            "price": course.price,
            "paid_until": e.paid_until.isoformat() if e.paid_until else None
        })

    return jsonify(result)


@student_bp.route("/my-courses/<int:course_id>", methods=["DELETE"])
@login_required
def cancel_enrollment(course_id):
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()

    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404

    if enrollment.paid:
        return jsonify({"error": "Can't remove a course you've already paid for"}), 400

    db.session.delete(enrollment)
    db.session.commit()

    return jsonify({"message": "Removed"})


@student_bp.route("/redeem-code", methods=["POST"])
@login_required
def redeem_code():
    from datetime import timedelta

    data = request.get_json()
    course_id = data.get("course_id")
    code = data.get("code", "").strip().upper()

    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()

    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404

    if not enrollment.access_code or enrollment.access_code != code:
        return jsonify({"error": "Invalid code. Please check with your tutor."}), 400

    enrollment.paid = True
    enrollment.paid_until = date.today() + timedelta(days=30)
    enrollment.reminder_sent = False
    db.session.commit()

    return jsonify({"message": "Access granted!"})


@student_bp.route("/schedule/<int:course_id>")
@login_required
def get_schedule(course_id):
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()

    if not enrollment or not enrollment.paid:
        return jsonify({"error": "You need to pay for this course first"}), 403

    slots = ClassSlot.query.filter_by(course_id=course_id).all()

    return jsonify([{
        "day": s.day,
        "time": s.time,
        "meeting_link": s.meeting_link
    } for s in slots])


@student_bp.route("/profile")
@login_required
def profile_page():
    return render_template("profile.html")


@student_bp.route("/profile/data")
@login_required
def profile_data():
    return jsonify({
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "profile_image": current_user.profile_image
    })


@student_bp.route("/profile/upload", methods=["POST"])
@login_required
def upload_profile_picture():
    if "photo" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["photo"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    allowed_extensions = {"png", "jpg", "jpeg", "gif"}
    ext = file.filename.rsplit(".", 1)[-1].lower()

    if ext not in allowed_extensions:
        return jsonify({"error": "Only image files are allowed (png, jpg, jpeg, gif)"}), 400

    filename = secure_filename(f"user_{current_user.id}.{ext}")
    upload_folder = os.path.join(current_app.static_folder, "uploads")
    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    current_user.profile_image = f"uploads/{filename}"
    db.session.commit()

    return jsonify({"message": "Profile picture updated", "profile_image": current_user.profile_image})