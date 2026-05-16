# src/ui/table_view.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QBrush


HEADERS = ["Peringkat", "Nama Mahasiswa", "NIM", "Prodi", "IPK ↓", "UKT (Rp)", "Status"]


class TableView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TableView")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ---- Table ----
        self.table = QTableWidget()
        self.table.setObjectName("MainTable")
        self.table.setColumnCount(len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 80)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        layout.addWidget(self.table)

    def tampilkan_data(self, semua_data, penerima_list, min_ipk, max_ukt):
        """Mengisi tabel dengan seluruh data + status lolos/tidak."""
        # Buat set NIM penerima untuk lookup cepat
        nim_lolos = {m["nim"] for m in penerima_list}

        # Gabungkan: tampilkan semua kandidat terurut
        data_tampil = sorted(semua_data, key=lambda m: (-m["ipk"], m["ukt"]))

        self.table.setRowCount(len(data_tampil))

        peringkat = 1
        for row, m in enumerate(data_tampil):
            lolos = m["nim"] in nim_lolos
            tidak_memenuhi_ipk = m["ipk"] < min_ipk
            tidak_memenuhi_ukt = m["ukt"] > max_ukt

            # Peringkat (hanya untuk yang lolos)
            rank_text = str(peringkat) if lolos else "-"
            if lolos:
                peringkat += 1

            values = [
                rank_text,
                m["nama"],
                m["nim"],
                m["prodi"],
                f"{m['ipk']:.2f}",
                f"Rp {m['ukt']:,.0f}",
                ""
            ]

            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)

                # Warna baris
                if lolos:
                    item.setBackground(QColor("#f0fdf4"))
                elif tidak_memenuhi_ipk:
                    item.setBackground(QColor("#fff7ed"))
                elif tidak_memenuhi_ukt:
                    item.setBackground(QColor("#fef2f2"))

                self.table.setItem(row, col, item)

            # Kolom status – pakai widget label berwarna
            status_widget = self._buat_status(lolos, tidak_memenuhi_ipk, tidak_memenuhi_ukt)
            self.table.setCellWidget(row, 6, status_widget)

            # Tinggi baris
            self.table.setRowHeight(row, 42)

    def _buat_status(self, lolos, tidak_ipk, tidak_ukt):
        container = QWidget()
        h = QHBoxLayout(container)
        h.setContentsMargins(8, 4, 8, 4)
        h.setAlignment(Qt.AlignCenter)

        lbl = QLabel()
        lbl.setAlignment(Qt.AlignCenter)

        if lolos:
            lbl.setText("✓  Lolos")
            lbl.setStyleSheet(
                "background:#16a34a; color:white; border-radius:10px;"
                "padding:3px 12px; font-weight:600; font-size:12px;"
            )
        elif tidak_ipk:
            lbl.setText("✗  IPK < 3.50")
            lbl.setStyleSheet(
                "background:#ea580c; color:white; border-radius:10px;"
                "padding:3px 12px; font-weight:600; font-size:12px;"
            )
        elif tidak_ukt:
            lbl.setText("✗  UKT > 5JT")
            lbl.setStyleSheet(
                "background:#dc2626; color:white; border-radius:10px;"
                "padding:3px 12px; font-weight:600; font-size:12px;"
            )
        else:
            lbl.setText("Tidak Lolos")
            lbl.setStyleSheet(
                "background:#6b7280; color:white; border-radius:10px;"
                "padding:3px 12px; font-weight:600; font-size:12px;"
            )

        h.addWidget(lbl)
        return container