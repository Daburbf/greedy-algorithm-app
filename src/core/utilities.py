# src/core/utilities.py
import json
import os
import csv
from config import DATA_PATH, OUTPUT_PATH

def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def import_data_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_hasil(penerima_list, min_ipk, max_ukt, kuota, total_anggaran, anggaran_terpakai, bobot_ipk):
    bobot_ukt = 100 - bobot_ipk
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("=" * 75 + "\n")
        f.write("       HASIL SELEKSI BEASISWA MAHASISWA UNGGUL\n")
        f.write("=" * 75 + "\n")
        f.write(f"Kriteria       : IPK >= {min_ipk} | UKT <= Rp {max_ukt:,.0f}\n")
        f.write(f"Bobot Penilaian: IPK {bobot_ipk}% | UKT {bobot_ukt}%\n")
        f.write(f"Batas Kuota    : {kuota} mahasiswa\n")
        f.write(f"Total Anggaran : Rp {total_anggaran:,.0f}\n")
        f.write(f"Dana Terpakai  : Rp {anggaran_terpakai:,.0f}\n")
        f.write(f"Jumlah Lolos   : {len(penerima_list)} mahasiswa\n")
        f.write("-" * 75 + "\n")
        f.write(f"{'No':<4} {'Nama':<18} {'NIM':<10} {'IPK':<6} {'UKT':>10}   {'Skor Akhir':>10}\n")
        f.write("-" * 75 + "\n")
        for i, m in enumerate(penerima_list, 1):
            skor = m.get('skor_akhir', 0)
            f.write(
                f"{i:<4} {m['nama']:<18} {m['nim']:<10} "
                f"{m['ipk']:<6.2f} Rp {m['ukt']:>8,.0f}   {skor:>10.2f}\n"
            )
        f.write("=" * 75 + "\n")
    return OUTPUT_PATH

def save_hasil_csv(penerima_list, filepath):
    headers = ["No", "Nama Mahasiswa", "NIM", "Prodi", "IPK", "UKT (Rp)", "Skor Akhir"]
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(headers)
            for i, m in enumerate(penerima_list, 1):
                skor = m.get('skor_akhir', 0)
                writer.writerow([
                    i, m["nama"], m["nim"], m["prodi"],
                    f"{m['ipk']:.2f}", m["ukt"], f"{skor:.2f}"
                ])
        return True
    except Exception:
        return False