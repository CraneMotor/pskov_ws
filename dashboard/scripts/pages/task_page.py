from .base_page import BasePage
from tools.badge_delegate import StatusBadgeDelegate
from PyQt5.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QWidget, QStyledItemDelegate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
from pathlib import Path
from PyQt5.QtWidgets import (QComboBox, QLineEdit, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFormLayout, QSpinBox)


class TaskPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setup_content()

    def setup_content(self):
        table_container = QWidget()
        table_container.setGeometry(0, 0, 1000, 800)

        self.createTable(table_container)
        self.getLabelTask(table_container)
        self.createComboBox(table_container)
        self.createLineEdit(table_container)
        self.createButton(table_container)
        self.addContentWidget(table_container)

   

    def fillTableData(self, table):
        table.setRowCount(0)
        tasks_data = [
            {"id": "001",   "robot": "Робот",    "status": "Завершено"},
            {"id": "0002",  "robot": "Тележка",  "status": "Завершено"},
            {"id": "0003",  "robot": "Робот",    "status": "Ошибка"},
            {"id": "0004",  "robot": "Тележка",  "status": "Выполняется"},
            {"id": "0005",  "robot": "Робот",    "status": "Завершено"},
            {"id": "0006",  "robot": "Тележка",  "status": "Отменено"},
            {"id": "0007",  "robot": "Робот",    "status": "Пауза"},
            {"id": "0008",  "robot": "Тележка",  "status": "Ожидание"},
            {"id": "0009",  "robot": "Робот",    "status": "Ошибка"},
            {"id": "0010",  "robot": "Тележка",  "status": "Пауза"}
        ]
        table.setRowCount(len(tasks_data))
        for row, task in enumerate(tasks_data):
           
            id_item = QTableWidgetItem(task["id"])
            id_item.setTextAlignment(Qt.AlignCenter)  
            table.setItem(row, 0, id_item)
            
            robot_item = QTableWidgetItem(task["robot"])
            robot_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, robot_item)
            
            status_item = QTableWidgetItem(task["status"])
            status_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 2, status_item)



    def getLabelTask(self, parent):
        title_label = QLabel("Задачи в работе", parent)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setGeometry(310, 10, 300, self.height_labels)
        title_label.setStyleSheet(Path("gss/label.gss").read_text())
        title_label.setFont(self.arial_16)

        type_part_label = QLabel("Тип детали", parent)
        type_part_label.setAlignment(Qt.AlignCenter)
        type_part_label.setGeometry(960, 80, 200, self.height_labels)
        type_part_label.setStyleSheet(Path("gss/label.gss").read_text())
        type_part_label.setFont(self.arial_14)

        stanok_label = QLabel("Тип станка", parent)
        stanok_label.setAlignment(Qt.AlignCenter)
        stanok_label.setGeometry(960, 80 + 50 + self.separator_labels, 200, self.height_labels)
        stanok_label.setStyleSheet(Path("gss/label.gss").read_text())
        stanok_label.setFont(self.arial_14)

        processing_time_one_part_label = QLabel("Время обработки<br/>одной детали", parent)
        processing_time_one_part_label.setAlignment(Qt.AlignCenter)
        processing_time_one_part_label.setGeometry(960, 80 + 2 * (self.height_labels + self.separator_labels), 200, self.height_labels * 2)
        processing_time_one_part_label.setStyleSheet(Path("gss/label.gss").read_text())
        processing_time_one_part_label.setFont(self.arial_14)

        quantity_in_batch_label = QLabel("Размер партии", parent)
        quantity_in_batch_label.setAlignment(Qt.AlignCenter)
        quantity_in_batch_label.setGeometry(960, 80 + 4 * self.height_labels + 3 * self.separator_labels, 200, self.height_labels)
        quantity_in_batch_label.setStyleSheet(Path("gss/label.gss").read_text())
        quantity_in_batch_label.setFont(self.arial_14)



    def createTable(self, parent):
        table_widget = QTableWidget(0, 3, parent)  
        table_widget.setHorizontalHeaderLabels(["Название / Идентификатор", "Робот / Тележка", "Статус задачи"])
        table_widget.setGeometry(10, 80, 900, 574)

        table_widget.setColumnWidth(0, 298)
        table_widget.setColumnWidth(1, 298)
        table_widget.setColumnWidth(2, 298)

        table_widget.verticalHeader().setDefaultSectionSize(50)
        table_widget.horizontalHeader().setFixedHeight(50)

        table_widget.setFont(self.arial_12)
        table_widget.horizontalHeader().setFont(self.arial_14)

        table_widget.setStyleSheet(Path("gss/table.gss").read_text())

        table_widget.horizontalHeader().setStyleSheet(
            "background-color: rgba(0,0,0,0);"
        )
        table_widget.verticalHeader().setVisible(False)

        
        status_delegate = StatusBadgeDelegate()
        table_widget.setItemDelegateForColumn(2, status_delegate)
        self.fillTableData(table_widget)

    def createComboBox(self, parent):
        part_combo = QComboBox(parent)
        part_combo.addItems(["Деталь A", "Деталь B", "Деталь C", "Деталь D", "Деталь E"])
        part_combo.setGeometry(960 + 200 + 50, 80 , 200, 50)
        part_combo.setStyleSheet(Path("gss/combo_box.gss").read_text())
        part_combo.setFont(self.arial_14)

        stanok_combo = QComboBox(parent)
        stanok_combo.addItems(["Станок A", "Станок B", "Станок C", "Станок D", "Станок E"])
        stanok_combo.setGeometry(960 + 200 + 50, 80 + 50 + self.separator_labels, 200, self.height_labels)
        stanok_combo.setStyleSheet(Path("gss/combo_box.gss").read_text())
        stanok_combo.setFont(self.arial_14)

        time_combo = QComboBox(parent)
        time_combo.addItems(["Секунда", "Минута", "Час"])
        time_combo.setGeometry(960 +200 +50 +40 +10 , 80 + 2 * (self.height_labels + self.separator_labels) + 25, 150, self.height_labels)
        time_combo.setStyleSheet(Path("gss/combo_box.gss").read_text())
        time_combo.setFont(self.arial_14)
       
    def createLineEdit(self, parent):
        time_one_part = QLineEdit(parent)
        time_one_part.setGeometry(960 +200 +50 , 80 + 2 * (self.height_labels + self.separator_labels) + 25, 40, self.height_labels)
        time_one_part.setStyleSheet(
            (
                "background-color: rgb(74,74,74) ;border-radius: 10px;  color: white"
            )
        )
        time_one_part.setFont(self.arial_14)

        number_batch = QLineEdit(parent)
        number_batch.setGeometry(960 +200 +50, 80 + 4 * self.height_labels + 3 * self.separator_labels, 200, self.height_labels )
        number_batch.setStyleSheet(
            (
                "background-color: rgb(74,74,74) ;border-radius: 10px;  color:  white"
            )
        )
        number_batch.setFont(self.arial_14)


    def createButton(self, parent):
        create_task = QPushButton("Создать задачу", parent)
        create_task.setGeometry(1070, 410+15, 300, self.height_labels)
        create_task.setFont(self.arial_16)
        create_task.setStyleSheet(Path("gss/button.gss").read_text())
        create_task.clicked.connect(self.createTask)
        
    def createTask(self):
        ...