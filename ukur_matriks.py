"""Ukur per-test-case: keputusan (D) mana yang dieksekusi dan bernilai apa.

Cara: setiap test dijalankan satu-satu dengan sys.settrace, lalu diperiksa
"setelah baris keputusan X, eksekusi lompat ke baris berapa" -> itu yang
menentukan keputusannya True atau False.

Hasilnya dipakai buat mengisi matriks D <-> TC di test-case-design.md.
Jalankan: python ukur_matriks.py
"""
import importlib.util
import io
import os
import sys
import unittest

BASE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE, "parkir.py")
TARGET = os.path.realpath(FILE)

# baris -> (ID, baris tujuan kalau True, baris tujuan kalau False)
DECISION = {
    33: ("D1", 34, 36),
    36: ("D2", 37, 39),
    43: ("D3", 44, 46),
    46: ("D4", 47, 48),
    53: ("D5", 54, 55),
    60: ("D6", 61, 63),
    64: ("D7", 65, 66),
    83: ("D8", 84, -1),      # -1 = keluar dari modul
}

TEKS = {
    "D1": "jenis_kendaraan not in TARIF",
    "D2": "jam <= 0",
    "D3": "batas_maksimum is None",
    "D4": "total > batas_maksimum",
    "D5": "hari.lower() in HARI_AKHIR_PEKAN",
    "D6": "not is_member",
    "D7": "potongan > MAKS_POTONGAN_MEMBER",
    "D8": '__name__ == "__main__"',
}


def lacak(fn):
    """Jalankan fn(), kembalikan urutan baris parkir.py yang dieksekusi."""
    jejak = []

    def local_trace(frame, event, arg):
        if event == "line":
            jejak.append(frame.f_lineno)
        return local_trace

    def global_trace(frame, event, arg):
        if frame.f_code.co_filename and os.path.realpath(frame.f_code.co_filename) == TARGET:
            return local_trace
        return None

    sys.settrace(global_trace)
    try:
        fn()
    finally:
        sys.settrace(None)
    return jejak


def nilai_keputusan(jejak):
    """Dari urutan baris -> {D: 'T'/'F'}."""
    kena = {}
    for i, baris in enumerate(jejak):
        if baris not in DECISION:
            continue
        did, ke_true, ke_false = DECISION[baris]
        berikut = jejak[i + 1] if i + 1 < len(jejak) else -1
        if berikut == ke_true:
            kena.setdefault(did, set()).add("T")
        elif berikut == ke_false:
            kena.setdefault(did, set()).add("F")
        else:
            kena.setdefault(did, set()).add("?")
    return {d: "".join(sorted(v)) for d, v in kena.items()}


def iter_tes(suite):
    for t in suite:
        if isinstance(t, unittest.TestSuite):
            yield from iter_tes(t)
        else:
            yield t


suite = unittest.TestLoader().loadTestsFromName("test_parkir")
hasil = {}

for tes in iter_tes(suite):
    nama = tes.id().split(".")[-1]
    hasil_tes = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(
        unittest.TestSuite([tes]))
    if not hasil_tes.wasSuccessful():
        raise SystemExit("TEST GAGAL: " + nama)
    hasil[nama] = nilai_keputusan(lacak(tes))

# ---- D8 sisi False diukur terpisah: saat modul diimpor, bukan dijalankan ----
spec = importlib.util.spec_from_file_location("parkir_probe", FILE)
modul = importlib.util.module_from_spec(spec)
d8_import = nilai_keputusan(lacak(lambda: spec.loader.exec_module(modul))).get("D8", "-")

print("=" * 128)
print("PETA TEST -> KEPUTUSAN (T = keputusan jadi True, F = jadi False)")
print("=" * 128)
print(f"{'TEST':<62} {'Keputusan yang dieksekusi'}")
print("-" * 128)
for nama in hasil:
    isi = ", ".join(f"{d}({v})" for d, v in sorted(hasil[nama].items()))
    print(f"{nama:<62} {isi or '-'}")
print(f"{'(impor modul - TC27)':<62} D8({d8_import})")

print("\n\n" + "=" * 128)
print("PETA KEPUTUSAN -> TEST (TC berapa yang bikin True, TC berapa yang bikin False)")
print("=" * 128)
print(f"{'ID':<4} {'Keputusan':<32} {'True oleh':<34} {'False oleh':<34} Status")
print("-" * 128)
ringkas = {}
for baris, (did, _, _) in sorted(DECISION.items(), key=lambda x: x[1][0]):
    ts, fs = [], []
    for nama, kena in hasil.items():
        if "T" in kena.get(did, ""):
            ts.append(nama.split("_")[1])
        if "F" in kena.get(did, ""):
            fs.append(nama.split("_")[1])
    if did == "D8" and d8_import == "F":
        fs.append("TC27")
    ts, fs = sorted(set(ts)), sorted(set(fs))
    st = "OK (kedua sisi)" if ts and fs else ("hanya True" if ts else ("hanya False" if fs else "NOL"))
    ringkas[did] = (ts, fs, st)
    print(f"{did:<4} {TEKS[did]:<32} {(','.join(ts) or '-'):<34} {(','.join(fs) or '-'):<34} {st}")

total_ok = sum(1 for v in ringkas.values() if v[2].startswith("OK"))
print(f"\nKeputusan diperiksa : {len(DECISION)}")
print(f"Kedua sisi tertutup : {total_ok}/{len(DECISION)}")
