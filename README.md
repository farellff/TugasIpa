## 📅 Tugas : Final Project membuat Aplikasi Manajemen Klinik dengan Database Flat File (.CSV) & Queue

**Deskripsi**
Program ini dibuat untuk memenuhi tugas UAS Struktur Data.  
Program berupa aplikasi manajemen antrean klinik berbasis console/terminal yang mengimplementasikan struktur data Queue (Antrean) dan Hash Map, serta menggunakan file CSV sebagai database permanen.

## 📂 Struktur File
**Struktur File**
- `main.py` = Kode program utama Python.
- `kunjungan.csv` = Database penyimpanan data rekam medis dan status pasien.
- `Pasien Antrean Management-2026-06-21-162141.png` = Flowchart alur program global.

![Flowchart](Pasien%20Antrean%20Management-2026-06-21-162141.png)
## 🛠️ Fitur Utama

Program memiliki 7 menu utama:
1. **Tambah Rekam Kunjungan Baru (Create)** - Input data pasien baru berupa ID, nama, umur, keluhan, dan diagnosis. Data otomatis disimpan ke CSV dengan status awal 'Antri' dan dimasukkan ke antrean memori.
2. **Lihat Semua Data & Antrean (Read)** - Menampilkan daftar antrean aktif saat ini beserta riwayat rekam medis dari CSV. Memiliki 3 pilihan urutan: sesuai database, urut nama (A-Z), atau urut tanggal (terlama ke terbaru).
3. **Update Rekam Medis Pasien (Update)** - Mengubah data keluhan, diagnosis, atau memperbarui status pasien secara manual (Antri, Selesai, Batal) berdasarkan ID.
4. **Hapus Rekam Medis (Delete)** - Menghapus data rekam medis pasien secara permanen dari file CSV berdasarkan ID yang dipilih.
5. **Panggil Antrean Berikutnya (Process Queue)** - Memanggil pasien terdepan di dalam antrean sesuai prinsip FIFO, lalu otomatis memperbarui statusnya menjadi 'Selesai' di database CSV.
6. **Ubah Tanggal Operasional Simulasi** - Mengubah tanggal simulasi secara fleksibel. Sistem otomatis menarik sisa pasien yang masih berstatus 'Antri' dari tanggal lampau ke antrean hari ini sebagai prioritas.
7. **Keluar** - Keluar dari program dan menampilkan pesan penutup sistem manajemen klinik.

## Cara Menjalankan Program
1. Pastikan Python 3 sudah terinstall.
2. Pastikan file `main.py`, `kunjungan.csv` dan gambar flowchart ada di folder yang sama.
3. Buka terminal/CMD di folder tersebut.
4. Jalankan perintah: `python main.py`.
