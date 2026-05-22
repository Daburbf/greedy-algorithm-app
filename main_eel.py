# main_eel.py
import sys
import os
import eel
from tkinter import Tk, filedialog

# Menambahkan folder 'src' ke sistem path agar 'config' di utilities.py terbaca
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.core.greedy import seleksi_greedy
from src.core.utilities import load_data, import_data_json, save_hasil, save_hasil_csv

eel.init('web')

# Variabel global untuk menyimpan data mahasiswa aktif
data_aktif = load_data()

@eel.expose
def ambil_data_awal():
    return data_aktif

@eel.expose
def jalankan_seleksi(min_ipk, max_ukt, kuota, anggaran, bobot_ipk):
    global data_aktif
    penerima, kandidat, terpakai = seleksi_greedy(
        data_aktif, min_ipk, max_ukt, kuota, anggaran, bobot_ipk
    )
    return {
        "penerima": penerima,
        "kandidat": kandidat,
        "terpakai": terpakai,
        "total_kandidat": len(data_aktif)
    }

@eel.expose
def import_data():
    global data_aktif
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    root.destroy()

    if path:
        data_aktif = import_data_json(path)
        return {"status": "success", "count": len(data_aktif)}
    return {"status": "cancel"}

@eel.expose
def ekspor_csv(penerima_list):
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    root.destroy()

    if path:
        success = save_hasil_csv(penerima_list, path)
        return "Data Berhasil Diekspor ke CSV!" if success else "Gagal Mengekspor Data."
    return None

@eel.expose
def unduh_txt(penerima_list, min_ipk, max_ukt, kuota, anggaran, terpakai, bobot):
    path = save_hasil(penerima_list, min_ipk, max_ukt, kuota, anggaran, terpakai, bobot)
    return f"Laporan Berhasil Disimpan di:\n{path}"

# Menentukan ukuran jendela aplikasi
eel.start('index.html', size=(1300, 850))