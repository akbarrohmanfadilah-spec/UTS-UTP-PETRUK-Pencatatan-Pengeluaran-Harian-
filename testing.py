"""testing.py - pengujian program dengan unittest."""
import os
import tempfile
import unittest

from .fileio import baca_data, buat_file_data, tambah_data, tulis_laporan, baca_teks
from .processing import AnalisisPengeluaran, buat_record, total_pengeluaran
from .validasi import DataTidakValidError, validasi_jumlah, validasi_record


class TestKeuangan(unittest.TestCase):
    def setUp(self):
        # Folder sementara agar pengujian tidak menyentuh data asli
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "data.txt")

    def tearDown(self):
        self.folder.cleanup()

    def test_total_pengeluaran_args(self):
        self.assertEqual(total_pengeluaran(10000, 5000, 2500), 17500)

    def test_jumlah_negatif_memunculkan_error(self):
        with self.assertRaises(DataTidakValidError):
            validasi_jumlah(-1)

    def test_field_kosong_memunculkan_error(self):
        with self.assertRaises(DataTidakValidError):
            validasi_record(tanggal="2026-10-01", kategori="", keterangan="x", jumlah=1)

    def test_buat_file_mode_x_tidak_menimpa(self):
        self.assertTrue(buat_file_data(self.path, "2026-10-01;Makanan;Nasi;10000\n"))
        self.assertFalse(buat_file_data(self.path, "ISI BARU\n"))  # sudah ada
        self.assertEqual(len(baca_data(self.path)), 1)             # isi lama aman

    def test_tambah_data_mode_a(self):
        buat_file_data(self.path, "2026-10-01;Makanan;Nasi;10000\n")
        tambah_data(self.path, buat_record(tanggal="2026-10-02", kategori="Transport",
                                           keterangan="Bus", jumlah=5000))
        self.assertEqual(len(baca_data(self.path)), 2)

    def test_baris_rusak_dilewati(self):
        buat_file_data(self.path, "2026-10-01;Makanan;Nasi;10000\n"
                                  "2026-10-02;Makanan;Soto;abc\n"
                                  "baris asal-asalan\n"
                                  "2026-10-03;Hiburan;Film;40000\n")
        self.assertEqual(len(baca_data(self.path)), 2)

    def test_file_tidak_ada_tidak_crash(self):
        self.assertEqual(baca_data(os.path.join(self.folder.name, "tidak_ada.txt")), [])

    def test_rekap_dan_kategori_terboros(self):
        daftar = [buat_record(tanggal="2026-10-01", kategori="Makanan", keterangan="a", jumlah=20000),
                  buat_record(tanggal="2026-10-01", kategori="Makanan", keterangan="b", jumlah=10000),
                  buat_record(tanggal="2026-10-02", kategori="Hiburan", keterangan="c", jumlah=25000)]
        analisis = AnalisisPengeluaran(daftar)
        self.assertEqual(analisis.rekap_per_kategori(), {"Makanan": 30000, "Hiburan": 25000})
        self.assertEqual(analisis.kategori_terboros(), ("Makanan", 30000))

    def test_cari_dengan_kwargs(self):
        daftar = [buat_record(tanggal="2026-10-01", kategori="Makanan", keterangan="a", jumlah=1),
                  buat_record(tanggal="2026-10-02", kategori="Hiburan", keterangan="b", jumlah=2)]
        hasil = AnalisisPengeluaran(daftar).cari(kategori="Hiburan")
        self.assertEqual([p.keterangan for p in hasil], ["b"])

    def test_tulis_laporan_mode_w(self):
        tulis_laporan(self.path, "versi 1\n")
        tulis_laporan(self.path, "versi 2\n")   # harus menggantikan isi lama
        self.assertEqual(baca_teks(self.path), "versi 2\n")


def jalankan_pengujian():
    """Menjalankan seluruh pengujian dan menampilkan hasilnya."""
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestKeuangan)
    return unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    # Jalankan: python -m keuangan.testing
    jalankan_pengujian()
