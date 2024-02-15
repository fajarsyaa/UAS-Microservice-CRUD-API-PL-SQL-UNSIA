##  Aplikasi Sistem Pembayaran

Aplikasi Sistem Pembayaran ini menyediakan fitur untuk manajemen pengguna, autentikasi pengguna, pengolahan pembayaran, dan pencatatan berbagai aktivitas dalam sistem.

### Fitur

1. **Manajemen Pengguna:**
   - Registrasi customer dan merchant dengan username, email, dan password unik.
   - Memperbarui data pengguna.
   - Menghapus akun pengguna.

2. **Autentikasi:**
   - Login customer dan merchant dengan email dan password.
   - Memastikan autentikasi yang aman melalui enkripsi dan dekripsi password.

3. **Pengolahan Pembayaran:**
   - Pembayaran dari customer ke merchant.
   - Mendapatkan detail pembayaran.

4. **Pencatatan:**
   - Mencatat berbagai aktivitas log transaksi pembayaran, perubahan informasi customer, dan merchant.

### Persiapan

Untuk menyiapkan Aplikasi Sistem Pembayaran, ikuti langkah-langkah ini:

1. **Clone Repository:** 
   - Clone repository dari GitHub menggunakan perintah berikut:
     ```
     git clone https://github.com/fajarsyaa/UAS-Microservice-CRUD-API-PL-SQL-UNSIA.git
     ```
   
2. **Instal Dependensi:**
   - Lalu pastikan masuk ke direktori proyek dan instal dependensi yang diperlukan menggunakan:
     ```
     cd <nama project hasil clone>
     pip install -r requirements.txt
     ```
   
3. **Konfigurasi Database:**
   - Konfigurasikan koneksi database di file `config.py`.
   - Pastikan anda sudah install Postgresql.
   - Setelah itu jalankan file sql yang disediakan pada database postgress anda
     ```
     database.sql
     ```

4. **Jalankan Aplikasi:**
   - Jalankan aplikasi menggunakan:
     ```
     flask run
     ```
   - Secara default, aplikasi akan berjalan di port `http://localhost:5000`.
   
### Penggunaan

Setelah aplikasi dijalankan, Anda dapat menggunakan postman atau software sejenis untuk menjalankan request. Berikut adalah contoh requestnya:

- **Registrasi customer:** 
  ```
  POST /customer
  ```
  Body Permintaan:
  ```json
  {
    "username": "nama_pengguna_customer",
    "email": "customer@example.com",
    "password": "password_customer",
    "no_rek": "1234567890"
  }
  ```

- **Registrasi merchant:** 
  ```
  POST /merchant
  ```
  Body Permintaan:
  ```json
  {
    "username": "nama_pengguna_merchant",
    "email": "merchant@example.com",
    "password": "password_merchant",
    "no_rek": "0987654321"
  }
  ```

- **Login customer:**
  ```
  POST /login/customer
  ```
  Body Permintaan:
  ```json
  {
    "email": "customer@example.com",
    "password": "password_customer"
  }
  ```

- **Login merchant:**
  ```
  POST /login/merchant
  ```
  Body Permintaan:
  ```json
  {
    "email": "merchant@example.com",
    "password": "password_merchant"
  }
  ```

- **Membuat Pembayaran:**
  ```
  POST /payment
  ```
  Body Permintaan:
  ```json
  {
    "customer_id": 1,
    "merchant_id": 4,
    "amount": 10000
  }
  ```

- **Edit Customer:**
  ```
  PUT /customer/<customer_id>
  ```
  Body Permintaan:
  ```json
  {
    "username": "username_baru",
    "email": "email_baru@example.com",
    "password": "password_baru",
    "no_rek": "1234567890"
  }

  ```

- **Edit Merchant:**
  ```
  PUT /merchant/<merchant_id>
  ```
  Body Permintaan:
  ```json
  {
    "username": "username_baru",
    "email": "email_baru@example.com",
    "password": "password_baru",
    "no_rek": "0987654321"
  }
  ```

- **Hapus Customer  berdasarkan ID:**
  ```
  DELETE /customer/<payment_id>
  ```

- **Hapus Merchant berdasarkan ID:**
  ```
  DELETE /merchant/<payment_id>
  ```

- **Mendapatkan data Pembayaran berdasarkan ID:**
  ```
  GET /payment/<payment_id>
  ```

- **Mendapatkan data Semua Pembayaran:**
  ```
  GET /payment
  ```

- **Mendapatkan data Log Pembayaran:**
  ```
  GET /log/payment
  ```

- **Mendapatkan data Log merchant:**
  ```
  GET /log/merchant
  ```

- **Mendapatkan data Log customer:**
  ```
  GET /log/customer
  ```

### Export collection postman
Atau jika anda ingin yang lebih simple, anda bisa mengimport collection postman yang sudah disediakan.
     ```
     postman_collection.json
     ```

### Kesimpulan

Aplikasi Sistem Pembayaran sederhana ini dibangun untuk menyelesaikan tugas UAS mata kuliah Pemrograman PL/SQL. Universitas Siber Asia