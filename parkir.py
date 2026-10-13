"""Tarif Parkir Mall - mini program untuk Tugas Pertemuan 4."""

TARIF = {
    # jenis: (tarif jam pertama, tarif per jam berikutnya, batas maksimum harian)
    "motor": (2000, 1000, 10000),
    "mobil": (5000, 3000, 25000),
}
HARI_AKHIR_PEKAN = {"sabtu", "minggu"}
TAMBAHAN_AKHIR_PEKAN = 2000
PERSEN_MEMBER = 0.20
MAKS_POTONGAN_MEMBER = 3000


def hitung_tarif_dasar(jenis_kendaraan, jam):
    """Tarif dasar sebelum tambahan dan potongan member."""
    if jenis_kendaraan not in TARIF:                    # D1
        raise ValueError("Jenis kendaraan tidak dikenal")
    if jam <= 0:                                        # D2
        raise ValueError("Durasi parkir harus lebih dari 0 jam")

    tarif_pertama, tarif_per_jam, batas_maksimum = TARIF[jenis_kendaraan]
    total = tarif_pertama + (jam - 1) * tarif_per_jam

    if total > batas_maksimum:                          # D3
        return batas_maksimum
    return total


def biaya_akhir_pekan(hari):
    """Tambahan flat kalau parkir di hari sabtu atau minggu."""
    if hari.lower() in HARI_AKHIR_PEKAN:                # D4
        return TAMBAHAN_AKHIR_PEKAN
    return 0


def potongan_member(total, is_member):
    """Potongan 20% untuk member, dibatasi 3.000."""
    if not is_member:                                   # D5
        return 0

    potongan = total * PERSEN_MEMBER
    if potongan > MAKS_POTONGAN_MEMBER:                 # D6
        return MAKS_POTONGAN_MEMBER
    return potongan


def hitung_total_bayar(jenis_kendaraan, jam, hari="senin", is_member=False):
    """Total bayar = tarif dasar + tambahan akhir pekan - potongan member."""
    total = hitung_tarif_dasar(jenis_kendaraan, jam) + biaya_akhir_pekan(hari)
    return total - potongan_member(total, is_member)
