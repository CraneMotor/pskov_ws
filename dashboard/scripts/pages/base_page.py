from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QFont

# Базовый класс страницы, остальные наследуются от него

class BasePage(QWidget):
    def __init__(self):
        super().__init__()
        
        # Шрифты
        self.arial_20 =QFont("Arial", 20, QFont.Bold)
        self.arial_18 =QFont("Arial", 18, QFont.Bold)
        self.arial_16 =QFont("Arial", 16, QFont.Bold)
        self.arial_14 =QFont("Arial", 14, QFont.Bold)
        self.arial_12 =QFont("Arial", 12, QFont.Bold)
        self.arial_10 =QFont("Arial", 10, QFont.Bold)

        self.times_10 = QFont("Times", 10, QFont.Bold)
        self.times_14 = QFont("Times", 14, QFont.Bold)

        # Геометрия
        self.height_labels = 50
        self.separator_labels = 70

        self.setupUI()

    def setupUI(self):
            main_layout = QVBoxLayout(self)
            main_layout.setSpacing(0)
            main_layout.setContentsMargins(0, 0, 0, 0)

            # Контентная область
            self.content_widget = QWidget()
            self.content_widget.setStyleSheet("background-color: transparent;")
            self.content_layout = QVBoxLayout(self.content_widget)
            self.content_layout.setContentsMargins(20, 0, 20, 20)
            
            main_layout.addWidget(self.content_widget, 1)  # 1 - коэффициент растяжения

    # Добавить виджет в content area
    def addContentWidget(self, widget):
           
            self.content_layout.addWidget(widget)

    # Очистить content area
    def clearContent(self):
            for i in reversed(range(self.content_layout.count())):
                widget = self.content_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)