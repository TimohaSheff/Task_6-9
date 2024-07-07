import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from library import Grup

class EmployeeApp(QMainWindow):
    def __init__(self):
        """
        Инициализация EmployeeApp и настройка интерфейса и соединений.
        Загружает интерфейс из файла .ui и устанавливает соединения с кноп-ками.
        """
        super().__init__()
        self.win = uic.loadUi("employee.ui", self)
        
        self.gr = Grup()
        self.gr.read_data("text.txt")
        
        self.win.loadTable.clicked.connect(self.btn_load_table)         # Кнопка для загрузки данных в таблицу
        self.win.addButton.clicked.connect(self.btn_append_employee)  # Кнопка для добавления нового сотрудника
        self.win.editButton.clicked.connect(self.btn_edit_employee)    # Кнопка для редактирования существующего сотрудника
        self.win.deleteButton.clicked.connect(self.btn_del_employee)     # Кнопка для удаления сотрудника
        self.win.saveButton.clicked.connect(self.btn_save_data)     # Кнопка для сохранения данных в файл
        
        self.show()

    def btn_load_table(self):
        """
        Загрузка данных из группы сотрудников в виджет таблицы.
        Очищает таблицу и загружает актуальные данные сотрудников.
        """
        self.win.tableWidget.setRowCount(self.gr.count)
        self.win.tableWidget.clearContents()  # Очищаем только содержимое таблицы
        
        row = 0
        for employee in self.gr.A.values():
            for col, value in enumerate(employee.get_employee_for_table()):
                self.win.tableWidget.setItem(row, col, QTableWidgetItem(value))
            row += 1

    def btn_append_employee(self):
        """
        Добавление нового сотрудника в группу и обновление виджета таблицы.
        Получает данные из текстовых полей и добавляет нового сотрудника в группу.
        """
        employee_data = [
            self.win.lineEdit_4.text(), self.win.lineEdit_5.text(), 
            self.win.lineEdit_6.text(), self.win.lineEdit_7.text(), 
            self.win.lineEdit_8.text(), self.win.lineEdit_9.text()
        ]
        
        self.gr.append_employee(employee_data)
        self.win.lineEdit_4.clear()
        self.win.lineEdit_5.clear()
        self.win.lineEdit_6.clear()
        self.win.lineEdit_7.clear()
        self.win.lineEdit_8.clear()
        self.win.lineEdit_9.clear()
        self.win.tableWidget.clearContents()  # Очищаем только содержимое таблицы
        self.btn_load_table()

    def btn_edit_employee(self):
        """
        Редактирование существующего сотрудника в группе и обновление ви-джета таблицы.
        Получает индекс строки и столбца для редактирования, находит со-трудника и обновляет его данные.
        """
        row = int(self.win.lineEdit_2.text() or '1') - 1
        col = int(self.win.lineEdit_3.text() or '1') - 1
        
        if row < self.win.tableWidget.rowCount() and col < self.win.tableWidget.columnCount():
            employee_data = [
                self.win.tableWidget.item(row, 0).text(), self.win.tableWidget.item(row, 1).text(), 
                self.win.tableWidget.item(row, 2).text(), self.win.tableWidget.item(row, 3).text(), 
                self.win.tableWidget.item(row, 4).text(), self.win.tableWidget.item(row, 5).text()
            ]
            
            key = self.gr.find_key_employee(employee_data)
            
            if key != -1:
                self.win.tableWidget.setItem(row, col, QTableWidgetItem(self.win.lineEdit.text()))
                
                updated_data = [
                    self.win.tableWidget.item(row, 0).text(), self.win.tableWidget.item(row, 1).text(), 
                    self.win.tableWidget.item(row, 2).text(), self.win.tableWidget.item(row, 3).text(), 
                    self.win.tableWidget.item(row, 4).text(), self.win.tableWidget.item(row, 5).text()
                ]
                
                self.gr.edit_employee(key, updated_data)

    def btn_del_employee(self):
        """
        Удаление существующего сотрудника из группы и обновление виджета таблицы.
        Получает данные сотрудника из текстовых полей и удаляет его из группы.
        """
        employee_data = [
            self.win.lineEdit_4.text(), self.win.lineEdit_5.text(), 
            self.win.lineEdit_6.text(), self.win.lineEdit_7.text(), 
            self.win.lineEdit_8.text(), self.win.lineEdit_9.text()
        ]
        
        self.gr.del_employee(employee_data)
        self.win.tableWidget.clearContents()  # Очищаем только содержимое таблицы
        self.btn_load_table()

    def btn_save_data(self):
        """
        Сохранение данных из таблицы в текстовый файл.
        """
        with open("text.txt", "w", encoding='utf-8') as file:
            for row in range(self.win.tableWidget.rowCount()):
                row_data = []
                for col in range(self.win.tableWidget.columnCount()):
                    item = self.win.tableWidget.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                file.write("&".join(row_data) + "\n")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Экземпляр приложения PyQt5
    window = EmployeeApp() # Создание и отображение главного окна приложе-ния
    sys.exit(app.exec_())
