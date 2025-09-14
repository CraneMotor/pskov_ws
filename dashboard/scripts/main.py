#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QHBoxLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

from sidebar import Sidebar
from pages.page_factory import PageFactory

# Главный класс, отвечает за страницы

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pckov")
        self.screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, self.screen.width(), self.screen.height())
        self.setupUI()

    def setupUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar()
        
        self.content_area = QWidget()
        self.content_area.setStyleSheet("background-color: #3C3C3C;")
        self.content_layout = QHBoxLayout(self.content_area)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area, 1)

        self.sidebar.tab_changed.connect(self.onTabChanged)
        self.showTab(0)

    def onTabChanged(self, index):
        self.showTab(index)

    def showTab(self, index):
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)
        tab_name = self.sidebar.tab_list.item(index).text()
        page = PageFactory.createPage(index, tab_name)
        self.content_layout.addWidget(page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    app.setPalette(palette)
    
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())