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
        self.width = 80
        self.height = 60
        self.speed = 5
        self.target_x = start_x
        self.target_y = start_y
        self.is_moving = False
        self.current_zone = 0
        self.direction = "right"  # Направление движения: "right", "left", "up", "down"
        
        # Таймер для анимации движения
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(50)  # Обновление каждые 50 мс
        
        # Заготовки на тележке
        self.workpieces = []
        
    def set_target(self, target_x, target_y, zone_number):
        self.target_x = target_x
        self.target_y = target_y
        self.is_moving = True
        self.current_zone = zone_number
        
        # Определяем направление движения
        if abs(target_x - self.x) > abs(target_y - self.y):
            self.direction = "right" if target_x > self.x else "left"
        else:
            self.direction = "down" if target_y > self.y else "up"
        
    def add_workpiece(self, workpiece_type="standard"):
        """Добавить заготовку на тележку"""
        self.workpieces.append(workpiece_type)
        
    def remove_workpiece(self):
        """Убрать заготовку с тележки"""
        if self.workpieces:
            return self.workpieces.pop()
        return None
        
    def animate(self):
        if self.is_moving:
            # Движение только по прямым углам
            if self.direction == "right":
                if self.x < self.target_x:
                    self.x += self.speed
                else:
                    self.x = self.target_x
                    self.is_moving = False
                    
            elif self.direction == "left":
                if self.x > self.target_x:
                    self.x -= self.speed
                else:
                    self.x = self.target_x
                    self.is_moving = False
                    
            elif self.direction == "down":
                if self.y < self.target_y:
                    self.y += self.speed
                else:
                    self.y = self.target_y
                    self.is_moving = False
                    
            elif self.direction == "up":
                if self.y > self.target_y:
                    self.y -= self.speed
                else:
                    self.y = self.target_y
                    self.is_moving = False
                
    def draw_cart(self, painter):
        painter.save()
        painter.translate(int(self.x), int(self.y))
        
        # Рисуем корпус тележки (вид сверху)
        self.draw_cart_body(painter)
        
        # Рисуем заготовки
        self.draw_workpieces(painter)
        
        # Рисуем стрелку направления
        self.draw_direction_indicator(painter)
        
        painter.restore()
        
    def draw_cart_body(self, painter):
        # Основной корпус тележки (вид сверху)
        body_gradient = QLinearGradient(0, 0, self.width, self.height)
        body_gradient.setColorAt(0, QColor(100, 100, 150))    # Сине-серый
        body_gradient.setColorAt(1, QColor(70, 70, 120))      # Темный сине-серый
        
        painter.setBrush(QBrush(body_gradient))
        painter.setPen(QPen(QColor(50, 50, 80), 2))
        
        # Рисуем прямоугольный корпус
        painter.drawRect(0, 0, self.width, self.height)
        
        # Добавляем детали для объема
        painter.setPen(QPen(QColor(120, 120, 170), 1))
        painter.drawRect(5, 5, self.width - 10, self.height - 10)
        
        # Металлические углы
        painter.setBrush(QBrush(QColor(180, 180, 200)))
        painter.setPen(QPen(QColor(150, 150, 180), 1))
        painter.drawRect(0, 0, 8, 8)  # Левый верхний
        painter.drawRect(self.width - 8, 0, 8, 8)  # Правый верхний
        painter.drawRect(0, self.height - 8, 8, 8)  # Левый нижний
        painter.drawRect(self.width - 8, self.height - 8, 8, 8)  # Правый нижний
        
    def draw_workpieces(self, painter):
        """Рисуем заготовки на тележке"""
        if not self.workpieces:
            return
            
        painter.setBrush(QBrush(QColor(200, 150, 100)))  # Цвет металла
        painter.setPen(QPen(QColor(150, 100, 70), 1))
        
        # Рисуем заготовки в виде прямоугольников
        for i, workpiece in enumerate(self.workpieces):
            if i < 4:  # Максимум 4 заготовки для визуализации
                row = i // 2
                col = i % 2
                
                x_pos = 15 + col * 20
                y_pos = 10 + row * 15
                
                # Разные типы заготовок
                if workpiece == "large":
                    painter.drawRect(x_pos, y_pos, 18, 12)
                else:  # standard
                    painter.drawRect(x_pos, y_pos, 15, 10)
                
                # Добавляем детали на заготовки
                painter.setPen(QPen(QColor(180, 180, 200), 1))
                painter.drawLine(x_pos + 3, y_pos + 2, x_pos + 12, y_pos + 2)
                painter.drawLine(x_pos + 3, y_pos + 8, x_pos + 12, y_pos + 8)
                painter.setPen(QPen(QColor(150, 100, 70), 1))
        
    def draw_direction_indicator(self, painter):
        """Рисуем стрелку направления движения"""
        if not self.is_moving:
            return
            
        painter.setPen(QPen(QColor(0, 255, 0), 2))  # Зеленая стрелка
        
        center_x = self.width // 2
        center_y = self.height // 2
        
        if self.direction == "right":
            painter.drawLine(center_x, center_y, self.width - 5, center_y)
            painter.drawLine(self.width - 10, center_y - 5, self.width - 5, center_y)
            painter.drawLine(self.width - 10, center_y + 5, self.width - 5, center_y)
            
        elif self.direction == "left":
            painter.drawLine(center_x, center_y, 5, center_y)
            painter.drawLine(10, center_y - 5, 5, center_y)
            painter.drawLine(10, center_y + 5, 5, center_y)
            
        elif self.direction == "down":
            painter.drawLine(center_x, center_y, center_x, self.height - 5)
            painter.drawLine(center_x - 5, self.height - 10, center_x, self.height - 5)
            painter.drawLine(center_x + 5, self.height - 10, center_x, self.height - 5)
            
        elif self.direction == "up":
            painter.drawLine(center_x, center_y, center_x, 5)
            painter.drawLine(center_x - 5, 10, center_x, 5)
            painter.drawLine(center_x + 5, 10, center_x, 5)