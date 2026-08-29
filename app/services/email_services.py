from flask_mail import Message
from app import mail


def send_payment_confirmation(user_email, user_name, course_title):
    try:
        msg = Message(
            subject=f"You're enrolled in {course_title}! 🎉",
            recipients=[user_email],
            body=(
                f"Hi {user_name},\n\n"
                f"Your payment was successful and you now have full access "
                f"to \"{course_title}\" on Joshim.\n\n"
                f"Log in anytime to watch your lessons:\n"
                f"http://127.0.0.1:5000/login-page\n\n"
                f"Talk soon,\n"
                f"The Joshim Team"
            )
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False
def send_renewal_reminder(user_email, user_name, course_title, paid_until):
    try:
        msg = Message(
            subject=f"Your access to {course_title} expires soon",
            recipients=[user_email],
            body=(
                f"Hi {user_name},\n\n"
                f"Your access to \"{course_title}\" on Joshim expires on "
                f"{paid_until}. To keep classes going without interruption, "
                f"please renew before then.\n\n"
                f"Log in to renew:\n"
                f"http://127.0.0.1:5000/login-page\n\n"
                f"Talk soon,\n"
                f"The Joshim Team"
            )
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Reminder email failed: {e}")
        return False
def send_password_reset_email(user_email, user_name, reset_link):
    try:
        msg = Message(
            subject="Reset your Joshim password",
            recipients=[user_email],
            body=(
                f"Hi {user_name},\n\n"
                f"We received a request to reset your Joshim password.\n\n"
                f"Click the link below to create a new password:\n\n"
                f"{reset_link}\n\n"
                f"This link expires in 1 hour.\n\n"
                f"If you did not request this, ignore this email.\n\n"
                f"Talk soon,\n"
                f"The Joshim Team"
            )
        )

        mail.send(msg)
        return True

    except Exception as e:
        print(f"Password reset email failed: {e}")
        return False