# SmartPrep AI – Certificate Verification System

A production-ready Flask app that lets you:
1. Upload a certificate image via an admin panel
2. Auto-generate a unique Certificate ID (e.g. `SPAI2026-A3F9C2`)
3. Generate a QR code pointing to the public verification URL
4. Scan the QR → see **only** the certificate image (full-screen, NPTEL style)

---

## ⚡ Quick Setup (Local)

### 1. Clone / Unzip the project
```bash
unzip smartprep.zip
cd smartprep
```

### 2. Create a Python virtual environment
```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up MySQL
```bash
mysql -u root -p < database/schema.sql
```
This creates the `smartprep` database and `certificates` table.

### 5. Configure the app

Edit **`config.py`** (or set environment variables):

| Key | Default | Description |
|-----|---------|-------------|
| `DB_HOST` | `localhost` | MySQL host |
| `DB_USER` | `root` | MySQL user |
| `DB_PASSWORD` | `your_mysql_password` | MySQL password |
| `DB_NAME` | `smartprep` | Database name |
| `BASE_URL` | `http://localhost:5000` | Change to your domain in production |
| `ADMIN_USERNAME` | `admin` | Admin login |
| `ADMIN_PASSWORD` | `admin@smartprep` | Admin password |
| `SECRET_KEY` | *(change this!)* | Flask session secret |

### 6. Run the app
```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 🧭 Usage

### Admin Panel
| URL | Description |
|-----|-------------|
| `/` or `/admin` | Dashboard – list all certificates |
| `/admin/login` | Login page |
| `/admin/add` | Add a new certificate |
| `/admin/logout` | Logout |

**Default credentials:** `admin` / `admin@smartprep`

### Public QR Scan
| URL | Description |
|-----|-------------|
| `/certificate/<CERT_ID>` | Full-screen certificate view (no UI chrome) |

---

## 📁 Project Structure
```
smartprep/
├── app.py                  # Main Flask app
├── config.py               # Configuration
├── requirements.txt
├── templates/
│   ├── base.html           # Admin layout
│   ├── login.html          # Admin login
│   ├── dashboard.html      # Certificate list
│   ├── add_certificate.html
│   ├── certificate.html    # Public view (QR lands here)
│   └── not_found.html
├── static/
│   ├── certificates/       # Uploaded certificate images
│   └── qr/                 # Generated QR PNGs
├── database/
│   └── schema.sql
└── utils/
    └── qr_generator.py
```

---

## 🚀 Production Deployment (Ubuntu + Gunicorn + Nginx)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Point Nginx to port 8000 and set BASE_URL to your real domain
```

Set environment variables instead of editing `config.py`:
```bash
export BASE_URL="https://certificates.yourdomain.com"
export DB_PASSWORD="your_secure_password"
export SECRET_KEY="a-very-long-random-string"
export ADMIN_PASSWORD="your_secure_admin_password"
```

---

## 🔐 Security Notes
- Certificate IDs use 6-char hex UUIDs — hard to guess (`SPAI2026-A3F9C2`)
- Change `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` before going live
- Consider HTTPS (Let's Encrypt / Certbot) in production
- Consider restricting `/static/certificates/` via Nginx (serve only via Flask route)
