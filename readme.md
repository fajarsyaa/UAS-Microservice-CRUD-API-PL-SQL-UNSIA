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
  Method    : POST 
  URL       : /customer
  ```
  Request:
  ```json
  {
    "username": "nama_pengguna_customer",
    "email": "customer@gmail.com",
    "password": "password_customer",
    "no_rek": "1234567890"
  }
  ```

- **Registrasi merchant:** 
  ```
  Method    : POST 
  URL       : /merchant
  ```
  Request:
  ```json
  {
    "username": "nama_pengguna_merchant",
    "email": "merchant@gmail.com",
    "password": "password_merchant",
    "no_rek": "0987654321"
  }
  ```

- **Login customer:**
  ```
  Method    : POST 
  URL       : /login/customer
  ```
  Request:
  ```json
  {
    "email": "customer@gmail.com",
    "password": "password_customer"
  }
  ```

- **Login merchant:**
  ```
  Method    : POST 
  URL       : /login/merchant
  ```
  Request:
  ```json
  {
    "email": "merchant@gmail.com",
    "password": "password_merchant"
  }
  ```

- **Membuat Pembayaran:**
  ```
  Method    : POST 
  URL       : /payment
  ```
  Request:
  ```json
  {
    "customer_id": 1,
    "merchant_id": 4,
    "amount": 10000
  }
  ```

- **Edit Customer:**
  ```
  Method  : PUT 
  URL     : /customer/<customer_id>
  ```
  Request:
  ```json
  {
    "username": "username_baru",
    "email": "email_baru@gmail.com",
    "password": "password_baru",
    "no_rek": "1234567890"
  }

  ```

- **Edit Merchant:**
  ```
  Method    : PUT 
  URL       : /merchant/<merchant_id>
  ```
  Request:
  ```json
  {
    "username": "username_baru",
    "email": "email_baru@gmail.com",
    "password": "password_baru",
    "no_rek": "0987654321"
  }
  ```

- **Hapus Customer  berdasarkan ID:**
  ```
  Method    : DELETE 
  URL       : /customer/<payment_id>
  ```

- **Hapus Merchant berdasarkan ID:**
  ```
  Method    : DELETE 
  URL       : /merchant/<merchant_id>
  ```

- **Mendapatkan data Pembayaran berdasarkan ID:**
  ```
  Method    : GET 
  URL       : /payment/<payment_id>
  ```

- **Mendapatkan data Semua Pembayaran:**
  ```
  Method    : GET 
  URL       : /payment  
  ```

- **Mendapatkan data Log Pembayaran:**
  ```
  Method    : GET 
  URL       : /log/payment
  ```

- **Mendapatkan data Log merchant:**
  ```
  Method    : GET 
  URL       : /log/merchant
  ```

- **Mendapatkan data Log customer:**
  ```
  Method    : GET 
  URL       : /log/customer
  ```

### Export collection postman
Atau jika anda ingin yang lebih simple, anda bisa mengimport collection postman yang sudah disediakan.
     ```
     postman_collection.json
     ```

### Kesimpulan

Aplikasi Sistem Pembayaran sederhana ini dibangun untuk menyelesaikan tugas UAS mata kuliah Pemrograman PL/SQL  Universitas Siber Asia yang dikerjakan secara berkelompok dengan nama kelompok : 
1. Mukhamad Fajar Syaihu Walid
2. RAFI ANDHIKA GALUH
3. NAH’L ADDINIYAH HASANAH
4. Muh.Wildan Fiqri Ali