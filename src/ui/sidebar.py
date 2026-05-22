# src/ui/sidebar.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QSpinBox, QDoubleSpinBox
from PyQt5.QtCore import Qt, pyqtSignal

class Sidebar(QWidget):
    seleksi_diminta = pyqtSignal(float, int, int, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        lbl_title = QLabel("⚙ KONFIGURASI PARAMETER & KONTROL")
        lbl_title.setProperty("class", "CardTitle")
        layout.addWidget(lbl_title)

        grid = QGridLayout()
        grid.setSpacing(12)

        # Kapasitas Kuota
        grid.addWidget(QLabel("Kapasitas Kuota (Orang):"), 0, 0)
        self.spin_kuota = QSpinBox()
        self.spin_kuota.setRange(1, 100)
        self.spin_kuota.setValue(10)
        grid.addWidget(self.spin_kuota, 1, 0)

        # Total Anggaran
        grid.addWidget(QLabel("Total Dana Anggaran (Rp):"), 0, 1)
        self.spin_anggaran = QSpinBox()
        self.spin_anggaran.setRange(1_000_000, 1_000_000_000)
        self.spin_anggaran.setSingleStep(1_000_000)
        self.spin_anggaran.setValue(50_000_000)
        grid.addWidget(self.spin_anggaran, 1, 1)

        # Bobot IPK
        grid.addWidget(QLabel("Proporsi Bobot IPK (%):"), 0, 2)
        self.spin_bobot = QSpinBox()
        self.spin_bobot.setRange(0, 100)
        self.spin_bobot.setValue(60)
        grid.addWidget(self.spin_bobot, 1, 2)

        # Minimal IPK (Dipertahankan agar fitur asli tidak hilang)
        grid.addWidget(QLabel("Minimal IPK:"), 2, 0)
        self.spin_ipk = QDoubleSpinBox()
        self.spin_ipk.setRange(0.0, 4.0)
        self.spin_ipk.setSingleStep(0.1)
        self.spin_ipk.setValue(3.50)
        grid.addWidget(self.spin_ipk, 3, 0)

        # Maksimal UKT (Dipertahankan agar fitur asli tidak hilang)
        grid.addWidget(QLabel("Maksimal UKT (Rp):"), 2, 1)
        self.spin_ukt = QSpinBox()
        self.spin_ukt.setRange(0, 50_000_000)
        self.spin_ukt.setSingleStep(500_000)
        self.spin_ukt.setValue(5_000_000)
        grid.addWidget(self.spin_ukt, 3, 1)

        layout.addLayout(grid)

    def _emit_seleksi(self):
        min_ipk = self.spin_ipk.value()
        max_ukt = self.spin_ukt.value()
        kuota = self.spin_kuota.value()
        total_anggaran = self.spin_anggaran.value()
        bobot_ipk = self.spin_bobot.value()
        self.seleksi_diminta.emit(min_ipk, max_ukt, kuota, total_anggaran, bobot_ipk)

    def get_min_ipk(self): return self.spin_ipk.value()
    def get_max_ukt(self): return self.spin_ukt.value()
    def get_kuota(self): return self.spin_kuota.value()
    def get_anggaran(self): return self.spin_anggaran.value()
    def get_bobot_ipk(self): return self.spin_bobot.value()