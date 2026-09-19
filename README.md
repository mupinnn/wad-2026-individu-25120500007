# WAD09 - Tugas Individu

**CIK3101 · Web Application Development · Sains Data · Semester 3 · Universitas Cakrawala**

---

## 1. Prasyarat

| Alat | Versi | Cek |
|---|---|---|
| Git | apa saja | `git --version` |
| Node.js | 20 LTS atau lebih baru | `node -v` |
| Python | 3.11 atau lebih baru | `python --version` |
| pip + venv | menyatu dengan Python | `python -m venv --help` |
| curl | apa saja | `curl --version` |
| Akun GitHub | — | sudah jadi anggota repo ini |

> Windows: saat install Python dari python.org, **centang "Add Python to PATH"**.
> Kalau `python` tidak dikenali, coba `py`.

Tidak ada yang perlu di-install untuk basis data sampai Sesi 5. Data buku saat ini masih
in-memory di `backend/app/services.py` (hilang saat server di-restart).

## 2. Layanan

| Layanan | Port lokal | URL | Catatan |
|---|---|---|---|
| Frontend (Vite + Vue 3) | `5173` | http://localhost:5173 | kerangka; isi `frontend/` belum diisi |
| Backend (FastAPI + Uvicorn) | `8000` | http://localhost:8000 | `app.main:app` — router di `main.py`, DTO di `schemas.py`, logika di `services.py` |
| OpenAPI | `8000` | http://localhost:8000/docs | skema request/response `BookCreate` vs `Book` |
| Basis data | — | — | belum dipakai; SQLite di Sesi 3–4, Postgres (Neon) di Sesi 5 lewat `DATABASE_URL` |

Endpoint backend yang sudah ada:

| Metode | Path | Status sukses | Keterangan |
|---|---|---|---|
| `GET` | `/health` | 200 | `{"status":"ok"}` |
| `GET` | `/books` | 200 | paginasi `?skip=&limit=&search=` (`skip` dari 0, `limit` 5–100) |
| `GET` | `/books/{id}` | 200 / 404 | detail buku |
| `POST` | `/books` | 201 / 422 | body `BookCreate` (tanpa `id`); `id` dibuat server; header `Location` |

Validasi `POST /books`: `isbn` tepat 13 digit, `tahun_terbit` 1900–2026, field ekstra (termasuk `id`) ditolak.

## 3. Cara menjalankan

```bash
# sekali saja, setelah clone
cp .env.example .env

# --- backend (terminal 1) ---
cd backend
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# --- frontend (terminal 2), setelah kerangka Vite ada ---
cd frontend
npm install
npm run dev
```

Uvicorn **harus** dijalankan dari folder `backend/`, supaya impor `app.schemas` dan `app.services` ketemu.

## 4. Cara memverifikasi

Pemeriksa dosen (jalankan dari akar repo):

```bash
python verify.py --sesi 3
```

`verify.py` adalah **perintah yang sama persis** yang dipakai dosen untuk memeriksa artefakmu.
Kalau hijau di laptopmu, hijau juga saat dinilai. Jalankan sebelum kamu keluar dari sesi.

Verifikasi manual backend — server harus sudah jalan di `:8000`. Pakai `-i` supaya status dan header kelihatan.

**GET `/health` → 200**

```bash
curl -i http://localhost:8000/health
```

Harus `200` dan `{"status":"ok"}`. Buka juga http://localhost:8000/docs.

**POST `/books` → 201**

```bash
curl -i -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "isbn": "9786020332475",
    "judul": "Laskar Pelangi",
    "tahun_terbit": 2005,
    "pengarang": "Andrea Hirata",
    "penerbit": "Bentang Pustaka",
    "jumlah_halaman": 529
  }'
```

Harus `201 Created`, header `Location` menuju `/books/{id}`, dan body JSON berisi `id` yang digenerate server.

**POST `/books` → 422**

```bash
curl -i -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "id": 99,
    "isbn": "123",
    "judul": "Buku Salah",
    "tahun_terbit": 1800,
    "pengarang": "Anonim",
    "penerbit": "Tidak Ada",
    "jumlah_halaman": 1
  }'
```

Harus `422 Unprocessable Entity` (`isbn` bukan 13 digit, `tahun_terbit` di luar 1900–2026, `id` dilarang di body create).

**GET `/books/{id}` → 404**

```bash
curl -i http://localhost:8000/books/99999
```

Harus `404 Not Found` dengan pesan buku tidak ditemukan.

Frontend (setelah kerangka ada): http://localhost:5173 masih rapi di lebar 360px.

## 5. Masalah yang sering muncul

| Gejala | Sebab biasanya | Tindakan |
|---|---|---|
| `python` tidak dikenali (Windows) | PATH tidak dicentang saat install | pakai `py`, atau install ulang dan centang "Add Python to PATH" |
| `ModuleNotFoundError: app.schemas` / `app.services` | `uvicorn` tidak dijalankan dari `backend/` | `cd backend` lalu `uvicorn app.main:app --reload` |
| `uvicorn: command not found` | venv belum aktif, atau dependensi belum di-install | `source venv/bin/activate` lalu `pip install -r requirements.txt` |
| `/health` 404 | modul yang dijalankan bukan `app.main` | jalankan `uvicorn` dari dalam folder `backend/` |
| `POST /books` 422 padahal data "sudah lengkap" | `isbn` bukan 13 digit, tahun di luar 1900–2026, atau body membawa `id` | ikut skema `BookCreate`; jangan kirim `id` |
| `GET /books/11` 404 setelah create | server sempat restart (data in-memory hilang) atau id salah | `POST` lagi, pakai `id` / `Location` dari respons 201 |
| `npm run dev` gagal / folder kosong | kerangka Vite belum dibuat | lihat `frontend/README.md`; `index.html` harus menunjuk `src/main.js` |
| CI merah karena `secret-scan` | ada rahasia ter-commit | **hapus nilainya, rotasi, commit ulang** — lihat Ketentuan di bawah |
| `venv/` ikut ter-commit | `.gitignore` diubah | kembalikan `.gitignore` bawaan repo |
| Menu **Branches → Add rule** tidak ada | repo dibuat **Private** | Settings → General → Danger Zone → **Change visibility → Public** |
| Tidak bisa merge PR sendiri | "Require approvals" sudah dinyalakan | matikan dulu malam ini (lihat bagian 0 langkah 4) |

---

## Penggunaan AI assistant

AI assistant **diizinkan** pada sesi praktikum, dan **dilarang pada UTS (Sesi 8) dan UAS
(Sesi 16)**. Syaratnya satu: tulis pengungkapan singkat di bawah ini, dan perbarui saat berubah.
Ketentuan 1 tetap berlaku penuh — kalau kamu tidak bisa menjelaskan kode yang dihasilkan AI,
nilainya 0.

<!-- ISI BAGIAN INI. Contoh:
- Sesi 2 — Claude, untuk menjelaskan pesan error `npm ERR! ENOENT`. Kode ditulis sendiri.
- Sesi 5 — GitHub Copilot, autocomplete pada model SQLAlchemy. Ditinjau dan diubah manual.
-->

- Sesi 3 - Untuk menjelaskan bagaimana penggunaan Pydantic, cara kerja offset pagination, penggunaan `response_model`, 
me-refactor kode menjadi file terpisah, skenario untuk bukti/dokumentasi dengan `cURL`, dan mengisi `README.md`

