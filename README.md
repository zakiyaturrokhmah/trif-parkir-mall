# Tarif Parkir Mall (Python)

Mini program untuk Tugas Pertemuan 4 - Analisis dan Pengujian Sistem (High Order
Testing): Unit Testing dan Test Case Design dengan kriteria **Decision Coverage**.

## Aturan Program

- Jenis kendaraan: `motor`, `mobil`, `bus`. Selain itu -> `ValueError`
- Durasi parkir (jam) harus lebih dari 0, dibulatkan ke atas per jam
- Tarif jam pertama: motor 2.000 | mobil 5.000 | bus 10.000
- Jam ke-2 dst per jam: motor 1.000 | mobil 3.000 | bus 5.000
- Batas maksimum harian: motor 10.000 | mobil 25.000 | bus tanpa batas
- Akhir pekan (sabtu/minggu) tambahan flat 2.000
- Member dapat potongan 20% dari total, maksimum potongan 3.000
- Total bayar = (tarif dasar + tambahan akhir pekan) - potongan member

## Fungsi

| Fungsi | Isi |
|--------|-----|
| `hitung_tarif_dasar(jenis_kendaraan, jam)` | tarif dasar + pembulatan ke atas + batas maksimum harian |
| `tambahan_akhir_pekan(hari)` | tambahan flat 2.000 untuk sabtu/minggu |
| `potongan_member(total, is_member)` | potongan 20% dibatasi 3.000 |
| `hitung_total_bayar(jenis_kendaraan, jam, hari, is_member)` | gabungan ketiga fungsi di atas |

## Cara Menjalankan

    python parkir.py                 # demo singkat (nilai tetap)

## Unit Test

    python -m unittest -v test_parkir

Hasil: 27 test, semua lulus.

## Cek Decision Coverage

    python -m pip install coverage
    python -m coverage run --branch -m unittest test_parkir
    python -m coverage report -m --include=parkir.py

Hasil:

    Name        Stmts   Miss Branch BrPart  Cover   Missing
    -------------------------------------------------------
    parkir.py      40      0     16      0   100%

8 keputusan x 2 hasil = 16 cabang, semuanya tercakup.

## Struktur

Test Case Design dipisah menjadi tiga berkas: **Daftar Keputusan -> Test Case -> Matriks**.

| Berkas | Isi |
|--------|-----|
| `parkir.py` | Program (4 fungsi, logikanya fungsi murni tanpa input/print) |
| `test_parkir.py` | 27 unit test (semua lulus) |
| `daftar-keputusan.md` | Daftar 8 keputusan (D1-D8) pada program |
| `test-case.md` | Daftar 27 test case, format Myers (Test case, Input, Expected output) + alasan |
| `matriks-decision-coverage.md` | Matriks keputusan ke test case + hasil tool coverage |
| `test-case-design.md` | Ringkasan + penunjuk ke tiga berkas di atas |
| `ukur_matriks.py` | Alat bantu: mengukur per test case keputusan mana yang kena True/False |

## Kenapa program ini gampang diuji

- Semua logika ada di fungsi murni: input angka/teks -> output angka, **tanpa**
  `input()` dan tanpa `print()`, jadi tidak perlu mocking sama sekali
- Tiap fungsi punya sedikit keputusan dengan kondisi jelas
- Tiap keputusan punya kedua sisi yang **feasible** (tidak ada cabang mati),
  jadi 100% decision coverage benar-benar bisa dicapai
- Batas-batasnya berupa angka nyata, sehingga boundary value testing
  (TC05: tepat di batas, TC09/TC10: pembulatan) langsung kelihatan gunanya
