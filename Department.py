import mysql.connector
import sys
from mysql.connector import Error
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class AuthorizationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Вхід")
        self.show()

    def init_ui(self):
        self.setFixedSize(400, 400)

        self.label_image = QtWidgets.QLabel(self)
        self.img = QtGui.QPixmap('img.png')
        self.label_image.setPixmap(self.img)
        self.label_image.move(152, 60)
        self.label_image.resize(self.img.width(), self.img.height())

        self.line_login = QtWidgets.QLineEdit(self)
        self.line_login.move(100, 180)
        self.line_login.resize(200, 30)
        self.line_login.setPlaceholderText(" Логін")

        self.line_password = QtWidgets.QLineEdit(self)
        self.line_password.move(100, 220)
        self.line_password.resize(200, 30)
        self.line_password.setPlaceholderText(" Пароль")
        self.line_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login_btn = QtWidgets.QPushButton('Увійти', self)
        self.login_btn.move(150, 260)
        self.login_btn.resize(100, 30)

        self.login_btn.clicked.connect(self.start_btn)

    def start_btn(self):
        user_login = self.line_login.text()
        user_password = self.line_password.text()
        if len(user_password) == 0 or len(user_login) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText('Помилка')
            msg.setInformativeText('Заповніть пусті поля')
            msg.setWindowTitle('Інформація')
            msg.exec_()
        else:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="artemon4uk100",
                    database='University'
                )
                sql = "SELECT * FROM deanery WHERE login = %s"
                val = (user_login,)
                cursor = connection.cursor()
                cursor.execute(sql, val)
                my_result = cursor.fetchall()
                if len(my_result) > 0:
                    if my_result[0][0] == user_login and my_result[0][1] == user_password:
                        self.super_role = 'deanery'
                        self.role()
                        self.close()
                    else:
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Critical)
                        msg.setText('Помилка')
                        msg.setInformativeText('Невірний пароль')
                        msg.setWindowTitle('Інформація')
                        msg.exec_()
                else:
                    sql = "SELECT * FROM HR_department WHERE login = %s"
                    val = (user_login,)
                    cursor = connection.cursor()
                    cursor.execute(sql, val)
                    my_result = cursor.fetchall()
                    if len(my_result) > 0:
                        if my_result[0][0] == user_login and my_result[0][1] == user_password:
                            self.super_role = 'HR_department'
                            self.role()
                            self.close()
                        else:
                            msg = QtWidgets.QMessageBox()
                            msg.setIcon(QtWidgets.QMessageBox.Critical)
                            msg.setText('Помилка')
                            msg.setInformativeText('Невірний пароль')
                            msg.setWindowTitle('Інформація')
                            msg.exec_()
                    else:
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Critical)
                        msg.setText('Помилка')
                        msg.setInformativeText('Логіна немає в базі даних')
                        msg.setWindowTitle('Інформація')
                        msg.exec_()
                if len(my_result) < 0:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setText('Помилка')
                    msg.setInformativeText('Логіна немає в базі даних')
                    msg.setWindowTitle('Інформація')
                    msg.exec_()
            except Error as e:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText('Помилка')
                msg.setInformativeText("Виникла проблема при з'єднанні з сервером: " + str(e))
                msg.setWindowTitle('Інформація')
                msg.exec_()

    def role(self):
        global aa
        aa = self.super_role
        self.win_open = MainWindow()
        self.win_open.show()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Головне меню")
        self.show()

    def init_ui(self):
        self.setFixedSize(1200, 544)
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        self.btn_add = QtWidgets.QPushButton('Додати', self)
        self.btn_delete = QtWidgets.QPushButton('Видалити', self)
        self.btn_other = QtWidgets.QPushButton('Інші відомості', self)
        self.btn_personal_data = QtWidgets.QPushButton('Персональні дані', self)
        self.grid_layout = QtWidgets.QGridLayout()

        self.btn_add.clicked.connect(self.open_add)
        self.btn_delete.clicked.connect(self.open_del)
        self.btn_other.clicked.connect(self.open_all)
        self.btn_personal_data.clicked.connect(self.open_personality)

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="artemon4uk100",
            database='University'
        )
        cursor = connection.cursor()
        sql = "SELECT * from info "
        cursor.execute(sql)
        res = cursor.fetchall()
        data = list(res)
        pib_list, fac_list, department_list, position_list, disciplines_list = [], [], [], [], []
        ii = 0
        while ii < len(data):
            pib_list.append(data[ii][0])
            fac_list.append(data[ii][1])
            department_list.append(data[ii][2])
            position_list.append(data[ii][3])
            disciplines_list.append(data[ii][4])
            ii += 1
        self.setLayout(self.grid_layout)
        central_widget.setLayout(self.grid_layout)
        self.model = QtGui.QStandardItemModel(len(pib_list), 1)
        self.model.setHorizontalHeaderLabels(['ПІБ', 'Факультет', 'Kафедра', 'Посада', 'Дисципліни'])
        for row, pb in enumerate(pib_list):
            for f, fc in enumerate(fac_list):
                for d, dep in enumerate(department_list):
                    for p, pt in enumerate(position_list):
                        for di, dis in enumerate(disciplines_list):
                            item = QtGui.QStandardItem(pb)
                            self.model.setItem(row, 0, item)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                            item_fac = QtGui.QStandardItem(fc)
                            self.model.setItem(f, 1, item_fac)
                            item_fac.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                            item_dep = QtGui.QStandardItem(dep)
                            self.model.setItem(d, 2, item_dep)
                            item_dep.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                            item_pos = QtGui.QStandardItem(pt)
                            self.model.setItem(p, 3, item_pos)
                            item_pos.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                            item_disciplines = QtGui.QStandardItem(dis)
                            self.model.setItem(di, 4, item_disciplines)
                            item_disciplines.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.table = QtWidgets.QTableView()
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.search_field = QtWidgets.QLineEdit()

        self.model_comb = QtGui.QStandardItemModel()
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)

        self.search_field.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.search_field.setPlaceholderText(" Пошук")
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()

        self.table.setModel(self.filter_proxy_model)
        self.grid_layout.addWidget(self.table)

        self.grid_layout.addWidget(self.search_field)
        self.grid_layout.addWidget(self.btn_add)
        self.grid_layout.addWidget(self.btn_delete)
        self.grid_layout.addWidget(self.btn_other)
        self.grid_layout.addWidget(self.btn_personal_data)

    def open_add(self):
        if aa == 'HR_department':
            self.close()
            self.open = AddWindow()
            self.open.setFixedSize(760, 390)
            self.open.show()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText('Помилка')
            msg.setInformativeText('У вас немає прав')
            msg.setWindowTitle('Інформація')
            msg.exec_()

    def open_del(self):
        if aa == 'HR_department':
            self.close()
            self.open = DeleteWindow()
            self.open.setFixedSize(400, 130)
            self.open.show()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText('Помилка')
            msg.setInformativeText('У вас немає прав')
            msg.setWindowTitle('Інформація')
            msg.exec_()

    def open_all(self):
        self.close()
        self.open = OtherWindow()
        self.open.show()

    def open_personality(self):
        self.close()
        self.open = PersonalityWindow()
        self.open.show()

    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()
        self.open = AuthorizationWindow()
        self.open.show()


class AddWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Додавання')
        self.show()

    def init_ui(self):
        self.model = QtGui.QStandardItemModel()

        self.label_pib = QtWidgets.QLabel('ПІБ:', self)
        self.label_pib.move(20, 20)
        self.label_pib.resize(130, 20)

        self.label_dep = QtWidgets.QLabel('Факультет:', self)
        self.label_dep.move(20, 60)
        self.label_dep.resize(130, 20)

        self.label_pos = QtWidgets.QLabel('Посада:', self)
        self.label_pos.move(20, 100)
        self.label_pos.resize(130, 20)

        self.label_degree = QtWidgets.QLabel('Науковий ступінь:', self)
        self.label_degree.move(20, 140)
        self.label_degree.resize(130, 20)

        self.label_dis = QtWidgets.QLabel('Дисципліни:', self)
        self.label_dis.move(20, 180)
        self.label_dis.resize(130, 20)

        self.label_workload = QtWidgets.QLabel('Навантаження:', self)
        self.label_workload.move(20, 220)
        self.label_workload.resize(130, 20)

        self.label_activity = QtWidgets.QLabel('Громадська робота:', self)
        self.label_activity.move(20, 260)
        self.label_activity.resize(130, 20)

        self.label_sum = QtWidgets.QLabel('Сумісництво:', self)
        self.label_sum.move(20, 300)
        self.label_sum.resize(130, 20)

        self.label_fac = QtWidgets.QLabel('Kафедра:', self)
        self.label_fac.move(400, 20)
        self.label_fac.resize(130, 20)

        self.label_date = QtWidgets.QLabel('Дата народження:', self)
        self.label_date.move(400, 60)
        self.label_date.resize(130, 20)

        self.label_address = QtWidgets.QLabel('Адреса проживання:', self)
        self.label_address.move(400, 100)
        self.label_address.resize(140, 20)

        self.label_phone = QtWidgets.QLabel('Hомер телефону:', self)
        self.label_phone.move(400, 140)
        self.label_phone.resize(130, 20)

        self.line_pib = QtWidgets.QLineEdit(self)
        self.line_pib.move(155, 15)
        self.line_pib.resize(210, 30)

        self.fac = QtWidgets.QComboBox(self)
        self.fac.move(150, 55)
        self.fac.resize(220, 30)
        self.fac.setModel(self.model)

        self.department = QtWidgets.QComboBox(self)
        self.department.move(535, 15)
        self.department.resize(220, 30)
        self.department.setModel(self.model)

        data = {'Факультет інформаційних і прикладних технологій': ['Кафедра прикладної математики',
                                                                    'Кафедра комп’ютерних наук та інформаційних технологій',
                                                                    'Кафедра радіофізики та кібербезпеки',
                                                                    'Кафедра інформаційних систем управління',
                                                                    'Кафедра політології та державного управління',
                                                                    'Кафедра журналістики'],
                'Факультет історії та міжнародних відносин': [
                    'Кафедра історії України та спеціальних галузей історичної науки',
                    'Кафедра всесвітньої історії',
                    'Кафедра філософії',
                    'Кафедра міжнародних відносин і зовнішньої політики'],
                'Філологічний факультет': ['Кафедра української мови і культури',
                                           'Кафедра загального та прикладного мовознавства і слов’янської філології',
                                           'Кафедра теорії та історії української і світової літератури',
                                           'Кафедра психології'],
                'Факультет іноземних мов': ['Кафедра теорії і практики перекладу',
                                            'Кафедра англійської філології',
                                            'Кафедра германської філології',
                                            'Кафедра романських мов і світової літератури',
                                            'Кафедра іноземних мов професійного спрямування'],
                'Економічний факультет': ['Кафедра маркетингу',
                                          'Кафедра обліку, аналізу та аудиту',
                                          'Кафедра фінансів та банківської справи',
                                          'Кафедра менеджменту та поведінкової економіки',
                                          'Кафедра підприємництва, корпоративної та просторової економіки',
                                          'Кафедра бізнес-статистики та економічної кібернетики',
                                          'Кафедра міжнародних економічних відносин'],
                'Юридичний факультет': ['Кафедра господарського права',
                                        'Кафедра цивільного права і процесу',
                                        'Кафедра теорії та історії держави і права та адміністративного права',
                                        'Кафедра конституційного, міжнародного і кримінального права'],
                'Факультет хімії, біології і біотехнологій': ['Кафедра біофізичної хімії і нанобіотехнологій',
                                                              'Кафедра біофізики та фізіології',
                                                              'Кафедра ботаніки та екології',
                                                              'Кафедра зоології',
                                                              'Кафедра неорганічної, органічної та аналітичної хімії'
                                                              'Навчально-науковий центр експериментальної хімії',
                                                              'Кафедра педагогіки, фізичної культури та управління освітою']}

        for k, v in data.items():
            s = QtGui.QStandardItem(k)
            self.model.appendRow(s)
            for value in v:
                c = QtGui.QStandardItem(value)
                s.appendRow(c)
        self.fac.currentIndexChanged.connect(self.update)
        self.update(0)

        self.line_pos = QtWidgets.QLineEdit(self)
        self.line_pos.move(155, 95)
        self.line_pos.resize(210, 30)

        self.line_degree = QtWidgets.QLineEdit(self)
        self.line_degree.move(155, 135)
        self.line_degree.resize(210, 30)

        self.line_dis = QtWidgets.QLineEdit(self)
        self.line_dis.move(155, 175)
        self.line_dis.resize(210, 30)

        self.line_workload = QtWidgets.QLineEdit(self)
        self.line_workload.move(155, 215)
        self.line_workload.resize(210, 30)

        self.line_activity = QtWidgets.QLineEdit(self)
        self.line_activity.move(155, 255)
        self.line_activity.resize(210, 30)

        self.line_sum = QtWidgets.QLineEdit(self)
        self.line_sum.move(155, 295)
        self.line_sum.resize(210, 30)

        self.line_date = QtWidgets.QLineEdit(self)
        self.line_date.move(540, 55)
        self.line_date.resize(210, 30)

        self.line_address = QtWidgets.QLineEdit(self)
        self.line_address.move(540, 95)
        self.line_address.resize(210, 30)

        self.line_phone = QtWidgets.QLineEdit(self)
        self.line_phone.move(540, 135)
        self.line_phone.resize(210, 30)
        self.line_phone.setMaxLength(13)

        self.add_btn = QtWidgets.QPushButton('Додати', self)
        self.add_btn.move(325, 340)
        self.add_btn.resize(100, 30)

        self.add_btn.clicked.connect(self.add)

    def update(self, index):
        indicator = self.model.index(index, 0, self.fac.rootModelIndex())
        self.department.setRootModelIndex(indicator)
        self.department.setCurrentIndex(0)

    def add(self):
        pib = self.line_pib.text()
        position = self.line_pos.text()
        degree = self.line_degree.text()
        disciplines = self.line_dis.text()
        workload = self.line_workload.text()
        activity = self.line_activity.text()
        moonlighting = self.line_sum.text()
        depart = self.department.currentText()
        fac = self.fac.currentText()
        date = self.line_date.text()
        address = self.line_address.text()
        phone = self.line_phone.text()

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="artemon4uk100",
            database='University'
        )
        connection.cursor()
        sql = "SELECT * FROM info WHERE phone = %s"
        val = (phone,)
        cursor = connection.cursor()
        cursor.execute(sql, val)
        my_result = cursor.fetchall()
        if len(pib) == 0 or len(position) == 0 or len(degree) == 0 or len(disciplines) == 0 or len(
                workload) == 0 or len(activity) == 0 or \
                len(moonlighting) == 0 or len(depart) == 0 or len(date) == 0 or len(address) == 0 or len(phone) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText('Помилка')
            msg.setInformativeText('Заповніть пусті поля')
            msg.setWindowTitle('Інформація')
            msg.exec_()
        elif len(my_result) > 0:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText('Помилка')
            msg.setInformativeText('Вже додано')
            msg.setWindowTitle('Інформація')
            msg.exec_()
            self.close()
        else:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="artemon4uk100",
                    database='University'
                )
                sql = "INSERT INTO info (pib,faculty,department,position,degree,disciplines,workload,activity," \
                      "moonlighting,date,address,phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                val = (pib, fac, depart, position, degree, disciplines, workload, activity,
                       moonlighting, date, address, phone)

                cursor = connection.cursor()
                cursor.execute(sql, val)
                connection.commit()
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Інформація')
                msg.setInformativeText('Відомості додано')
                msg.setWindowTitle('Інформація')
                msg.exec_()
                self.close()
                self.open = MainWindow()
                self.open.show()
            except Error as e:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText('Помилка')
                msg.setInformativeText('Відомості не додано: ' + str(e))
                msg.setWindowTitle('Інформація')
                msg.exec_()

    def closeEvent(self, event):
        self.open = MainWindow()
        self.open.show()


class DeleteWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Видалення')
        self.show()

    def init_ui(self):
        self.text_del = QtWidgets.QLabel('ПІБ:', self)
        self.text_del.move(15, 40)
        self.text_del.resize(70, 20)

        self.line_del = QtWidgets.QLineEdit(self)
        self.line_del.move(50, 30)
        self.line_del.resize(330, 40)

        self.btn_del = QtWidgets.QPushButton('Видалити', self)
        self.btn_del.move(150, 80)
        self.btn_del.resize(100, 30)

        self.btn_del.clicked.connect(self.delete)

    def delete(self):
        element = self.line_del.text()
        if len(element) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText('Помилка')
            msg.setInformativeText('Заповніть пусте поле')
            msg.setWindowTitle('Інформація')
            msg.exec_()
        else:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="artemon4uk100",
                database='University'
            )
            connection.cursor()
            sql = "SELECT * FROM info WHERE pib = %s"
            val = (element,)
            cursor = connection.cursor()
            cursor.execute(sql, val)
            my_result = cursor.fetchall()

            if len(my_result) > 0:
                sql = "DELETE FROM info WHERE pib = %s"
                val_del = (element,)
                cursor.execute(sql, val_del)
                connection.commit()
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Інформація')
                msg.setInformativeText('Відомості видалено')
                msg.setWindowTitle('Інформація')
                msg.exec_()
                self.close()
                self.open = MainWindow()
                self.open.show()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText('Помилка')
                msg.setInformativeText('Такої особи немає')
                msg.setWindowTitle('Інформація')
                msg.exec_()
                self.close()

    def closeEvent(self, event):
        self.open = MainWindow()
        self.open.show()


class OtherWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Інші відомості")
        self.show()

    def init_ui(self):
        self.setFixedSize(1200, 544)
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QtWidgets.QGridLayout()
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="artemon4uk100",
            database='University'
        )
        cursor = connection.cursor()

        sql = "SELECT * from info "
        cursor.execute(sql)
        res = cursor.fetchall()
        data = list(res)
        pib_list, degree_list, workload_list, activity_list, sum_list = [], [], [], [], []
        ii = 0
        while ii < len(data):
            pib_list.append(data[ii][0])
            degree_list.append(data[ii][4])
            workload_list.append(data[ii][6])
            activity_list.append(data[ii][7])
            sum_list.append(data[ii][8])
            ii += 1

        self.setLayout(self.grid_layout)
        central_widget.setLayout(self.grid_layout)
        self.model = QtGui.QStandardItemModel(len(pib_list), 1)
        self.model.setHorizontalHeaderLabels(['ПІБ', 'Науковий ступінь', 'Навантаження', 'Громадська робота',
                                              'Сумісництво'])
        for row, pb in enumerate(pib_list):
            for d, dg in enumerate(degree_list):
                for w, wl in enumerate(workload_list):
                    for a, at in enumerate(activity_list):
                        for s, sm in enumerate(sum_list):
                            item = QtGui.QStandardItem(pb)
                            self.model.setItem(row, 0, item)
                            item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                            item_degree = QtGui.QStandardItem(dg)
                            self.model.setItem(d, 1, item_degree)
                            item_degree.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                            item_workload = QtGui.QStandardItem(wl)
                            self.model.setItem(w, 2, item_workload)
                            item_workload.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                            item_activity = QtGui.QStandardItem(at)
                            self.model.setItem(a, 3, item_activity)
                            item_activity.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                            item_sum = QtGui.QStandardItem(sm)
                            self.model.setItem(s, 4, item_sum)
                            item_sum.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.table = QtWidgets.QTableView()
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.search_field = QtWidgets.QLineEdit()

        self.model_comb = QtGui.QStandardItemModel()
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)

        self.search_field.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.search_field.setPlaceholderText(" Пошук")
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()

        self.table.setModel(self.filter_proxy_model)
        self.grid_layout.addWidget(self.table)
        self.grid_layout.addWidget(self.search_field)

    def closeEvent(self, event):
        self.open = MainWindow()
        self.open.show()


class PersonalityWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Персональні дані")
        self.show()

    def init_ui(self):
        self.setFixedSize(1200, 544)
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QtWidgets.QGridLayout()
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="artemon4uk100",
            database='University'
        )
        cursor = connection.cursor()

        sql = "SELECT * from info "
        cursor.execute(sql)
        res = cursor.fetchall()
        data = list(res)
        pib_list, date_list, address_list, phone_list = [], [], [], []
        ii = 0
        while ii < len(data):
            pib_list.append(data[ii][0])
            date_list.append(data[ii][9])
            address_list.append(data[ii][10])
            phone_list.append(data[ii][11])
            ii += 1

        self.setLayout(self.grid_layout)
        central_widget.setLayout(self.grid_layout)
        self.model = QtGui.QStandardItemModel(len(pib_list), 1)
        self.model.setHorizontalHeaderLabels(['ПІБ', 'Дата народження', 'Адреса проживання', 'Hомер телефону'])
        for row, pb in enumerate(pib_list):
            for d, dt in enumerate(date_list):
                for a, ds in enumerate(address_list):
                    for p, pn in enumerate(phone_list):
                        item = QtGui.QStandardItem(pb)
                        self.model.setItem(row, 0, item)
                        item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                        item_dat = QtGui.QStandardItem(dt)
                        self.model.setItem(d, 1, item_dat)
                        item_dat.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                        item_ad = QtGui.QStandardItem(ds)
                        self.model.setItem(a, 2, item_ad)
                        item_ad.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                        item_ph = QtGui.QStandardItem(pn)
                        self.model.setItem(p, 3, item_ph)
                        item_ph.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.table = QtWidgets.QTableView()
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.search_field = QtWidgets.QLineEdit()

        self.model_comb = QtGui.QStandardItemModel()
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)

        self.search_field.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.search_field.setPlaceholderText(" Пошук")
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()

        self.table.setModel(self.filter_proxy_model)
        self.grid_layout.addWidget(self.table)
        self.grid_layout.addWidget(self.search_field)

    def closeEvent(self, event):
        self.open = MainWindow()
        self.open.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = AuthorizationWindow()
    sys.exit(app.exec_())
