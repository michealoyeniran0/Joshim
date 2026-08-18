from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


# ---------------------------
# USERS TABLE
# ---------------------------
class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    child_name = db.Column(
        db.String(120),
        nullable=True
    )

    child_class_level = db.Column(
        db.String(50),
        nullable=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    phone = db.Column(
        db.String(20)
    )

    password_hash = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="student",
        nullable=False
    )

    requested_course = db.Column(
        db.String(200),
        nullable=True
    )

    profile_image = db.Column(
        db.String(200),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    enrollments = db.relationship(
        "Enrollment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    payments = db.relationship(
        "Payment",
        back_populates="user"
    )




# ---------------------------
# COURSES TABLE
# ---------------------------
class Course(db.Model):

    __tablename__ = "courses"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(200),
        nullable=False
    )


    video_url = db.Column(
        db.String(300),
        nullable=True
    )


    description = db.Column(
        db.Text
    )


    price = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )


    is_published = db.Column(
        db.Boolean,
        default=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    lessons = db.relationship(
        "Lesson",
        back_populates="course",
        cascade="all, delete-orphan"
    )


    enrollments = db.relationship(
        "Enrollment",
        back_populates="course"
    )


    payments = db.relationship(
        "Payment",
        back_populates="course"
    )


    slots = db.relationship(
        "ClassSlot",
        back_populates="course",
        cascade="all, delete-orphan"
    )




# ---------------------------
# LESSONS TABLE
# ---------------------------
class Lesson(db.Model):

    __tablename__ = "lessons"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    course_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "courses.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    title = db.Column(
        db.String(200)
    )


    video_url = db.Column(
        db.String(500)
    )


    lesson_order = db.Column(
        db.Integer
    )


    course = db.relationship(
        "Course",
        back_populates="lessons"
    )




# ---------------------------
# PAYMENTS TABLE
# ---------------------------
class Payment(db.Model):

    __tablename__ = "payments"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id"
        ),
        nullable=False
    )


    course_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "courses.id"
        ),
        nullable=False
    )


    amount = db.Column(
        db.Integer,
        nullable=False
    )


    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )


    reference = db.Column(
        db.String(200),
        unique=True,
        index=True,
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    user = db.relationship(
        "User",
        back_populates="payments"
    )


    course = db.relationship(
        "Course",
        back_populates="payments"
    )




# ---------------------------
# ENROLLMENTS TABLE
# ---------------------------
class Enrollment(db.Model):

    __tablename__ = "enrollments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id")
    )

    user = db.relationship(
        "User",
        back_populates="enrollments"
    )

    course = db.relationship(
        "Course",
        back_populates="enrollments"
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    enrolled_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    paid = db.Column(
        db.Boolean,
        default=False
    )

    access_code = db.Column(
        db.String(20),
        nullable=True
    )

    paid_until = db.Column(
        db.Date,
        nullable=True
    )

    reminder_sent = db.Column(
        db.Boolean,
        default=False
    )



# ---------------------------
# CLASS SLOTS TABLE
# ---------------------------
class ClassSlot(db.Model):

    __tablename__ = "class_slots"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    course_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "courses.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    day = db.Column(
        db.String(20)
    )


    time = db.Column(
        db.String(20)
    )


    max_students = db.Column(
        db.Integer
    )


    meeting_link = db.Column(
        db.String(300)
    )


    course = db.relationship(
        "Course",
        back_populates="slots"
    )




# ---------------------------
# BOOKINGS TABLE
# ---------------------------
class Booking(db.Model):

    __tablename__ = "bookings"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id"
        )
    )


    slot_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "class_slots.id"
        )
    )


    status = db.Column(
        db.String(20),
        default="confirmed"
    )


    booked_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )