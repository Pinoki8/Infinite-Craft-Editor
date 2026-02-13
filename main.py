#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'other'))
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet("""
        QWidget {
            background-color: #000000;
            color: #00ff00;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }
        QToolTip {
            background-color: #0a0a0a;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 5px;
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
