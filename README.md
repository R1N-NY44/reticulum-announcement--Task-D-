# Task D — Reticulum Announcement

## 1. Tujuan

Program ini bertujuan untuk mengimplementasikan komunikasi antara dua node menggunakan Reticulum Network Stack (RNS)

Node A berfungsi sebagai pengirim announcement, sedangkan Node B berfungsi sebagai penerima announcement dan menampilkan pesan yang diterima

Implementasi menggunakan Docker Compose untuk menjalankan kedua node dalam container terpisah

## 2. Arsitektur Sistem

![Ilustrasi komunikasi Node A dan Node B](illust/Screenshot%202026-10-13%20202153.png)

*(itu gambar cloud, cuman aku nga dapet asset yg bagus, jadi pakai bulet2)

Sistem terdiri dari tiga komponen utama

- **Node A** sebagai pengirim announcement
- **Reticulum** sebagai network stack yang mengelola identity, destination, dan announcement
- **Node B** sebagai penerima announcement

Kedua node berkomunikasi menggunakan TCP interface melalui jaringan internal Docker pada port `4242`

## 3. Penjelasan Komponen

### 3.1 Node A — Sender

Node A berfungsi sebagai pengirim announcement

Proses yang dilakukan oleh Node A meliputi

1. Menginisialisasi Reticulum
2. Membuat identity baru atau memuat identity yang telah tersimpan
3. Membuat destination berdasarkan identity
4. Menghubungkan TCP client ke `node_b:4242`
5. Mengirim announcement dengan application data berisi pesan `Hello from Node A!`

Identity digunakan sebagai identitas kriptografis dalam Reticulum, sedangkan destination merupakan alamat logis yang mengidentifikasi tujuan komunikasi

Pesan dikodekan menggunakan UTF-8 sebelum dimasukkan ke dalam application data pada announcement

### 3.2 Reticulum dan TCP Interface

Reticulum mengelola komunikasi pada tingkat jaringan Reticulum, termasuk identity, destination, dan announcement

TCP digunakan sebagai interface transport yang menghubungkan Node A dan Node B

Node A bertindak sebagai TCP client yang terhubung ke hostname `node_b` pada port `4242`

Node B bertindak sebagai TCP server yang mendengarkan koneksi masuk pada port `4242`

TCP port merupakan bagian dari mekanisme transport, sedangkan destination Reticulum merupakan alamat logis dalam jaringan Reticulum

### 3.3 Node B — Receiver

Node B berfungsi sebagai penerima announcement

Proses yang dilakukan oleh Node B meliputi

1. Menginisialisasi Reticulum
2. Membuka TCP server pada port `4242`
3. Mendaftarkan announcement handler
4. Menerima announcement melalui mekanisme Reticulum
5. Menampilkan destination hash
6. Mendekode application data menggunakan UTF-8
7. Menampilkan pesan yang diterima

Announcement handler memproses announcement yang diterima oleh Reticulum

Application data didekode menggunakan UTF-8 agar dapat ditampilkan sebagai teks

## 4. Alur Kerja Program

1. Docker Compose menjalankan Node A dan Node B dalam container terpisah
2. Node B menginisialisasi Reticulum dan membuka TCP server pada port `4242`
3. Node B mendaftarkan announcement handler
4. Node A menginisialisasi Reticulum dan terhubung ke `node_b:4242`
5. Node A membuat atau memuat identity
6. Node A membuat destination Reticulum
7. Node A mengirim announcement dengan application data
8. Node B menerima announcement melalui announcement handler
9. Node B menampilkan destination hash dan mendekode application data menggunakan UTF-8
10. Node B menampilkan pesan yang diterima pada log container

## 5. Implementasi Docker

Docker digunakan untuk menjalankan Node A dan Node B dalam lingkungan terisolasi

Docker Compose mengatur pembangunan image, pembuatan container, jaringan internal, dan penyimpanan konfigurasi Reticulum

File `Dockerfile` digunakan untuk menyiapkan lingkungan Python dan memasang dependensi `rns`

File `docker-compose.yml` digunakan untuk menjalankan kedua node sebagai layanan terpisah

Jaringan bridge Docker memungkinkan Node A mengakses Node B melalui hostname `node_b` tanpa harus mengekspos port `4242` ke jaringan eksternal

## 6. Hasil Pengujian

Pengujian dilakukan dengan menjalankan layanan menggunakan Docker Compose dan memeriksa status container serta log komunikasi

Node B berhasil berjalan sebagai penerima dan mendengarkan koneksi TCP pada port `4242`

Node A berhasil mengirim announcement melalui Reticulum

Node B berhasil menerima announcement, menampilkan destination hash, dan mendekode application data menggunakan UTF-8

![Hasil pengujian melalui Docker CLI](illust/Screenshot%202026-10-13%20204031.png)

## 7. Kesimpulan

Program berhasil mengimplementasikan komunikasi announcement menggunakan Reticulum Network Stack

Node A membuat atau memuat identity, membentuk destination, dan mengirim announcement yang membawa application data

Node B menerima announcement melalui handler Reticulum dan menampilkan destination hash serta pesan yang diterima

Docker Compose digunakan untuk menjalankan kedua node dalam container terpisah dan menyediakan jaringan internal untuk komunikasi TCP
