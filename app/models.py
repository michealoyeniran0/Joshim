from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


# ---------------------------
# USERS TABLE
# ---------------------------
class User(db.Model,UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    child_name = db.Column(db.String(120), nullable=True)

    child_class_level = db.Column(db.String(50), nullable=True)

    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(20))

    password_hash = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="student")

    requested_course = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile_image = db.Column(db.String(200), nullable=True)

# ---------------------------
# COURSES TABLE
# ---------------------------
class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    
    video_url = db.Column(db.String(300), nullable=True)

    description = db.Column(db.Text)

    price = db.Column(db.Integer, default=0)

    is_published = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------
# LESSONS TABLE
# ---------------------------
class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    title = db.Column(db.String(200))

    video_url = db.Column(db.String(500))

    lesson_order = db.Column(db.Integer)


# ---------------------------
# PAYMENTS TABLE
# ---------------------------
class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    amount = db.Column(db.Integer)

    status = db.Column(db.String(20))

    reference = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------
# ENROLLMENTS TABLE
# ---------------------------
class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    active = db.Column(db.Boolean, default=True)

    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    paid = db.Column(db.Boolean, default=False)

    access_code = db.Column(db.String(20), nullable=True)

    paid_until = db.Column(db.Date, nullable=True)
    
    reminder_sent = db.Column(db.Boolean, default=False)


# ---------------------------
# CLASS SLOTS TABLE
# ---------------------------
class ClassSlot(db.Model):
    __tablename__ = "class_slots"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    day = db.Column(db.String(20))

    time = db.Column(db.String(20))

    max_students = db.Column(db.Integer)

    meeting_link = db.Column(db.String(300), nullable=True)


# ---------------------------
# BOOKINGS TABLE
# ---------------------------
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    slot_id = db.Column(db.Integer, db.ForeignKey("class_slots.id"))

    booked_at = db.Column(db.DateTime, default=datetime.utcnow)