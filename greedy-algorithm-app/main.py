# main.py
import sys
import os

# Menambahkan folder 'src' ke sistem path agar 'import config' dikenali
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Menjalankan aplikasi utama
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())