# tools/cart_widget.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPointF
import random
import math

class CartWidget:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.width = 60
        self.height = 40
        self.speed = 2
        self.target_x = start_x
        self.target_y = start_y
        self.is_moving = False
        self.current_zone = 0
        self.wheel_rotation = 0
        
        # Таймер для анимации движения и вращения колес
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(50)  # Обновление каждые 50 мс
        
    def set_target(self, target_x, target_y, zone_number):
        self.target_x = target_x
        self.target_y = target_y
        self.is_moving = True
        self.current_zone = zone_number
        
    def animate(self):
        # Анимируем вращение колес
        self.wheel_rotation = (self.wheel_rotation + 10) % 360
        
        if self.is_moving:
            # Вычисляем направление движения
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > self.speed:
                # Двигаемся к цели
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
            else:
                # Достигли цели
                self.x = self.target_x
                self.y = self.target_y
                self.is_moving = False
                
    def draw_cart(self, painter):
        painter.save()
        painter.translate(int(self.x), int(self.y))
        
        # Рисуем корпус тележки
        self.draw_cart_body(painter)
        
        # Рисуем колеса
        self.draw_wheels(painter)
        
        # Рисуем ручку
        self.draw_handle(painter)
        
        painter.restore()
        
    def draw_cart_body(self, painter):
        # Градиент для корпуса тележки
        body_gradient = QLinearGradient(0, 0, 0, self.height)
        body_gradient.setColorAt(0, QColor(200, 50, 50))    # Красный
        body_gradient.setColorAt(1, QColor(150, 30, 30))    # Темно-красный
        
        painter.setBrush(QBrush(body_gradient))
        painter.setPen(QPen(QColor(100, 20, 20), 2))
        
        # Рисуем основной корпус
        painter.drawRoundedRect(5, 10, self.width - 10, self.height - 15, 8, 8)
        
        # Рисуем верхнюю часть
        painter.drawRect(15, 5, self.width - 30, 10)
        
    def draw_wheels(self, painter):
        # Сохраняем состояние для вращения колес
        painter.save()
        
        # Левое колесо
        painter.translate(15, self.height - 5)
        painter.rotate(self.wheel_rotation)
        self.draw_wheel(painter)
        painter.restore()
        
        # Правое колесо
        painter.save()
        painter.translate(self.width - 15, self.height - 5)
        painter.rotate(self.wheel_rotation)
        self.draw_wheel(painter)
        painter.restore()
        
    def draw_wheel(self, painter):
        # Внешняя часть колеса
        painter.setBrush(QBrush(QColor(50, 50, 50)))
        painter.setPen(QPen(QColor(30, 30, 30), 2))
        painter.drawEllipse(-8, -8, 16, 16)
        
        # Внутренняя часть колеса (ступица)
        painter.setBrush(QBrush(QColor(100, 100, 100)))
        painter.drawEllipse(-4, -4, 8, 8)
        
        # Спицы
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        for i in range(0, 360, 45):
            painter.drawLine(0, 0, 6 * math.cos(math.radians(i)), 6 * math.sin(math.radians(i)))
        
    def draw_handle(self, painter):
        painter.setPen(QPen(QColor(80, 80, 80), 3))
        # Ручка тележки
        painter.drawLine(self.width // 2, 5, self.width // 2 + 20, -15)
        painter.drawLine(self.width // 2 + 20, -15, self.width // 2 + 40, -10)
        
        # Ручка на конце
        painter.setPen(QPen(QColor(60, 60, 60), 4))
        painter.drawLine(self.width // 2 + 35, -12, self.width // 2 + 45, -8)