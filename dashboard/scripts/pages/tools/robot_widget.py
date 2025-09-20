
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath, QLinearGradient, QRadialGradient

from PyQt5.QtCore import QTimer, Qt, QPointF, QRectF
from PyQt5.QtGui import (QPainter, QColor, QBrush, QPen, QPainterPath, 
                         QLinearGradient, QRadialGradient)
class RobotWidget(QLabel):
    def __init__(self,  coordinate_x, coordinate_y, parent=None):
        super().__init__(parent)
        self.coordinate_y =coordinate_y
        self.coordinate_x =coordinate_x
        
        # Параметры кинематической цепи
        self.joint_angles = [0, 45, -30, 0, 0]
        self.target_angles = [0, 45, -30, 0, 0]
        self.gripper_openness = 0.5  # 0.0 - закрыт, 1.0 - открыт
        
        # Таймер анимации
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)

    def update_animation(self):
        # Плавная интерполяция углов
        for i in range(len(self.joint_angles)):
            diff = self.target_angles[i] - self.joint_angles[i]
            if abs(diff) > 0.5:
                self.joint_angles[i] += diff * 0.08
        self.update()

    def set_target_pose(self, new_angles):
        self.target_angles = new_angles

    def set_gripper_openness(self, openness):
        self.gripper_openness = max(-1.0, min(0.0, openness))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_realistic_robot(painter, self.coordinate_x, self.coordinate_y, self.joint_angles)

    def draw_realistic_robot(self, painter, x, y, angles):
        painter.save()
        painter.translate(x, y)
        painter.scale(0.5, 0.5)  # Масштаб для встраивания
        
        # Основные цвета
        arm_red = QColor(200, 50, 50)
        joint_gray = QColor(100, 100, 110)
        metallic_dark = QColor(60, 60, 70)
        highlight = QColor(255, 255, 255, 150)
        gripper_color = QColor(80, 80, 90)

        # Основание
        self.draw_rounded_base(painter, metallic_dark, highlight)
        painter.rotate(angles[0])
        self.draw_rotational_joint(painter, joint_gray, 0, 0, 50)

        # Первое плечо
        shoulder_length = 70
        self.draw_arm_segment(painter, QPointF(0, 0), QPointF(0, shoulder_length), arm_red, 30, 25)
        painter.translate(0, shoulder_length)
        painter.rotate(angles[1])
        self.draw_complex_joint(painter, joint_gray, 0, 0, 35)

        # Второе плечо
        forearm_length = 60
        self.draw_arm_segment(painter, QPointF(0, 0), QPointF(0, forearm_length), arm_red, 25, 20)
        painter.translate(0, forearm_length)
        painter.rotate(angles[2])
        self.draw_wrist_joint(painter, joint_gray, 0, 0, 28)

        # Кисть
        hand_length = 40
        self.draw_arm_segment(painter, QPointF(0, 0), QPointF(0, hand_length), arm_red, 20, 18)

        # Схват
        painter.translate(0, hand_length)
        painter.rotate(angles[3])
        self.draw_realistic_gripper(painter, gripper_color, highlight)

        painter.restore()

    def draw_rounded_base(self, painter, color, highlight):
        path = QPainterPath()
        path.addRoundedRect(QRectF(-40, -20, 80, 40), 10, 10)
        
        gradient = QLinearGradient(-40, -20, -40, 20)
        gradient.setColorAt(0, color.lighter(120))
        gradient.setColorAt(0.5, color)
        gradient.setColorAt(1, color.darker(120))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(color.darker(150), 2))
        painter.drawPath(path)

    def draw_arm_segment(self, painter, start, end, color, start_width, end_width):
        path = QPainterPath()
        path.moveTo(start)
        path.lineTo(end)
        
        gradient = QLinearGradient(start, end)
        gradient.setColorAt(0, color.lighter(115))
        gradient.setColorAt(0.5, color)
        gradient.setColorAt(1, color.darker(115))
        
        pen = QPen(QBrush(gradient), start_width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawPath(path)

    def draw_rotational_joint(self, painter, color, x, y, size):
        radius = size / 2
        gradient = QRadialGradient(x, y, radius)
        gradient.setColorAt(0, color.lighter(130))
        gradient.setColorAt(0.7, color)
        gradient.setColorAt(1, color.darker(130))
        
        painter.setPen(QPen(color.darker(150), 2))
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QRectF(-radius, -radius, size, size))

    def draw_complex_joint(self, painter, color, x, y, size):
        radius = size / 2
        gradient = QRadialGradient(x, y, radius)
        gradient.setColorAt(0, color.lighter(130))
        gradient.setColorAt(0.7, color)
        gradient.setColorAt(1, color.darker(130))
        
        painter.setPen(QPen(color.darker(150), 2))
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(QRectF(-radius, -radius, size, size))

    def draw_wrist_joint(self, painter, color, x, y, size):
        self.draw_complex_joint(painter, color, x, y, size)

    def draw_realistic_gripper(self, painter, color, highlight):
        # Основание схвата
        base_gradient = QLinearGradient(-12, -15, -12, 15)
        base_gradient.setColorAt(0, color.lighter(120))
        base_gradient.setColorAt(1, color.darker(120))
        
        painter.setPen(QPen(color.darker(150), 1))
        painter.setBrush(QBrush(base_gradient))
        painter.drawRoundedRect(QRectF(-10, -12, 20, 24), 4, 4)
        
        # Пальцы схвата
        finger_length = 35
        finger_width = 8
        finger_offset = 6 + self.gripper_openness * 15
        
        # Левый палец
        left_finger = QPainterPath()
        left_finger.moveTo(-finger_offset, 0)
        left_finger.lineTo(-finger_offset - finger_width, -finger_length * 0.3)
        left_finger.lineTo(-finger_offset - finger_width, -finger_length)
        left_finger.lineTo(-finger_offset, -finger_length + 2)
        left_finger.lineTo(-finger_offset, 0)
        left_finger.closeSubpath()
        
        # Правый палец
        right_finger = QPainterPath()
        right_finger.moveTo(finger_offset, 0)
        right_finger.lineTo(finger_offset + finger_width, -finger_length * 0.3)
        right_finger.lineTo(finger_offset + finger_width, -finger_length)
        right_finger.lineTo(finger_offset, -finger_length + 2)
        right_finger.lineTo(finger_offset, 0)
        right_finger.closeSubpath()
        
        finger_gradient = QLinearGradient(0, 0, 0, -finger_length)
        finger_gradient.setColorAt(0, color.lighter(110))
        finger_gradient.setColorAt(0.7, color)
        finger_gradient.setColorAt(1, color.darker(110))
        
        painter.setBrush(QBrush(finger_gradient))
        painter.setPen(QPen(QColor(30, 30, 35), 1))
        painter.drawPath(left_finger)
        painter.drawPath(right_finger)