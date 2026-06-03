import os
import uuid
from datetime import date

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import mysql.connector

from config import Config
from utils.qr_generator import generate_qr

app = Flask(__name__)
app.config.from_object(Config)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# ───────────────────────────────
# CREATE FOLDERS IF NOT EXISTS
# ───────────────────────────────
os.makedirs(app.config['CERT_FOLDER'], exist_ok=True)
os.makedirs(app.config['QR_FOLDER'], exist_ok=True)


# ───────────────────────────────
# DATABASE CONNECTION
# ───────────────────────────────
def get_db():
    return mysql.connector.connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME']
    )


# ───────────────────────────────
# HELPERS
# ───────────────────────────────
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_certificate_id():
    year = date.today().year
    unique = uuid.uuid4().hex[:6].upper()
    return f"SPAI{year}-{unique}"


# ───────────────────────────────
# ADMIN LOGIN
# ───────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if (request.form['username'] == app.config['ADMIN_USERNAME'] and
                request.form['password'] == app.config['ADMIN_PASSWORD']):
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))

        flash('Invalid credentials.', 'error')

    return render_template('login.html')


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


def admin_required(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)

    return decorated


# ───────────────────────────────
# DASHBOARD
# ───────────────────────────────
@app.route('/')
@app.route('/admin')
@admin_required
def admin_dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM certificates ORDER BY id DESC")
    certs = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('dashboard.html', certs=certs)


# ───────────────────────────────
# ADD CERTIFICATE
# ───────────────────────────────
@app.route('/admin/add', methods=['GET', 'POST'])
@admin_required
def add_certificate():
    if request.method == 'POST':

        student_name = request.form['student_name'].strip()
        course_name = request.form['course_name'].strip()
        score = request.form['score'].strip()
        issue_date = request.form['issue_date']
        file = request.files.get('certificate_image')

        if not file or file.filename == '':
            flash('Please upload certificate image', 'error')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Only PNG, JPG, JPEG allowed', 'error')
            return redirect(request.url)

        # Generate certificate ID
        cert_id = generate_certificate_id()

        # Save image
        filename = secure_filename(f"{cert_id}_{file.filename}")
        img_path = os.path.join(app.config['CERT_FOLDER'], filename)
        file.save(img_path)

        db_image_path = f"certificates/{filename}"

        # QR URL
        cert_url = f"{app.config['BASE_URL']}/certificate/{cert_id}"
        qr_filename = f"{cert_id}.png"
        qr_path = os.path.join(app.config['QR_FOLDER'], qr_filename)

        generate_qr(cert_url, qr_path)

        # Save to DB
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO certificates
            (certificate_id, student_name, course_name, score, issue_date, image_path)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            cert_id,
            student_name,
            course_name,
            score,
            issue_date,
            db_image_path
        ))

        db.commit()
        cursor.close()
        db.close()

        flash(f'Certificate {cert_id} created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_certificate.html')


# ───────────────────────────────
# 🔥 DELETE CERTIFICATE (NEW FEATURE)
# ───────────────────────────────
@app.route('/admin/delete/<certificate_id>', methods=['POST'])
@admin_required
def delete_certificate(certificate_id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get certificate
    cursor.execute(
        "SELECT * FROM certificates WHERE certificate_id = %s",
        (certificate_id,)
    )
    cert = cursor.fetchone()

    if cert:

        # Delete image file
        image_file = os.path.join(app.config['BASE_DIR'], 'static', cert['image_path'])
        if os.path.exists(image_file):
            os.remove(image_file)

        # Delete QR file
        qr_file = os.path.join(app.config['QR_FOLDER'], f"{certificate_id}.png")
        if os.path.exists(qr_file):
            os.remove(qr_file)

        # Delete DB record
        cursor.execute(
            "DELETE FROM certificates WHERE certificate_id = %s",
            (certificate_id,)
        )
        db.commit()

    cursor.close()
    db.close()

    flash(f'Certificate {certificate_id} deleted permanently!', 'success')
    return redirect(url_for('admin_dashboard'))


# ───────────────────────────────
# PUBLIC CERTIFICATE VIEW (QR OPENS HERE)
# ───────────────────────────────
@app.route('/certificate/<certificate_id>')
def view_certificate(certificate_id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM certificates WHERE certificate_id = %s",
        (certificate_id,)
    )

    cert = cursor.fetchone()

    cursor.close()
    db.close()

    if not cert:
        return render_template('not_found.html'), 404

    return render_template('certificate.html', cert=cert)


# ───────────────────────────────
# RUN APP
# ───────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)