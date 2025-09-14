from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QListWidget
)
from PyQt5.QtCore import pyqtSignal
from pathlib import Path

# Левое боковое меню
class Sidebar(QFrame):
    tab_changed = pyqtSignal(int)  # Сигнал при изменении вкладки

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setFixedWidth(250)
        self.setStyleSheet(Path("gss/sidebar.gss").read_text())
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 20, 10, 20)

        self.tab_list = QListWidget()
        self.tab_list.setStyleSheet(Path("gss/tab_style.gss").read_text())
        
        tabs = ["Главная страница", "Задачи", "Отслеживание","Настройки"]
        
        for tab in tabs:
            self.tab_list.addItem(tab)
        
        layout.addWidget(self.tab_list)

        self.tab_list.currentRowChanged.connect(self.tab_changed.emit) # сигнал