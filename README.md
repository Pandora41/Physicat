# Flask RESTful API - Production Ready

Modern, production-ready RESTful API built with Flask 3.x and Python 3.11.

## Features

- ✅ Python 3.11 with full type hints support
- ✅ Flask 3.x with blueprints architecture
- ✅ Pydantic v2 for settings and validation
- ✅ Structured logging with structlog
- ✅ OpenAPI/Swagger documentation auto-generation
- ✅ Comprehensive test coverage (>95%)
- ✅ Docker multi-stage build (<100MB)
- ✅ PostgreSQL support with SQLAlchemy
- ✅ Dependency injection ready

## Cara Menjalankan Aplikasi

### Metode 1: Setup Lengkap dengan Validasi (Recommended)

Ini adalah cara terbaik untuk memastikan environment sudah benar sebelum menjalankan aplikasi.

#### 1. Buat Virtual Environment

```bash
python -m venv venv
```

#### 2. Aktifkan Virtual Environment

**Windows (PowerShell/CMD):**
```bash
venv\Scripts\activate
```

**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Jalankan Environment Validation & Start Server

```bash
python scripts/test_env.py
```

Script ini akan:
- ✅ Memverifikasi virtual environment aktif
- ✅ Mengecek Python version (harus 3.11.9)
- ✅ Menginstall/update requirements jika hash berubah
- ✅ Menjalankan semua test dengan coverage check (>95%)
- ✅ Menjalankan Flask dev server di port 5000 (hanya jika semua test pass)

Setelah server berjalan, akses:
- **Swagger UI**: http://localhost:5000/apidocs
- **API Endpoint**: http://localhost:5000/api/v1
- **Health Check**: http://localhost:5000/health

---

### Metode 2: Development Server Manual

Jika ingin menjalankan tanpa validasi lengkap:

#### Setup Environment Variables (Opsional)

Buat file `.env` di root project:

```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///app.db
SECRET_KEY=dev-secret-key-change-in-production
LOG_LEVEL=INFO
```

#### Jalankan Flask Development Server

```bash
# Set Flask app
export FLASK_APP=app:create_app  # Linux/Mac
set FLASK_APP=app:create_app      # Windows CMD
$env:FLASK_APP="app:create_app"   # Windows PowerShell

# Run server
flask run --host=0.0.0.0 --port=5000
```

Atau langsung:

```bash
python -m flask run --host=0.0.0.0 --port=5000
```

---

### Metode 3: Production Server dengan Gunicorn

Untuk production atau testing dengan Gunicorn:

```bash
python scripts/run.py
```

Atau langsung dengan Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

**Parameter Gunicorn:**
- `-w 4`: Jumlah worker processes (sesuaikan dengan CPU cores)
- `-b 0.0.0.0:5000`: Bind address dan port
- `app:create_app()`: Flask app factory

---

### Metode 4: Menggunakan Docker

#### Development dengan Docker Compose (PostgreSQL included)

```bash
# Start semua services (API + PostgreSQL)
docker-compose up -d

# Lihat logs
docker-compose logs -f api

# Stop services
docker-compose down
```

Akses API di: http://localhost:5000

#### Production Build

```bash
# Build image
docker build -t flask-api .

# Run container
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  flask-api
```

---

## Testing

### Menjalankan Tests

```bash
# Run semua tests dengan coverage
pytest -q --cov=app --cov-report=term-missing

# Run tests tanpa coverage
pytest -q

# Run test tertentu
pytest tests/test_health.py -v

# Run dengan verbose output
pytest -v
```

### Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Buka report di browser
# Windows: start htmlcov/index.html
# Linux/Mac: open htmlcov/index.html
```

---

## Troubleshooting

### Error: Virtual environment tidak aktif

**Gejala:** Error saat menjalankan `python scripts/test_env.py`

**Solusi:**
```bash
# Pastikan venv aktif (lihat prompt terminal ada (venv))
# Jika tidak, aktifkan lagi:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Error: Python version tidak sesuai

**Gejala:** Script menolak karena Python bukan 3.11.9

**Solusi:**
- Install Python 3.11.9 dari python.org
- Atau ubah versi di `scripts/test_env.py` jika ingin menggunakan versi lain

### Error: Port 5000 sudah digunakan

**Gejala:** `Address already in use` atau port sudah dipakai

**Solusi:**
```bash
# Gunakan port lain
flask run --port=5001

# Atau set environment variable
export PORT=5001  # Linux/Mac
set PORT=5001     # Windows CMD
$env:PORT=5001    # Windows PowerShell
```

### Error: Requirements tidak terinstall

**Gejala:** ImportError saat menjalankan aplikasi

**Solusi:**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Atau install ulang dengan upgrade
pip install -r requirements.txt --upgrade
```

### Error: Database connection failed

**Gejala:** Error saat akses `/ready` endpoint

**Solusi:**
- Pastikan database URL di `.env` benar
- Untuk PostgreSQL, pastikan service berjalan
- Untuk SQLite, pastikan folder writable

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Pydantic settings
│   ├── routes/              # API blueprints
│   ├── models/              # Database models
│   └── utils/               # Utilities & helpers
├── tests/                   # Test suite
│   └── conftest.py          # Pytest configuration
├── scripts/                 # Utility scripts
│   ├── run.py               # Production runner
│   └── test_env.py          # Environment validation
├── docker-compose.yml       # Local development setup
├── Dockerfile               # Multi-stage production build
└── requirements.txt         # Pinned dependencies
```

## Quick Reference Commands

```bash
# Setup awal
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Development
python scripts/test_env.py          # Validasi + run server
flask run                             # Run manual
pytest -q --cov=app                  # Run tests

# Production
python scripts/run.py                # Run dengan Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Docker
docker-compose up -d                 # Development
docker build -t flask-api .          # Build production
```

## Environment Variables

Buat file `.env` di root project (copy dari `env.example`):

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# Database Configuration
DATABASE_URL=postgresql://flaskuser:flaskpass@localhost:5432/flaskdb
# Atau untuk SQLite (default):
# DATABASE_URL=sqlite:///app.db

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Logging Configuration
LOG_LEVEL=INFO

# API Configuration
API_TITLE=Flask RESTful API
API_VERSION=1.0.0
```

**Catatan:** File `.env` sudah di-ignore oleh Git untuk keamanan. Gunakan `env.example` sebagai template.

## License

MIT

