# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClientMain.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClientLogin(object):
    def setupUi(self, ClientLogin):
        ClientLogin.setObjectName("ClientLogin")
        ClientLogin.resize(955, 631)
        self.centralwidget = QtWidgets.QWidget(ClientLogin)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(120, 90, 211, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(120, 50, 211, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(570, 50, 221, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(570, 90, 221, 31))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 260, 291, 171))
        self.pushButton.setObjectName("pushButton")
        ClientLogin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ClientLogin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 955, 26))
        self.menubar.setObjectName("menubar")
        ClientLogin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ClientLogin)
        self.statusbar.setObjectName("statusbar")
        ClientLogin.setStatusBar(self.statusbar)

        self.retranslateUi(ClientLogin)
        QtCore.QMetaObject.connectSlotsByName(ClientLogin)

    def retranslateUi(self, ClientLogin):
        _translate = QtCore.QCoreApplication.translate
        ClientLogin.setWindowTitle(_translate("ClientLogin", "MainWindow"))
        self.textEdit.setHtml(_translate("ClientLogin", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">서버 IP를 입력해주세요</p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_2.setHtml(_translate("ClientLogin", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">서버 PORT를 입력해주세요</p>\n"
                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("ClientLogin", "접속하기"))
        self.pushButton.clicked.connect(self.btn_prt)
    
    def btn_prt(self):
        print("zzz")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ClientLogin = QtWidgets.QMainWindow()
    ui = Ui_ClientLogin()
    ui.setupUi(ClientLogin)
    ClientLogin.show()
    sys.exit(app.exec_())
