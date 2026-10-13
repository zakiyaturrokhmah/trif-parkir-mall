# Test Case - Tarif Parkir Mall

Format Myers: **Test case | Input | Expected output**

Program: `parkir.py` | Kriteria: Decision Coverage | Total: **27 test case**

Pemetaan tiap test case ke keputusan yang ditutupnya ada di
`matriks-decision-coverage.md`.

## Fungsi 1: `hitung_tarif_dasar(jenis_kendaraan, jam)`

| Test case | Input | Expected output | Keputusan dicakup |
|-----------|-------|-----------------|-------------------|
| TC01 | `("motor", 1)` | `2000` | D1 F, D2 F, D3 F, D4 F |
| TC02 | `("motor", 5)` | `6000` | D1 F, D2 F, D3 F, D4 F |
| TC03 | `("mobil", 1)` | `5000` | D1 F, D2 F, D3 F, D4 F |
| TC04 | `("bus", 3)` | `20000` | D3 True |
| TC05 | `("motor", 9)` | `10000` | D4 False (boundary tepat di batas) |
| TC06 | `("mobil", 8)` | `25000` | D4 True |
| TC07 | `("motor", 10)` | `10000` | D4 True |
| TC08 | `("bus", 100)` | `505000` | D3 True (tanpa batas) |
| TC09 | `("motor", 0.5)` | `2000` | D2 F (pembulatan ke atas) |
| TC10 | `("motor", 2.5)` | `4000` | D2 F (pembulatan ke atas) |
| TC11 | `("sepeda", 2)` | `ValueError` | D1 True |
| TC12 | `("motor", 0)` | `ValueError` | D2 True |
| TC13 | `("mobil", -2)` | `ValueError` | D2 True |

## Fungsi 2: `tambahan_akhir_pekan(hari)`

| Test case | Input | Expected output | Keputusan dicakup |
|-----------|-------|-----------------|-------------------|
| TC14 | `"sabtu"` | `2000` | D5 True |
| TC15 | `"minggu"` | `2000` | D5 True |
| TC16 | `"senin"` | `0` | D5 False |
| TC17 | `"Sabtu"` | `2000` | D5 True (huruf besar tetap dikenali) |

## Fungsi 3: `potongan_member(total, is_member)`

| Test case | Input | Expected output | Keputusan dicakup |
|-----------|-------|-----------------|-------------------|
| TC18 | `(2000, False)` | `0` | D6 True |
| TC19 | `(2000, True)` | `400` | D6 False, D7 False |
| TC20 | `(27000, True)` | `3000` | D7 True |

## Fungsi 4: `hitung_total_bayar(jenis_kendaraan, jam, hari, is_member)` - integrasi

| Test case | Input | Expected output | Keputusan dicakup |
|-----------|-------|-----------------|-------------------|
| TC21 | `("motor", 1)` | `2000` | D5 F, D6 True |
| TC22 | `("motor", 1, "sabtu", False)` | `4000` | D5 True, D6 True |
| TC23 | `("mobil", 8, "sabtu", True)` | `24000` | D4 True, D5 True, D6 F, D7 True |
| TC24 | `("bus", 2, "minggu", True)` | `14000` | D3 True, D5 True, D6 F, D7 True |
| TC25 | `("mobil", 7, "senin", False)` | `23000` | D4 F, D5 F, D6 True |

## Modul

| Test case | Aksi | Expected output | Keputusan dicakup |
|-----------|------|-----------------|-------------------|
| TC26 | jalankan `parkir.py` sebagai skrip | keluaran memuat `motor 1 jam senin non-member   : 2000` dan `mobil 8 jam sabtu member       : 24000` | D8 True |
| TC27 | impor `parkir` sebagai modul | `parkir.__name__ == "parkir"` | D8 False |

## Alasan tiap expected output

| TC | Alasan |
|----|--------|
| TC01 | Motor jam pertama = tarif dasar, belum ada tambahan jam. |
| TC02 | 2000 + (5-1) x 1000 = 6000. |
| TC03 | Mobil tarif jam pertama 5000. |
| TC04 | Bus 10.000 + 2 x 5.000 = 20.000. |
| TC05 | **Boundary value.** 2000 + 8 x 1000 = 10.000, TEPAT sama dengan batas. Kode memakai `>` bukan `>=`, jadi tidak dipotong. |
| TC06 | 5000 + 7 x 3000 = 26.000 > 25.000 -> dipotong jadi 25.000. |
| TC07 | 2000 + 9 x 1000 = 11.000 > 10.000 -> dipotong jadi 10.000. |
| TC08 | Bus 10.000 + 99 x 5.000 = 505.000. Kalau bus ikut dibatasi, hasilnya bukan ini. |
| TC09 | 0,5 jam dibulatkan ke atas jadi 1 jam. Kalau salah pakai `int()`, jadi 0 jam. |
| TC10 | 2,5 jam -> 3 jam: 2000 + 2 x 1000 = 4000. Kalau `int()`: 3000. |
| TC11 | Jenis tidak dikenal harus ditolak, bukan diam-diam dihitung. |
| TC12 | Durasi 0 tidak masuk akal - negative testing. |
| TC13 | Durasi negatif tidak masuk akal - negative testing. |
| TC14 | Sabtu termasuk akhir pekan. |
| TC15 | Minggu termasuk akhir pekan. |
| TC16 | Senin bukan akhir pekan -> 0. |
| TC17 | `hari.lower()` membuat pengecekan tidak sensitif huruf besar/kecil. |
| TC18 | Non-member langsung `return 0` tanpa menghitung 20%. |
| TC19 | 2000 x 20% = 400, masih di bawah batas 3.000. |
| TC20 | 27.000 x 20% = 5.400 > 3.000 -> dipotong jadi 3.000. |
| TC21 | Integrasi dengan nilai default `hari="senin"`, `is_member=False`. |
| TC22 | 2000 + 2000 - 0 = 4000. |
| TC23 | 25.000 (kena batas harian) + 2.000 = 27.000; potongan 5.400 -> dibatasi 3.000; 27.000 - 3.000 = 24.000. |
| TC24 | 10.000 + 5.000 = 15.000; + 2.000 = 17.000; potongan 3.400 -> dibatasi 3.000; hasil 14.000. |
| TC25 | 5000 + 6 x 3000 = 23.000, belum kena batas 25.000. |
| TC26 | `runpy.run_path(..., run_name="__main__")` membuat `__name__ == "__main__"` True. |
| TC27 | Saat diimpor, `__name__` berisi nama modul sehingga demo tidak ikut jalan. |
