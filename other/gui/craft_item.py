from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

class CraftItem(QFrame):
    clicked = pyqtSignal(int)
    def __init__(self, name, emoji, craft_id):
        super().__init__()
        self.craft_id = craft_id
        self.name = name
        self.emoji = emoji
        self.init_ui()
        self.apply_styles()
    def init_ui(self):
        self.setFixedHeight(50)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        self.emoji_label = QLabel(self.emoji)
        self.emoji_label.setFont(QFont("Segoe UI Emoji", 16))
        self.emoji_label.setFixedWidth(40)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setObjectName("emojiLabel")
        layout.addWidget(self.emoji_label)
        self.name_label = QLabel(self.name)
        self.name_label.setFont(QFont("Segoe UI", 11))
        self.name_label.setObjectName("craftNameLabel")
        layout.addWidget(self.name_label, 1)
    def apply_styles(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #0a0a0a;
                border: 1px solid #33cc33;
                border-radius: 5px;
            }
        """)
        self.emoji_label.setStyleSheet("color: #33cc33; border: none; background: transparent;")
        self.name_label.setStyleSheet("color: #33cc33; border: none; background: transparent;")
    def enterEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                background-color: #33cc3320;
                border: 2px solid #33cc33;
                border-radius: 5px;
            }
        """)
        self.name_label.setStyleSheet("color: #33cc33; text-shadow: 0 0 10px #33cc33; border: none; background: transparent;")
        super().enterEvent(event)
    def leaveEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                background-color: #0a0a0a;
                border: 1px solid #33cc33;
                border-radius: 5px;
            }
        """)
        self.name_label.setStyleSheet("color: #33cc33; border: none; background: transparent;")
        super().leaveEvent(event)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setStyleSheet("""
                QFrame {
                    background-color: #33cc3340;
                    border: 2px solid #33cc33;
                    border-radius: 5px;
                }
            """)
            self.clicked.emit(self.craft_id)
        super().mousePressEvent(event)
    def mouseReleaseEvent(self, event):
        if self.underMouse():
            self.enterEvent(event)
        else:
            self.leaveEvent(event)
        super().mouseReleaseEvent(event)
