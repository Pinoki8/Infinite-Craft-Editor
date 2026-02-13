import gzip
import re
import random
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QFileDialog, 
                             QMessageBox, QScrollArea, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from gui.styles import *
from gui.craft_item import CraftItem
from gui.dialogs import AddCraftDialog, EditCraftDialog
from utils.file_handler import FileHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IC Editor")
        self.setGeometry(100, 100, 700, 500)
        self.file_handler = FileHandler()
        self.crafts = []
        self.loaded_items = []
        self.load_batch_size = 50
        self.current_loaded = 0
        self.init_ui()
        self.apply_styles()
        self.open_file()
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
    def create_left_panel(self):
        panel = QFrame()
        panel.setObjectName("leftPanel")
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        title = QLabel("IC EDITOR")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        name_label = QLabel("Save Name")
        name_label.setObjectName("normalLabel")
        layout.addWidget(name_label)
        self.save_name_input = QLineEdit()
        self.save_name_input.setPlaceholderText("Enter save name...")
        layout.addWidget(self.save_name_input)
        add_btn = QPushButton("+ Add Craft")
        add_btn.setObjectName("addButton")
        add_btn.clicked.connect(self.show_add_dialog)
        layout.addWidget(add_btn)
        random_btn = QPushButton("Add 10 Random Crafts")
        random_btn.setObjectName("randomButton")
        random_btn.clicked.connect(self.add_random_crafts)
        layout.addWidget(random_btn)
        save_btn = QPushButton("Save File")
        save_btn.setObjectName("saveButton")
        save_btn.clicked.connect(self.save_file)
        layout.addWidget(save_btn)
        layout.addSpacing(20)
        stats_label = QLabel("Statistics")
        stats_label.setObjectName("normalLabel")
        layout.addWidget(stats_label)
        self.stats_label = QLabel("Crafts: 0")
        self.stats_label.setObjectName("statsLabel")
        layout.addWidget(self.stats_label)
        layout.addStretch()
        watermark = QLabel("Made by Pin0ki0")
        watermark.setObjectName("watermarkLabel")
        layout.addWidget(watermark)
        return panel
    def create_right_panel(self):
        panel = QFrame()
        panel.setObjectName("rightPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        header = QLabel("CRAFTS LIST")
        header.setObjectName("headerLabel")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.crafts_container = QWidget()
        self.crafts_layout = QVBoxLayout(self.crafts_container)
        self.crafts_layout.setSpacing(5)
        self.crafts_layout.setContentsMargins(10, 10, 10, 10)
        self.crafts_layout.addStretch()
        scroll_area.setWidget(self.crafts_container)
        scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.scroll_area = scroll_area
        layout.addWidget(scroll_area)
        return panel
    def apply_styles(self):
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self.findChild(QFrame, "leftPanel").setStyleSheet(PANEL_STYLE)
        self.findChild(QFrame, "rightPanel").setStyleSheet(PANEL_STYLE)
        title_label = self.findChild(QLabel, "titleLabel")
        if title_label:
            title_label.setStyleSheet(TITLE_LABEL_STYLE)
        header_label = self.findChild(QLabel, "headerLabel")
        if header_label:
            header_label.setStyleSheet(HEADER_LABEL_STYLE)
        stats_label = self.findChild(QLabel, "statsLabel")
        if stats_label:
            stats_label.setStyleSheet(STATS_LABEL_STYLE)
        for label in self.findChildren(QLabel):
            if label.objectName() == "normalLabel":
                label.setStyleSheet(NORMAL_LABEL_STYLE)
        watermark = self.findChild(QLabel, "watermarkLabel")
        if watermark:
            watermark.setStyleSheet("font-size: 9px; font-style: italic; color: #226622; border: none; background: transparent;")
        for button in self.findChildren(QPushButton):
            button.setStyleSheet(BUTTON_STYLE)
        self.save_name_input.setStyleSheet(INPUT_STYLE)
        self.scroll_area.verticalScrollBar().setStyleSheet(SCROLLBAR_STYLE)
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open IC File", "", "IC Files (*.ic);;All Files (*)"
        )
        if not file_path:
            self.close()
            return
        try:
            self.file_handler.load_file(file_path)
            self.save_name_input.setText(self.file_handler.get_save_name())
            self.update_crafts_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")
            self.close()
    def update_crafts_list(self):
        for item in self.loaded_items:
            self.crafts_layout.removeWidget(item)
            item.deleteLater()
        self.loaded_items.clear()
        self.crafts = self.file_handler.get_crafts()
        self.current_loaded = 0
        self.load_more_crafts()
        self.stats_label.setText(f"Crafts: {len(self.crafts)}")
    def load_more_crafts(self):
        end = min(self.current_loaded + self.load_batch_size, len(self.crafts))
        for i in range(self.current_loaded, end):
            craft_data = self.crafts[i]
            craft_item = CraftItem(
                craft_data['text'], 
                craft_data['emoji'], 
                craft_data['id']
            )
            craft_item.clicked.connect(lambda cid=craft_data['id']: self.edit_craft(cid))
            self.crafts_layout.insertWidget(self.crafts_layout.count() - 1, craft_item)
            self.loaded_items.append(craft_item)
            self.animate_craft_item(craft_item)
        self.current_loaded = end
    def animate_craft_item(self, item):
        item.setStyleSheet(item.styleSheet() + "background-color: rgba(51, 204, 51, 0);")
        QTimer.singleShot(10, lambda: item.setStyleSheet(
            item.styleSheet().replace("rgba(51, 204, 51, 0)", "#0a0a0a")
        ))
    def on_scroll(self, value):
        scrollbar = self.scroll_area.verticalScrollBar()
        if value >= scrollbar.maximum() - 100 and self.current_loaded < len(self.crafts):
            self.load_more_crafts()
    def show_add_dialog(self):
        dialog = AddCraftDialog(self.file_handler, self)
        if dialog.exec_():
            self.update_crafts_list()
    def edit_craft(self, craft_id):
        dialog = EditCraftDialog(craft_id, self.file_handler, self)
        result = dialog.exec_()
        if result:
            self.update_crafts_list()
    def add_random_crafts(self):
        try:
            crafts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'crafts.txt')
            if not os.path.exists(crafts_path):
                crafts_path = 'crafts.txt'
            try:
                with open(crafts_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                QMessageBox.warning(self, "Warning", "crafts.txt file not found!")
                return
            available_crafts = []
            for line in lines:
                line = line.strip()
                if ' - ' in line:
                    name, emoji = line.split(' - ', 1)
                    available_crafts.append({'name': name.strip(), 'emoji': emoji.strip()})
            if not available_crafts:
                QMessageBox.warning(self, "Warning", "No crafts found in crafts.txt!")
                return
            existing_names = {craft['text'] for craft in self.crafts}
            added = 0
            attempts = 0
            max_attempts_per_craft = 10
            while added < 10 and attempts < len(available_crafts) * max_attempts_per_craft:
                craft = random.choice(available_crafts)
                attempts += 1
                if craft['name'] not in existing_names:
                    self.file_handler.add_craft(craft['name'], craft['emoji'])
                    existing_names.add(craft['name'])
                    added += 1
            if added > 0:
                self.update_crafts_list()
                QMessageBox.information(self, "Success", f"Added {added} random craft(s)!")
            else:
                QMessageBox.information(self, "Info", "All crafts from crafts.txt are already in the file.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add random crafts:\n{str(e)}")
    def save_file(self):
        new_name = self.save_name_input.text().strip()
        if new_name:
            self.file_handler.set_save_name(new_name)
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save IC File", "", "IC Files (*.ic);;All Files (*)"
        )
        if file_path:
            try:
                self.file_handler.save_file(file_path)
                QMessageBox.information(self, "Success", f"File saved successfully!\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
