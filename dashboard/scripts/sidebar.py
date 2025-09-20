
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QListWidget, QPushButton, QSpacerItem, 
    QSizePolicy, QLabel, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QColor
from pathlib import Path
from PyQt5.QtCore import Qt

# Левое боковое меню
class Sidebar(QFrame):
    tab_changed = pyqtSignal(int)  # Сигнал при изменении вкладки
    stop_pressed = pyqtSignal()    # Новый сигнал для кнопки СТОП

    def __init__(self):
        super().__init__()
        self.battery_level = 100  # Начальный уровень заряда
        self.setupUI()
        self.setupBatteryTimer()

    def setupUI(self):
        self.setFixedWidth(250)
        self.setStyleSheet(Path("gss/sidebar.gss").read_text())
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 20, 10, 20)

        self.tab_list = QListWidget()
        self.tab_list.setStyleSheet(Path("gss/tab_style.gss").read_text())
        
        tabs = ["Мониторинг", "Задачи", "Настройки"]
        
        for tab in tabs:
            self.tab_list.addItem(tab)
        
        layout.addWidget(self.tab_list)

        # Добавляем растягивающийся спейсер
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Создаем зеленое поле с зарядом тележки
        self.createBatteryWidget(layout)

        # Добавляем еще немного пространства между батареей и кнопкой
        layout.addSpacerItem(QSpacerItem(300, 300, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Создаем красную кнопку СТОП
        self.stop_button = QPushButton("E-STOP")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #FF5555, stop: 1 #CC0000);
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: 3px solid #AA0000;
                border-radius: 15px;
                padding: 20px;
                margin: 15px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #FF7777, stop: 1 #DD0000);
                border: 3px solid #BB0000;
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #CC0000, stop: 1 #AA0000);
                border: 3px solid #990000;
                padding: 22px 20px 18px 20px;
            }
            QPushButton:disabled {
                background-color: #888888;
                border: 3px solid #666666;
                color: #CCCCCC;
            }
        """)

        # Подключаем сигнал нажатия кнопки
        self.stop_button.clicked.connect(self.on_stop_pressed)
        
        # Добавляем кнопку в layout
        layout.addWidget(self.stop_button)

        self.tab_list.currentRowChanged.connect(self.tab_changed.emit)

    def createBatteryWidget(self, layout):
        """Создает виджет с информацией о заряде батареи"""
        # Контейнер для батареи
        battery_container = QFrame()
        battery_container.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #2ECC71, stop: 1 #27AE60);
                border-radius: 7px;
                border: 1px solid #219653;
            }
        """)
        
        battery_layout = QVBoxLayout(battery_container)
        battery_layout.setSpacing(8)
        battery_layout.setContentsMargins(15, 15, 15, 15)

        # Иконка батареи и заголовок
        icon_title_layout = QHBoxLayout()
        
        # Заголовок
        title_label = QLabel("   🔋 Заряд тележки   ")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
               
            }
        """)
        icon_title_layout.addWidget(title_label)
        icon_title_layout.addStretch()
        
        battery_layout.addLayout(icon_title_layout)

        # Уровень заряда
        self.battery_level_label = QLabel("100%")
        self.battery_level_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        self.battery_level_label.setAlignment(Qt.AlignCenter)
        battery_layout.addWidget(self.battery_level_label)

       
    

        
        layout.addWidget(battery_container)

    def setupBatteryTimer(self):
        """Настраивает таймер для обновления уровня заряда"""
        self.battery_timer = QTimer()
        self.battery_timer.timeout.connect(self.updateBatteryLevel)
        self.battery_timer.start(5000)  # Обновление каждые 20 секунд

    def updateBatteryLevel(self):
        """Обновляет уровень заряда батареи"""
        if self.battery_level > 0:
            self.battery_level -= 1
            self.battery_level_label.setText(f"{self.battery_level}%")
            
            # Меняем цвет в зависимости от уровня заряда
            if self.battery_level > 70:
                color = "#2ECC71"  # Зеленый
            elif self.battery_level > 30:
                color = "#F39C12"  # Оранжевый
            else:
                color = "#E74C3C"  # Красный
                
            self.battery_level_label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-size: 24px;
                    font-weight: bold;
                    background-color: transparent;
                }}
            """)

    def on_stop_pressed(self):
        """Обработчик нажатия кнопки СТОП"""
        print("Кнопка СТОП нажата!")
        self.stop_pressed.emit()

    def set_stop_button_enabled(self, enabled):
        """Включить/выключить кнопку СТОП"""
        self.stop_button.setEnabled(enabled)

    def resetBattery(self):
        """Сбросить уровень заряда до 100%"""
        self.battery_level = 100
        self.battery_level_label.setText("100%")
        self.battery_level_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background-color: transparent;
            }
        """)