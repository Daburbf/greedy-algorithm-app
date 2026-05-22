# src/config.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "data_mahasiswa.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "hasil_seleksi.txt")

MIN_IPK = 3.50
MAX_UKT = 5000000
TOTAL_ANGGARAN = 50000000
KUOTA = 10
BOBOT_IPK = 60