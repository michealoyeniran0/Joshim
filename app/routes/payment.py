import requests
from flask import Blueprint, request, jsonify, redirect, current_app
from app.models import db, Enrollment, Course, Payment, User
from app.services.email_services import send_payment_confirmation
from flask_login import current_user, login_required
from datetime import date, timedelta

payment_bp = Blueprint("payment", __name__)


@payment_bp.route("/enroll", methods=["POST"])
@login_required
def enroll():
    data = request.get_json()
    course_id = data.get("course_id")

    existing = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()

    if existing:
        return jsonify({"message": "Already enrolled. Proceed to payment."})

    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course_id,
        paid=False
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({"message": "Enrollment created. Proceed to payment."})


@payment_bp.route("/pay", methods=["POST"])
@login_required
def pay():
    data = request.get_json()
    course_id = data.get("course_id")

    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()

    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Paystack works in kobo, not naira -> multiply by 100
    amount_kobo = int(course.price) * 100

    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json"
    }

    payload = {
        "email": current_user.email,
        "amount": amount_kobo,
        "callback_url": request.host_url.rstrip("/") + "/payment/verify",
        "metadata": {
            "course_id": course_id,
            "user_id": current_user.id
        }
    }

    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        json=payload,
        headers=headers
    )

    result = response.json()

    if not result.get("status"):
        return jsonify({"error": "Could not start payment. Try again."}), 400

    reference = result["data"]["reference"]

    payment = Payment(
        user_id=current_user.id,
        course_id=course_id,
        amount=course.price,
        status="pending",
        reference=reference
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({"authorization_url": result["data"]["authorization_url"]})


@payment_bp.route("/payment/verify", methods=["GET"])
@login_required
def verify_payment():
    reference = request.args.get("reference")

    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}"
    }

    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers=headers
    )

    result = response.json()

    payment = Payment.query.filter_by(reference=reference).first()

    if not payment:
        return "Payment record not found", 404

    if result.get("status") and result["data"]["status"] == "success":
        payment.status = "success"

    enrollment = Enrollment.query.filter_by(
        user_id=payment.user_id,
        course_id=payment.course_id
    ).first()

    if enrollment:
        enrollment.paid = True
        enrollment.paid_until = date.today() + timedelta(days=30)

    db.session.commit()

    # Send confirmation email (won't break the payment if it fails)
    course = Course.query.get(payment.course_id)
    payer = User.query.get(payment.user_id)
    send_payment_confirmation(payer.email, payer.name, course.title)

    return redirect("/student")