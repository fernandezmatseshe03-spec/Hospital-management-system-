from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
from datetime import datetime, date

app = Flask(__name__)

# Change this before production deployment
app.config["SECRET_KEY"] = "change-this-secret-key"

DATABASE = "hospital.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)

    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            date_of_birth TEXT,
            gender TEXT,
            address TEXT,
            emergency_contact TEXT,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'patient',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            staff_id INTEGER,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            department TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            notes TEXT,
            created_at TEXT NOT NULL,

            FOREIGN KEY(patient_id)
                REFERENCES users(id),

            FOREIGN KEY(staff_id)
                REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS medical_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            staff_response TEXT,
            created_at TEXT NOT NULL,

            FOREIGN KEY(patient_id)
                REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            staff_id INTEGER NOT NULL,
            diagnosis TEXT NOT NULL,
            treatment TEXT,
            prescription TEXT,
            notes TEXT,
            created_at TEXT NOT NULL,

            FOREIGN KEY(patient_id)
                REFERENCES users(id),

            FOREIGN KEY(staff_id)
                REFERENCES users(id)
        );
    """)

    # Create demo administrator
    existing_admin = db.execute(
        "SELECT id FROM users WHERE email = ?",
        ("admin@carepoint.test",)
    ).fetchone()

    if not existing_admin:
        db.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                phone,
                password,
                role,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "System Administrator",
                "admin@carepoint.test",
                "0700000000",
                generate_password_hash("Admin123!"),
                "admin",
                datetime.now().isoformat(timespec="seconds")
            )
        )

    db.commit()
    db.close()


# =========================================================
# AUTHENTICATION HELPERS
# =========================================================

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped


def roles_required(*roles):
    def decorator(view):

        @wraps(view)
        def wrapped(*args, **kwargs):

            if "user_id" not in session:
                flash("Please log in first.", "warning")
                return redirect(url_for("login"))

            if session.get("role") not in roles:
                flash(
                    "You do not have permission to access that page.",
                    "danger"
                )

                return redirect(url_for("dashboard"))

            return view(*args, **kwargs)

        return wrapped

    return decorator


@app.context_processor
def inject_user():

    return {
        "logged_in": "user_id" in session,
        "current_user": session.get("full_name"),
        "current_role": session.get("role")
    }


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# REGISTRATION
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        date_of_birth = request.form.get("date_of_birth", "").strip()
        gender = request.form.get("gender", "").strip()
        address = request.form.get("address", "").strip()
        emergency_contact = request.form.get(
            "emergency_contact",
            ""
        ).strip()

        password = request.form.get("password", "")
        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not full_name or not email or not password:
            flash(
                "Please complete all required fields.",
                "danger"
            )

            return render_template("register.html")

        if password != confirm_password:
            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template("register.html")

        if len(password) < 8:
            flash(
                "Password must contain at least 8 characters.",
                "danger"
            )

            return render_template("register.html")

        db = get_db()

        try:

            db.execute(
                """
                INSERT INTO users
                (
                    full_name,
                    email,
                    phone,
                    date_of_birth,
                    gender,
                    address,
                    emergency_contact,
                    password,
                    role,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'patient', ?)
                """,
                (
                    full_name,
                    email,
                    phone,
                    date_of_birth,
                    gender,
                    address,
                    emergency_contact,
                    generate_password_hash(password),
                    datetime.now().isoformat(
                        timespec="seconds"
                    )
                )
            )

            db.commit()

            flash(
                "Registration successful. You can now log in.",
                "success"
            )

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            flash(
                "An account with that email already exists.",
                "danger"
            )

    return render_template("register.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = get_db().execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session.clear()

            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]

            flash(
                "Welcome back!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template("login.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# =========================================================
# DASHBOARD ROUTER
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    if session["role"] == "patient":
        return redirect(
            url_for("patient_dashboard")
        )

    return redirect(
        url_for("staff_dashboard")
    )


# =========================================================
# PATIENT DASHBOARD
# =========================================================

@app.route("/patient/dashboard")
@roles_required("patient")
def patient_dashboard():

    db = get_db()

    appointments = db.execute(
        """
        SELECT
            a.*,
            s.full_name AS staff_name

        FROM appointments a

        LEFT JOIN users s
            ON a.staff_id = s.id

        WHERE a.patient_id = ?

        ORDER BY
            a.appointment_date DESC,
            a.appointment_time DESC
        """,
        (session["user_id"],)
    ).fetchall()

    requests = db.execute(
        """
        SELECT *
        FROM medical_requests

        WHERE patient_id = ?

        ORDER BY created_at DESC
        """,
        (session["user_id"],)
    ).fetchall()

    records = db.execute(
        """
        SELECT
            r.*,
            u.full_name AS staff_name

        FROM medical_records r

        JOIN users u
            ON r.staff_id = u.id

        WHERE r.patient_id = ?

        ORDER BY created_at DESC
        """,
        (session["user_id"],)
    ).fetchall()

    return render_template(
        "patient_dashboard.html",
        appointments=appointments,
        requests=requests,
        records=records
    )


# =========================================================
# BOOK APPOINTMENT
# =========================================================

@app.route("/appointment", methods=["POST"])
@roles_required("patient")
def book_appointment():

    appointment_date = request.form.get(
        "appointment_date",
        ""
    )

    appointment_time = request.form.get(
        "appointment_time",
        ""
    )

    department = request.form.get(
        "department",
        ""
    )

    reason = request.form.get(
        "reason",
        ""
    ).strip()

    if not all([
        appointment_date,
        appointment_time,
        department,
        reason
    ]):

        flash(
            "Please complete all appointment fields.",
            "danger"
        )

        return redirect(
            url_for("patient_dashboard")
        )

    # Prevent booking dates in the past
    try:

        selected_date = datetime.strptime(
            appointment_date,
            "%Y-%m-%d"
        ).date()

        if selected_date < date.today():

            flash(
                "Please select a future appointment date.",
                "danger"
            )

            return redirect(
                url_for("patient_dashboard")
            )

    except ValueError:

        flash(
            "Invalid appointment date.",
            "danger"
        )

        return redirect(
            url_for("patient_dashboard")
        )

    db = get_db()

    # Prevent duplicate appointment at same time
    existing = db.execute(
        """
        SELECT id
        FROM appointments

        WHERE patient_id = ?
        AND appointment_date = ?
        AND appointment_time = ?
        AND status != 'Cancelled'
        """,
        (
            session["user_id"],
            appointment_date,
            appointment_time
        )
    ).fetchone()

    if existing:

        flash(
            "You already have an appointment at that time.",
            "warning"
        )

        return redirect(
            url_for("patient_dashboard")
        )

    db.execute(
        """
        INSERT INTO appointments
        (
            patient_id,
            appointment_date,
            appointment_time,
            department,
            reason,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, 'Pending', ?)
        """,
        (
            session["user_id"],
            appointment_date,
            appointment_time,
            department,
            reason,
            datetime.now().isoformat(
                timespec="seconds"
            )
        )
    )

    db.commit()

    flash(
        "Appointment request submitted successfully.",
        "success"
    )

    return redirect(
        url_for("patient_dashboard")
    )


# =========================================================
# MEDICAL HELP REQUEST
# =========================================================

@app.route("/medical-request", methods=["POST"])
@roles_required("patient")
def medical_request():

    subject = request.form.get(
        "subject",
        ""
    ).strip()

    message = request.form.get(
        "message",
        ""
    ).strip()

    if not subject or not message:

        flash(
            "Please provide a subject and message.",
            "danger"
        )

        return redirect(
            url_for("patient_dashboard")
        )

    db = get_db()

    db.execute(
        """
        INSERT INTO medical_requests
        (
            patient_id,
            subject,
            message,
            status,
            created_at
        )

        VALUES (?, ?, ?, 'Open', ?)
        """,
        (
            session["user_id"],
            subject,
            message,
            datetime.now().isoformat(
                timespec="seconds"
            )
        )
    )

    db.commit()

    flash(
        "Your request has been sent to hospital staff.",
        "success"
    )

    return redirect(
        url_for("patient_dashboard")
    )


# =========================================================
# STAFF DASHBOARD
# =========================================================

@app.route("/staff/dashboard")
@roles_required(
    "admin",
    "doctor",
    "nurse",
    "receptionist"
)
def staff_dashboard():

    db = get_db()

    patients = db.execute(
        """
        SELECT
            id,
            full_name,
            email,
            phone,
            date_of_birth,
            gender,
            address,
            emergency_contact,
            created_at

        FROM users

        WHERE role = 'patient'

        ORDER BY full_name
        """
    ).fetchall()

    appointments = db.execute(
        """
        SELECT
            a.*,
            p.full_name AS patient_name,
            s.full_name AS staff_name

        FROM appointments a

        JOIN users p
            ON a.patient_id = p.id

        LEFT JOIN users s
            ON a.staff_id = s.id

        ORDER BY
            a.appointment_date ASC,
            a.appointment_time ASC
        """
    ).fetchall()

    requests = db.execute(
        """
        SELECT
            r.*,
            p.full_name AS patient_name

        FROM medical_requests r

        JOIN users p
            ON r.patient_id = p.id

        ORDER BY created_at DESC
        """
    ).fetchall()

    stats = {

        "patients": db.execute(
            """
            SELECT COUNT(*)
            FROM users
            WHERE role = 'patient'
            """
        ).fetchone()[0],

        "appointments": db.execute(
            """
            SELECT COUNT(*)
            FROM appointments
            """
        ).fetchone()[0],

        "pending": db.execute(
            """
            SELECT COUNT(*)
            FROM appointments
            WHERE status = 'Pending'
            """
        ).fetchone()[0],

        "requests": db.execute(
            """
            SELECT COUNT(*)
            FROM medical_requests
            WHERE status = 'Open'
            """
        ).fetchone()[0]
    }

    return render_template(
        "staff_dashboard.html",
        patients=patients,
        appointments=appointments,
        requests=requests,
        stats=stats
    )


# =========================================================
# UPDATE APPOINTMENT
# =========================================================

@app.route(
    "/staff/appointment/<int:appointment_id>",
    methods=["POST"]
)
@roles_required(
    "admin",
    "doctor",
    "nurse",
    "receptionist"
)
def update_appointment(appointment_id):

    status = request.form.get(
        "status",
        ""
    )

    notes = request.form.get(
        "notes",
        ""
    ).strip()

    allowed = {
        "Pending",
        "Confirmed",
        "Completed",
        "Cancelled"
    }

    if status not in allowed:

        flash(
            "Invalid appointment status.",
            "danger"
        )

        return redirect(
            url_for("staff_dashboard")
        )

    db = get_db()

    db.execute(
        """
        UPDATE appointments

        SET
            status = ?,
            notes = ?,
            staff_id = ?

        WHERE id = ?
        """,
        (
            status,
            notes,
            session["user_id"],
            appointment_id
        )
    )

    db.commit()

    flash(
        "Appointment updated.",
        "success"
    )

    return redirect(
        url_for("staff_dashboard")
    )


# =========================================================
# RESPOND TO MEDICAL REQUEST
# =========================================================

@app.route(
    "/staff/request/<int:request_id>",
    methods=["POST"]
)
@roles_required(
    "admin",
    "doctor",
    "nurse",
    "receptionist"
)
def respond_to_request(request_id):

    status = request.form.get(
        "status",
        ""
    )

    response = request.form.get(
        "staff_response",
        ""
    ).strip()

    allowed = {
        "Open",
        "In Progress",
        "Resolved"
    }

    if status not in allowed:

        flash(
            "Invalid request status.",
            "danger"
        )

        return redirect(
            url_for("staff_dashboard")
        )

    db = get_db()

    db.execute(
        """
        UPDATE medical_requests

        SET
            status = ?,
            staff_response = ?

        WHERE id = ?
        """,
        (
            status,
            response,
            request_id
        )
    )

    db.commit()

    flash(
        "Medical request updated.",
        "success"
    )

    return redirect(
        url_for("staff_dashboard")
    )


# =========================================================
# ADD MEDICAL RECORD
# =========================================================

@app.route(
    "/staff/patient/<int:patient_id>/record",
    methods=["POST"]
)
@roles_required(
    "admin",
    "doctor",
    "nurse"
)
def add_record(patient_id):

    diagnosis = request.form.get(
        "diagnosis",
        ""
    ).strip()

    treatment = request.form.get(
        "treatment",
        ""
    ).strip()

    prescription = request.form.get(
        "prescription",
        ""
    ).strip()

    notes = request.form.get(
        "notes",
        ""
    ).strip()

    if not diagnosis:

        flash(
            "Diagnosis is required.",
            "danger"
        )

        return redirect(
            url_for("staff_dashboard")
        )

    db = get_db()

    patient = db.execute(
        """
        SELECT id
        FROM users

        WHERE id = ?
        AND role = 'patient'
        """,
        (patient_id,)
    ).fetchone()

    if not patient:

        flash(
            "Patient not found.",
            "danger"
        )

        return redirect(
            url_for("staff_dashboard")
        )

    db.execute(
        """
        INSERT INTO medical_records
        (
            patient_id,
            staff_id,
            diagnosis,
            treatment,
            prescription,
            notes,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            session["user_id"],
            diagnosis,
            treatment,
            prescription,
            notes,
            datetime.now().isoformat(
                timespec="seconds"
            )
        )
    )

    db.commit()

    flash(
        "Medical record added.",
        "success"
    )

    return redirect(
        url_for("staff_dashboard")
    )


# =========================================================
# PROFILE
# =========================================================

@app.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    db = get_db()

    if request.method == "POST":

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        date_of_birth = request.form.get(
            "date_of_birth",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        emergency_contact = request.form.get(
            "emergency_contact",
            ""
        ).strip()

        if not full_name:

            flash(
                "Full name is required.",
                "danger"
            )

        else:

            db.execute(
                """
                UPDATE users

                SET
                    full_name = ?,
                    phone = ?,
                    date_of_birth = ?,
                    gender = ?,
                    address = ?,
                    emergency_contact = ?

                WHERE id = ?
                """,
                (
                    full_name,
                    phone,
                    date_of_birth,
                    gender,
                    address,
                    emergency_contact,
                    session["user_id"]
                )
            )

            db.commit()

            session["full_name"] = full_name

            flash(
                "Profile updated.",
                "success"
            )

    user = db.execute(
        """
        SELECT
            id,
            full_name,
            email,
            phone,
            date_of_birth,
            gender,
            address,
            emergency_contact,
            role,
            created_at

        FROM users

        WHERE id = ?
        """,
        (session["user_id"],)
    ).fetchone()

    return render_template(
        "profile.html",
        user=user
    )


# =========================================================
# ADMIN CREATE STAFF
# =========================================================

@app.route(
    "/admin/create-staff",
    methods=["POST"]
)
@roles_required("admin")
def create_staff():

    full_name = request.form.get(
        "full_name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    role = request.form.get(
        "role",
        ""
    )

    allowed_roles = {
        "admin",
        "doctor",
        "nurse",
        "receptionist"
    }

    if role not in allowed_roles:

        flash(
            "Invalid staff role.",
            "danger"
        )

        return redirect(
            url_for("staff_dashboard")
        )

    if len(password) < 8:

        flash(
            "Staff password must contain at least 8 characters.",
            "danger"
        )

        return redirect(
            url_for("staff_dashboard")
        )

    try:

        db = get_db()

        db.execute(
            """
            INSERT INTO users
            (
                full_name,
                email,
                phone,
                password,
                role,
                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                full_name,
                email,
                phone,
                generate_password_hash(password),
                role,
                datetime.now().isoformat(
                    timespec="seconds"
                )
            )
        )

        db.commit()

        flash(
            "Staff account created.",
            "success"
        )

    except sqlite3.IntegrityError:

        flash(
            "That email is already registered.",
            "danger"
        )

    return redirect(
        url_for("staff_dashboard")
    )


# =========================================================
# START APPLICATION
# =========================================================

with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)