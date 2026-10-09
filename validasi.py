"""validasi.py - pengecekan input dan data pengeluaran."""
from datetime import datetime


class DataTidakValidError(Exception):
    """Exception buatan sendiri: dimunculkan saat data tidak valid."""


def validasi_teks(nilai, nama_field):
    """Memastikan teks tidak kosong dan tidak mengandung pemisah ';'."""
    if nilai is None or not str(nilai).strip():
        # raise: field kosong tidak diperbolehkan
        raise DataTidakValidError(f"Field '{nama_field}' tidak boleh kosong")
    teks = str(nilai).strip()
    if ";" in teks:
        raise DataTidakValidError(f"Field '{nama_field}' tidak boleh mengandung ';'")
    return teks


def validasi_jumlah(nilai):
    """Mengubah nilai menjadi int, menolak angka negatif atau bukan angka."""
    try:
        jumlah = int(nilai)
    except (ValueError, TypeError):
        raise DataTidakValidError(f"Jumlah harus berupa angka bulat, diterima: {nilai!r}")
    if jumlah < 0:
        # raise: jumlah negatif tidak diperbolehkan
        raise DataTidakValidError("Jumlah tidak boleh negatif")
    return jumlah


def validasi_tanggal(nilai):
    """Memastikan tanggal berformat YYYY-MM-DD."""
    try:
        datetime.strptime(str(nilai), "%Y-%m-%d")
    except ValueError:
        raise DataTidakValidError(f"Tanggal harus berformat YYYY-MM-DD, diterima: {nilai!r}")
    return str(nilai)


def validasi_record(**data):
    """Memvalidasi satu record. Atribut diterima lewat **kwargs."""
    for field in ("tanggal", "kategori", "keterangan", "jumlah"):
        if field not in data:
            raise DataTidakValidError(f"Field '{field}' tidak ditemukan")
    return {
        "tanggal": validasi_tanggal(data["tanggal"]),
        "kategori": validasi_teks(data["kategori"], "kategori").title(),
        "keterangan": validasi_teks(data["keterangan"], "keterangan"),
        "jumlah": validasi_jumlah(data["jumlah"]),
    }


if __name__ == "__main__":
    # Pengujian lokal modul validasi (dijalankan: python validasi.py)
    print(validasi_record(tanggal="2026-10-01", kategori="makanan",
                          keterangan="Nasi goreng", jumlah="15000"))
    for kasus in ({"tanggal": "2026-10-01", "kategori": "", "keterangan": "x", "jumlah": 1},
                  {"tanggal": "2026-10-01", "kategori": "Makanan", "keterangan": "x", "jumlah": -5}):
        try:
            validasi_record(**kasus)
        except DataTidakValidError as err:
            print("Ditolak:", err)
