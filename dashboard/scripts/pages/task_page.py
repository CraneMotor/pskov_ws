from .base_page import BasePage
from tools.badge_delegate import StatusBadgeDelegate

from PyQt5.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QWidget, QStyledItemDelegate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
from pathlib import Path
from PyQt5.QtWidgets import (QComboBox, QLineEdit, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFormLayout, QSpinBox, QDialog)


class TaskPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setup_content()

    def setup_content(self):
        table_container = QWidget()
        table_container.setGeometry(0, 0, 1500, 1000)

        self.createTable(table_container)
        self.getLabelTask(table_container)
        self.createComboBox(table_container)
        self.createLineEdit(table_container)
        self.createButton(table_container)
        self.addContentWidget(table_container)

   

    def fillTableData(self, table):
        table.setRowCount(0)
        tasks_data = [
            {"id": "001",   "robot": "Неподвижен", "stanok": "Неактивен",    "status": "Завершено"},
            {"id": "0002",  "robot": "Неподвижен", "stanok": "Неактивен", "status": "Завершено"},
            {"id": "0003",  "robot": "Ошибка",  "stanok": "Неактивен",  "status": "Ошибка"},
            {"id": "0004",  "robot": "Движение", "stanok": "Фрезерование", "status": "Выполняется"},
            {"id": "0005",  "robot": "Неподвижен", "stanok": "Неактивен",   "status": "Завершено"},
            {"id": "0006",  "robot": "Неподвижен","stanok": "Неактивен",  "status": "Отменено"},
            {"id": "0007",  "robot": "Пауза", "stanok": "Пауза",   "status": "Пауза"},
            {"id": "0008",  "robot": "Ожидание",  "stanok": "Ожидание","status": "Ожидание"},
            {"id": "0009",  "robot": "Неподвижен",    "stanok": "Ошибка","status": "Ошибка"},
            {"id": "0010",  "robot": "Пауза","stanok": "Пауза",  "status": "Пауза"}
        ]
        table.setRowCount(len(tasks_data))
        for row, task in enumerate(tasks_data):
           
            id_item = QTableWidgetItem(task["id"])
            id_item.setTextAlignment(Qt.AlignCenter)  
            table.setItem(row, 0, id_item)
            
            robot_item = QTableWidgetItem(task["robot"])
            robot_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, robot_item)

            robot_item = QTableWidgetItem(task["stanok"])
            robot_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 2, robot_item)
            
            status_item = QTableWidgetItem(task["status"])
            status_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 3, status_item)



    def getLabelTask(self, parent):

        title_label = QLabel("Задачи в работе", parent)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setGeometry(600, 10, 300, self.height_labels)
        title_label.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/label.gss").read_text())
        title_label.setFont(self.arial_16)
    

        type_part_label = QLabel("Тип детали", parent)
        type_part_label.setAlignment(Qt.AlignCenter)
        type_part_label.setGeometry(50, 750, 200, self.height_labels)
        type_part_label.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/label.gss").read_text())
        type_part_label.setFont(self.arial_12)

        stanok_label = QLabel("Тип станка", parent)
        stanok_label.setAlignment(Qt.AlignCenter)
        stanok_label.setGeometry(50, 750 + 50 + self.separator_labels, 200, self.height_labels)
        stanok_label.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/label.gss").read_text())
        stanok_label.setFont(self.arial_12)

        processing_time_one_part_label = QLabel("Время обработки одной детали", parent)
        processing_time_one_part_label.setAlignment(Qt.AlignCenter)
        processing_time_one_part_label.setGeometry(50 + 200 + self.separator_labels + 200 + 50, 750, 350, self.height_labels )
        processing_time_one_part_label.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/label.gss").read_text())
        processing_time_one_part_label.setFont(self.arial_12)

        quantity_in_batch_label = QLabel("Размер партии", parent)
        quantity_in_batch_label.setAlignment(Qt.AlignCenter)
        quantity_in_batch_label.setGeometry(50 + 200 + self.separator_labels + 200 + 50, 750 + 50 + self.separator_labels, 200, self.height_labels)
        quantity_in_batch_label.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/label.gss").read_text())
        quantity_in_batch_label.setFont(self.arial_12)



    def createTable(self, parent):

        table_widget = QTableWidget(0, 4, parent)  
        table_widget.setHorizontalHeaderLabels(["Идентификатор задачи", "Статус pобота", "Статус станка", "Статус задачи" ])
        table_widget.setGeometry(150, 80, 1200, 574)

        table_widget.setColumnWidth(0, 298)
        table_widget.setColumnWidth(1, 298)
        table_widget.setColumnWidth(2, 298)
        table_widget.setColumnWidth(3, 298)
        

        table_widget.verticalHeader().setDefaultSectionSize(50)
        table_widget.horizontalHeader().setFixedHeight(50)

        table_widget.setFont(self.arial_12)
        table_widget.horizontalHeader().setFont(self.arial_14)

        table_widget.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/table.gss").read_text())

        table_widget.horizontalHeader().setStyleSheet(
            "background-color: rgba(0,0,0,0);"
        )
        table_widget.verticalHeader().setVisible(False)

        

        status_delegate = StatusBadgeDelegate()  # Для столбца 1 (робот)
        
        
        table_widget.setItemDelegateForColumn(1, status_delegate)
        table_widget.setItemDelegateForColumn(2, status_delegate)
        table_widget.setItemDelegateForColumn(3, status_delegate)

        # Подключаем обработчик клика по ячейке
        table_widget.cellClicked.connect(self.onCellClicked)

        self.fillTableData(table_widget)

    def onCellClicked(self, row, column):
        """Обработчик клика по ячейке таблицы"""
        table_widget = self.sender()  # Получаем таблицу, которая отправила сигнал
        
        # Получаем идентификатор задачи из первого столбца
        task_id_item = table_widget.item(row, 0)
        if task_id_item:
            task_id = task_id_item.text()
            
            # Получаем полную информацию о задаче (этот метод нужно реализовать)
            task_info = self.getTaskDetails(task_id)
            
            # Отображаем информацию в диалоговом окне
            self.showTaskDetailsDialog(task_info)

    def getTaskDetails(self, task_id):
        """Метод для получения детальной информации о задаче"""
        # Здесь реализуйте логику получения данных о задаче
        # Это может быть запрос к базе данных, API или другому источнику данных
        
        # Пример возвращаемых данных:
        task_details = {
            "Идентификатор": task_id,
            "Время начала": "2024-01-15 10:30:00",
            "Время окончания": "2024-01-15 12:45:00",
            "Статус": "Выполнено",
            "Описание": "Обработка деталей",
            "Оператор": "Иванов И.И.",
            "Приоритет": "Высокий"
        }
        
        return task_details

    def showTaskDetailsDialog(self, task_info):
        """Отображение диалогового окна с информацией о задаче"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Детальная информация о задаче")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Создаем форму для отображения информации
        form_layout = QFormLayout()
        
        for key, value in task_info.items():
            label = QLabel(f"<b>{key}:</b>")
            value_label = QLabel(str(value))
            form_layout.addRow(label, value_label)
        
        layout.addLayout(form_layout)
        
        # Добавляем кнопку закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        
        dialog.setLayout(layout)
        dialog.exec_()
    def createComboBox(self, parent):
        part_combo = QComboBox(parent)
        part_combo.addItems(["Деталь A", "Деталь B", "Деталь C", "Деталь D", "Деталь E"])
        part_combo.setGeometry(50 + 200 + 50, 750 , 200, 50)
        part_combo.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/combo_box.gss").read_text())
        part_combo.setFont(self.arial_12)

        stanok_combo = QComboBox(parent)
        stanok_combo.addItems(["Станок 1", "Станок 2", "Станок 3", "Станок 4", "Станок 5"])
        stanok_combo.setGeometry(50 + 200 + 50, 750 + 50 + self.separator_labels, 200, self.height_labels)
        stanok_combo.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/combo_box.gss").read_text())
        stanok_combo.setFont(self.arial_12)

        time_combo = QComboBox(parent)
        time_combo.addItems(["Секунда", "Минута", "Час"])
        time_combo.setGeometry(50 + 200 + self.separator_labels + 200 + 50 + 350 + 50 +40+10 , 750, 150, self.height_labels)
        time_combo.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/combo_box.gss").read_text())
        time_combo.setFont(self.arial_14)
       
    def createLineEdit(self, parent):
        time_one_part = QLineEdit(parent)
        time_one_part.setGeometry(50 + 200 + self.separator_labels + 200 + 50 + 350 + 50 , 750, 40, self.height_labels)
        time_one_part.setStyleSheet(
            (
                "background-color: rgb(74,74,74) ;border-radius: 10px;  color: white"
            )
        )
        time_one_part.setFont(self.arial_12)

        number_batch = QLineEdit(parent)
        number_batch.setGeometry(50 + 200 + self.separator_labels + 200 + 50 + 200 + 50, 750 + 50 + self.separator_labels, 200, self.height_labels )
        number_batch.setStyleSheet(
            (
                "background-color: rgb(74,74,74) ;border-radius: 10px;  color:  white"
            )
        )
        number_batch.setFont(self.arial_14)


    def createButton(self, parent):
        create_task = QPushButton("Создать задачу", parent)
        create_task.setGeometry(1250, 815, 200, self.height_labels)
        create_task.setFont(self.arial_12)
        create_task.setStyleSheet(Path("/home/cranemotor/workspace/pskov_ws/dashboard/scripts/gss/button.gss").read_text())
        create_task.clicked.connect(self.createTask)
        
    def createTask(self):
        ...