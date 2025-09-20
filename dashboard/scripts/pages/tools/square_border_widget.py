# tools/square_border.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt

class SquareBorderWidget:
    def __init__(self, center_x, center_y, side_length, border_color=QColor(117, 62, 218), border_width=1.5):
        self.center_x = center_x
        self.center_y = center_y
        self.side_length = side_length
        self.border_color = border_color
        self.border_width = border_width
        
    def drawSquare(self, painter):
        painter.save()

        half_side = self.side_length / 2
        x1 = int(self.center_x - half_side)
        y1 = int(self.center_y - half_side)
        x2 = int(self.center_x + half_side)
        y2 = int(self.center_y + half_side)
        
        pen = QPen(self.border_color, self.border_width)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        painter.drawLine(x2, y1+100, x2, y2) # Правая линия
        painter.drawLine(x2, y2, x1, y2) # Нижняя линия
        painter.drawLine(x1, y2, x1, y1+100) # Левая линия
        
        painter.restore()