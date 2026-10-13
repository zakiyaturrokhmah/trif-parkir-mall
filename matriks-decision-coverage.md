# Matriks Decision Coverage - Tarif Parkir Mall

Program: `parkir.py` | Kriteria: Decision Coverage

Daftar keputusan: `daftar-keputusan.md` | Daftar test case: `test-case.md`

## Matriks Keputusan -> Test Case

Diukur otomatis per test case: tiap test dijalankan satu-satu dengan
`sys.settrace`, lalu dicatat cabang mana yang diambil (`python ukur_matriks.py`).

| Keputusan | True dicakup oleh | False dicakup oleh |
|-----------|-------------------|--------------------|
| D1 `jenis_kendaraan not in TARIF` | TC11 | TC01, TC02, TC03, TC04, TC05, TC06, TC07, TC08, TC09, TC10 |
| D2 `jam <= 0` | TC12, TC13 | TC01, TC02, TC03, TC04, TC05, TC06, TC07, TC08, TC09, TC10 |
| D3 `batas_maksimum is None` | TC04, TC08, TC24 | TC01, TC02, TC03, TC05, TC06, TC07, TC09, TC10 |
| D4 `total > batas_maksimum` | TC06, TC07, TC23 | TC01, TC02, TC03, TC05, TC09, TC10 |
| D5 `hari.lower() in HARI_AKHIR_PEKAN` | TC14, TC15, TC17, TC22, TC23, TC24 | TC16, TC21, TC25 |
| D6 `not is_member` | TC18, TC21, TC22, TC25 | TC19, TC20, TC23, TC24 |
| D7 `potongan > MAKS_POTONGAN_MEMBER` | TC20, TC23, TC24 | TC19 |
| D8 `__name__ == "__main__"` | TC26 | TC27 |

**Semua 16 cabang (8 keputusan x 2) tercakup oleh 27 test case.**

## Peta balik: test case mana mengeksekusi keputusan apa

Keterangan: T = keputusan jadi True, F = keputusan jadi False.

| Test case | Keputusan yang dieksekusi |
|-----------|---------------------------|
| TC01-TC03, TC09, TC10 | D1(F), D2(F), D3(F), D4(F) |
| TC04, TC08 | D1(F), D2(F), D3(T) |
| TC05 | D1(F), D2(F), D3(F), D4(F) |
| TC06, TC07 | D1(F), D2(F), D3(F), D4(T) |
| TC11 | D1(T) |
| TC12, TC13 | D1(F), D2(T) |
| TC14, TC15, TC17 | D5(T) |
| TC16 | D5(F) |
| TC18 | D6(T) |
| TC19 | D6(F), D7(F) |
| TC20 | D6(F), D7(T) |
| TC21 | D5(F), D6(T) |
| TC22 | D5(T), D6(T) |
| TC23 | D4(T), D5(T), D6(F), D7(T) |
| TC24 | D3(T), D5(T), D6(F), D7(T) |
| TC25 | D4(F), D5(F), D6(T) |
| TC26 | D8(T) |
| TC27 | D8(F) |

## Hasil tool

```
$ python -m unittest test_parkir
Ran 27 tests in 0.004s

OK

$ python -m coverage run --branch -m unittest test_parkir
$ python -m coverage report -m --include=parkir.py
Name        Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------
parkir.py      40      0     16      0   100%
```

- `Branch 16` = 8 keputusan x 2
- `BrPart 0` = tidak ada cabang yang setengah jalan
- `Missing` kosong = tidak ada baris/cabang yang terlewat
