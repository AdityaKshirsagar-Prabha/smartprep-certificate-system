import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production-abc123')

    # ── Database ──────────────────────────────────────────────────────────────
    DB_HOST     = os.environ.get('DB_HOST', 'localhost')
    DB_USER     = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_NAME     = os.environ.get('DB_NAME', 'smartprepcollage')

    # ── File Paths ────────────────────────────────────────────────────────────
    BASE_DIR    = os.path.abspath(os.path.dirname(__file__))
    CERT_FOLDER = os.path.join(BASE_DIR, 'static', 'certificates')
    QR_FOLDER   = os.path.join(BASE_DIR, 'static', 'qr')

    # ── Base URL (change to your domain in production) ────────────────────────
    BASE_URL = os.environ.get('BASE_URL', 'http://verify.nptlai.in')

    # ── Admin Credentials ─────────────────────────────────────────────────────
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin@smartprep')
