import sqlite3

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, \
    QMessageBox, QInputDialog, QFormLayout, QDialog, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit, \
    QDoubleSpinBox, QGridLayout, QHBoxLayout, QDesktopWidget

class MainMenu(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()

        main_layout = QVBoxLayout()

        documents_button = QPushButton("Нормативные документы", self)
        documents_button.clicked.connect(self.show_documents_dialog)
        documents_button.setStyleSheet("font-size: 14px; background-color: White; color: Black;")
        documents_button.setFixedSize(180, 18)
        main_layout.addWidget(documents_button, alignment=Qt.AlignTop | Qt.AlignRight)

        welcome_label = QLabel("Добро пожаловать!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Arial", 20))
        main_layout.addWidget(welcome_label, alignment=Qt.AlignTop)

        logo_label = QLabel(self)
        logo_image = QPixmap("Логотип-2.jpg")
        logo_label.setPixmap(logo_image.scaledToWidth(200))
        main_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        title_label = QLabel("Информационная система<br>по учёту перевозки багажа<br>на самолётах")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24))
        title_label.setWordWrap(True)
        main_layout.addWidget(title_label)

        admin_label = QLabel("Вход в систему под именем")
        admin_label.setAlignment(Qt.AlignCenter)
        admin_label.setFont(QFont("Arial", 16))
        main_layout.addWidget(admin_label)
        admin_button = QPushButton("Администратор")
        admin_button.clicked.connect(self.login_as_admin)
        admin_button.setStyleSheet("font-size: 25px; background-color: #B22222; color: #FFFFFF;")
        admin_button.setFixedSize(250, 50)
        main_layout.addWidget(admin_button, alignment=Qt.AlignCenter)

        user_label = QLabel("Вход в систему под именем")
        user_label.setAlignment(Qt.AlignCenter)
        user_label.setFont(QFont("Arial", 16))
        main_layout.addWidget(user_label)
        user_button = QPushButton("Клиент")
        user_button.clicked.connect(self.show_user_window)
        user_button.setStyleSheet("font-size: 25px; background-color: #B22222	; color: #FFFFFF;")
        user_button.setFixedSize(250, 50)
        main_layout.addWidget(user_button, alignment=Qt.AlignCenter)

        main_layout.setSpacing(10)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.db_connection = db_connection
        self.user_window = UserWindow(self.db_connection)
        self.admin_panel = AdminPanel(self.db_connection)

        self.setStyleSheet("background-color: #CD5C5C;")

    def login_as_admin(self):
        password_input, ok = QInputDialog.getText(None, "Вход как администратор", "Введите пароль:", QLineEdit.Password)
        if not ok:
            return
        entered_password = password_input.strip()
        if entered_password == "8922":
            self.admin_panel.show()
            self.window().hide()
        else:
            QMessageBox.warning(None, "Ошибка", "Неверный пароль")

    def show_user_window(self):
        self.user_window.show()
        self.window().hide()
        pass

    def show_documents_dialog(self):
        documents_dialog = QDialog(self)
        documents_dialog.setWindowTitle("Нормативные документы")
        documents_dialog.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()

        documents_label = QLabel(
            "Нормативные документы:\n"
            "1. Политика конфиденциальности:\n"
            "Приложение собирает, хранит и обрабатывает личные данные пользователей с соблюдением действующего законодательства о защите данных.\n"
            "2. Права и обязанности пользователя:\n"
            "- Пользователь обязуется соблюдать все правила и условия, установленные при использовании приложения.\n"
            "- Пользователь несет ответственность за конфиденциальность своего пароля и аккаунта.\n"
            "3. Условия использования:\n"
            "- Запрещено использование приложения в незаконных или вредоносных целях.\n"
            "- ИС оставляет за собой право временно или постоянно приостановить предоставление услуг при нарушении пользователем соглашения.\n"
            "4. Интеллектуальная собственность:\n"
            "- Все права на контент и интеллектуальную собственность, предоставляемые через приложение, принадлежат ИС.\n"
            "5. Ответственность:\n"
            "- ИС не несет ответственности за убытки или ущерб, вызванные использованием или невозможностью использования приложения.\n"
            "6. Изменения в соглашении:\n"
            "- ИС оставляет за собой право вносить изменения в это соглашение. Изменения вступают в силу с момента их публикации.\n"
            "7. Контактная информация:\n"
            "- По всем вопросам, касающимся пользовательского соглашения, обращайтесь по адресу [Kirill.Porubovvv@yandex.ru].\n"
        )

        layout.addWidget(documents_label)
        documents_dialog.setLayout(layout)

        documents_dialog.exec_()


class AdminPanel(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Панель администратора")
        self.setGeometry(100, 100, 800, 600)
        self.db_connection = db_connection
        self.closeEvent = self.on_close
        grid_layout = QGridLayout()

        buttons = [
            {"text": "Управление базой данных", "handler": self.show_database_management_dialog},
            {"text": "Зарегистрировать багаж клиента", "handler": self.show_baggage_registration_dialog},
            {"text": "Общая статистика", "handler": self.generate_general_statistics_report},
            {"text": "Отчет о багаже", "handler": self.generate_baggage_report}
        ]

        for i, button_info in enumerate(buttons):
            button = QPushButton(button_info["text"])
            button.clicked.connect(button_info["handler"])
            self.style_button(button)
            grid_layout.addWidget(button, i // 2, i % 2, alignment=Qt.AlignCenter)

        self.setStyleSheet("background-color: #CD5C5C;")

        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

    def style_button(self, button):
        button.setStyleSheet("font-size: 25px; background-color: #B22222; color: #FFFFFF;")
        button.setFixedSize(500, 300)

    def show_baggage_registration_dialog(self):
        baggage_registration_dialog = BaggageRegistrationDialog(self.db_connection)
        baggage_registration_dialog.exec_()

    def show_database_management_dialog(self):
        database_management_dialog = DatabaseManagementDialog(self.db_connection)
        database_management_dialog.exec_()

    def generate_general_statistics_report(self):
        users_count = self.get_users_count()
        flights_count = self.get_flights_count()
        baggage_count = self.get_baggage_count()
        report_text = f"Общая статистика:\n\n"
        report_text += f"Количество зарегистрированных клиентов: {users_count}\n"
        report_text += f"Общее количество рейсов: {flights_count}\n"
        report_text += f"Общее количество зарегистрированного багажа: {baggage_count}\n"

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Общая статистика")
        msg_box.setText(report_text)
        msg_box.setStyleSheet("background-color: white;")

        msg_box.exec_()

    def generate_baggage_report(self):
        baggage_report = self.get_baggage_report()

        if hasattr(self, 'report_dialog'):
            self.report_dialog.close()

        self.report_dialog = QDialog(self)
        self.report_dialog.setWindowTitle("Отчет о багаже")

        width = 800
        height = 600
        self.report_dialog.setGeometry(
            QDesktopWidget().screenGeometry().width() // 2 - width // 2,
            QDesktopWidget().screenGeometry().height() // 2 - height // 2,
            width,
            height
        )

        layout = QVBoxLayout()

        if baggage_report:
            self.table = QTableWidget()
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["ID пользователя", "ФИО", "ID рейса", "ID багажа", "Статус багажа"])

            for row, record in enumerate(baggage_report):
                user_id, user_fullname, flight_id, baggage_id, baggage_status = record
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(user_id)))
                self.table.setItem(row, 1, QTableWidgetItem(user_fullname))
                self.table.setItem(row, 2, QTableWidgetItem(str(flight_id)))
                self.table.setItem(row, 3, QTableWidgetItem(str(baggage_id)))
                self.table.setItem(row, 4, QTableWidgetItem(baggage_status))

            layout.addWidget(self.table)

            update_status_button = QPushButton("Изменить статусы багажа")
            update_status_button.clicked.connect(self.show_baggage_status_update_dialog)
            layout.addWidget(update_status_button)
        else:
            no_baggage_label = QLabel("Нет зарегистрированных багажей.")
            layout.addWidget(no_baggage_label)

        self.report_dialog.setLayout(layout)
        self.report_dialog.setStyleSheet("background-color: white;")

        self.report_dialog.exec_()

    def show_baggage_status_update_dialog(self):
        baggage_status_update_dialog = BaggageStatusUpdateDialog(self.db_connection)
        baggage_status_update_dialog.status_updated.connect(self.handle_status_updated)
        baggage_status_update_dialog.exec_()

    def handle_status_updated(self, flight_id, new_status):
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE Багаж SET Статус = ? WHERE Рейс = ?', (new_status, flight_id))
        self.db_connection.commit()
        self.generate_baggage_report()

    def get_users_count(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM Пользователь')
        users_count = cursor.fetchone()[0]
        return users_count

    def get_flights_count(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM Рейс')
        flights_count = cursor.fetchone()[0]
        return flights_count

    def get_baggage_count(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM Багаж')
        baggage_count = cursor.fetchone()[0]
        return baggage_count

    def get_baggage_report(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                'SELECT Пользователь.idПользователя, Пользователь.Фамилия || " " || Пользователь.Имя|| " " || Пользователь.Отчество, '
                'Пользователь.Рейс, Багаж.idБагажа, Багаж.Статус '
                'FROM Багаж '
                'JOIN Пользователь ON Багаж.Владелец = Пользователь.idПользователя'
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def on_close(self, event):
        self.window = MainMenu(db_connection=self.db_connection)
        self.window.setGeometry(100, 100, 1000, 800)
        self.window.show()


class UserWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.setStyleSheet("background-color: #CD5C5C;")
        self.setWindowTitle("Клиент")
        self.setGeometry(100, 100, 1000, 800)
        self.db_connection = db_connection
        self.closeEvent = self.on_close
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        client_label = QLabel("Клиент", central_widget)
        client_label.setAlignment(Qt.AlignCenter)
        client_label.setFont(QFont("Arial", 28, QFont.Bold))
        layout.addWidget(client_label)

        logo_label = QLabel(self)
        logo_image = QPixmap("Логотип-2.jpg")
        logo_label.setPixmap(logo_image.scaledToWidth(200))
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        login_label = QLabel("Логин:", central_widget)
        login_label.setAlignment(Qt.AlignCenter)
        login_label.setFont(QFont("Arial", 18))
        layout.addWidget(login_label)

        self.login_input = QLineEdit(central_widget)
        self.login_input.setStyleSheet("background-color: white; font-size: 18px;")
        layout.addWidget(self.login_input)

        self.password_label = QLabel("Пароль:", central_widget)
        self.password_label.setAlignment(Qt.AlignCenter)
        self.password_label.setFont(QFont("Arial", 18))
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(central_widget)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("background-color: white; font-size: 18px;")
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()

        login_button = QPushButton("Вход", central_widget)
        login_button.clicked.connect(self.login)
        login_button.setStyleSheet("font-size: 25px; background-color: #B22222; color: #FFFFFF;")
        login_button.setFixedSize(400, 50)
        button_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        forgot_password_label = QLabel(
            '<a href="http://example.com" style="color: blue; font-size: 20px; ">Забыли пароль</a>',
            central_widget)
        forgot_password_label.setAlignment(Qt.AlignCenter)
        forgot_password_label.linkActivated.connect(self.show_password_recovery_dialog)
        button_layout.addWidget(forgot_password_label, alignment=Qt.AlignCenter)

        layout.addLayout(button_layout)

        registration_button = QPushButton("Регистрация", central_widget)
        registration_button.clicked.connect(self.show_registration_window)
        registration_button.setStyleSheet("font-size: 25px; background-color: #B22222; color: #FFFFFF;")
        registration_button.setFixedSize(400, 50)
        layout.addWidget(registration_button, alignment=Qt.AlignCenter)

        central_widget.setLayout(layout)

    def on_close(self, event):
        self.window = MainMenu(db_connection=self.db_connection)
        self.window.setGeometry(100, 100, 1000, 800)
        self.window.show()

    def show_registration_window(self):
        registration_window = RegistrationWindow(self.db_connection)
        registration_window.exec_()

    def login(self):
        entered_login = self.login_input.text()
        entered_password = self.password_input.text()

        db = Database(self.db_connection)

        try:
            user_id = db.check_user_login(entered_login, entered_password)
            if user_id:
                self.show_user_profile(user_id)
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
        except Exception as e:
            print(f"Error during login: {e}")
            import traceback
            traceback.print_exc()

    def show_user_profile(self, user_id):
        profile_window = UserProfile(user_id, db_connection)
        profile_window.show()
        self.user_profile = profile_window

    def show_password_recovery_dialog(self):
        password_recovery_dialog = PasswordRecoveryDialog(self.db_connection)
        password_recovery_dialog.exec_()


class UserProfile(QWidget):
    def __init__(self, user_id, db_connection):
        super().__init__()

        self.setWindowTitle("Личный кабинет")
        self.setGeometry(100, 100, 800, 600)
        self.user_id = user_id
        self.db_connection = db_connection
        self.setStyleSheet("background-color: #CD5C5C;")

        layout = QVBoxLayout()
        self.load_user_data()
        self.load_user_baggage()
        self.load_user_flights()
        self.setLayout(layout)

    def load_user_data(self):
        query = f"SELECT * FROM Пользователь WHERE idПользователя = {self.user_id};"
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        user_data = cursor.fetchone()

        if user_data:
            user_label = QLabel(
                f"Табельный номер клиента: #{user_data[0]}\n"
                f"Имя: {user_data[2]}\n"
                f"Фамилия: {user_data[3]}\n"
                f"Отчество: {user_data[4]}\n"
                f"Дата рождения: {user_data[5]}\n"
                f"Паспортные данные: {user_data[6]}\n"
                f"Номер телефона: {user_data[7]}\n"
                f"Email: {user_data[8]}")
            user_label.setStyleSheet("color: #FFFACD; font-size: 20px;")

            layout = self.layout() or QVBoxLayout()
            layout.addWidget(user_label)
            self.setLayout(layout)

    def load_user_baggage(self):
        db = Database(self.db_connection)
        baggage = db.get_user_baggage(self.user_id)

        layout = self.layout() or QVBoxLayout()

        if baggage:
            for item in baggage:
                baggage_info_label = QLabel(
                    f"Информация о багаже:\n"
                    f"Регистрационный номер багажа: №{item[0]}\n"
                    f"Вес - {item[3]} кг\n"
                    f"Условия ограничения - {item[4]}\n"
                    f"Описание - {item[5]}\n"
                    f"Статус - {item[6]}\n"
                )
                baggage_info_label.setStyleSheet("color: #FFFACD; font-size: 20px;")
                layout.addWidget(baggage_info_label)

                if item[6] == "Ожидает получения":
                    issue_receipt_button = QPushButton("Выдать чек")
                    issue_receipt_button.clicked.connect(lambda _, baggage_id=item[0]: self.issue_receipt(baggage_id))
                    layout.addWidget(issue_receipt_button)

                    setattr(self, f"issue_receipt_button_{item[0]}", issue_receipt_button)

        else:
            no_baggage_label = QLabel("Нет зарегистрированных багажей")
            no_baggage_label.setStyleSheet("color: #FFFACD; font-size: 20px;")
            layout.addWidget(no_baggage_label)

        self.setLayout(layout)

    def issue_receipt(self, baggage_id):
        QMessageBox.information(self, "Чек выдан", "Чек успешно выдан!")

        issue_receipt_button = getattr(self, f"issue_receipt_button_{baggage_id}", None)
        if issue_receipt_button:
            issue_receipt_button.hide()

        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE Багаж SET Статус=? WHERE idБагажа=?', ("Получен пользователем", baggage_id))
        self.db_connection.commit()

    def show_flight_registration_dialog(self):
        flight_registration_dialog = FlightRegistrationDialog(self.db_connection, self.user_id)
        result = flight_registration_dialog.exec_()
        if result == QDialog.Accepted:
            self.close()
            user_profile = UserProfile(self.user_id, self.db_connection)
            user_profile.show()

    def show_baggage_registration_dialog(self):
        db = Database(self.db_connection)
        current_flight = db.get_user_current_flight(self.user_id)

        if current_flight:
            user_flight_id = current_flight[0]
            baggage_registration_dialog = BaggageRegistrationDialog(self.db_connection, self.user_id, user_flight_id)
            baggage_registration_dialog.exec_()
            self.load_user_baggage()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить текущий рейс пользователя.")

    def load_user_flights(self):
        db = Database(self.db_connection)
        flights = db.get_user_flights(self.user_id)

        layout = self.layout() or QVBoxLayout()

        flight_widgets = [layout.itemAt(i).widget() for i in range(layout.count()) if
                          layout.itemAt(i).widget() and layout.itemAt(i).widget().objectName().startswith(
                              "flight_widget_")]
        for widget in flight_widgets:
            widget.setParent(None)

        if flights:
            for item in flights:
                flight_label = QLabel(
                    f"Информация о зарегистрированном рейсе:\n"
                    f"idРейса - {item[0]}\n"
                    f"Авиакомпания - {item[1]}\n"
                    f"Аэропорт отправления - {item[2]}\n"
                    f"Аэропорт прибытия - {item[3]}\n"
                    f"Дата вылета - {item[4]}\n"
                    f"Время вылета - {item[5]}\n"
                    f"Дата прибытия - {item[6]}\n"
                    f"Дата время - {item[7]}\n"
                )
                flight_label.setStyleSheet(
                    "color: #FFFACD; font-size: 20px;")

                flight_label.setObjectName(f"flight_widget_{item[0]}")

                layout.addWidget(flight_label)

        else:
            no_flight_label = QLabel("У пользователя нет зарегистрированных рейсов")
            no_flight_label.setStyleSheet(
                "color: #FFFACD; font-size: 20px;")

            layout.addWidget(no_flight_label)

            existing_button = layout.findChild(QPushButton, "register_flight_button")
            if not existing_button:
                register_flight_button = QPushButton("Зарегистрироваться на рейс", objectName="register_flight_button")
                register_flight_button.clicked.connect(self.show_flight_registration_dialog)
                layout.addWidget(register_flight_button)

        self.setLayout(layout)


class Database:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def check_user_login(self, login, password):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute('SELECT idПользователя FROM Пользователь WHERE Логин=? AND Пароль=?', (login, password))
            user = cursor.fetchone()
            return user[0] if user else None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_user_baggage(self, user_id):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute('SELECT * FROM Багаж WHERE Владелец=?', (user_id,))
            baggage = cursor.fetchall()
            return baggage
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_user_flights(self, user_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                'SELECT * FROM Рейс WHERE idРейса IN (SELECT Рейс FROM Пользователь WHERE idПользователя = ?)',
                (user_id,))
            flights = cursor.fetchall()
            return flights
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_user_current_flight(self, user_id):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute('SELECT Рейс FROM Пользователь WHERE idПользователя=?', (user_id,))
            current_flight = cursor.fetchone()
            return current_flight
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_departure_locations(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute('SELECT DISTINCT Местоположение FROM Аэропорт')
            departure_locations = cursor.fetchall()
            return [str(location[0]) for location in departure_locations]
        except Exception as e:
            print(f"Error during getting departure locations: {e}")
            return []

    def register_user(self, login, password, name, surname, patronymic, birthdate, passport, phone, email):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                'INSERT INTO Пользователь (Логин, Пароль, Имя, Фамилия, Отчество, ДатаРождения, ПаспортныеДанные, НомерТелефона, Email) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (login, password, name, surname, patronymic, birthdate, passport, phone, email)
            )
            self.db_connection.commit()
            user_id = cursor.lastrowid
            return user_id
        except Exception as e:
            print(f"Error during user registration: {e}")
            return None

    def get_filtered_flights(self, departure_location, arrival_location):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                'SELECT * FROM Рейс WHERE АэропортОтправления = ? AND АэропортПрибытия = ?',
                (departure_location, arrival_location)
            )
            flights = cursor.fetchall()
            return flights
        except Exception as e:
            print(f"Error during getting filtered flights: {e}")
            return []

    def get_airports(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM Аэропорт')
        airports = cursor.fetchall()
        return airports

    def get_arrival_airports(self, departure_location):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                'SELECT * FROM Аэропорт WHERE Местоположение != ?',
                (departure_location,)
            )
            arrival_airports = cursor.fetchall()
            return arrival_airports
        except Exception as e:
            print(f"Error during getting arrival airports: {e}")
            return []

    def get_all_flights(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM Рейс')
        flights = cursor.fetchall()
        return flights

    def register_user_for_flight(self, user_id, flight_id):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute('UPDATE Пользователь SET Рейс=? WHERE idПользователя=?', (flight_id, user_id))
            self.db_connection.commit()
            return True
        except Exception as e:
            print(f"Error during user registration for flight: {e}")
            return False

    def check_recovery_data(self, passport, phone, email):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                'SELECT * FROM Пользователь WHERE ПаспортныеДанные=? AND НомерТелефона=? AND Email=?',
                (passport, phone, email)
            )
            user_data = cursor.fetchone()
            return user_data is not None
        except Exception as e:
            print(f"Error during password recovery check: {e}")
            return False

    def get_login_and_password(self, passport, phone, email):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                'SELECT Логин, Пароль FROM Пользователь WHERE ПаспортныеДанные=? AND НомерТелефона=? AND Email=?',
                (passport, phone, email)
            )
            login, password = cursor.fetchone()
            return login, password
        except Exception as e:
            print(f"Error during getting login and password: {e}")
            return None, None

    def get_filtered_departure_airports(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute('SELECT * FROM Аэропорт')
            departure_airports = cursor.fetchall()
            return departure_airports
        except Exception as e:
            print(f"Error during getting filtered departure airports: {e}")
            return []

    def get_filtered_flights(self, departure_airport_id):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                'SELECT * FROM Рейс WHERE АэропортОтправления = ?',
                (departure_airport_id,)
            )
            flights = cursor.fetchall()
            return flights
        except Exception as e:
            print(f"Error during getting filtered flights: {e}")
            return []

    def get_airport_by_id(self, airport_id):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute('SELECT * FROM Аэропорт WHERE idАэропорта = ?', (airport_id,))
            airport = cursor.fetchone()
            return airport
        except Exception as e:
            print(f"Error during getting airport by id: {e}")
            return None


class FlightRegistrationDialog(QDialog):
    def __init__(self, db_connection, user_id):
        super().__init__()

        self.registered_flight_id = None

        self.setWindowTitle("Регистрация на рейс")
        self.setGeometry(200, 200, 1500, 400)

        self.db_connection = db_connection
        self.user_id = user_id

        layout = QVBoxLayout()

        self.departure_airport_label = QLabel("Аэропорт отправления:")
        self.departure_airport_combobox = QComboBox()
        self.departure_airport_combobox.currentIndexChanged.connect(self.load_flights)
        layout.addWidget(self.departure_airport_label)
        layout.addWidget(self.departure_airport_combobox)

        self.flights_table = QTableWidget()
        self.flights_table.setColumnCount(8)
        self.flights_table.setHorizontalHeaderLabels(
            ["ID Рейса", "Авиакомпания", "Аэропорт отправления", "Аэропорт прибытия", "ДатаВылета", "ВремяОтправления",
             "ДатаПрибытия", "ВремяПрибытия"])
        layout.addWidget(self.flights_table)

        register_button = QPushButton("Зарегистрироваться на рейс")
        register_button.clicked.connect(self.register_user_for_flight)
        layout.addWidget(register_button)

        self.setLayout(layout)

        self.load_departure_airports()

    def load_departure_airports(self):
        db = Database(self.db_connection)
        departure_airports = db.get_filtered_departure_airports()

        for airport in departure_airports:
            departure_airport_id, _, _ = airport[1], airport[2], airport[3]
            airport_data = db.get_airport_by_id(departure_airport_id)
            airport_name, airport_location = airport_data[2], airport_data[3]
            self.departure_airport_combobox.addItem(f"{departure_airport_id}: {airport_name}, {airport_location}",
                                                    userData=departure_airport_id)

    def load_flights(self):
        self.flights_table.clearContents()
        self.flights_table.setRowCount(0)

        selected_departure_airport_id = self.departure_airport_combobox.currentData()

        db = Database(self.db_connection)
        flights = db.get_filtered_flights(selected_departure_airport_id)

        for row, flight in enumerate(flights):
            self.flights_table.insertRow(row)
            for col, value in enumerate(flight):
                if col in [2, 3]:
                    airport_data = db.get_airport_by_id(value)
                    airport_location = f"{airport_data[2]}, {airport_data[3]}"
                    item = QTableWidgetItem(airport_location)
                else:
                    item = QTableWidgetItem(str(value))
                self.flights_table.setItem(row, col, item)

    def register_user_for_flight(self):
        selected_row = self.flights_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите рейс для регистрации")
            return

        selected_flight_id = self.flights_table.item(selected_row, 0).text()

        db = Database(self.db_connection)
        success = db.register_user_for_flight(self.user_id, selected_flight_id)

        if success:
            QMessageBox.information(self, "Успешная регистрация", "Регистрация на рейс прошла успешно!")
            self.registered_flight_id = selected_flight_id
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось зарегистрироваться на рейс")


class BaggageStatusUpdateDialog(QDialog):
    status_updated = pyqtSignal(int, str)

    def __init__(self, db_connection):
        super().__init__()

        self.db_connection = db_connection
        self.setWindowTitle("Обновление статуса багажа")

        layout = QVBoxLayout()

        self.flight_combo = QComboBox(self)
        self.populate_flights()
        layout.addWidget(self.flight_combo)

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Зарегистрирован", "На борту", "Ожидает получения"])
        layout.addWidget(self.status_combo)

        update_status_button = QPushButton("Принять изменения")
        update_status_button.clicked.connect(self.update_status)
        layout.addWidget(update_status_button)

        self.setLayout(layout)

    def populate_flights(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT idРейса FROM Рейс")
        flights = [str(flight[0]) for flight in cursor.fetchall()]
        self.flight_combo.addItems(flights)

    def update_status(self):
        selected_flight_id = int(self.flight_combo.currentText())
        selected_status = self.status_combo.currentText()

        self.status_updated.emit(selected_flight_id, selected_status)

        self.accept()


class DatabaseManagementDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.deleted_rows = []

        self.setWindowTitle("Управление базой данных")
        self.setGeometry(200, 200, 800, 600)

        self.db_connection = db_connection
        self.column_names = []

        layout = QVBoxLayout()

        self.table_combobox = QComboBox()
        layout.addWidget(self.table_combobox)

        self.data_table = QTableWidget()
        layout.addWidget(self.data_table)

        self.new_data_widgets = [QLineEdit() for _ in range(len(self.column_names))]
        for col_index, column_name in enumerate(self.column_names):
            label = QLabel(column_name)
            self.data_table.setHorizontalHeaderItem(col_index, QTableWidgetItem(label.text()))
            self.data_table.setCellWidget(0, col_index, self.new_data_widgets[col_index])

        add_record_button = QPushButton("Добавить запись")
        add_record_button.clicked.connect(self.add_record)
        layout.addWidget(add_record_button)

        apply_changes_button = QPushButton("Принять изменения")
        apply_changes_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_changes_button)

        delete_record_button = QPushButton("Удалить запись")
        delete_record_button.clicked.connect(self.delete_record)
        layout.addWidget(delete_record_button)

        self.setLayout(layout)

        self.load_tables()

    def delete_record(self):
        selected_table = self.table_combobox.currentText()

        selected_row = self.data_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для удаления", QMessageBox.Ok)
            return

        primary_key_value = self.data_table.item(selected_row, 0).text()

        query = f"DELETE FROM {selected_table} WHERE {self.column_names[0]} = ?"

        cursor = self.db_connection.cursor()
        cursor.execute(query, [primary_key_value])

        self.db_connection.commit()

        self.load_table_data()

        QMessageBox.information(self, "Уведомление", "Запись успешно удалена", QMessageBox.Ok)

    def load_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            self.table_combobox.addItem(table[0])

        self.table_combobox.currentIndexChanged.connect(self.load_table_data)

    def load_table_data(self):
        selected_table = self.table_combobox.currentText()

        cursor = self.db_connection.cursor()
        cursor.execute(f'SELECT * FROM {selected_table}')
        data = cursor.fetchall()
        self.column_names = [column[0] for column in cursor.description]

        self.data_table.clear()
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(self.column_names))

        self.data_table.setHorizontalHeaderLabels(self.column_names)

        for row_index, row_data in enumerate(data):
            for col_index, cell_value in enumerate(row_data):
                item = QTableWidgetItem(str(cell_value))
                self.data_table.setItem(row_index, col_index, item)

        for widget in self.new_data_widgets:
            widget.clear()

    def apply_changes(self):
        if not self.column_names:
            print("Column names not loaded. Cannot apply changes.")
            return

        selected_table = self.table_combobox.currentText()

        for row in range(self.data_table.rowCount()):
            values = []
            for col in range(self.data_table.columnCount()):
                item = self.data_table.item(row, col)
                values.append(item.text())

            set_clause = ', '.join([f"{column} = ?" for column in self.column_names])
            query = f"UPDATE {selected_table} SET {set_clause} WHERE {self.column_names[0]} = ?"

            primary_key_value = self.data_table.item(row, 0).text()

            cursor = self.db_connection.cursor()
            cursor.execute(query, values + [primary_key_value])

        self.db_connection.commit()

        self.load_table_data()

        QMessageBox.information(self, "Уведомление", "Изменения успешно приняты", QMessageBox.Ok)

    def add_record(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить запись")
        dialog.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout(dialog)

        input_widgets = []

        for column_name in self.column_names:
            label = QLabel(f"Введите значение для '{column_name}':")
            layout.addWidget(label)

            line_edit = QLineEdit()
            layout.addWidget(line_edit)

            input_widgets.append(line_edit)

        add_button = QPushButton("Добавить запись")
        add_button.clicked.connect(dialog.accept)
        layout.addWidget(add_button)

        if dialog.exec_() == QDialog.Accepted:
            new_data = [widget.text() for widget in input_widgets]

            if any(value == '' for value in new_data):
                QMessageBox.warning(self, "Предупреждение", "Заполните все поля", QMessageBox.Ok)
                return
            selected_table = self.table_combobox.currentText()
            placeholders = ', '.join(['?' for _ in range(len(self.column_names))])
            query = f"INSERT INTO {selected_table} VALUES ({placeholders})"
            cursor = self.db_connection.cursor()
            cursor.execute(query, new_data)
            self.db_connection.commit()
            self.load_table_data()
            QMessageBox.information(self, "Уведомление", "Запись успешно добавлена", QMessageBox.Ok)


class PasswordRecoveryDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Восстановление пароля")
        self.setGeometry(100, 100, 400, 200)
        self.db_connection = db_connection

        layout = QVBoxLayout()

        passport_label = QLabel("Паспорт:")
        layout.addWidget(passport_label)
        self.passport_input = QLineEdit()
        layout.addWidget(self.passport_input)

        phone_label = QLabel("Номер телефона:")
        layout.addWidget(phone_label)
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_input)

        email_label = QLabel("Email:")
        layout.addWidget(email_label)
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        recover_button = QPushButton("Восстановить пароль")
        recover_button.clicked.connect(self.recover_password)
        layout.addWidget(recover_button)

        self.setLayout(layout)

    def recover_password(self):
        entered_passport = self.passport_input.text()
        entered_phone = self.phone_input.text()
        entered_email = self.email_input.text()

        db = Database(self.db_connection)

        try:
            if db.check_recovery_data(entered_passport, entered_phone, entered_email):
                login, password = db.get_login_and_password(entered_passport, entered_phone, entered_email)
                if login and password:
                    QMessageBox.information(self, "Пароль восстановлен", f"Ваш логин: {login}, пароль: {password}")
                else:
                    QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            else:
                QMessageBox.warning(self, "Ошибка", "Данные восстановления не совпадают")
        except Exception as e:
            print(f"Error during password recovery: {e}")
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при восстановлении пароля")


class RegistrationWindow(QDialog):
    def __init__(self, db_connection):
        super().__init__()

        self.setWindowTitle("Регистрация")
        self.setGeometry(200, 200, 400, 400)

        self.db_connection = db_connection

        layout = QFormLayout()

        self.surname_label = QLabel("Фамилия:")
        self.surname_input = QLineEdit()
        layout.addRow(self.surname_label, self.surname_input)

        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        layout.addRow(self.name_label, self.name_input)

        self.patronymic_label = QLabel("Отчество:")
        self.patronymic_input = QLineEdit()
        layout.addRow(self.patronymic_label, self.patronymic_input)

        self.birthdate_label = QLabel("Дата рождения:")
        self.birthdate_input = QLineEdit()
        layout.addRow(self.birthdate_label, self.birthdate_input)

        self.passport_label = QLabel("Паспортные данные:")
        self.passport_input = QLineEdit()
        layout.addRow(self.passport_label, self.passport_input)

        self.phone_label = QLabel("Телефон:")
        self.phone_input = QLineEdit()
        layout.addRow(self.phone_label, self.phone_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addRow(self.email_label, self.email_input)

        self.login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        layout.addRow(self.login_label, self.login_input)

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow(self.password_label, self.password_input)

        self.confirm_password_label = QLabel("Подтвердите пароль:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addRow(self.confirm_password_label, self.confirm_password_input)

        register_button = QPushButton("Зарегистрироваться")
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register_user(self):
        surname = self.surname_input.text()
        name = self.name_input.text()
        patronymic = self.patronymic_input.text()
        birthdate = self.birthdate_input.text()
        passport = self.passport_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        login = self.login_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not all([surname, name, patronymic, birthdate, passport, phone, email, login, password, confirm_password]):
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        if not all([surname.isalpha(), name.isalpha(), patronymic.isalpha()]):
            QMessageBox.warning(self, "Ошибка", "Фамилия, имя и отчество должны содержать только буквы")
            return

        birthdate_parts = birthdate.split('.')
        if len(birthdate_parts) != 3 or not all(part.isdigit() for part in birthdate_parts):
            QMessageBox.warning(self, "Ошибка",
                                "Дата рождения должна быть в формате дд.мм.гггг, и содержать только цифры")
            return

        if not passport.replace(" ", "").isdigit():
            QMessageBox.warning(self, "Ошибка", "Паспортные данные должны содержать только цифры и пробел")
            return

        if not phone.isdigit():
            QMessageBox.warning(self, "Ошибка", "Телефон должен содержать только цифры и символы")
            return

        db = Database(self.db_connection)

        user_id = db.register_user(login, password, name, surname, patronymic, birthdate, passport, phone, email)

        if user_id is not None:
            QMessageBox.information(self, "Успешная регистрация", f"Регистрация прошла успешно! Ваш ID: {user_id}")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось зарегистрироваться")


class BaggageRegistrationDialog(QDialog):
    def __init__(self, db_connection):
        super().__init__()

        self.setWindowTitle("Регистрация багажа")
        self.setGeometry(200, 200, 400, 300)

        self.db_connection = db_connection

        layout = QFormLayout()

        self.user_label = QLabel("Выберите пользователя:")
        self.user_combobox = QComboBox()
        layout.addRow(self.user_label, self.user_combobox)

        self.flight_label = QLabel("Рейс:")
        self.flight_input = QLineEdit()
        layout.addRow(self.flight_label, self.flight_input)

        self.weight_label = QLabel("Вес багажа:")
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setSuffix(" кг")
        self.weight_input.setDecimals(2)
        layout.addRow(self.weight_label, self.weight_input)

        self.limitations_label = QLabel("Условия ограничения:")
        self.limitations_combobox = QComboBox()
        self.limitations_combobox.addItems(["Соблюдены", "Не соблюдены"])
        layout.addRow(self.limitations_label, self.limitations_combobox)

        self.description_label = QLabel("Описание:")
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("(Отсутствует)")
        layout.addRow(self.description_label, self.description_text)

        self.status_label = QLabel("Статус:")
        self.status_input = QLineEdit()
        layout.addRow(self.status_label, self.status_input)

        register_button = QPushButton("Зарегистрировать багаж")
        register_button.clicked.connect(self.register_baggage)
        layout.addWidget(register_button)
        self.setLayout(layout)
        self.load_users()

    def load_users(self):

        cursor = self.db_connection.cursor()
        cursor.execute('SELECT idПользователя, Имя, Фамилия, Рейс FROM Пользователь')
        users = cursor.fetchall()

        for user in users:
            user_info = f"{user[0]}: {user[1]} {user[2]}"
            if user[3]:
                user_info += f" (Рейс: {user[3]})"
            self.user_combobox.addItem(user_info)

    def register_baggage(self):
        user_id = int(self.user_combobox.currentText().split(":")[0])

        weight_str = self.weight_input.text().replace(',', '.').split()[0]
        try:
            weight = float(weight_str)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат веса. Используйте числовой формат, например, '1.23'")
            return

        limitations = self.limitations_combobox.currentText()
        description = self.description_text.toPlainText()
        status = self.status_input.text()
        flight = self.flight_input.text()

        cursor = self.db_connection.cursor()
        cursor.execute(
            'INSERT INTO Багаж (Владелец, Вес, УсловияОграничения, Описание, Статус, Рейс) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, weight, limitations, description, status, flight)
        )
        self.db_connection.commit()

        QMessageBox.information(self, "Успешная регистрация", "Багаж успешно зарегистрирован!")
        self.accept()


if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    window.setWindowTitle("ИС по учёту перевозки багажа на самолётах")
    window.resize(800, 700)
    db_connection = sqlite3.connect("ИС по учёту перевозки багажа на самолётах.db)")
    main_menu = MainMenu(db_connection)

    window.setCentralWidget(main_menu)
    window.show()
    app.exec_()
