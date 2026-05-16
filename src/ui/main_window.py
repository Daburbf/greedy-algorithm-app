# src/ui/main_window.py

import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from src.ui.sidebar import Sidebar
from src.ui.table_view import TableView
from src.core.greedy import seleksi_greedy
from src.core.utilities import load_data, save_hasil
from config import MIN_IPK, MAX_UKT, KUOTA


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleksi Beasiswa Mahasiswa Unggul")
        self.setMinimumSize(1000, 600)

        self.semua_data = load_data()
        self.penerima = []
        self.kandidat = []

        self._build_ui()
        self._jalankan_seleksi(MIN_IPK, MAX_UKT)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---- Header ----
        header = self._buat_header()
        root.addWidget(header)

        # ---- Body ----
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.seleksi_diminta.connect(self._jalankan_seleksi)
        body.addWidget(self.sidebar)

        # Divider vertikal
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setObjectName("VDivider")
        body.addWidget(vline)

        # Konten kanan
        right = QVBoxLayout()
        right.setContentsMargins(20, 16, 20, 16)
        right.setSpacing(12)

        # Info bar atas
        self.info_bar = self._buat_info_bar()
        right.addLayout(self.info_bar)

        # Tabel
        self.table_view = TableView()
        right.addWidget(self.table_view)

        body_widget = QWidget()
        body_widget.setLayout(right)
        body_widget.setObjectName("RightPanel")
        body.addWidget(body_widget, 1)

        root.addLayout(body)

    def _buat_header(self):
        header = QWidget()
        header.setObjectName("Header")
        header.setFixedHeight(56)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 0, 20, 0)

        icon_lbl = QLabel("🎓")
        icon_lbl.setFont(QFont("Segoe UI Emoji", 18))
        hl.addWidget(icon_lbl)

        title = QLabel("Seleksi Beasiswa Mahasiswa Unggul")
        title.setObjectName("HeaderTitle")
        hl.addWidget(title)
        hl.addStretch()

        return header

    def _buat_info_bar(self):
        layout = QHBoxLayout()
        layout.setSpacing(12)

        # Judul halaman
        lbl_page = QLabel("Daftar Calon Penerima Beasiswa")
        lbl_page.setObjectName("PageTitle")
        layout.addWidget(lbl_page)

        layout.addStretch()

        # Badge kandidat lolos
        self.lbl_kandidat = QLabel("Kandidat Lolos: 0 / Total Pendaftar: 0")
        self.lbl_kandidat.setObjectName("BadgeInfo")
        layout.addWidget(self.lbl_kandidat)

        # Tombol unduh
        self.btn_unduh = QPushButton("⬇  Unduh Data Hasil")
        self.btn_unduh.setObjectName("BtnUnduh")
        self.btn_unduh.clicked.connect(self._unduh_hasil)
        layout.addWidget(self.btn_unduh)

        return layout

    def _jalankan_seleksi(self, min_ipk, max_ukt):
        self.penerima, self.kandidat = seleksi_greedy(
            self.semua_data, min_ipk, max_ukt, KUOTA
        )
        # Update info
        total = len(self.semua_data)
        lolos = len(self.penerima)
        self.lbl_kandidat.setText(f"Kandidat Lolos: {lolos}  /  Total Pendaftar: {total}")

        # Tampilkan tabel
        self.table_view.tampilkan_data(
            self.semua_data, self.penerima, min_ipk, max_ukt
        )

        # Update info bar greedy di sidebar
        self.sidebar.slider_ipk.setValue(int(min_ipk * 100))
        self.sidebar.slider_ukt.setValue(int(max_ukt // 1_000_000))

    def _unduh_hasil(self):
        min_ipk = self.sidebar.get_min_ipk()
        max_ukt = self.sidebar.get_max_ukt()
        path = save_hasil(self.penerima, min_ipk, max_ukt, KUOTA)
        QMessageBox.information(
            self,
            "Berhasil",
            f"Data hasil seleksi berhasil disimpan ke:\n{path}"
        )