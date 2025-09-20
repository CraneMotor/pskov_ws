
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
        self.x_robot = 250
        self.y_robot = 100

        self.separator_x = 550
        self.separator_y = 350
        
        # Очищаем существующий layout
        while main_layout.count():
            child = main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Создаем холст
        self.canvas = PaintObjects()
        self.canvas.setMinimumSize(1800, 1000)  
        
        self.createRobots()
        self.createTables()
        self.createMillingMachines()
        self.createSquareBorders()
        self.createLabels()

        self.canvas.addRobot(self.robot_widget_1)
        self.canvas.addRobot(self.robot_widget_2)
        self.canvas.addRobot(self.robot_widget_3)
        self.canvas.addRobot(self.robot_widget_4)
        self.canvas.addRobot(self.robot_widget_5)

        main_layout.addWidget(self.canvas, 1)
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)
        
        # Таймер для обновления холста и анимации станков
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.canvas.update)
        self.update_timer.start(30)

        # Создаем таймер
        self.update_timer_2 = QTimer()
        self.update_timer_2.timeout.connect(self.randomMovementRobot)  # Подключаем вашу функцию
        self.update_timer_2.start(2000)  # 2000 миллисекунд = 2 секунды


    def randomMovementRobot(self):
        list_robot = [self.robot_widget_1, self.robot_widget_2, self.robot_widget_3, self.robot_widget_4, self.robot_widget_5]
        for robot in list_robot:
            new_angles = [
                # random.randint(-60, 60),
                # random.randint(20, 100),
                # random.randint(-80, -10),
                # random.randint(-45, 45),
                # 0,
                # 20,
                # -80, станок
                # 0,
                # 0
            ]
            robot.set_target_pose(new_angles)
            robot.set_gripper_openness(random.random())


   

    def createRobots(self):
        # Создаем роботов
        self.robot_widget_1 = RobotWidget(self.x_robot, self.y_robot)
        self.robot_widget_2 = RobotWidget(self.x_robot + self.separator_x, self.y_robot)
        self.robot_widget_3 = RobotWidget(self.x_robot + self.separator_x * 2, self.y_robot)
        self.robot_widget_4 = RobotWidget(self.x_robot + int(self.separator_x / 2), self.y_robot +  self.separator_y )
        self.robot_widget_5 = RobotWidget(self.x_robot + int(self.separator_x * 1.5) , self.y_robot +  self.separator_y)



    def createTables(self):
        # Создаем 10 столов
        self.tables = []
        table_positions = [
            (self.x_robot - 130,                            self.y_robot - 40, 75),   # x, y, size
            (self.x_robot + 50,                             self.y_robot - 40, 75),
            ((self.x_robot + self.separator_x - 130),       self.y_robot - 40, 75),
            ((self.x_robot + self.separator_x + 50),        self.y_robot - 40, 75),
            ((self.x_robot + 2 * self.separator_x - 130),   self.y_robot - 40, 75),
            ((self.x_robot + 2 * self.separator_x + 50),    self.y_robot - 40, 75),
          
            (self.x_robot + int(self.separator_x / 2) - 130,    self.y_robot +  self.separator_y - 40, 75),
            (self.x_robot + int(self.separator_x / 2) + 50 ,    self.y_robot +  self.separator_y - 40, 75),
            (self.x_robot + int(self.separator_x * 1.5) - 130,  self.y_robot +  self.separator_y - 40, 75),
            (self.x_robot + int(self.separator_x * 1.5) +50,    self.y_robot +  self.separator_y - 40, 75)
        ]
        
        for x, y, size in table_positions:
            table = TableWidget(size, x, y)
            self.tables.append(table)
            self.canvas.addTable(table)


    def createMillingMachines(self):
        # Создаем 5 фрезерных станков
        self.milling_machines = []
        machine_positions = [
            (self.x_robot  - 100,                                self.y_robot,                     200, 150, 1),   # x, y, width, height
            (self.x_robot + self.separator_x - 100,              self.y_robot,                     220, 160, 2),
            (self.x_robot + 2 * self.separator_x - 100,          self.y_robot,                     180, 140, 3),
            (self.x_robot + int(self.separator_x / 2) - 100,     self.y_robot +  self.separator_y, 200, 150,4 ),
            (self.x_robot + int(self.separator_x * 1.5) - 100,   self.y_robot +  self.separator_y, 190, 145,5 )
        ]
        
        for x, y, width, height, number in machine_positions:
            machine = MillingMachineWidget(width, height, x, y)
            self.milling_machines.append(machine)
            self.canvas.addMillingMachine(machine)


    def createSquareBorders(self):
        # Создаем 5 квадратных границ 
        self.square_borders = []
        square_positions = [
            (self.x_robot,                                  self.y_robot + 70,                      300, 1),  # Зона 1
            (self.x_robot + self.separator_x ,              self.y_robot + 70,                      300, 2),  # Зона 2
            (self.x_robot + self.separator_x * 2,           self.y_robot + 70,                      300, 3), # Зона 3
            (self.x_robot + int(self.separator_x / 2),      self.y_robot + self.separator_y + 70,  300, 4),  # Зона 4
            (self.x_robot + int(self.separator_x * 1.5),    self.y_robot + self.separator_y + 70,  300, 5),  # Зона 5

            (self.x_robot + int(self.separator_x / 2) + 70 ,     self.y_robot + self.separator_y + 390,  300, 5),  # Зона 5
            (self.x_robot + int(self.separator_x * 1.5) - 70,    self.y_robot + self.separator_y + 390,  300, 5)  # Зона 5
        ]
        
        for center_x, center_y, side_length, zone_number in square_positions:
            square_border = SquareBorderWidget(center_x, center_y, side_length)
            self.square_borders.append(square_border)
            self.canvas.addSquareBorder(square_border)


    def createLabels(self):
        # Создаем подписи зон с использованием QLabel
        stanok_labels_info = [
            (self.x_robot - 110,                                self.y_robot + 180, "Станок 1"),    # x, y, text
            (self.x_robot + self.separator_x - 110,             self.y_robot + 180, "Станок 2"),
            (self.x_robot + 2 * self.separator_x - 110,          self.y_robot + 180, "Станок 3"),
            (self.x_robot + int(self.separator_x / 2) - 110,    self.y_robot + self.separator_y + 180, "Станок 4"),
            (self.x_robot + int(self.separator_x * 1.5) - 110,  self.y_robot + self.separator_y + 180, "Станок 5"),

            (self.x_robot + int(self.separator_x / 2) - 110 + 70,    self.y_robot + self.separator_y + 390 + 110, "Зона загрузки"),
            (self.x_robot + int(self.separator_x * 1.5) - 110 - 70,  self.y_robot + self.separator_y + 390 + 110, "Зона выгрузки")
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
