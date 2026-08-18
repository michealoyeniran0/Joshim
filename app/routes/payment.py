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

    if not data:
        return jsonify({"error": "Invalid request"}), 400


    course_id = data.get("course_id")


    if not course_id:
        return jsonify({"error": "Course ID required"}), 400



    course = Course.query.get(course_id)


    if not course:
        return jsonify({"error": "Course not found"}), 404



    existing = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()



    if existing:
        return jsonify({
            "message": "Already enrolled. Proceed to payment."
        })



    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=course_id,
        paid=False
    )


    db.session.add(enrollment)

    db.session.commit()



    return jsonify({
        "message": "Enrollment created. Proceed to payment."
    })





@payment_bp.route("/pay", methods=["POST"])
@login_required
def pay():

    data = request.get_json()


    if not data:
        return jsonify({"error": "Invalid request"}), 400



    course_id = data.get("course_id")



    course = Course.query.get(course_id)



    if not course:
        return jsonify({
            "error": "Course not found"
        }), 404





    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id
    ).first()



    if not enrollment:
        return jsonify({
            "error": "Please enroll before payment"
        }), 400





    existing_payment = Payment.query.filter_by(
        user_id=current_user.id,
        course_id=course_id,
        status="success"
    ).first()



    if existing_payment:
        return jsonify({
            "error": "Payment already completed"
        }), 400





    if not course.price or int(course.price) <= 0:
        return jsonify({
            "error": "Invalid course price"
        }), 400





    amount_kobo = int(course.price) * 100





    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json"
    }





    payload = {

        "email": current_user.email,

        "amount": amount_kobo,

        "callback_url":
            request.host_url.rstrip("/") + "/payment/verify",

        "metadata": {

            "course_id": course.id,

            "user_id": current_user.id

        }

    }





    try:

        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            json=payload,
            headers=headers,
            timeout=15
        )


        result = response.json()



    except Exception:

        return jsonify({
            "error": "Payment service unavailable"
        }), 500





    if not result.get("status"):

        return jsonify({
            "error": "Could not start payment"
        }), 400





    reference = result["data"]["reference"]





    payment = Payment(

        user_id=current_user.id,

        course_id=course.id,

        amount=course.price,

        status="pending",

        reference=reference

    )



    db.session.add(payment)

    db.session.commit()





    return jsonify({

        "authorization_url":
            result["data"]["authorization_url"]

    })








@payment_bp.route("/payment/verify", methods=["GET"])
@login_required
def verify_payment():


    reference = request.args.get("reference")



    if not reference:

        return "Missing payment reference", 400





    payment = Payment.query.filter_by(
        reference=reference
    ).first()



    if not payment:

        return "Payment record not found", 404





    headers = {

        "Authorization":
            f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}"

    }





    try:

        response = requests.get(

            f"https://api.paystack.co/transaction/verify/{reference}",

            headers=headers,

            timeout=15

        )


        result = response.json()



    except Exception:

        return "Payment verification failed", 500





    if not (
        result.get("status")
        and result.get("data", {}).get("status") == "success"
    ):

        return redirect("/student")





    if payment.status != "success":


        payment.status = "success"



        enrollment = Enrollment.query.filter_by(

            user_id=payment.user_id,

            course_id=payment.course_id

        ).first()



        if enrollment:


            enrollment.paid = True

            enrollment.paid_until = date.today() + timedelta(days=30)



        db.session.commit()





        course = Course.query.get(payment.course_id)

        payer = User.query.get(payment.user_id)



        if course and payer:

            try:

                send_payment_confirmation(

                    payer.email,

                    payer.name,

                    course.title

                )

            except Exception:

                pass






    return redirect("/student")