import csv
import os
from datetime import datetime

FILE_NAME = "kunjungan.csv"

# =====================================================================
# INITIALIZATION & DATABASE (CSV) OPERATIONS
# =====================================================================
def init_database():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID_Pasien", "Nama", "Umur", "Keluhan", "Diagnosis", "Tanggal", "Status"])

def scan_tanggal_terlama_antri():
    """
    Mencari tanggal paling lampau dari pasien yang statusnya masih 'Antri'.
    Jika tidak ada yang antre, pakai tanggal hari ini dari sistem komputer.
    """
    init_database()
    tanggal_terlama = None
    
    with open(FILE_NAME, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            status = row.get("Status", "Selesai") or "Selesai"
            if status == "Antri":
                try:
                    tgl_obj = datetime.strptime(row["Tanggal"], "%d-%m-%Y")
                    if tanggal_terlama is None or tgl_obj < tanggal_terlama:
                        tanggal_terlama = tgl_obj
                except ValueError:
                    continue
                    
    if tanggal_terlama:
        return tanggal_terlama.strftime("%d-%m-%Y")
    else:
        # Default balik ke tanggal komputer sekarang jika semua data sudah Selesai/Kosong
        return datetime.now().strftime("%d-%m-%Y")

def load_data(antrean, tanggal_target):
    """
    Memuat data berdasarkan TANGGAL TARGET yang dipilih.
    Menyusun Queue secara kronologis (kronologi tanggal paling lama naik duluan).
    """
    data_map = {}
    init_database()
    
    antrean.queue = []  # Reset antrean memori setiap reload
    semua_baris = []
    
    with open(FILE_NAME, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id_pasien = row["ID_Pasien"]
            status = row.get("Status", "Selesai") or "Selesai"
            
            data_map[id_pasien] = {
                "Nama": row["Nama"],
                "Umur": row["Umur"],
                "Keluhan": row["Keluhan"],
                "Diagnosis": row["Diagnosis"],
                "Tanggal": row["Tanggal"],
                "Status": status
            }
            
            semua_baris.append({
                "id": id_pasien,
                "nama": row["Nama"],
                "tanggal": row["Tanggal"],
                "status": status
            })

    # SORTING KRONOLOGIS (Terlama ke Terbaru)
    def ambil_kunci_tanggal(item):
        try:
            return datetime.strptime(item["tanggal"], "%d-%m-%Y")
        except ValueError:
            return datetime.min

    semua_baris.sort(key=ambil_kunci_tanggal)

    # MASUKKAN KE QUEUE ANTREAN
    antrean_hari_ini = 0
    antrean_sisa_kemarin = 0

    for pasien in semua_baris:
        if pasien["status"] == "Antri":
            if pasien["tanggal"] == tanggal_target:
                antrean.enqueue_all_day(pasien["id"], pasien["nama"])
                antrean_hari_ini += 1
            else:
                antrean.enqueue_all_day(pasien["id"], pasien["nama"])
                antrean_sisa_kemarin += 1
                
    if antrean_sisa_kemarin > 0:
        print(f"⚠️ [Sistem] Terdeteksi {antrean_sisa_kemarin} sisa antrean LAMPAU yang BELUM diperiksa. Dimasukkan ke urutan TERDEPAN!")
    if antrean_hari_ini > 0:
        print(f"✓ [Sistem] Berhasil memuat {antrean_hari_ini} pasien antrean baru untuk tanggal operasional: {tanggal_target}.")
    else:
        print(f"ℹ [Sistem] Tidak ada antrean pasien baru khusus di tanggal {tanggal_target}.")
        
    return data_map

def save_all_data(data_map):
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID_Pasien", "Nama", "Umur", "Keluhan", "Diagnosis", "Tanggal", "Status"])
        for id_pasien, info in data_map.items():
            writer.writerow([id_pasien, info["Nama"], info["Umur"], info["Keluhan"], info["Diagnosis"], info["Tanggal"], info["Status"]])

# =====================================================================
# STRUKTUR DATA: QUEUE
# =====================================================================
class AntreanKlinik:
    def __init__(self):
        self.queue = []

    def enqueue(self, id_pasien, nama):
        self.queue.append({"id": id_pasien, "nama": nama})
        print(f"--> [Antrean] {nama} berhasil dimasukkan ke antrean.")

    def enqueue_all_day(self, id_pasien, nama):
        self.queue.append({"id": id_pasien, "nama": nama})

    def dequeue(self, data_map):
        if self.is_empty():
            print("--> [Antrean] Antrean kosong! Tidak ada pasien yang menunggu.")
            return None
        
        pasien = self.queue.pop(0)
        print(f"--> [Antrean] Pasien {pasien['nama']} dipanggil ke ruang dokter.")
        
        if pasien['id'] in data_map:
            data_map[pasien['id']]["Status"] = "Selesai"
            save_all_data(data_map)
            print(f"✓ [Database] Status pasien {pasien['nama']} diperbarui menjadi 'Selesai'.")
            
        return pasien

    def is_empty(self):
        return len(self.queue) == 0

    def tampilkan_antrean(self):
        if self.is_empty():
            print("Antrean Aktif: (Kosong)")
        else:
            print("Daftar Antrean Pasien Aktif Saat Ini:")
            for i, pasien in enumerate(self.queue, 1):
                print(f"{i}. [{pasien['id']}] {pasien['nama']}")

# =====================================================================
# SORTING ALGORITHM (Bubble Sort berdasarkan Nama)
# =====================================================================
def bubble_sort_by_name(daftar_pasien):
    n = len(daftar_pasien)
    for i in range(n):
        for j in range(0, n-i-1):
            if daftar_pasien[j]["Nama"].lower() > daftar_pasien[j+1]["Nama"].lower():
                daftar_pasien[j], daftar_pasien[j+1] = daftar_pasien[j+1], daftar_pasien[j]
    return daftar_pasien

def bubble_sort_by_date(daftar_pasien):
    """
    Mengurutkan data pasien berdasarkan tanggal paling lama ke terbaru
    menggunakan algoritma Bubble Sort manual.
    """
    n = len(daftar_pasien)
    for i in range(n):
        for j in range(0, n-i-1):
            # Ubah string "DD-MM-YYYY" menjadi objek datetime untuk dibandingkan
            try:
                tgl_j = datetime.strptime(daftar_pasien[j]["Tanggal"], "%d-%m-%Y")
                tgl_j1 = datetime.strptime(daftar_pasien[j+1]["Tanggal"], "%d-%m-%Y")
            except ValueError:
                continue
                
            # Jika tanggal j lebih baru daripada j+1, tukar posisinya (Ascending)
            if tgl_j > tgl_j1:
                daftar_pasien[j], daftar_pasien[j+1] = daftar_pasien[j+1], daftar_pasien[j]
    return daftar_pasien
# =====================================================================
# CORE CRUD OPERATIONS
# =====================================================================
def create_kunjungan(data_map, antrean, tanggal_aktif):
    print("\n--- TAMBAH REKAM KUNJUNGAN ---")
    id_pasien = input("Masukkan ID Pasien (unik): ")
    if id_pasien in data_map:
        print("Error: ID Pasien sudah terdaftar!")
        return
    nama = input("Nama Pasien: ")
    umur = input("Umur: ")
    keluhan = input("Keluhan Utama: ")
    diagnosis = input("Diagnosis Awal: ")
    tanggal = tanggal_aktif

    data_map[id_pasien] = {
        "Nama": nama,
        "Umur": umur,
        "Keluhan": keluhan,
        "Diagnosis": diagnosis,
        "Tanggal": tanggal,
        "Status": "Antri"
    }
    save_all_data(data_map)
    print(f"✓ Data Rekam Medis berhasil disimpan untuk tanggal {tanggal}.")
    antrean.enqueue(id_pasien, nama)

def read_kunjungan(data_map, antrean):
    print("\n--- LIHAT DATA REKAM MEDIS & ANTREAN ---")
    antrean.tampilkan_antrean()
    print("-" * 50)
    
    if not data_map:
        print("Database CSV masih kosong.")
        return

    # Pindahkan semua data dari Hash Map ke list agar bisa disorting
    list_pasien = []
    for id_p, info in data_map.items():
        item = {"ID": id_p}
        item.update(info)
        list_pasien.append(item)

    print("Pilihan Tampilan Riwayat:")
    print("1. Sesuai Urutan Database")
    print("2. Urutkan Berdasarkan Nama Pasien (Sorting Nama)")
    print("3. Urutkan Berdasarkan Tanggal Kunjungan (Sorting Tanggal)")
    pilihan = input("Pilih (1/2/3): ")

    if pilihan == "2":
        list_pasien = bubble_sort_by_name(list_pasien)
        print("\n--- Data Pasien Terurut Berdasarkan Nama (A-Z) ---")
    elif pilihan == "3":
        list_pasien = bubble_sort_by_date(list_pasien)
        print("\n--- Data Pasien Terurut Berdasarkan Tanggal Kunjungan (Terlama -> Terbaru) ---")
    else:
        print("\n--- Data Riwayat Kunjungan Pasien (Sesuai Database) ---")

    # Cetak data ke layar terminal
    for p in list_pasien:
        print(f"ID: {p['ID']} | Nama: {p['Nama']} | Umur: {p['Umur']} | Keluhan: {p['Keluhan']} | Status: {p['Status']} | Tgl: {p['Tanggal']}")

def update_kunjungan(data_map):
    print("\n--- UPDATE REKAM KUNJUNGAN ---")
    id_pasien = input("Masukkan ID Pasien yang dicari (Searching): ")
    if id_pasien in data_map:
        print(f"Data Ditemukan! Pasien atas nama: {data_map[id_pasien]['Nama']}")
        data_map[id_pasien]['Keluhan'] = input(f"Keluhan baru ({data_map[id_pasien]['Keluhan']}): ") or data_map[id_pasien]['Keluhan']
        data_map[id_pasien]['Diagnosis'] = input(f"Diagnosis baru ({data_map[id_pasien]['Diagnosis']}): ") or data_map[id_pasien]['Diagnosis']
        
        print(f"Status saat ini: {data_map[id_pasien]['Status']}")
        print("Pilihan status baru (Tekan ENTER jika tidak ingin mengubah):")
        print("1. Antri\n2. Selesai\n3. Batal")
        pilihan_status = input("Pilih (1/2/3): ")
        if pilihan_status == "1": data_map[id_pasien]['Status'] = "Antri"
        elif pilihan_status == "2": data_map[id_pasien]['Status'] = "Selesai"
        elif pilihan_status == "3": data_map[id_pasien]['Status'] = "Batal"
            
        save_all_data(data_map)
        print("✓ Data dan Status pasien berhasil diperbarui di database CSV.")
    else:
        print("✗ Data pasien tidak ditemukan.")

def delete_kunjungan(data_map):
    print("\n--- HAPUS REKAM KUNJUNGAN ---")
    id_pasien = input("Masukkan ID Pasien yang akan dihapus: ")
    if id_pasien in data_map:
        nama = data_map[id_pasien]['Nama']
        del data_map[id_pasien]
        save_all_data(data_map)
        print(f"✓ Rekam medis pasien {nama} telah dihapus permanen dari CSV.")
    else:
        print("✗ ID Pasien tidak ditemukan.")

# =====================================================================
# MAIN CONTROL PROGRAM
# =====================================================================
def main():
    antrean_klinik = AntreanKlinik()
    
    # [OTOMATISASI] Scan database nyari tanggal paling tua dari pasien yang masih 'Antri'
    tanggal_operasional = scan_tanggal_terlama_antri()
    
    # Load database awal menggunakan tanggal terlama yang ketemu tadi
    database_pasien = load_data(antrean_klinik, tanggal_operasional)

    while True:
        print("\n" + "="*45)
        print(f"SISTEM KLINIK | TANGGAL OPERASIONAL ACTIVE: {tanggal_operasional}")
        print("="*45)
        print("1. Tambah Rekam Kunjungan Baru (Create)")
        print("2. Lihat Semua Data & Antrean (Read)")
        print("3. Update Rekam Medis Pasien (Update)")
        print("4. Hapus Rekam Medis (Delete)")
        print("5. Panggil Antrean Berikutnya (Process Queue)")
        print("6. Ubah Tanggal Operasional Simulasi")
        print("7. Keluar")
        pilihan = input("Pilih Menu (1-7): ")

        if pilihan == "1":
            create_kunjungan(database_pasien, antrean_klinik, tanggal_operasional)
        elif pilihan == "2":
            read_kunjungan(database_pasien, antrean_klinik)
        elif pilihan == "3":
            update_kunjungan(database_pasien)
        elif pilihan == "4":
            delete_kunjungan(database_pasien)
        elif pilihan == "5":
            antrean_klinik.dequeue(database_pasien)
        elif pilihan == "6":
            print("\n--- UBAH TANGGAL SIMULASI ---")
            print(f"Tanggal saat ini berjalan: {tanggal_operasional}")
            input_tgl = input("Masukkan tanggal target baru (Format: DD-MM-YYYY): ")
            if input_tgl:
                tanggal_operasional = input_tgl
                database_pasien = load_data(antrean_klinik, tanggal_operasional)
            else:
                print("Tanggal tidak diubah.")
        elif pilihan == "7":
            print("Terima kasih telah menggunakan sistem manajemen klinik.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()