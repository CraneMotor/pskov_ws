
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient, QRadialGradient

class StatusBadgeDelegate(QStyledItemDelegate):
    # Градиенты для текста столбцов 1 и 2
    text_gradients = {
        1: {
            "Неподвижен": (QColor(160, 160, 160), QColor(120, 120, 120)),
            "Движение": (QColor(0, 200, 83), QColor(0, 160, 63)),
            "Ошибка": (QColor(255, 82, 82), QColor(200, 40, 40)),
            "Пауза": (QColor(255, 193, 7), QColor(230, 160, 0)),
            "Ожидание": (QColor(79, 195, 247), QColor(49, 155, 207)),
        },
        2: {
            "Неактивен": (QColor(160, 160, 160), QColor(120, 120, 120)),
            "Фрезерование": (QColor(0, 200, 83), QColor(0, 160, 63)),
            "Пауза": (QColor(255, 193, 7), QColor(230, 160, 0)),
            "Ожидание": (QColor(79, 195, 247), QColor(49, 155, 207)),
            "Ошибка": (QColor(244, 67, 54), QColor(200, 40, 40)),
        }
    }

    # Градиенты для баджей столбца 3
    badge_gradients = {
        3: {
            "Завершено": ("radial", QColor(0, 100, 0), QColor(0, 150, 80)),
            "Выполняется": ("radial", QColor(138, 43, 226), QColor(75, 0, 130)),
            "Ошибка": ("radial", QColor(255, 0, 0), QColor(139, 0, 0)),
            "Ожидание": ("radial", QColor(59, 175, 227), QColor(29, 135, 187)),
            "Отменено": ("radial", QColor(169, 169, 169), QColor(105, 105, 105)),
            "Пауза": ("radial", QColor(235, 145, 0), QColor(160, 100, 0)),
        }
    }

    def paint(self, painter, option, index):
        status_text = index.data(Qt.DisplayRole)
        column = index.column()
        
        # Для столбцов 1 и 2 - градиентный текст
        if column in [1, 2] and status_text in self.text_gradients.get(column, {}):
            self.paintGradientText(painter, option, index, status_text, column)
        
        # Для столбца 3 - градиентные баджи
        elif column == 3 and status_text in self.badge_gradients.get(column, {}):
            self.paintGradientBadge(painter, option, index, status_text, column)
        
        else:
            super().paint(painter, option, index)

    def paintGradientText(self, painter, option, index, status_text, column):
        """Отрисовка градиентного текста для столбцов 1 и 2"""
        color_start, color_end = self.text_gradients[column][status_text]
        
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        rect = option.rect

        # Создаем градиент для текста
        text_gradient = QLinearGradient(rect.left(), rect.center().y(), 
                                      rect.right(), rect.center().y())
        text_gradient.setColorAt(0, color_start)
        text_gradient.setColorAt(1, color_end)

        # Настраиваем шрифт
        font = QFont("Arial", 12, QFont.Bold)
        
        # Добавляем легкую тень для лучшей читаемости
        painter.setPen(QPen(QColor(0, 0, 0, 50), 1))
        painter.setFont(font)
        shadow_rect = rect.adjusted(1, 1, 1, 1)
        painter.drawText(shadow_rect, Qt.AlignCenter, status_text)

        # Рисуем основной градиентный текст
        painter.setPen(QPen(text_gradient, 1))
        painter.drawText(rect, Qt.AlignCenter, status_text)

        painter.restore()

    def paintGradientBadge(self, painter, option, index, status_text, column):
        """Отрисовка градиентных баджей для столбца 3"""
        gradient_type, color_start, color_end = self.badge_gradients[column][status_text]
        text_color = QColor(255, 255, 255)
        
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        rect = option.rect.adjusted(60, 7, -60, -7)
   
        # Создаем градиент в зависимости от типа
        if gradient_type == "linear":
            gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        else:  # radial
            center = rect.center()
            radius = max(rect.width(), rect.height()) / 2
            gradient = QRadialGradient(center, radius, center)
        
        gradient.setColorAt(0, color_start)
        gradient.setColorAt(1, color_end)

        # Рисуем основной бадж с градиентом
        painter.setPen(QPen(color_end.darker(120), 2))
        painter.setBrush(QBrush(gradient))
        painter.drawRoundedRect(rect, 8, 8)

        # Добавляем легкое свечение
        if gradient_type == "radial":
            glow_rect = rect.adjusted(-1, -1, 1, 1)
            painter.setPen(QPen(color_start.lighter(120), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(glow_rect, 9, 9)

        # Рисуем текст
        painter.setPen(text_color)
        font = QFont("Arial", 11, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, status_text)

        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        if index.column() == 3:  # Увеличиваем высоту только для столбца с баджами
            size.setHeight(45)
        return size