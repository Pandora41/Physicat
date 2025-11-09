## Panduan Struktur Frontend (FE) dan Backend (BE)

Dokumen ini menjelaskan di mana menaruh kode Frontend dan Backend, serta cara menjalankannya saat pengembangan dan saat produksi.

### Tujuan
- Memastikan semua kontributor tahu lokasi penempatan kode FE dan BE.
- Menyediakan langkah cepat untuk setup dev (proxy, CORS) dan opsi deploy.

### Struktur Direktori yang Disarankan

```
Schrodicats/
├─ app/                  # Backend Flask (BE)
│  ├─ routes/            # Blueprint & endpoint API
│  ├─ models/            # Model/database
│  ├─ utils/             # Utilitas
│  ├─ __init__.py        # create_app(), registrasi blueprint, logging, dll
│  └─ config.py          # Pydantic Settings (env, port, CORS, dll)
├─ frontend/             # Frontend (FE) - aplikasi web (contoh: React + Vite)
├─ scripts/
├─ tests/
├─ requirements.txt
├─ docker-compose.yml
├─ PROJECT.md            # (dokumen ini)
└─ README.md
```

---

## Backend (BE)

- Lokasi kode: `app/`
- Tambah endpoint: letakkan di `app/routes/` (contoh: ubah atau tambah file seperti `api_v1.py`), lalu pastikan blueprint didaftarkan di `create_app()` pada `app/__init__.py`.
- Prefix API: saat ini API `v1` terdaftar di `"/api/v1"`.

### Menjalankan Backend (Dev)

1. Aktifkan virtualenv (Windows PowerShell):
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. Jalankan Flask di port default 5000:
   ```bash
   flask run --host 0.0.0.0 --port 5000
   ```

### Konfigurasi CORS (Opsional tapi disarankan saat dev)

- Atur asal (origin) FE di file `.env` (buat jika belum ada):
  ```env
  CORS_ORIGINS=http://localhost:5173
  ```

- Di `app/config.py` sudah ada field `cors_origins`. Untuk mengaktifkan CORS, gunakan paket `flask-cors` di `create_app()` (contoh implementasi):
  ```python
  from flask_cors import CORS

  # ... di dalam create_app(...):
  if settings.cors_origins:
      origins = [o.strip() for o in settings.cors_origins.split(",")]
      CORS(app, resources={r"/api/*": {"origins": origins}})
  ```

> Catatan: instal terlebih dahulu dependensi CORS:
```bash
pip install flask-cors
```

---

## Frontend (FE)

- Lokasi kode: `frontend/` (buat folder baru ini di root bila belum ada).
- Rekomendasi tool: React + Vite (bebas menggunakan framework lain).

### Membuat Frontend (Contoh: React + Vite)

```bash
# dari root proyek Schrodicats
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

### Proxy Dev ke Backend

Agar pemanggilan API dari FE ke BE tidak terkendala CORS saat pengembangan, pakai proxy Vite ke `http://localhost:5000`.

Contoh `frontend/vite.config.ts`:
```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
})
```

Contoh pemanggilan API dari FE:
```ts
export async function getHealth() {
  const res = await fetch('/api/v1/health')
  return res.json()
}
```

### Menjalankan Frontend (Dev)

```bash
cd frontend
npm run dev
```

---

## Menjalankan Bersamaan (Dev)

- Jalankan BE di port 5000 dan FE di port 5173.
- FE akan memanggil endpoint BE dengan path berawalan `/api` (contoh: `/api/v1/...`).

Ringkasan perintah:
```bash
# Terminal 1 (Backend)
.\venv\Scripts\Activate.ps1
flask run --host 0.0.0.0 --port 5000

# Terminal 2 (Frontend)
cd frontend
npm run dev
```

---

## Build & Deploy

Ada dua pendekatan umum:

1) Deploy Terpisah (Disarankan)
- FE dibuild (`npm run build`) lalu dihosting di CDN/hosting statis (mis. Vercel/Netlify/Nginx).
- BE dijalankan terpisah (Gunicorn/uwsgi) di server atau platform yang sesuai.
- FE memanggil domain API terpisah, misal `https://api.domainmu.com/api/...`.

2) Disajikan oleh Flask (Satu layanan)
- Build FE menghasilkan folder `frontend/dist`.
- Konfigurasikan Flask untuk menyajikan `dist` sebagai static files dan sediakan fallback `index.html` untuk SPA.
- Cocok untuk deploy sederhana, namun kurang fleksibel dibanding terpisah.

---

## Konvensi Routing API

- Semua endpoint versi 1 berada di bawah prefix `"/api/v1"`.
- Contoh healthcheck: `GET /api/v1/health`.
- Saat menambah endpoint baru, gunakan blueprint di `app/routes/` dan daftarkan pada `create_app()`.

---

## FAQ Singkat

- Di mana saya menaruh kode FE? → `frontend/`
- Di mana saya menaruh kode BE? → `app/` (routes di `app/routes/`)
- Bagaimana FE berkomunikasi dengan BE? → Panggil path berawalan `/api` (contoh `/api/v1/...`), gunakan proxy saat dev.
- Perlu CORS? → Ya, saat dev bila tidak pakai proxy; set `CORS_ORIGINS` dan aktifkan `flask-cors`.


