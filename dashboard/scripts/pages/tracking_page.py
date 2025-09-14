
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel
import random
import math
import sys

from .base_page import BasePage
from pages.tools.robot_widget import RobotWidget
from pages.tools.table_widget import TableWidget
from pages.tools.milling_machine_widget import MillingMachineWidget
from pages.tools.square_border_widget import SquareBorderWidget

class PaintObjects(QWidget):
    def __init__(self):
        super().__init__()
        self.robots = []
        self.tables = []
        self.milling_machines = []  
        self.square_borders = []
  
    def addRobot(self, robot):
        self.robots.append(robot)
        
    def addTable(self, table):
        self.tables.append(table)
        
    def addMillingMachine(self, machine):
        self.milling_machines.append(machine)

    def addSquareBorder(self, square_border):
        self.square_borders.append(square_border)

        
    def paintEvent(self, event):
        painter = QPainter(self)
        for square_border in self.square_borders:
            square_border.drawSquare(painter)
        
        for table in self.tables:
            table.drawTable(painter)
        
        for machine in self.milling_machines:
            machine.draw_milling_machine(painter)

        for robot in self.robots:
            robot.draw_realistic_robot(painter, robot.coordinate_x, robot.coordinate_y, robot.joint_angles)

 
class TrackingPage(BasePage):
    def __init__(self):
        super().__init__()
        self.stanok_labels = []
        self.setup_content()

    def setup_content(self):
        main_layout = self.layout()
        
        # Очищаем существующий layout
        while main_layout.count():
            child = main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Создаем холст
        self.canvas = PaintObjects()
        self.canvas.setMinimumSize(1800, 1000)  
        
        # Создаем роботов
        self.robot_widget_1 = RobotWidget(200, 200)
        self.robot_widget_2 = RobotWidget(750, 200)
        self.robot_widget_3 = RobotWidget(1300, 200)
        self.robot_widget_4 = RobotWidget(375+100, 600)
        self.robot_widget_5 = RobotWidget(900+100, 600)

        # Создаем 10 столов
        self.tables = []
        table_positions = [
            (70, 160, 75),   # x, y, size
            (250, 160, 75),
            (620, 160, 75),
            (800, 160, 75),
            (1170, 160, 75),
            (1350, 160, 75),
          
            (345, 560, 75),
            (525, 560, 75),
            (870, 560, 75),
            (1050, 560, 75)
        ]
        
        for x, y, size in table_positions:
            table = TableWidget(size, x, y)
            self.tables.append(table)
            self.canvas.addTable(table)
        
        # Создаем 5 фрезерных станков
        self.milling_machines = []
        machine_positions = [
            (100, 200, 200, 150, 1),   # x, y, width, height
            (650, 200, 220, 160, 2),
            (1200, 200, 180, 140, 3),
            (375, 600, 200, 150,4 ),
            (900, 600, 190, 145,5 )
        ]
        
        for x, y, width, height, number in machine_positions:
            machine = MillingMachineWidget(width, height, x, y)
            self.milling_machines.append(machine)
            self.canvas.addMillingMachine(machine)
           
            

        # Создаем 5 квадратных границ 
        self.square_borders = []
        square_positions = [
            (200, 270, 370, 1),  # Зона 1
            (750, 270, 370, 2),  # Зона 2
            (1300, 270, 370, 3), # Зона 3
            (475, 670, 370, 4),  # Зона 4
            (1000, 670, 370, 5)  # Зона 5
        ]
        
        for center_x, center_y, side_length, zone_number in square_positions:
            square_border = SquareBorderWidget(center_x, center_y, side_length)
            self.square_borders.append(square_border)
            self.canvas.addSquareBorder(square_border)
           
        # Создаем подписи зон с использованием QLabel
        stanok_labels_info = [
            (55, 415, "Станок 1"),    # x, y, text
            (605, 415, "Станок 2"),
            (1155, 415, "Станок 3"),
            (330, 815, "Станок 4"),
            (855, 815, "Станок 5")
        ]
        
        for x, y, text in stanok_labels_info:
            zone_label = QLabel(text, self.canvas)
            zone_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 200);
                    color: #000000;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 5px 10px;
                    border: 2px solid #000000;
                    border-radius: 8px;
                }
            """)
            zone_label.move(x - 30, y)  # Центрируем по x
            zone_label.adjustSize()
            self.stanok_labels.append(zone_label)

 
        self.canvas.addRobot(self.robot_widget_1)
        self.canvas.addRobot(self.robot_widget_2)
        self.canvas.addRobot(self.robot_widget_3)
        self.canvas.addRobot(self.robot_widget_4)
        self.canvas.addRobot(self.robot_widget_5)

        main_layout.addWidget(self.canvas, 1)
        
        control_layout = QHBoxLayout()
        random_btn = QPushButton("Случайное движение")
        random_btn.clicked.connect(self.randomMovementRobot)
        random_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        control_layout.addWidget(random_btn)
        
        main_layout.addLayout(control_layout)
        

        # Таймер для обновления холста и анимации станков
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.canvas.update)
        self.update_timer.start(30)


    def randomMovementRobot(self):
        list_robot = [self.robot_widget_1, self.robot_widget_2, self.robot_widget_3, self.robot_widget_4, self.robot_widget_5]
        for robot in list_robot:
            new_angles = [
                random.randint(-60, 60),
                random.randint(20, 100),
                random.randint(-80, -10),
                random.randint(-45, 45),
                0
            ]
            robot.set_target_pose(new_angles)
            robot.set_gripper_openness(random.random())


   



