from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QCheckBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from gui.styles import *

class AddCraftDialog(QDialog):
    def __init__(self, file_handler, parent=None):
        super().__init__(parent)
        self.file_handler = file_handler
        self.setWindowTitle("Add New Craft")
        self.setFixedSize(380, 340)
        self.setModal(True)
        self.init_ui()
        self.apply_styles()
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Add New Craft")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #33cc33; text-shadow: 0 0 10px #33cc33;")
        layout.addWidget(title)
        layout.addSpacing(10)
        name_label = QLabel("Craft Name")
        name_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter craft name...")
        layout.addWidget(self.name_input)
        emoji_label = QLabel("Emoji")
        emoji_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        layout.addWidget(emoji_label)
        self.emoji_input = QLineEdit()
        self.emoji_input.setText("🌍")
        layout.addWidget(self.emoji_input)
        self.custom_id_check = QCheckBox("Use Custom ID")
        self.custom_id_check.stateChanged.connect(self.toggle_custom_id)
        layout.addWidget(self.custom_id_check)
        self.id_label = QLabel("Custom ID")
        self.id_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        self.id_label.hide()
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter custom ID...")
        self.id_input.hide()
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addStretch()
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(100)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        add_btn = QPushButton("Add Craft")
        add_btn.setMinimumWidth(100)
        add_btn.clicked.connect(self.add_craft)
        add_btn.setDefault(True)
        btn_layout.addWidget(add_btn)
        layout.addLayout(btn_layout)
    def apply_styles(self):
        self.setStyleSheet(DIALOG_STYLE)
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(BUTTON_STYLE)
        for input_field in self.findChildren(QLineEdit):
            input_field.setStyleSheet(INPUT_STYLE)
        self.custom_id_check.setStyleSheet(CHECKBOX_STYLE)
    def toggle_custom_id(self, state):
        if state == Qt.Checked:
            self.id_label.show()
            self.id_input.show()
        else:
            self.id_label.hide()
            self.id_input.hide()
    def add_craft(self):
        name = self.name_input.text().strip()
        emoji = self.emoji_input.text().strip() or "🌍"
        if not name:
            QMessageBox.warning(self, "Warning", "Craft name cannot be empty!")
            return
        if self.custom_id_check.isChecked():
            craft_id = self.id_input.text().strip()
            if not craft_id.isdigit():
                craft_id = "0"
        else:
            craft_id = None
        try:
            self.file_handler.add_craft(name, emoji, craft_id)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add craft:\n{str(e)}")

class EditCraftDialog(QDialog):
    def __init__(self, craft_id, file_handler, parent=None):
        super().__init__(parent)
        self.craft_id = craft_id
        self.file_handler = file_handler
        self.craft_data = file_handler.get_craft_by_id(craft_id)
        self.setWindowTitle("Edit Craft")
        self.setFixedSize(380, 280)
        self.setModal(True)
        self.init_ui()
        self.apply_styles()
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel(f"Edit Craft (ID: {self.craft_id})")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #33cc33; text-shadow: 0 0 10px #33cc33;")
        layout.addWidget(title)
        layout.addSpacing(10)
        name_label = QLabel("Craft Name")
        name_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setText(self.craft_data['text'])
        layout.addWidget(self.name_input)
        emoji_label = QLabel("Emoji")
        emoji_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        layout.addWidget(emoji_label)
        self.emoji_input = QLineEdit()
        self.emoji_input.setText(self.craft_data['emoji'])
        layout.addWidget(self.emoji_input)
        layout.addStretch()
        btn_layout = QHBoxLayout()
        delete_btn = QPushButton("Delete")
        delete_btn.setMinimumWidth(100)
        delete_btn.clicked.connect(self.delete_craft)
        delete_btn.setStyleSheet(DELETE_BUTTON_STYLE)
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(100)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        save_btn = QPushButton("Save Changes")
        save_btn.setMinimumWidth(120)
        save_btn.clicked.connect(self.save_changes)
        save_btn.setDefault(True)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
    def apply_styles(self):
        self.setStyleSheet(DIALOG_STYLE)
        for btn in self.findChildren(QPushButton):
            if btn.text() != "Delete":
                btn.setStyleSheet(BUTTON_STYLE)
        for input_field in self.findChildren(QLineEdit):
            input_field.setStyleSheet(INPUT_STYLE)
    def save_changes(self):
        name = self.name_input.text().strip()
        emoji = self.emoji_input.text().strip() or "🌍"
        if not name:
            QMessageBox.warning(self, "Warning", "Craft name cannot be empty!")
            return
        try:
            self.file_handler.update_craft(self.craft_id, name, emoji)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update craft:\n{str(e)}")
    def delete_craft(self):
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{self.craft_data['text']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                self.file_handler.delete_craft(self.craft_id)
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete craft:\n{str(e)}")
