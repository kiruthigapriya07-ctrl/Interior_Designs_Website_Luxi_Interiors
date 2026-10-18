from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)

import mysql.connector
from mysql.connector import Error

import os
import re
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "luxe_interiors_secret_key"
)


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv(
        "DB_NAME",
        "interior_design_studio"
    ),
    "port": int(
        os.getenv("DB_PORT", 3306)
    )
}


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    try:

        connection = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            port=db_config["port"]
        )

        if connection.is_connected():
            return connection

    except Error as e:

        print(
            "Error connecting to MySQL:",
            e
        )

    return None


# =========================================================
# ADMIN AUTHENTICATION HELPER
# =========================================================

def admin_required():

    return bool(
        session.get("admin_logged_in")
    )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# HOME ALIAS
# =========================================================

@app.route("/home")
def home():

    return redirect(
        url_for("index")
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# =========================================================
# SERVICES
# =========================================================

@app.route("/services")
def services():

    conn = get_db_connection()

    services_data = []

    if conn:

        try:

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM services
                ORDER BY id DESC
                """
            )

            services_data = cursor.fetchall()

            cursor.close()
            conn.close()

        except Error as e:

            print(
                "Error fetching services:",
                e
            )

            try:
                conn.close()
            except:
                pass

    return render_template(
        "services.html",
        services=services_data
    )


# =========================================================
# PROJECTS
# =========================================================

@app.route("/projects")
def projects():

    conn = get_db_connection()

    projects_data = []

    if conn:

        try:

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM projects
                ORDER BY id DESC
                """
            )

            projects_data = cursor.fetchall()

            cursor.close()
            conn.close()

        except Error as e:

            print(
                "Error fetching projects:",
                e
            )

            try:
                conn.close()
            except:
                pass

    return render_template(
        "projects.html",
        projects=projects_data
    )


# =========================================================
# CONTACT PAGE
# =========================================================

@app.route("/contact")
def contact():

    return render_template(
        "contact.html"
    )


# =========================================================
# CONSULTATION PAGE
# =========================================================

@app.route("/consultation")
def consultation():

    return render_template(
        "consultation.html"
    )


# =========================================================
# CONTACT API
# =========================================================

@app.route(
    "/api/contact",
    methods=["POST"]
)
def api_contact():

    data = request.get_json(
        silent=True
    ) or {}

    name = data.get(
        "name",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip()

    phone = data.get(
        "phone",
        ""
    ).strip()

    subject = data.get(
        "subject",
        ""
    ).strip()

    message = data.get(
        "message",
        ""
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name:

        return jsonify({
            "success": False,
            "message": "Please enter your name."
        }), 400


    if not email:

        return jsonify({
            "success": False,
            "message": "Please enter your email."
        }), 400


    email_pattern = (
        r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    )

    if not re.match(
        email_pattern,
        email
    ):

        return jsonify({
            "success": False,
            "message": "Please enter a valid email."
        }), 400


    if not message:

        return jsonify({
            "success": False,
            "message": "Please enter your message."
        }), 400


    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    conn = get_db_connection()

    if not conn:

        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500


    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages
            (
                name,
                email,
                phone,
                subject,
                message
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                name,
                email,
                phone,
                subject,
                message
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Your message has been sent successfully."
        })


    except Error as e:

        print(
            "Error saving contact message:",
            e
        )

        try:
            conn.close()
        except:
            pass

        return jsonify({
            "success": False,
            "message": "Unable to save your message."
        }), 500


# =========================================================
# CONSULTATION API
# =========================================================

@app.route(
    "/api/consultation",
    methods=["POST"]
)
def api_consultation():

    data = request.get_json(
        silent=True
    ) or {}


    name = data.get(
        "name",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip()

    phone = data.get(
        "phone",
        ""
    ).strip()

    project_type = data.get(
        "project_type",
        ""
    ).strip()

    preferred_date = data.get(
        "preferred_date",
        ""
    ).strip()

    preferred_time = data.get(
        "preferred_time",
        ""
    ).strip()

    budget = data.get(
        "budget",
        ""
    ).strip()

    message = data.get(
        "message",
        ""
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name:

        return jsonify({
            "success": False,
            "message": "Please enter your name."
        }), 400


    if not email:

        return jsonify({
            "success": False,
            "message": "Please enter your email."
        }), 400


    email_pattern = (
        r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    )

    if not re.match(
        email_pattern,
        email
    ):

        return jsonify({
            "success": False,
            "message": "Please enter a valid email."
        }), 400


    if not phone:

        return jsonify({
            "success": False,
            "message": "Please enter your phone number."
        }), 400


    if not project_type:

        return jsonify({
            "success": False,
            "message": "Please select a project type."
        }), 400


    # -----------------------------------------------------
    # DATABASE
    # -----------------------------------------------------

    conn = get_db_connection()

    if not conn:

        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500


    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO consultations
            (
                name,
                email,
                phone,
                project_type,
                preferred_date,
                preferred_time,
                budget,
                message,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                name,
                email,
                phone,
                project_type,
                preferred_date,
                preferred_time,
                budget,
                message,
                "Pending"
            )
        )

        conn.commit()

        consultation_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Your consultation request has been submitted successfully.",
            "consultation_id": consultation_id
        })


    except Error as e:

        print(
            "Error saving consultation:",
            e
        )

        try:
            conn.close()
        except:
            pass

        return jsonify({
            "success": False,
            "message": "Unable to submit consultation request."
        }), 500


# =========================================================
# PROJECTS API
# =========================================================

@app.route(
    "/api/projects",
    methods=["GET"]
)
def api_projects():

    conn = get_db_connection()

    if not conn:

        return jsonify({
            "success": False,
            "message": "Database connection failed.",
            "projects": []
        }), 500


    try:

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM projects
            ORDER BY id DESC
            """
        )

        projects_data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "projects": projects_data
        })


    except Error as e:

        print(
            "Error fetching projects:",
            e
        )

        try:
            conn.close()
        except:
            pass

        return jsonify({
            "success": False,
            "message": "Unable to fetch projects.",
            "projects": []
        }), 500


# =========================================================
# SERVICES API
# =========================================================

@app.route(
    "/api/services",
    methods=["GET"]
)
def api_services():

    conn = get_db_connection()

    if not conn:

        return jsonify({
            "success": False,
            "message": "Database connection failed.",
            "services": []
        }), 500


    try:

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM services
            ORDER BY id DESC
            """
        )

        services_data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "services": services_data
        })


    except Error as e:

        print(
            "Error fetching services:",
            e
        )

        try:
            conn.close()
        except:
            pass

        return jsonify({
            "success": False,
            "message": "Unable to fetch services.",
            "services": []
        }), 500


# =========================================================
# SINGLE PROJECT API
# =========================================================

@app.route(
    "/api/project/<int:project_id>",
    methods=["GET"]
)
def api_project(project_id):

    conn = get_db_connection()

    if not conn:

        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500


    try:

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM projects
            WHERE id = %s
            LIMIT 1
            """,
            (project_id,)
        )

        project = cursor.fetchone()

        cursor.close()
        conn.close()


        if not project:

            return jsonify({
                "success": False,
                "message": "Project not found."
            }), 404


        return jsonify({
            "success": True,
            "project": project
        })


    except Error as e:

        print(
            "Error fetching project:",
            e
        )

        try:
            conn.close()
        except:
            pass

        return jsonify({
            "success": False,
            "message": "Unable to fetch project."
        }), 500


# =========================================================
# ADMIN LOGIN
# =========================================================
#
# IMPORTANT:
# Your file name is:
#
# templates/admin_login.html
#
# So every render_template below uses:
# admin_login.html
#
# login.html is NOT used.
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    # -----------------------------------------------------
    # ALREADY LOGGED IN
    # -----------------------------------------------------

    if session.get("admin_logged_in"):

        return redirect(
            url_for("admin_dashboard")
        )


    # -----------------------------------------------------
    # LOGIN SUBMISSION
    # -----------------------------------------------------

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()


        # -------------------------------------------------
        # EMPTY FIELDS
        # -------------------------------------------------

        if not username or not password:

            return render_template(
                "admin_login.html",
                error="Please enter username and password."
            )


        # -------------------------------------------------
        # DATABASE CONNECTION
        # -------------------------------------------------

        conn = get_db_connection()

        if not conn:

            return render_template(
                "admin_login.html",
                error="Database connection failed. Please start MySQL."
            )


        try:

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM admins
                WHERE username = %s
                LIMIT 1
                """,
                (username,)
            )

            admin = cursor.fetchone()

            cursor.close()
            conn.close()


            # ---------------------------------------------
            # LOGIN SUCCESS
            # ---------------------------------------------

            if admin and password == admin["password"]:

                session["admin_logged_in"] = True

                session["admin_id"] = admin["id"]

                session["admin_username"] = (
                    admin["username"]
                )

                return redirect(
                    url_for("admin_dashboard")
                )


            # ---------------------------------------------
            # LOGIN FAILED
            # ---------------------------------------------

            return render_template(
                "admin_login.html",
                error="Invalid username or password."
            )


        except Error as e:

            print(
                "Admin login error:",
                e
            )

            try:
                conn.close()
            except:
                pass

            return render_template(
                "admin_login.html",
                error="Unable to process login."
            )


    # -----------------------------------------------------
    # GET REQUEST
    # -----------------------------------------------------

    return render_template(
        "admin_login.html"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route(
    "/admin/dashboard"
)
def admin_dashboard():

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )


    conn = get_db_connection()

    if not conn:

        return render_template(
            "admin_dashboard.html",
            total_bookings=0,
            pending_bookings=0,
            confirmed_bookings=0,
            completed_bookings=0,
            total_messages=0,
            unread_messages=0,
            total_projects=0,
            total_services=0,
            consultations=[],
            db_error=True
        )


    try:

        cursor = conn.cursor(
            dictionary=True
        )


        # -------------------------------------------------
        # TOTAL BOOKINGS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM consultations
            """
        )

        total_bookings = (
            cursor.fetchone()["total"]
        )


        # -------------------------------------------------
        # PENDING BOOKINGS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM consultations
            WHERE status = 'Pending'
            """
        )

        pending_bookings = (
            cursor.fetchone()["total"]
        )


        # -------------------------------------------------
        # CONFIRMED BOOKINGS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM consultations
            WHERE status = 'Confirmed'
            """
        )

        confirmed_bookings = (
            cursor.fetchone()["total"]
        )


        # -------------------------------------------------
        # COMPLETED BOOKINGS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM consultations
            WHERE status = 'Completed'
            """
        )

        completed_bookings = (
            cursor.fetchone()["total"]
        )


        # -------------------------------------------------
        # TOTAL MESSAGES
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM messages
            """
        )

        total_messages = (
            cursor.fetchone()["total"]
        )


        # -------------------------------------------------
        # UNREAD MESSAGES
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM messages
            WHERE is_read = 0
            """
        )

        unread_messages = (
            cursor.fetchone()["total"]
        )


        # -------------------------------------------------
        # TOTAL PROJECTS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM projects
            """
        )

        total_projects = (
            cursor.fetchone()["total"]
        )


        # -------------------------------------------------
        # TOTAL SERVICES
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM services
            """
        )

        total_services = (
            cursor.fetchone()["total"]
        )


        # -------------------------------------------------
        # RECENT CONSULTATIONS
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM consultations
            ORDER BY id DESC
            LIMIT 10
            """
        )

        consultations = cursor.fetchall()


        cursor.close()
        conn.close()


        return render_template(
            "admin_dashboard.html",

            total_bookings=total_bookings,

            pending_bookings=pending_bookings,

            confirmed_bookings=confirmed_bookings,

            completed_bookings=completed_bookings,

            total_messages=total_messages,

            unread_messages=unread_messages,

            total_projects=total_projects,

            total_services=total_services,

            consultations=consultations,

            db_error=False
        )


    except Error as e:

        print(
            "Dashboard error:",
            e
        )

        try:
            conn.close()
        except:
            pass

        return render_template(
            "admin_dashboard.html",

            total_bookings=0,

            pending_bookings=0,

            confirmed_bookings=0,

            completed_bookings=0,

            total_messages=0,

            unread_messages=0,

            total_projects=0,

            total_services=0,

            consultations=[],

            db_error=True
        )


# =========================================================
# ADMIN CONSULTATIONS
# =========================================================

@app.route(
    "/admin/consultations"
)
def admin_consultations():

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )


    conn = get_db_connection()

    consultations = []


    if conn:

        try:

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM consultations
                ORDER BY id DESC
                """
            )

            consultations = cursor.fetchall()

            cursor.close()
            conn.close()


        except Error as e:

            print(
                "Error fetching consultations:",
                e
            )

            try:
                conn.close()
            except:
                pass


    return render_template(
        "admin_consultations.html",
        consultations=consultations
    )


# =========================================================
# UPDATE CONSULTATION STATUS
# =========================================================

@app.route(
    "/admin/consultation/<int:consultation_id>/status",
    methods=["POST"]
)
def update_consultation_status(
    consultation_id
):

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )


    status = request.form.get(
        "status",
        ""
    ).strip()


    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Completed",
        "Cancelled"
    ]


    if status not in allowed_statuses:

        return redirect(
            url_for(
                "admin_consultations"
            )
        )


    conn = get_db_connection()

    if not conn:

        return redirect(
            url_for(
                "admin_consultations"
            )
        )


    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE consultations
            SET status = %s
            WHERE id = %s
            """,
            (
                status,
                consultation_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()


    except Error as e:

        print(
            "Error updating consultation status:",
            e
        )

        try:
            conn.close()
        except:
            pass


    return redirect(
        url_for(
            "admin_consultations"
        )
    )


# =========================================================
# ADMIN MESSAGES
# =========================================================

@app.route(
    "/admin/messages"
)
def admin_messages():

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )


    conn = get_db_connection()

    messages = []


    if conn:

        try:

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM messages
                ORDER BY id DESC
                """
            )

            messages = cursor.fetchall()

            cursor.close()
            conn.close()


        except Error as e:

            print(
                "Error fetching messages:",
                e
            )

            try:
                conn.close()
            except:
                pass


    return render_template(
        "admin_messages.html",
        messages=messages
    )


# =========================================================
# MARK MESSAGE AS READ
# =========================================================

@app.route(
    "/admin/message/<int:message_id>/read",
    methods=["POST", "GET"]
)
def mark_message_read(
    message_id
):

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )


    conn = get_db_connection()

    if not conn:

        return redirect(
            url_for("admin_messages")
        )


    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE messages
            SET is_read = 1
            WHERE id = %s
            """,
            (message_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()


    except Error as e:

        print(
            "Error marking message as read:",
            e
        )

        try:
            conn.close()
        except:
            pass


    return redirect(
        url_for("admin_messages")
    )


# =========================================================
# DELETE MESSAGE
# =========================================================

@app.route(
    "/admin/message/<int:message_id>/delete",
    methods=["POST", "GET"]
)
def delete_message(
    message_id
):

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )


    conn = get_db_connection()

    if not conn:

        return redirect(
            url_for("admin_messages")
        )


    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM messages
            WHERE id = %s
            """,
            (message_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()


    except Error as e:

        print(
            "Error deleting message:",
            e
        )

        try:
            conn.close()
        except:
            pass


    return redirect(
        url_for("admin_messages")
    )


# =========================================================
# ADMIN PROJECTS
# =========================================================

@app.route(
    "/admin/projects"
)
def admin_projects():

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )


    conn = get_db_connection()

    projects_data = []


    if conn:

        try:

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM projects
                ORDER BY id DESC
                """
            )

            projects_data = cursor.fetchall()

            cursor.close()
            conn.close()


        except Error as e:

            print(
                "Error fetching admin projects:",
                e
            )

            try:
                conn.close()
            except:
                pass


    return render_template(
        "admin_projects.html",
        projects=projects_data
    )


# =========================================================
# ADMIN SERVICES
# =========================================================

@app.route(
    "/admin/services"
)
def admin_services():

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )


    conn = get_db_connection()

    services_data = []


    if conn:

        try:

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM services
                ORDER BY id DESC
                """
            )

            services_data = cursor.fetchall()

            cursor.close()
            conn.close()


        except Error as e:

            print(
                "Error fetching admin services:",
                e
            )

            try:
                conn.close()
            except:
                pass


    return render_template(
        "admin_services.html",
        services=services_data
    )


# =========================================================
# ADMIN TESTIMONIALS
# =========================================================

@app.route(
    "/admin/testimonials"
)
def admin_testimonials():

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )


    conn = get_db_connection()

    testimonials = []


    if conn:

        try:

            cursor = conn.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT *
                FROM testimonials
                ORDER BY id DESC
                """
            )

            testimonials = cursor.fetchall()

            cursor.close()
            conn.close()


        except Error as e:

            print(
                "Error fetching testimonials:",
                e
            )

            try:
                conn.close()
            except:
                pass


    return render_template(
        "admin_testimonials.html",
        testimonials=testimonials
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route(
    "/admin/logout"
)
def admin_logout():

    session.clear()

    return redirect(
        url_for("admin_login")
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route(
    "/api/health"
)
def health():

    conn = get_db_connection()


    if conn:

        try:
            conn.close()
        except:
            pass

        return jsonify({
            "success": True,
            "status": "running",
            "database": "connected"
        })


    return jsonify({
        "success": True,
        "status": "running",
        "database": "disconnected"
    })


# =========================================================
# ERROR HANDLER - 404
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


# =========================================================
# ERROR HANDLER - 500
# =========================================================

@app.errorhandler(500)
def internal_server_error(error):

    return render_template(
        "500.html"
    ), 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print(
        "=============================================="
    )

    print(
        "       LUXE INTERIORS WEBSITE"
    )

    print(
        "=============================================="
    )

    print(
        "Server running on:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print(
        "Admin Login:"
    )

    print(
        "http://127.0.0.1:5000/admin/login"
    )

    print(
        "=============================================="
    )


    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )