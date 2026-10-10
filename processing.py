"""processing.py - class data serta perhitungan dan analisis pengeluaran."""
from .validasi import DataTidakValidError, validasi_record


def total_pengeluaran(*jumlah):
    """Menjumlahkan sejumlah angka pengeluaran (*args)."""
    # assert: jumlah negatif tidak seharusnya sampai ke tahap perhitungan
    assert all(j >= 0 for j in jumlah), "Jumlah pengeluaran tidak boleh negatif"
    return sum(jumlah)


def format_rupiah(angka):
    """Memformat angka menjadi teks rupiah, contoh: Rp15.000."""
    return "Rp" + f"{angka:,.0f}".replace(",", ".")


class Pengeluaran:
    """Satu catatan pengeluaran."""

    def __init__(self, tanggal, kategori, keterangan, jumlah):
        self.tanggal = tanggal
        self.kategori = kategori
        self.keterangan = keterangan
        self.jumlah = jumlah

    def ke_baris(self):
        """Mengubah objek menjadi satu baris teks untuk disimpan ke file."""
        return f"{self.tanggal};{self.kategori};{self.keterangan};{self.jumlah}"

    @classmethod
    def dari_baris(cls, baris):
        """Membuat objek dari satu baris teks; error jika format salah."""
        bagian = baris.strip().split(";")
        if len(bagian) != 4:
            raise DataTidakValidError(f"Jumlah kolom harus 4, ditemukan {len(bagian)}")
        tanggal, kategori, keterangan, jumlah = bagian
        return cls(**validasi_record(tanggal=tanggal, kategori=kategori,
                                     keterangan=keterangan, jumlah=jumlah))

    def __repr__(self):
        return f"Pengeluaran({self.ke_baris()})"


def buat_record(**atribut):
    """Membuat objek Pengeluaran dari atribut bervariasi (**kwargs) setelah divalidasi."""
    return Pengeluaran(**validasi_record(**atribut))


class AnalisisPengeluaran:
    """Kumpulan fungsi analisis untuk daftar pengeluaran."""

    def __init__(self, daftar):
        self.daftar = daftar

    def total(self):
        """Total seluruh pengeluaran."""
        return total_pengeluaran(*[p.jumlah for p in self.daftar])

    def rata_rata_harian(self):
        """Rata-rata pengeluaran per hari (hanya hari yang ada catatannya)."""
        if not self.daftar:
            return 0
        hari_unik = {p.tanggal for p in self.daftar}
        return self.total() / len(hari_unik)

    def rekap_per_kategori(self):
        """Dictionary total pengeluaran untuk setiap kategori."""
        rekap = {}
        for p in self.daftar:
            rekap[p.kategori] = rekap.get(p.kategori, 0) + p.jumlah
        return rekap

    def kategori_terboros(self):
        """Mengembalikan (kategori, total) dengan pengeluaran terbesar."""
        rekap = self.rekap_per_kategori()
        if not rekap:
            return None
        return max(rekap.items(), key=lambda item: item[1])  # lambda sebagai key

    def terbesar(self, n=3):
        """n pengeluaran terbesar, diurutkan menurun."""
        return sorted(self.daftar, key=lambda p: p.jumlah, reverse=True)[:n]

    def cari(self, **kriteria):
        """Mencari data dengan kriteria bebas, contoh: cari(kategori='Makanan')."""
        return list(filter(
            lambda p: all(getattr(p, k, None) == v for k, v in kriteria.items()),
            self.daftar))


def susun_laporan(analisis):
    """Menyusun teks laporan dari objek AnalisisPengeluaran."""
    baris = ["LAPORAN PENGELUARAN HARIAN", "=" * 40]
    baris.append(f"Jumlah catatan       : {len(analisis.daftar)}")
    baris.append(f"Total pengeluaran    : {format_rupiah(analisis.total())}")
    baris.append(f"Rata-rata per hari   : {format_rupiah(analisis.rata_rata_harian())}")
    baris.append("-" * 40)
    baris.append("Rekap per kategori:")
    total = analisis.total() or 1  # hindari pembagian dengan nol
    for kategori, jumlah in sorted(analisis.rekap_per_kategori().items(),
                                   key=lambda item: item[1], reverse=True):
        baris.append(f"  {kategori:<10}: {format_rupiah(jumlah):>12} ({jumlah / total * 100:.1f}%)")
    terboros = analisis.kategori_terboros()
    if terboros:
        baris.append(f"Kategori terboros    : {terboros[0]} ({format_rupiah(terboros[1])})")
    baris.append("-" * 40)
    baris.append("3 pengeluaran terbesar:")
    for p in analisis.terbesar(n=3):  # keyword argument
        baris.append(f"  {p.tanggal} {p.keterangan:<18} {format_rupiah(p.jumlah):>10}")
    return "\n".join(baris) + "\n"


if __name__ == "__main__":
    # Pengujian lokal (dijalankan: python -m keuangan.processing)
    contoh = [buat_record(tanggal="2026-10-01", kategori="makanan", keterangan="Makan siang", jumlah=20000),
              buat_record(tanggal="2026-10-01", kategori="transport", keterangan="Ojek", jumlah=15000)]
    print(susun_laporan(AnalisisPengeluaran(contoh)))
