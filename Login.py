# Form implementation generated from reading ui file 'Login.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(403, 294)
        self.centralwidget = QtWidgets.QWidget(parent=Login)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 371, 221))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setGeometry(QtCore.QRect(30, 40, 61, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 61, 21))
        self.label_2.setObjectName("label_2")
        self.user = QtWidgets.QLineEdit(parent=self.widget)
        self.user.setGeometry(QtCore.QRect(110, 40, 211, 20))
        self.user.setObjectName("user")
        self.btnDangnhap = QtWidgets.QPushButton(parent=self.widget)
        self.btnDangnhap.setGeometry(QtCore.QRect(130, 130, 81, 31))
        self.btnDangnhap.setObjectName("btnDangnhap")
        self.checkBox = QtWidgets.QCheckBox(parent=self.widget)
        self.checkBox.setGeometry(QtCore.QRect(110, 100, 101, 21))
        self.checkBox.setObjectName("checkBox")
        self.pw = QtWidgets.QLineEdit(parent=self.widget)
        self.pw.setGeometry(QtCore.QRect(110, 70, 211, 20))
        self.pw.setObjectName("pw")
        self.tbnDangky = QtWidgets.QPushButton(parent=self.widget)
        self.tbnDangky.setGeometry(QtCore.QRect(230, 130, 81, 31))
        self.tbnDangky.setObjectName("tbnDangky")
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setGeometry(QtCore.QRect(230, 100, 91, 21))
        self.label_3.setObjectName("label_3")
        Login.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Login)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 403, 18))
        self.menubar.setObjectName("menubar")
        Login.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(parent=Login)
        self.statusBar.setObjectName("statusBar")
        Login.setStatusBar(self.statusBar)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Đăng nhập"))
        self.label.setText(_translate("Login", "Tài Khoản:"))
        self.label_2.setText(_translate("Login", "Mật Khẩu:"))
        self.user.setPlaceholderText(_translate("Login", "Nhập tài khoản"))
        self.btnDangnhap.setText(_translate("Login", "Đăng nhập"))
        self.checkBox.setText(_translate("Login", "Nhớ mật khẩu"))
        self.pw.setPlaceholderText(_translate("Login", "Nhập mật khẩu"))
        self.tbnDangky.setText(_translate("Login", "Đăng ký"))
        self.label_3.setText(_translate("Login", "Quên mật khẩu?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QMainWindow()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec())
