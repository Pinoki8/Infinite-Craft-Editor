COLORS = {
    'bg_black': '#000000',
    'bg_dark': '#0a0a0a',
    'bg_medium': '#151515',
    'neon_green': '#33cc33',
    'neon_green_glow': '#33cc3340',
    'neon_red': '#cc3333',
    'neon_red_glow': '#cc333340',
    'text_green': '#33cc33',
    'text_dim': '#226622',
}

MAIN_WINDOW_STYLE = """
QMainWindow {
    background-color: #000000;
}
"""

BUTTON_STYLE = """
QPushButton {
    background-color: #000000;
    color: #33cc33;
    border: 2px solid #33cc33;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #33cc3320;
    box-shadow: 0 0 10px #33cc33;
}
QPushButton:pressed {
    background-color: #33cc3340;
}
QPushButton:disabled {
    color: #226622;
    border-color: #226622;
}
"""

DELETE_BUTTON_STYLE = """
QPushButton {
    background-color: #000000;
    color: #cc3333;
    border: 2px solid #cc3333;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #cc333320;
    box-shadow: 0 0 10px #cc3333;
}
QPushButton:pressed {
    background-color: #cc333340;
}
"""

INPUT_STYLE = """
QLineEdit {
    background-color: #0a0a0a;
    color: #33cc33;
    border: 2px solid #33cc33;
    border-radius: 3px;
    padding: 8px;
    font-size: 11px;
}
QLineEdit:focus {
    border-color: #33cc33;
    box-shadow: 0 0 8px #33cc33;
}
QLineEdit::placeholder {
    color: #226622;
}
"""

CHECKBOX_STYLE = """
QCheckBox {
    color: #33cc33;
    spacing: 8px;
    font-size: 11px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #33cc33;
    border-radius: 3px;
    background-color: #0a0a0a;
}
QCheckBox::indicator:hover {
    background-color: #33cc3320;
    box-shadow: 0 0 8px #33cc33;
}
QCheckBox::indicator:checked {
    background-color: #33cc33;
    image: url(none);
}
QCheckBox::indicator:checked:hover {
    box-shadow: 0 0 10px #33cc33;
}
"""

SCROLLBAR_STYLE = """
QScrollBar:vertical {
    background-color: #000000;
    width: 12px;
    border: 1px solid #33cc33;
    border-radius: 6px;
}
QScrollBar::handle:vertical {
    background-color: #33cc33;
    min-height: 30px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background-color: #33cc33;
    box-shadow: 0 0 8px #33cc33;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
    height: 0px;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""

TITLE_LABEL_STYLE = """
QLabel {
    color: #33cc33;
    font-size: 24px;
    font-weight: bold;
    text-shadow: 0 0 10px #33cc33;
    border: none;
    background: transparent;
}
"""

HEADER_LABEL_STYLE = """
QLabel {
    color: #33cc33;
    font-size: 14px;
    font-weight: bold;
    padding: 10px;
    background-color: #000000;
    border-bottom: 2px solid #33cc33;
}
"""

STATS_LABEL_STYLE = """
QLabel {
    color: #33cc33;
    font-size: 11px;
    padding: 5px;
    border: none;
    background: transparent;
}
"""

NORMAL_LABEL_STYLE = """
QLabel {
    color: #33cc33;
    border: none;
    background: transparent;
}
"""

PANEL_STYLE = """
QFrame {
    background-color: #000000;
    border: 2px solid #33cc33;
    border-radius: 8px;
}
"""

CRAFT_ITEM_STYLE = """
QFrame {
    background-color: #0a0a0a;
    border: 1px solid #33cc33;
    border-radius: 5px;
    padding: 5px;
}
QFrame:hover {
    background-color: #33cc3320;
    border: 2px solid #33cc33;
    box-shadow: 0 0 15px #33cc3380;
}
"""

DIALOG_STYLE = """
QDialog {
    background-color: #000000;
    border: 2px solid #33cc33;
}
"""

MESSAGEBOX_STYLE = """
QMessageBox {
    background-color: #000000;
    color: #33cc33;
}
QMessageBox QLabel {
    color: #33cc33;
}
QMessageBox QPushButton {
    background-color: #000000;
    color: #33cc33;
    border: 2px solid #33cc33;
    border-radius: 5px;
    padding: 8px 16px;
    min-width: 80px;
}
QMessageBox QPushButton:hover {
    background-color: #33cc3320;
}
"""
