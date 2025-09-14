
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont

# Класс для отрисовки статус-баджей

class StatusBadgeDelegate(QStyledItemDelegate):

    status_colors = {
        "Завершено": QColor(6, 157, 101, 150),    # Мягкий зеленый (было: 76, 175, 80)
        "Выполняется": QColor(164, 6, 189, 150),  # Мягкий фиолетовый (было: 156, 39, 176)
        "Ошибка": QColor(202, 14, 117, 150),       # Мягкий красный (было: 244, 67, 54)
        "Ожидание": QColor(7, 133, 186, 150),     # Очень светлый фиолетовый
        "Отменено": QColor(112, 108, 98, 150),     # Мягкий серо-голубой (было: 96, 125, 139)
        "Пауза": QColor(186, 133, 7, 150),        # Мягкий желтый (было: 255, 193, 7)
    }
    def paint(self, painter, option, index):
        status_text = index.data(Qt.DisplayRole)
        if status_text not in self.status_colors:
            super().paint(painter, option, index)
            return
        bg_color = self.status_colors[status_text]
        text_color = QColor(255, 255, 255)
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
    
        rect = option.rect.adjusted(50, 7, -50, -7)  
        painter.setPen(QPen(bg_color.darker(120), 2))  
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(rect, 12, 12)  
        
        painter.setPen(text_color)
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, status_text)
        
        painter.restore()
     