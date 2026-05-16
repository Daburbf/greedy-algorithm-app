# src/ui/sidebar.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSlider,
    QPushButton, QFrame, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class Sidebar(QWidget):
    seleksi_diminta = pyqtSignal(float, int)  # min_ipk, max_ukt

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(16)

        # Judul filter
        lbl_filter = QLabel("Filter Seleksi")
        lbl_filter.setObjectName("SidebarTitle")
        layout.addWidget(lbl_filter)

        # ---- IPK ----
        lbl_ipk_title = QLabel("Minimal IPK")
        lbl_ipk_title.setObjectName("FilterLabel")
        layout.addWidget(lbl_ipk_title)

        self.lbl_ipk_val = QLabel("3.50")
        self.lbl_ipk_val.setAlignment(Qt.AlignCenter)
        self.lbl_ipk_val.setObjectName("FilterValue")
        layout.addWidget(self.lbl_ipk_val)

        self.slider_ipk = QSlider(Qt.Horizontal)
        self.slider_ipk.setMinimum(200)
        self.slider_ipk.setMaximum(400)
        self.slider_ipk.setValue(350)
        self.slider_ipk.setObjectName("SliderIPK")
        self.slider_ipk.valueChanged.connect(self._on_ipk_changed)
        layout.addWidget(self.slider_ipk)

        # ---- UKT ----
        lbl_ukt_title = QLabel("Maksimal UKT")
        lbl_ukt_title.setObjectName("FilterLabel")
        layout.addWidget(lbl_ukt_title)

        self.lbl_ukt_val = QLabel("5 Juta")
        self.lbl_ukt_val.setAlignment(Qt.AlignCenter)
        self.lbl_ukt_val.setObjectName("FilterValue")
        layout.addWidget(self.lbl_ukt_val)

        self.slider_ukt = QSlider(Qt.Horizontal)
        self.slider_ukt.setMinimum(1)
        self.slider_ukt.setMaximum(10)
        self.slider_ukt.setValue(5)
        self.slider_ukt.setObjectName("SliderUKT")
        self.slider_ukt.valueChanged.connect(self._on_ukt_changed)
        layout.addWidget(self.slider_ukt)

        # ---- Divider ----
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setObjectName("Divider")
        layout.addWidget(line)

        # ---- Kriteria Info ----
        lbl_kriteria = QLabel("Kriteria Seleksi")
        lbl_kriteria.setObjectName("FilterLabel")
        layout.addWidget(lbl_kriteria)

        self.lbl_kriteria_detail = QLabel(
            "IPK ≥ 3.50, UKT ≤ Rp 5 Juta\n(Prioritas IPK Tertinggi & UKT Terendah)"
        )
        self.lbl_kriteria_detail.setObjectName("KriteriaDetail")
        self.lbl_kriteria_detail.setWordWrap(True)
        layout.addWidget(self.lbl_kriteria_detail)

        layout.addStretch()

        # ---- Tombol Terapkan ----
        self.btn_terapkan = QPushButton("🔍  Terapkan Seleksi Greedy")
        self.btn_terapkan.setObjectName("BtnTerapkan")
        self.btn_terapkan.clicked.connect(self._emit_seleksi)
        layout.addWidget(self.btn_terapkan)

    def _on_ipk_changed(self, val):
        ipk = val / 100.0
        self.lbl_ipk_val.setText(f"{ipk:.2f}")
        min_ipk = val / 100.0
        max_ukt = self.slider_ukt.value() * 1_000_000
        self._update_kriteria(min_ipk, max_ukt)

    def _on_ukt_changed(self, val):
        self.lbl_ukt_val.setText(f"{val} Juta")
        min_ipk = self.slider_ipk.value() / 100.0
        max_ukt = val * 1_000_000
        self._update_kriteria(min_ipk, max_ukt)

    def _update_kriteria(self, min_ipk, max_ukt):
        juta = int(max_ukt // 1_000_000)
        self.lbl_kriteria_detail.setText(
            f"IPK ≥ {min_ipk:.2f}, UKT ≤ Rp {juta} Juta\n"
            f"(Prioritas IPK Tertinggi & UKT Terendah)"
        )

    def _emit_seleksi(self):
        min_ipk = self.slider_ipk.value() / 100.0
        max_ukt = self.slider_ukt.value() * 1_000_000
        self.seleksi_diminta.emit(min_ipk, max_ukt)

    def get_min_ipk(self):
        return self.slider_ipk.value() / 100.0

    def get_max_ukt(self):
        return self.slider_ukt.value() * 1_000_000