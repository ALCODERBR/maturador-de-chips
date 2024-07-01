from PyQt5 import QtWidgets, QtCore, QtGui

from controller import Controller

class Ui_work(QtWidgets.QMainWindow):
    def setupUi(self, controller:Controller):
        self.controller = controller
        self.setFixedSize(687, 505)
        self.setStyleSheet("background:rgb(26, 26, 26);")

        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        layout = QtWidgets.QVBoxLayout(centralWidget)

        title = QtWidgets.QLabel('Maturação em andamento')
        title.setStyleSheet("color: #333; font-size: 24px; text-align: center;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['Enviado de', 'Recebido por', 'Mensagem', 'Horário'])
        self.table.horizontalHeader().setStyleSheet("background: #F0C2B8; color: #333444;")
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: #fff; border: 1px solid #ddd;")
        layout.addWidget(self.table)

        self.stopButton = QtWidgets.QPushButton('Parar')
        self.stopButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stopButton.setStyleSheet('''
                QPushButton {
                width:120px;
                background-color: #dc3545;
                color: #fff;
                border: none;
                border-radius: 5px;
                padding: 10px 0;
                font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgb(205, 92, 92);
                }
        ''')
        self.stopButton.clicked.connect(lambda: self.controller.stop_maturation_signal.emit())
        layout.addWidget(self.stopButton, alignment=QtCore.Qt.AlignCenter)

    def closeEvent(self, event:QtCore.QEvent):
        self.controller.umount_webviews()
        event.accept()