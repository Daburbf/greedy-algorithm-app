# src/ui/main_window.py
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.ui.sidebar import Sidebar
from src.ui.table_view import TableView
from src.core.greedy import seleksi_greedy
from src.core.utilities import load_data, save_hasil, import_data_json, save_hasil_csv
from config import MIN_IPK, MAX_UKT, KUOTA, TOTAL_ANGGARAN, BOBOT_IPK

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Seleksi Beasiswa")
        self.setMinimumSize(1100, 700)

        self.semua_data = load_data()
        self.penerima = []
        self.kandidat = []
        self.anggaran_terpakai = 0

        self._build_ui()
        self._jalankan_seleksi(MIN_IPK, MAX_UKT, KUOTA, TOTAL_ANGGARAN, BOBOT_IPK)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(15)

        # --- 1. HEADER (Mac Style) ---
        root.addWidget(self._buat_header())

        # --- BODY: Split Layout Kiri & Kanan ---
        body = QHBoxLayout()
        body.setSpacing(20)

        # KIRI: Data Kandidat
        left_panel = QWidget()
        left_panel.setProperty("class", "Card")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)

        lbl_kandidat_title = QLabel("🗂 DATA KANDIDAT TERDAFTAR")
        lbl_kandidat_title.setProperty("class", "CardTitle")
        left_layout.addWidget(lbl_kandidat_title)

        self.table_view = TableView()
        left_layout.addWidget(self.table_view)

        self.lbl_total_kandidat = QLabel("Total Kandidat: 0")
        self.lbl_total_kandidat.setStyleSheet("color: #475569; font-weight: bold; padding-top: 5px;")
        left_layout.addWidget(self.lbl_total_kandidat)

        body.addWidget(left_panel, 5) # Proporsi lebar (weight) 5

        # KANAN: Konfigurasi, Aksi, Analisis
        right_panel = QVBoxLayout()
        right_panel.setSpacing(20)

        # Kartu 1: Konfigurasi
        self.sidebar = Sidebar()
        self.sidebar.setProperty("class", "Card")
        self.sidebar.seleksi_diminta.connect(self._jalankan_seleksi)
        right_panel.addWidget(self.sidebar)

        # Kartu 2: Aksi Utama
        aksi_card = QWidget()
        aksi_card.setProperty("class", "Card")
        aksi_layout = QVBoxLayout(aksi_card)
        aksi_layout.setContentsMargins(15, 15, 15, 15)

        lbl_aksi = QLabel("Action")

        lbl_aksi.setProperty("class", "CardTitle")
        aksi_layout.addWidget(lbl_aksi)

        aksi_btn_layout = QHBoxLayout()
        self.btn_proses = QPushButton("🚀 PROSES SELEKSI TERINTEGRASI")
        self.btn_proses.setObjectName("BtnProses")
        self.btn_proses.clicked.connect(self.sidebar._emit_seleksi)
        aksi_btn_layout.addWidget(self.btn_proses)

        self.btn_import = QPushButton("💾 HASILKAN DATA ACAK / IMPORT")
        self.btn_import.setObjectName("BtnAcak")
        self.btn_import.clicked.connect(self._import_data)
        aksi_btn_layout.addWidget(self.btn_import)
        aksi_layout.addLayout(aksi_btn_layout)

        eks_btn_layout = QHBoxLayout()
        self.btn_csv = QPushButton("📊 Ekspor CSV")
        self.btn_csv.setObjectName("BtnUnduh")
        self.btn_csv.clicked.connect(self._ekspor_csv)
        eks_btn_layout.addWidget(self.btn_csv)

        self.btn_unduh = QPushButton("📝 Laporan TXT")
        self.btn_unduh.setObjectName("BtnUnduh")
        self.btn_unduh.clicked.connect(self._unduh_hasil)
        eks_btn_layout.addWidget(self.btn_unduh)
        aksi_layout.addLayout(eks_btn_layout)

        right_panel.addWidget(aksi_card)

        # Kartu 3: Analisis Hasil
        analisis_card = QWidget()
        analisis_card.setProperty("class", "Card")
        analisis_layout = QVBoxLayout(analisis_card)
        analisis_layout.setContentsMargins(15, 15, 15, 15)

        lbl_analisis = QLabel("📊 ANALISIS HASIL SELEKSI GREEDY")
        lbl_analisis.setProperty("class", "CardTitle")
        analisis_layout.addWidget(lbl_analisis)

        self.lbl_status = QLabel("STATUS: MENUNGGU ANALISIS\nLakukan proses seleksi untuk melihat daftar penerima.")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("background: #f1f5f9; padding: 15px; border-radius: 6px; color: #475569; font-weight: bold;")
        analisis_layout.addWidget(self.lbl_status)

        right_panel.addWidget(analisis_card)
        right_panel.addStretch()

        right_container = QWidget()
        right_container.setLayout(right_panel)
        body.addWidget(right_container, 4) # Proporsi lebar (weight) 4

        root.addLayout(body)

        self.statusBar().showMessage("Algoritma: Greedy v2.0 (Scoring Berbasis Bobot) | Data Terisi | Menunggu Input.")

    def _buat_header(self):
        header = QWidget()
        header.setObjectName("Header")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(10, 5, 10, 15)

        dots_layout = QHBoxLayout()
        dots_layout.setSpacing(8)
        for color in ["#ff5f56", "#ffbd2e", "#27c93f"]:
            dot = QFrame()
            dot.setFixedSize(12, 12)
            dot.setStyleSheet(f"background-color: {color}; border-radius: 6px;")
            dots_layout.addWidget(dot)
        dots_layout.addStretch()

        title_layout = QVBoxLayout()
        title = QLabel("SISTEM SELEKSI BEASISWA BERBASIS ALGORITMA GREEDY")
        title.setObjectName("HeaderTitle")
        title.setAlignment(Qt.AlignCenter)
        subtitle = QLabel("v2.0 - Optimasi Alokasi Kuota dan Anggaran Terintegrasi")
        subtitle.setObjectName("HeaderSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        hl.addLayout(dots_layout, 1)
        hl.addLayout(title_layout, 3)
        hl.addStretch(1)
        return header

    def _jalankan_seleksi(self, min_ipk, max_ukt, kuota, total_anggaran, bobot_ipk):
        self.penerima, self.kandidat, self.anggaran_terpakai = seleksi_greedy(
            self.semua_data, min_ipk, max_ukt, kuota, total_anggaran, bobot_ipk
        )
        lolos = len(self.penerima)
        sisa_dana = total_anggaran - self.anggaran_terpakai

        status_text = f"STATUS: SELEKSI SELESAI\nLolos: {lolos}/{kuota} org  |  Anggaran Terpakai: Rp {self.anggaran_terpakai:,.0f}  |  Sisa: Rp {sisa_dana:,.0f}"
        self.lbl_status.setText(status_text)
        self.lbl_status.setStyleSheet("background: #d1fae5; padding: 15px; border-radius: 6px; color: #065f46; font-weight: bold;")

        self.lbl_total_kandidat.setText(f"Total Kandidat: {len(self.semua_data)}")
        self.statusBar().showMessage(f"Algoritma: Greedy v2.0 | Data Terisi: {len(self.semua_data)} Kandidat | Siap.")

        self.table_view.tampilkan_data(self.semua_data, self.penerima, min_ipk, max_ukt)

        # Sinkronkan Spinbox jika seleksi dipanggil via fungsi eksternal
        self.sidebar.spin_ipk.setValue(min_ipk)
        self.sidebar.spin_ukt.setValue(max_ukt)
        self.sidebar.spin_kuota.setValue(kuota)
        self.sidebar.spin_anggaran.setValue(total_anggaran)
        self.sidebar.spin_bobot.setValue(bobot_ipk)

    def _import_data(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Import Data", "", "JSON Files (*.json);;Semua File (*)", options=options)

        if filepath:
            try:
                data_baru = import_data_json(filepath)
                if data_baru and isinstance(data_baru, list):
                    self.semua_data = data_baru
                    self.sidebar._emit_seleksi()
                    QMessageBox.information(self, "Berhasil", f"Berhasil mengimpor {len(data_baru)} data pendaftar!")
                else:
                    QMessageBox.warning(self, "Gagal", "File kosong atau format JSON tidak sesuai.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat membaca file:\n{str(e)}")

    def _ekspor_csv(self):
        if not self.penerima:
            QMessageBox.warning(self, "Peringatan", "Tidak ada data pendaftar yang lolos untuk diekspor.")
            return
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getSaveFileName(self, "Simpan CSV", "hasil_seleksi.csv", "CSV Files (*.csv)", options=options)
        if filepath:
            if save_hasil_csv(self.penerima, filepath):
                QMessageBox.information(self, "Berhasil", f"Data berhasil diekspor ke:\n{filepath}")
            else:
                QMessageBox.critical(self, "Gagal", "Gagal mengekspor data ke CSV.")

    def _unduh_hasil(self):
        path = save_hasil(
            self.penerima, self.sidebar.get_min_ipk(), self.sidebar.get_max_ukt(),
            self.sidebar.get_kuota(), self.sidebar.get_anggaran(), self.anggaran_terpakai, self.sidebar.get_bobot_ipk()
        )
        QMessageBox.information(self, "Berhasil", f"Laporan berhasil disimpan ke:\n{path}")