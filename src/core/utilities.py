# src/core/utilities.py

import json
import os
from config import DATA_PATH, OUTPUT_PATH


def load_data():
    """Membaca data mahasiswa dari file JSON."""
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_hasil(penerima_list, min_ipk, max_ukt, kuota):
    """Menyimpan hasil seleksi ke file teks."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("       HASIL SELEKSI BEASISWA MAHASISWA UNGGUL\n")
        f.write("=" * 60 + "\n")
        f.write(f"Kriteria  : IPK >= {min_ipk} | UKT <= Rp {max_ukt:,.0f}\n")
        f.write(f"Kuota     : {kuota} mahasiswa\n")
        f.write(f"Lolos     : {len(penerima_list)} mahasiswa\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'No':<4} {'Nama':<20} {'NIM':<10} {'Prodi':<15} {'IPK':<6} {'UKT':>12}\n")
        f.write("-" * 60 + "\n")
        for i, m in enumerate(penerima_list, 1):
            f.write(
                f"{i:<4} {m['nama']:<20} {m['nim']:<10} {m['prodi']:<15} "
                f"{m['ipk']:<6.2f} Rp {m['ukt']:>10,.0f}\n"
            )
        f.write("=" * 60 + "\n")
    return OUTPUT_PATH