
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import  QLinearGradient, QColor, QBrush

class TableWidget:
    def __init__(self, size, x, y):
        self.size = size
        self.x = x
        self.y = y
        
    def drawTable(self, painter):
        painter.save()
        painter.translate(self.x, self.y)
        
        gradient = QLinearGradient(0, 0, self.size, self.size)
        gradient.setColorAt(0, QColor(139, 69, 19))
        gradient.setColorAt(0.3, QColor(160, 82, 45))
        gradient.setColorAt(0.7, QColor(205, 133, 63))
        gradient.setColorAt(1, QColor(222, 184, 135))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        
        rect = QRectF(5, 5, self.size - 10, self.size - 10)
        painter.drawRoundedRect(rect, 15, 15)
        
        painter.setPen(QColor(101, 67, 33))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 15, 15)
        
        painter.setPen(QColor(101, 67, 33, 100))
        for i in range(5, self.size - 5, 8):
            painter.drawLine(i, 10, i, self.size - 10)
        
        painter.restore()