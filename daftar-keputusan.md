# Daftar Keputusan (Decision List) - Tarif Parkir Mall

Program: `parkir.py` | Kriteria: Decision Coverage

## Aturan Program

1. Jenis kendaraan: `motor`, `mobil`, `bus`. Selain itu -> `ValueError`
2. Durasi parkir (jam) harus lebih dari 0, dibulatkan ke atas per jam
3. Tarif jam pertama: motor 2.000 | mobil 5.000 | bus 10.000
4. Jam ke-2 dst per jam: motor 1.000 | mobil 3.000 | bus 5.000
5. Batas maksimum harian: motor 10.000 | mobil 25.000 | bus tanpa batas
6. Akhir pekan (sabtu/minggu) tambahan flat 2.000
7. Member dapat potongan 20% dari total, maksimum potongan 3.000
8. Total bayar = (tarif dasar + tambahan akhir pekan) - potongan member

## Daftar Keputusan

| ID | Baris | Fungsi | Keputusan |
|----|-------|--------|-----------|
| D1 | 33 | `hitung_tarif_dasar` | `jenis_kendaraan not in TARIF` |
| D2 | 36 | `hitung_tarif_dasar` | `jam <= 0` |
| D3 | 43 | `hitung_tarif_dasar` | `batas_maksimum is None` |
| D4 | 46 | `hitung_tarif_dasar` | `total > batas_maksimum` |
| D5 | 53 | `tambahan_akhir_pekan` | `hari.lower() in HARI_AKHIR_PEKAN` |
| D6 | 60 | `potongan_member` | `not is_member` |
| D7 | 64 | `potongan_member` | `potongan > MAKS_POTONGAN_MEMBER` |
| D8 | 83 | modul | `__name__ == "__main__"` |

## Ringkasan

- **8 keputusan** (D1-D7 keputusan logika program, D8 penjaga modul)
- 8 keputusan x 2 hasil (True dan False) = **16 cabang** yang harus tercakup
- Semua 8 keputusan punya kedua sisi yang **feasible** (tidak ada cabang mati),
  jadi 100% decision coverage bisa dicapai

Fungsi `hitung_total_bayar` **tidak punya keputusan** karena isinya hanya
memanggil tiga fungsi lain dan menghitung - jadi tidak muncul di daftar ini.

File terkait:

- `test-case.md` - daftar test case (format Myers)
- `matriks-decision-coverage.md` - peta keputusan ke test case
