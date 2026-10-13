"""Unit test + Decision Coverage untuk Tarif Parkir Mall.

Jalankan:
    python -m unittest -v test_parkir

Cek decision coverage:
    python -m coverage run --branch -m unittest test_parkir
    python -m coverage report -m --include=parkir.py

Setiap nama test memuat ID test case (TC) dan ID keputusan (D) yang ditutupnya,
supaya jelas kenapa input itu yang dipilih.
"""
import io
import os
import runpy
import unittest
from contextlib import redirect_stdout

from parkir import (
    hitung_tarif_dasar,
    tambahan_akhir_pekan,
    potongan_member,
    hitung_total_bayar,
)

BASE = os.path.dirname(os.path.abspath(__file__))
PATH_PARKIR = os.path.join(BASE, "parkir.py")


# =========================================================================
# Fungsi 1: hitung_tarif_dasar  -> D1 (jenis dikenal), D2 (jam > 0),
#                                 D3 (bus tanpa batas), D4 (kena batas)
# =========================================================================
class TestHitungTarifDasar(unittest.TestCase):

    def test_TC01_motor_satu_jam_tarif_jam_pertama(self):
        """D1 F, D2 F, D3 F, D4 F"""
        self.assertEqual(hitung_tarif_dasar("motor", 1), 2000)

    def test_TC02_motor_lima_jam_tambah_per_jam(self):
        """2000 + 4 x 1000"""
        self.assertEqual(hitung_tarif_dasar("motor", 5), 6000)

    def test_TC03_mobil_satu_jam(self):
        self.assertEqual(hitung_tarif_dasar("mobil", 1), 5000)

    def test_TC04_D3_true_bus_tanpa_batas_maksimum(self):
        """Bus: batas maksimum None, tarif dibiarkan tumbuh"""
        self.assertEqual(hitung_tarif_dasar("bus", 3), 20000)

    def test_TC08_D3_true_bus_durasi_panjang(self):
        """Bukti bus benar-benar tanpa batas: 10000 + 99 x 5000"""
        self.assertEqual(hitung_tarif_dasar("bus", 100), 505000)

    def test_TC05_D4_false_boundary_tepat_di_batas(self):
        """Boundary value: motor 9 jam = 2000 + 8 x 1000 = 10000,
        TEPAT sama dengan batas. Kode memakai '>' bukan '>=',
        jadi hasilnya tetap 10000 lewat jalur normal, bukan dipotong."""
        self.assertEqual(hitung_tarif_dasar("motor", 9), 10000)

    def test_TC06_D4_true_mobil_kena_batas_maksimum(self):
        """5000 + 7 x 3000 = 26000 > 25000 -> dipotong jadi 25000"""
        self.assertEqual(hitung_tarif_dasar("mobil", 8), 25000)

    def test_TC07_D4_true_motor_kena_batas_maksimum(self):
        """2000 + 9 x 1000 = 11000 > 10000 -> dipotong jadi 10000"""
        self.assertEqual(hitung_tarif_dasar("motor", 10), 10000)

    def test_TC09_jam_pecahan_dibulatkan_ke_atas(self):
        """0.5 jam tetap dihitung 1 jam -> tarif jam pertama"""
        self.assertEqual(hitung_tarif_dasar("motor", 0.5), 2000)

    def test_TC10_jam_pecahan_lebih_dari_satu(self):
        """2.5 jam dibulatkan jadi 3 jam -> 2000 + 2 x 1000"""
        self.assertEqual(hitung_tarif_dasar("motor", 2.5), 4000)

    def test_TC11_D1_true_jenis_kendaraan_tidak_dikenal(self):
        with self.assertRaises(ValueError):
            hitung_tarif_dasar("sepeda", 2)

    def test_TC12_D2_true_jam_nol(self):
        with self.assertRaises(ValueError):
            hitung_tarif_dasar("motor", 0)

    def test_TC13_D2_true_jam_negatif(self):
        with self.assertRaises(ValueError):
            hitung_tarif_dasar("mobil", -2)


# =========================================================================
# Fungsi 2: tambahan_akhir_pekan -> D5
# =========================================================================
class TestTambahanAkhirPekan(unittest.TestCase):

    def test_TC14_D5_true_sabtu(self):
        self.assertEqual(tambahan_akhir_pekan("sabtu"), 2000)

    def test_TC15_D5_true_minggu(self):
        self.assertEqual(tambahan_akhir_pekan("minggu"), 2000)

    def test_TC16_D5_false_hari_kerja(self):
        self.assertEqual(tambahan_akhir_pekan("senin"), 0)

    def test_TC17_huruf_besar_tetap_dikenali(self):
        """hari di-lowercase dulu, jadi 'Sabtu' tetap kena tambahan"""
        self.assertEqual(tambahan_akhir_pekan("Sabtu"), 2000)


# =========================================================================
# Fungsi 3: potongan_member -> D6 (member), D7 (batas potongan)
# =========================================================================
class TestPotonganMember(unittest.TestCase):

    def test_TC18_D6_true_bukan_member(self):
        self.assertEqual(potongan_member(2000, False), 0)

    def test_TC19_D6_false_D7_false_member_potongan_normal(self):
        """2000 x 20% = 400, masih di bawah batas 3000"""
        self.assertEqual(potongan_member(2000, True), 400)

    def test_TC20_D7_true_potongan_kena_batas_maksimum(self):
        """27000 x 20% = 5400 > 3000 -> dipotong jadi 3000"""
        self.assertEqual(potongan_member(27000, True), 3000)


# =========================================================================
# Fungsi 4: hitung_total_bayar (integrasi ketiga fungsi di atas)
# =========================================================================
class TestHitungTotalBayar(unittest.TestCase):

    def test_TC21_total_motor_satu_jam_hari_kerja_non_member(self):
        self.assertEqual(hitung_total_bayar("motor", 1), 2000)

    def test_TC22_total_motor_akhir_pekan_non_member(self):
        """2000 + 2000 tambahan - 0 potongan"""
        self.assertEqual(hitung_total_bayar("motor", 1, "sabtu", False), 4000)

    def test_TC23_total_mobil_akhir_pekan_member_kena_semua_batas(self):
        """25000 (kena batas harian) + 2000 (akhir pekan) - 3000 (kena batas potongan)"""
        self.assertEqual(hitung_total_bayar("mobil", 8, "sabtu", True), 24000)

    def test_TC24_total_bus_akhir_pekan_member(self):
        """15000 + 2000 = 17000; 17000 x 20% = 3400 -> dipotong 3000 -> 14000"""
        self.assertEqual(hitung_total_bayar("bus", 2, "minggu", True), 14000)

    def test_TC25_total_mobil_tujuh_jam_hari_kerja_non_member(self):
        """5000 + 6 x 3000 = 23000, belum kena batas 25000"""
        self.assertEqual(hitung_total_bayar("mobil", 7, "senin", False), 23000)


# =========================================================================
# Blok if __name__ == "__main__" -> D8 (dua sisi harus dieksekusi)
# =========================================================================
class TestBlokUtama(unittest.TestCase):

    def test_TC26_D8_true_dijalankan_sebagai_skrip(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            runpy.run_path(PATH_PARKIR, run_name="__main__")
        hasil = buf.getvalue()
        self.assertIn("motor 1 jam senin non-member   : 2000", hasil)
        self.assertIn("mobil 8 jam sabtu member       : 24000", hasil)

    def test_TC27_D8_false_diimpor_sebagai_modul(self):
        """Saat diimpor, __name__ != '__main__' sehingga demo tidak ikut jalan."""
        import parkir
        self.assertEqual(parkir.__name__, "parkir")
        self.assertNotEqual(parkir.__name__, "__main__")


if __name__ == "__main__":
    unittest.main(verbosity=2)
