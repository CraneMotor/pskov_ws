

from PyQt5.QtGui import (QColor, QBrush, QPen, QLinearGradient)


class MillingMachineWidget:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.spindle_rotation = 0
        
    def draw_milling_machine(self, painter):
        painter.save()
        painter.translate(int(self.x), int(self.y))  # Преобразуем в int
        
        # Рисуем основание станка
        self.draw_base(painter)
        
        # Рисуем колонну
        self.draw_column(painter)
        
        # Рисуем консоль
        self.draw_console(painter)
        
        # Рисуем шпиндель
        self.draw_spindle(painter)
        
        # Рисуем стол
        self.draw_machine_table(painter)
        
        # Анимируем шпиндель
        self.spindle_rotation = (self.spindle_rotation + 5) % 360
        
        painter.restore()
    
    def draw_base(self, painter):
        # Основание станка (серый чугун)
        base_gradient = QLinearGradient(0, self.height - 30, 0, self.height)
        base_gradient.setColorAt(0, QColor(100, 100, 100))
        base_gradient.setColorAt(1, QColor(60, 60, 60))
        
        painter.setBrush(QBrush(base_gradient))
        painter.setPen(QPen(QColor(40, 40, 40), 2))
        painter.drawRect(0, int(self.height - 30), int(self.width), 30)  # Преобразуем в int
        
        # Ребра жесткости на основании
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        for i in range(20, int(self.width), 40):  # Преобразуем в int
            painter.drawLine(i, int(self.height - 30), i, int(self.height - 10))  # Преобразуем в int
    
    def draw_column(self, painter):
        # Колонна станка
        column_gradient = QLinearGradient(self.width/2 - 40, 0, self.width/2 + 40, 0)
        column_gradient.setColorAt(0, QColor(120, 120, 120))
        column_gradient.setColorAt(0.5, QColor(180, 180, 180))
        column_gradient.setColorAt(1, QColor(120, 120, 120))
        
        painter.setBrush(QBrush(column_gradient))
        painter.setPen(QPen(QColor(80, 80, 80), 2))
        
        # Преобразуем все координаты в int
        x = int(self.width/2 - 40)
        y = 50
        width = 80
        height = int(self.height - 100)
        painter.drawRect(x, y, width, height)
        
        # Направляющие на колонне
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.drawLine(int(self.width/2 - 35), 60, int(self.width/2 - 35), int(self.height - 110))
        painter.drawLine(int(self.width/2 + 35), 60, int(self.width/2 + 35), int(self.height - 110))
    
    def draw_console(self, painter):
        # Консоль (движущаяся часть)
        console_gradient = QLinearGradient(0, 0, 0, 40)
        console_gradient.setColorAt(0, QColor(150, 150, 150))
        console_gradient.setColorAt(1, QColor(100, 100, 100))
        
        painter.setBrush(QBrush(console_gradient))
        painter.setPen(QPen(QColor(70, 70, 70), 2))
        
        # Преобразуем координаты в int
        x = int(self.width/2 - 60)
        y = 100
        width = 120
        height = 40
        painter.drawRect(x, y, width, height)
        
        # Крепление консоли к колонне
        painter.setBrush(QBrush(QColor(90, 90, 90)))
        painter.drawRect(int(self.width/2 - 10), 90, 20, 10)
    
    def draw_spindle(self, painter):
        # Шпиндельная бабка
        spindle_gradient = QLinearGradient(0, 0, 0, 60)
        spindle_gradient.setColorAt(0, QColor(140, 140, 140))
        spindle_gradient.setColorAt(1, QColor(90, 90, 90))
        
        painter.setBrush(QBrush(spindle_gradient))
        painter.setPen(QPen(QColor(60, 60, 60), 2))
        
        # Преобразуем координаты в int
        x = int(self.width/2 - 25)
        y = 140
        width = 50
        height = 60
        painter.drawRect(x, y, width, height)
        
        # Вращающийся шпиндель
        painter.save()
        painter.translate(int(self.width/2), 170)  # Преобразуем в int
        painter.rotate(self.spindle_rotation)
        
        # Сам шпиндель
        spindle_grad = QLinearGradient(-5, -20, -5, 20)
        spindle_grad.setColorAt(0, QColor(200, 200, 200))
        spindle_grad.setColorAt(1, QColor(120, 120, 120))
        
        painter.setBrush(QBrush(spindle_grad))
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        painter.drawRect(-5, -20, 10, 40)
        
        # Режущий инструмент (фреза)
        painter.setBrush(QBrush(QColor(60, 60, 60)))
        painter.drawRect(-8, -25, 16, 5)
        painter.drawRect(-8, 15, 16, 5)
        
        # Полосы движения на шпинделе
        painter.setPen(QPen(QColor(50, 50, 50), 1))
        for i in range(-15, 16, 5):
            painter.drawLine(-4, i, 4, i)
        
        painter.restore()
    
    def draw_machine_table(self, painter):
        # Стол фрезерного станка
        table_gradient = QLinearGradient(0, self.height - 80, 0, self.height - 50)
        table_gradient.setColorAt(0, QColor(180, 180, 180))
        table_gradient.setColorAt(1, QColor(140, 140, 140))
        
        painter.setBrush(QBrush(table_gradient))
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        
        # Преобразуем координаты в int
        x = 50
        y = int(self.height - 80)
        width = int(self.width - 100)
        height = 30
        painter.drawRect(x, y, width, height)
        
        # Т-образные пазы на столе
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        for i in range(70, int(self.width - 50), 50):  # Преобразуем в int
            # Основная канавка
            painter.drawLine(i, int(self.height - 75), i, int(self.height - 55))  # Преобразуем в int
            # Поперечные канавки
            painter.drawLine(i - 5, int(self.height - 70), i + 5, int(self.height - 70))  # Преобразуем в int
            painter.drawLine(i - 5, int(self.height - 60), i + 5, int(self.height - 60))  # Преобразуем в int
        
        # Прижимные элементы
        painter.setBrush(QBrush(QColor(100, 100, 100)))
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        for i in range(80, int(self.width - 80), 150):  # Преобразуем в int
            painter.drawRect(i, int(self.height - 85), 20, 5)  # Преобразуем в int
            painter.drawRect(i, int(self.height - 45), 20, 5)  # Преобразуем в int