"""main.py - program utama Pencatat Pengeluaran Harian."""
import os
from datetime import date

from keuangan.fileio import baca_data, baca_teks, buat_file_data, tambah_data, tulis_laporan
from keuangan.processing import AnalisisPengeluaran, buat_record, format_rupiah, susun_laporan
from keuangan.testing import jalankan_pengujian
from keuangan.validasi import DataTidakValidError

# Path dibuat dari lokasi main.py agar program bisa dijalankan dari folder mana pun
FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_DATA = os.path.join(FOLDER, "data", "pengeluaran.txt")
PATH_LAPORAN = os.path.join(FOLDER, "laporan", "laporan_pengeluaran.txt")

DATA_AWAL = (
    "2026-10-01;Makanan;Nasi goreng;15000\n"
    "2026-10-01;Transport;Ojek online;22000\n"
    "2026-10-02;Makanan;Makan siang;20000\n"
    "2026-10-02;Belanja;Alat tulis;35000\n"
    "2026-10-03;Hiburan;Tiket bioskop;50000\n"
    "2026-10-04;Makanan;Kopi;18000\n"
    "2026-10-05;Transport;Bensin;40000\n"
    "2026-10-05;Belanja;Buku catatan;27000\n"
)


def siapkan_file():
    """Membuat folder dan file data awal (mode x) bila belum ada."""
    os.makedirs(os.path.dirname(PATH_DATA), exist_ok=True)
    os.makedirs(os.path.dirname(PATH_LAPORAN), exist_ok=True)
    if buat_file_data(PATH_DATA, isi_awal=DATA_AWAL):
        print("File data baru dibuat dengan contoh data.")


def menu_tambah():
    """Meminta input pengguna lalu menyimpan satu catatan (mode a)."""
    tanggal = input("Tanggal (YYYY-MM-DD, kosong = hari ini): ").strip() or date.today().isoformat()
    kategori = input("Kategori   : ")
    keterangan = input("Keterangan : ")
    jumlah = input("Jumlah (Rp): ")
    try:
        catatan = buat_record(tanggal=tanggal, kategori=kategori, keterangan=keterangan, jumlah=jumlah)
    except DataTidakValidError as err:
        print("Data ditolak:", err)
        return
    tambah_data(PATH_DATA, catatan)
    print("Tersimpan:", catatan)


def menu_tampilkan():
    """Menampilkan semua catatan diurutkan berdasarkan tanggal."""
    daftar = sorted(baca_data(PATH_DATA), key=lambda p: p.tanggal)
    for nomor, p in enumerate(daftar, start=1):
        print(f"{nomor:>2}. {p.tanggal} {p.kategori:<10} {p.keterangan:<18} {format_rupiah(p.jumlah):>10}")
    print(f"Total {len(daftar)} catatan.")


def menu_cari():
    """Mencari catatan berdasarkan kategori."""
    kategori = input("Kategori yang dicari: ").strip().title()
    for p in AnalisisPengeluaran(baca_data(PATH_DATA)).cari(kategori=kategori):
        print(f"  {p.tanggal} {p.keterangan:<18} {format_rupiah(p.jumlah):>10}")


def menu_laporan():
    """Membuat laporan (mode w) lalu menampilkannya di layar."""
    teks = susun_laporan(AnalisisPengeluaran(baca_data(PATH_DATA)))
    tulis_laporan(PATH_LAPORAN, teks)
    print(baca_teks(PATH_LAPORAN))


def main():
    siapkan_file()
    pilihan = {"1": menu_tambah, "2": menu_tampilkan, "3": menu_cari,
               "4": menu_laporan, "5": jalankan_pengujian}
    while True:
        print("\n=== PENCATAT PENGELUARAN HARIAN ===")
        print("1. Tambah pengeluaran\n2. Tampilkan semua data\n3. Cari berdasarkan kategori")
        print("4. Buat laporan\n5. Jalankan pengujian\n0. Keluar")
        kode = input("Pilih menu: ").strip()
        if kode == "0":
            print("Sampai jumpa!")
            break
        aksi = pilihan.get(kode)
        if aksi:
            aksi()
        else:
            print("Pilihan tidak dikenal.")


if __name__ == "__main__":
    main()
