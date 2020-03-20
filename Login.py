import sys
# import Signup
import sqlite3
import SentimentAnalysis
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton, QDialog, QLineEdit, QGridLayout, QLabel

database = sqlite3.connect("database.sqlite3")
database.execute('''CREATE TABLE IF NOT EXISTS "record" (
                "username"	TEXT NOT NULL UNIQUE,
                "name"	TEXT NOT NULL,
                "email"	TEXT NOT NULL UNIQUE,
                "pwd"	TEXT NOT NULL,
                "customerkey"	TEXT NOT NULL,
                "customersecret"	TEXT NOT NULL,
                "accesstoken"	TEXT NOT NULL,
                "accesstokensecret"	TEXT NOT NULL)
                ''')
cursor = database.cursor()


class Login(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        # Creating Grid Layout
        layout = QGridLayout()

        # Window Title
        self.setWindowTitle("Login")

        # Labels
        self.text1 = QLabel()
        self.text2 = QLabel()
        self.text1.setText("Login ID")
        self.text2.setText("Password")

        # Line Edit
        self.loc1 = QLineEdit(self)
        self.loc1.setPlaceholderText("Enter Your Username")

        self.loc2 = QLineEdit(self)
        self.loc2.setPlaceholderText("Enter Your Password")
        self.loc2.setEchoMode(QLineEdit.Password)

        # Push Buttons
        login_button = QPushButton("Login")
        signup_button = QPushButton("Sign Up")
        close_button = QPushButton("Close")

        # Layout
        layout.addWidget(self.text1, 0, 0)
        layout.addWidget(self.text2, 1, 0)
        layout.addWidget(self.loc1, 0, 1)
        layout.addWidget(self.loc2, 1, 1)
        layout.addWidget(signup_button)
        layout.addWidget(login_button, )
        layout.addWidget(close_button, 3, 0, 3, 2)

        self.setLayout(layout)
        self.setFocus()

        # Events and Signals
        login_button.clicked.connect(self.login)
        signup_button.clicked.connect(self.signup)
        close_button.clicked.connect(self.close)

    def login(self):
        try:
            login = (str(self.loc1.text()), str(self.loc2.text()))
            try:
                database = sqlite3.connect("database.sqlite3")
                # cursor = database.cursor()
                data = database.execute('''SELECT username, pwd FROM record where username == "{}" and pwd == "{}"'''.format(login[0], login[1]))
                keys = database.execute('''SELECT customerkey, customersecret, accesstoken, accesstokensecret FROM record where username == "{}" and pwd == "{}"'''.format(login[0], login[1]))
                data2 = []
                data3 = []
                for record in data:
                    # print(record)
                    data2.append(record)
                for key in keys:
                    # print(key)
                    data3.append(key)
                data2 = data2[0]
                extras = data3[0]
                # print("extras", extras)
                if(data2 == login):
                    QMessageBox.information(self, "Success", "Logged in successfully...!!!".format(QMessageBox.warning))
                    dialogl.close()
                    dialogs = SentimentAnalysis.SentimentAnalysis(extras)
                    dialogs.show()
                    dialogs.exec_()
                    dialogs.close()
                    database.close()
                    # cursor.close()
                database.close()
                if(data2 != login):
                    QMessageBox.warning(self, "Error", "Username or Password is incorrect, try again...".format(QMessageBox.warning))
                    database.close()
                # elif (data2 != login):
                #         QMessageBox.warning(self, "Error", "Username or Password is incorrect, try again...".format(QMessageBox.warning))
                #         database.close()
                database.close()
            except:
                QMessageBox.warning(self, "Error", "Username or Password is incorrect, try again...".format(QMessageBox.warning))
        except:
            QMessageBox.information(self, "Error", "Some error has occurred...".format(QMessageBox.warning))

    def signup(self):
        dialogs1 = Signup()
        dialogs1.show()
        dialogs1.exec_()
        dialogs1.close()


class Signup(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        # Creating Grid Layout
        layout = QGridLayout()

        # Window Title
        self.setWindowTitle("Sign Up")

        # Labels
        self.text1 = QLabel()
        self.text2 = QLabel()
        self.text3 = QLabel()
        self.text4 = QLabel()
        self.text5 = QLabel()
        self.text6 = QLabel()
        self.text7 = QLabel()
        self.text8 = QLabel()
        self.text9 = QLabel()
        self.text1.setText("Username")
        self.text2.setText("Name")
        self.text3.setText("e-Mail")
        self.text4.setText("Password")
        self.text5.setText("Confirm Password")
        self.text6.setText("Customer Key")
        self.text7.setText("Customer Secret")
        self.text8.setText("Access Token")
        self.text9.setText("Access Token Secret")

        self.loc1 = QLineEdit(self)
        self.loc1.setPlaceholderText("Enter Your username")

        self.loc2 = QLineEdit(self)
        self.loc2.setPlaceholderText("Enter Your Name")

        self.loc3 = QLineEdit(self)
        self.loc3.setPlaceholderText("Enter Your e-Mail")

        self.loc4 = QLineEdit(self)
        self.loc4.setPlaceholderText("Enter Your Password")
        self.loc4.setEchoMode(QLineEdit.Password)

        self.loc5 = QLineEdit(self)
        self.loc5.setPlaceholderText("Confirm Your Password")
        self.loc5.setEchoMode(QLineEdit.Password)

        self.loc6 = QLineEdit(self)
        self.loc6.setPlaceholderText("Enter Your Customer Key")

        self.loc7 = QLineEdit(self)
        self.loc7.setPlaceholderText("Enter Your Customer Secret")

        self.loc8 = QLineEdit(self)
        self.loc8.setPlaceholderText("Enter Your Access Token")

        self.loc9 = QLineEdit(self)
        self.loc9.setPlaceholderText("Enter Your Access Token Secret")

        # Push Buttons
        signup_button = QPushButton("Sign Up")
        close_button = QPushButton("Close")

        # Layout
        layout.addWidget(self.text1, 0, 0)
        layout.addWidget(self.text2, 1, 0)
        layout.addWidget(self.text3, 2, 0)
        layout.addWidget(self.text4, 3, 0)
        layout.addWidget(self.text5, 4, 0)
        layout.addWidget(self.text6, 5, 0)
        layout.addWidget(self.text7, 6, 0)
        layout.addWidget(self.text8, 7, 0)
        layout.addWidget(self.text9, 8, 0)
        layout.addWidget(self.loc1, 0, 1)
        layout.addWidget(self.loc2, 1, 1)
        layout.addWidget(self.loc3, 2, 1)
        layout.addWidget(self.loc4, 3, 1)
        layout.addWidget(self.loc5, 4, 1)
        layout.addWidget(self.loc6, 5, 1)
        layout.addWidget(self.loc7, 6, 1)
        layout.addWidget(self.loc8, 7, 1)
        layout.addWidget(self.loc9, 8, 1)
        layout.addWidget(signup_button, 9, 0)
        layout.addWidget(close_button, 9, 1)

        self.setLayout(layout)
        self.setFocus()

        # Events and Signals
        signup_button.clicked.connect(self.signup2)
        close_button.clicked.connect(self.close)

    def signup2(self):
        try:
            username = self.loc1.text()
            name = self.loc2.text()
            email = self.loc3.text()
            pwd1 = self.loc4.text()
            pwd2 = self.loc5.text()
            customerkey = self.loc6.text()
            customersecret = self.loc7.text()
            accesstoken = self.loc8.text()
            accesstokensecret = self.loc9.text()

            # print("username {}, name {}, email {}, pwd1 {}, pwd2 {}, customerkey {}, customersecret {}, accesstoken {}, accesstokensecret {}".format
            #       (username, name, email, pwd1, pwd2, customerkey, customersecret, accesstoken, accesstokensecret))

            if pwd1 == '' or pwd2 == '':
                QMessageBox.information(self, "Password can not be blank", "Password can not be blank...".format(QMessageBox.warning))

            elif pwd1 == pwd2:
                database = sqlite3.connect("database.sqlite3")
                database.execute('''CREATE TABLE IF NOT EXISTS "record" (
                                "username"	TEXT NOT NULL UNIQUE,
                                "name"	TEXT NOT NULL,
                                "email"	TEXT NOT NULL UNIQUE,
                                "pwd"	TEXT NOT NULL,
                                "customerkey"	TEXT NOT NULL,
                                "customersecret"	TEXT NOT NULL,
                                "accesstoken"	TEXT NOT NULL,
                                "accesstokensecret"	TEXT NOT NULL)
                                ''')

                database.execute('''INSERT INTO record(username, name, email, pwd, customerkey, customersecret, accesstoken, accesstokensecret)
                                VALUES (?,?,?,?,?,?,?,?)''',
                                (username, name, email, pwd1, customerkey, customersecret, accesstoken, accesstokensecret))
                database.commit()
                database.close()

                QMessageBox.information(self, "Sign Up Success", "Successfully signed up...".format(QMessageBox.information))

                dialogl.close()
                app.closeAllWindows()

                dialogsa1 = SentimentAnalysis.SentimentAnalysis()
                dialogsa1.show()
                dialogsa1.exec_()
                dialogsa1.close()
            elif pwd1 != pwd2:
                QMessageBox.warning(self, "Password Mismatch Error", "Your Password do not match...".format(QMessageBox.warning))
        except:
            QMessageBox.warning(self, "Error", "Some error 2 has occurred...".format(QMessageBox.warning))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogl = Login()
    dialogl.show()
    # dialogl.close()
    dialogl.exec_()
