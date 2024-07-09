
from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser
import os

from controller import Controller

class QFilters(QtCore.QObject):
    def __init__(self, parent: QtCore.QObject | None = ...) -> None:
        super().__init__(parent)
    
    def eventFilter(self, obj, event):

        if event.type() == event.MouseButtonPress and self.parent().see_accounts_label == obj:
            self.parent().controller.accounts_ui()
        
        if event.type() == event.MouseButtonPress and self.parent().DeveloperLabel == obj:
            webbrowser.open('https://github.com/ALCODERBR')
        
        if event.type() == event.MouseButtonPress and self.parent().IssuesLabel == obj:
            webbrowser.open('https://github.com/ALCODERBR/maturador-de-chips/issues')

        if event.type() == event.MouseButtonPress and self.parent().NumbersLabel == obj:
            if os.path.exists(os.path.join(os.environ['APPDATA'], 'Telegram Desktop')):
                webbrowser.open('tg://resolve?domain=NotzSMSBot&start=6455672508')
            else:
                webbrowser.open('https://t.me/NotzSMSBot?start=6455672508')

        if event.type() == event.MouseButtonPress and self.parent().LicenseLabel == obj:
            webbrowser.open(url="https://github.com/ALCODERBR/maturador-de-chips/blob/main/LICENSE")

        if event.type() == event.MouseButtonPress and self.parent().VersionLabel == obj:
            self.parent().controller.show_version(self.parent())

        if event.type() == event.MouseButtonPress and self.parent().LibsLabel == obj:
            file_path = os.path.join(os.getcwd(), 'libs-open-source.html')
            webbrowser.open('file://' + file_path)

        if event.type() == event.MouseButtonPress and self.parent().startMatutarationLabel == obj:
            self.parent().controller.start_maturation(self.parent())

        return super().eventFilter(obj,event)
    
class Ui_home(QtWidgets.QMainWindow):
    def setupUi(self, controller:Controller):
        self.event_filter = QFilters(self)
        self.controller = controller
        self.setObjectName("MainWindow")
        self.setFixedSize(684, 510)
        self.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.Shutdown = QtWidgets.QCheckBox(self.centralwidget)

        self.Shutdown.setGeometry(QtCore.QRect(10, 30, 171, 31))
        self.Shutdown.setObjectName("Shutdown")

        self.ContinueOnBlock = QtWidgets.QCheckBox(self.centralwidget)
        self.ContinueOnBlock.setGeometry(QtCore.QRect(10, 0, 281, 31))
        self.ContinueOnBlock.setObjectName("ContinueOnBlock")

        self.MinInterval = QtWidgets.QSpinBox(self.centralwidget)
        self.MinInterval.setGeometry(QtCore.QRect(10, 90, 61, 22))
        self.MinInterval.setStyleSheet("background:rgb(255, 255, 255);")
        self.MinInterval.setObjectName("MinInterval")
        self.MinInterval.setMinimum(1)
        self.MaxInterval = QtWidgets.QSpinBox(self.centralwidget)
        self.MaxInterval.setGeometry(QtCore.QRect(120, 90, 61, 22))
        self.MaxInterval.setStyleSheet("background:rgb(255, 255, 255);")
        self.MaxInterval.setObjectName("MaxInterval")
        self.MaxInterval.setMinimum(2)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 281, 20))
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 90, 20, 21))
        self.label_2.setStyleSheet("font: 75 8pt \"MS Shell Dlg 2\";\n""font: 75 11pt \"MS Shell Dlg 2\";\n""")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(190, 90, 81, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 240, 211, 20))
        self.label_4.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_4.setObjectName("label_4")

        self.MessageMethod = QtWidgets.QComboBox(self.centralwidget)
        self.MessageMethod.setGeometry(QtCore.QRect(10, 270, 211, 21))
        self.MessageMethod.setStyleSheet("background:rgb(255, 255, 255);")
        self.MessageMethod.setObjectName("MessageMethod")
        self.MessageMethod.addItem("")
        self.MessageMethod.addItem("")
        self.MessageMethod.addItem("")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 350, 201, 20))
        self.label_5.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_5.setObjectName("label_5")

        self.token = QtWidgets.QLineEdit(self.centralwidget)
        self.token.setEnabled(False)
        self.token.setGeometry(QtCore.QRect(10, 370, 191, 20))
        self.token.setStyleSheet("background:rgb(255, 255, 255);")
        self.token.setObjectName("token")

        self.menu_resources = QtWidgets.QTableView(self.centralwidget)
        self.menu_resources.setGeometry(QtCore.QRect(280, 410, 391, 81))
        self.menu_resources.setStyleSheet("background:rgb(26, 26, 26);\n""border-radius:15px;\n""color:rgb(255, 255, 255);")
        self.menu_resources.setObjectName("menu_resources")

        self.DeveloperLabel = QtWidgets.QLabel(self.centralwidget)
        self.DeveloperLabel.setGeometry(QtCore.QRect(300, 420, 121, 21))

        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)

        self.DeveloperLabel.setFont(font)
        self.DeveloperLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.DeveloperLabel.setStyleSheet("    font-size: 12px;\n""    font-weight: bold;\n""    color:rgb(117, 117, 117);\n""background:rgb(26, 26, 26);")
        self.DeveloperLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.DeveloperLabel.setObjectName("DeveloperLabel")
        
        self.VersionLabel = QtWidgets.QLabel(self.centralwidget)
        self.VersionLabel.setGeometry(QtCore.QRect(320, 440, 51, 41))
        
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)

        self.VersionLabel.setFont(font)
        self.VersionLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.VersionLabel.setStyleSheet("    font-size: 12px;\n""    font-weight: bold;\n""    color:rgb(117, 117, 117);\n""\n""background:rgb(26, 26, 26);")
        self.VersionLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.VersionLabel.setObjectName("VersionLabel")
        self.LicenseLabel = QtWidgets.QLabel(self.centralwidget)
        self.LicenseLabel.setGeometry(QtCore.QRect(380, 450, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.LicenseLabel.setFont(font)
        self.LicenseLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.LicenseLabel.setStyleSheet("    font-size: 12px;\n""    font-weight: bold;\n""    color:rgb(117, 117, 117);\n""background:rgb(26, 26, 26);")
        self.LicenseLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.LicenseLabel.setObjectName("LicenseLabel")
        
        self.IssuesLabel = QtWidgets.QLabel(self.centralwidget)
        self.IssuesLabel.setGeometry(QtCore.QRect(410, 420, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.IssuesLabel.setFont(font)
        self.IssuesLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.IssuesLabel.setStyleSheet("    font-size: 12px;\n""    font-weight: bold;\n""    color:rgb(117, 117, 117);\n""background:rgb(26, 26, 26);")
        self.IssuesLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.IssuesLabel.setObjectName("IssuesLabel")
        
        self.NumbersLabel = QtWidgets.QLabel(self.centralwidget)
        self.NumbersLabel.setGeometry(QtCore.QRect(540, 420, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.NumbersLabel.setFont(font)
        self.NumbersLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NumbersLabel.setStyleSheet("    font-size: 12px;\n""      color:rgb(117, 117, 117);\n""background:rgb(26, 26, 26);")
        self.NumbersLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.NumbersLabel.setObjectName("NumbersLabel")
        
        self.LibsLabel = QtWidgets.QLabel(self.centralwidget)
        self.LibsLabel.setGeometry(QtCore.QRect(450, 440, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.LibsLabel.setFont(font)
        self.LibsLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.LibsLabel.setStyleSheet("    font-size: 12px;\n""    font-weight: bold;\n""    color:rgb(117, 117, 117);\n""background:rgb(26, 26, 26);")
        self.LibsLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.LibsLabel.setObjectName("LibsLabel")
       
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 300, 211, 20))
        self.label_6.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_6.setObjectName("label_6")
        
        self.file_path = QtWidgets.QLineEdit(self.centralwidget)
        self.file_path.setEnabled(False)
        self.file_path.setGeometry(QtCore.QRect(10, 320, 151, 20))
        self.file_path.setStyleSheet("background:rgb(255, 255, 255);")
        self.file_path.setObjectName("file_path")

        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setEnabled(False)
        self.toolButton.setGeometry(QtCore.QRect(160, 320, 41, 21))
        self.toolButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toolButton.setAcceptDrops(True)
        self.toolButton.setStyleSheet("background:rgb(108, 108, 108);\n""color:rgb(255, 255, 255);")
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButton.setObjectName("toolButton")

        self.tableView_2 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_2.setGeometry(QtCore.QRect(10, 410, 261, 81))
        self.tableView_2.setStyleSheet("background:rgb(26, 26, 26);\n""border-radius:15px;")
        self.tableView_2.setObjectName("tableView_2")
        self.see_accounts_label = QtWidgets.QLabel(self.centralwidget)
        self.see_accounts_label.setGeometry(QtCore.QRect(45, 420, 91, 61))
        
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)

        self.see_accounts_label.setFont(font)
        self.see_accounts_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.see_accounts_label.setStyleSheet("    font-size: 12px;\n""    font-weight: bold;\n""    color:rgb(117, 117, 117);\n""background:rgb(26, 26, 26);")
        self.see_accounts_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.see_accounts_label.setObjectName("see_accounts_label")
        
        self.startMatutarationLabel = QtWidgets.QLabel(self.centralwidget)
        self.startMatutarationLabel.setGeometry(QtCore.QRect(170, 420, 81, 61))
        
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)

        self.startMatutarationLabel.setFont(font)
        self.startMatutarationLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startMatutarationLabel.setStyleSheet("    font-size: 12px;\n""    font-weight: bold;\n""    color:rgb(117, 117, 117);\n""background:rgb(26, 26, 26);")
        self.startMatutarationLabel.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.startMatutarationLabel.setObjectName("startMatutarationLabel")
        
        self.ChangeAfterMessages = QtWidgets.QSpinBox(self.centralwidget)
        self.ChangeAfterMessages.setGeometry(QtCore.QRect(10, 150, 91, 22))
        self.ChangeAfterMessages.setStyleSheet("background:rgb(255, 255, 255);")
        self.ChangeAfterMessages.setObjectName("ChangeAfterMessages")
       
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 120, 281, 20))
        self.label_7.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_7.setObjectName("label_7")
        
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(110, 150, 81, 20))
        self.label_8.setObjectName("label_8")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(300, 20, 361, 371))
        self.tableWidget.setStyleSheet("background:rgb(26, 26, 26);\n""border-radius:15px;")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.setColumnWidth(0, 230)
        self.tableWidget.setColumnWidth(1, 135)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 180, 281, 20))
        self.label_9.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_9.setObjectName("label_9")

        self.MaxMessages = QtWidgets.QSpinBox(self.centralwidget)
        self.MaxMessages.setGeometry(QtCore.QRect(10, 210, 91, 22))
        self.MaxMessages.setStyleSheet("background:rgb(255, 255, 255);")
        self.MaxMessages.setObjectName("MaxMessages_2")
        
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(120, 210, 81, 20))
        self.label_10.setObjectName("label_10")
        
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Shutdown.setText(_translate("MainWindow", "Desligar maquina após termino"))
        self.ContinueOnBlock.setText(_translate("MainWindow", "Ignorar contas bloqueadas e continuar maturação "))
        self.label.setText(_translate("MainWindow", "Aguardar esse intervalo entre uma mensagem e outra:"))

        self.label_2.setText(_translate("MainWindow", "á"))
        self.label_3.setText(_translate("MainWindow", "segundos"))
        self.label_4.setText(_translate("MainWindow", "Usar essa fonte para criar mensagens:"))

        self.MessageMethod.setItemText(0, _translate("MainWindow", "Arquivo de mensagem "))
        self.MessageMethod.setItemText(1, _translate("MainWindow", "ChatGpt (official)"))
        self.MessageMethod.setItemText(2, _translate("MainWindow", "Lorem Ipsum API"))

        self.label_5.setText(_translate("MainWindow", "chave da API:"))

        self.DeveloperLabel.setText(_translate("MainWindow", "Desenvolvedor"))
        self.VersionLabel.setText(_translate("MainWindow", "Versão"))
        self.LicenseLabel.setText(_translate("MainWindow", "Licença"))
        self.IssuesLabel.setText(_translate("MainWindow", "Relatar problema "))
        self.NumbersLabel.setText(_translate("MainWindow", "Numero virtual "))
        self.LibsLabel.setText(_translate("MainWindow", "Bibliotecas de codigo aberto"))
        self.label_6.setText(_translate("MainWindow", "Arquivo de mensagens :"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.see_accounts_label.setText(_translate("MainWindow", "   Contas\n""conectadas "))
        self.startMatutarationLabel.setText(_translate("MainWindow", "   Iniciar\n""Maturador"))
        self.label_7.setText(_translate("MainWindow", "Trocar de conta após o envio de:"))
        self.label_8.setText(_translate("MainWindow", "mensagens "))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Instância "))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Telefone "))

        self.label_9.setText(_translate("MainWindow", "Parar após atingir esse numero de mensagens  :"))
        self.label_10.setText(_translate("MainWindow", "mensagens "))

        for phone_number in self.controller.home_display_connected_phones_numbers:
            session_id = self.controller.home_display_connected_phones_numbers[phone_number]
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

            item = QtWidgets.QTableWidgetItem(session_id)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            item.setForeground(QtGui.QBrush(QtGui.QColor("white")))
            font = QtGui.QFont("Arial Black", 7)
            item.setFont(font)

            self.tableWidget.setItem(row_position, 0, item)
            item = QtWidgets.QTableWidgetItem(phone_number)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            item.setForeground(QtGui.QBrush(QtGui.QColor("white")))
            font = QtGui.QFont("Arial Black", 7)
            item.setFont(font)
            self.tableWidget.setItem(row_position, 1, item)

        self.DeveloperLabel.installEventFilter(self.event_filter)
        self.see_accounts_label.installEventFilter(self.event_filter)
        self.IssuesLabel.installEventFilter(self.event_filter)
        self.LibsLabel.installEventFilter(self.event_filter)
        self.VersionLabel.installEventFilter(self.event_filter)
        self.NumbersLabel.installEventFilter(self.event_filter)
        self.LicenseLabel.installEventFilter(self.event_filter)
        self.startMatutarationLabel.installEventFilter(self.event_filter)

        self.MinInterval.setValue(
            self.controller.get_preference('MinInterval', 67, int)
        )
        self.MinInterval.valueChanged.connect(
            lambda status:  self.controller.set_preference('MinInterval', status)
        )

        self.MaxInterval.setValue(
            self.controller.get_preference('MaxInterval', 90, int)
        )
        self.MaxInterval.valueChanged.connect(
            lambda status:  self.controller.set_preference('MaxInterval', status)
        )
        
        self.Shutdown.setChecked(
            self.controller.get_preference('Shutdown', False, bool)
        )
        self.Shutdown.stateChanged.connect(
            lambda status:  self.controller.set_preference('shutdown', not status == 0)
        )

        self.ContinueOnBlock.setChecked(
            self.controller.get_preference('ContinueOnBlock', False, bool) 
        )
        self.ContinueOnBlock.stateChanged.connect(
            lambda status:  self.controller.set_preference('ContinueOnBlock', not status == 0)
        )

        self.ChangeAfterMessages.setValue(
            self.controller.get_preference('ChangeAfterMessages', 3, int)
        )

        self.ChangeAfterMessages.valueChanged.connect(
            lambda status : self.controller.set_preference('ChangeAfterMessages', status)
        )
        self.MaxMessages.setValue(
            self.controller.get_preference('MaxMessages', 10, int)
        )
        self.MaxMessages.valueChanged.connect(
            lambda status : self.controller.set_preference('MaxMessages', status)
        )

        self.ChangeAfterMessages.setMinimum(1)
        self.MaxMessages.setMinimum(1)

        self.MessageMethod.currentIndexChanged.connect(
            lambda status : self.message_method_event(status))
        
        self.token.textChanged.connect(
            lambda text: self.token_change_event(text)
        
        )

        self.MessageMethod.setCurrentIndex(
            self.controller.get_preference('MessageMethod', 0, int) 
        )

        self.message_method_event( self.controller.get_preference('MessageMethod', 0, int))
        self.toolButton.clicked.connect(lambda x: self.select_message_file())

    def message_method_event(self, index:int):
        self.controller.set_preference('MessageMethod', index)
        if index == 0:
            self.toolButton.setEnabled(True)
            self.file_path.setText(self.controller.get_preference('file_path', ''))
            self.token.setEnabled(False)
            return
        
        if index == 1:
            self.token.setText(self.controller.get_preference('token', ''))
            self.toolButton.setEnabled(False)
            self.token.setEnabled(True)
            return
        
        self.toolButton.setEnabled(False)
        self.token.setEnabled(False)

    def token_change_event(self, text:str):
        return self.controller.set_preference('token', text)
    
    def select_message_file(self):
        path = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Selecione um arquivo para mensagens ',
            filter='Arquivo de texto (*.txt);;'
        )

        if path:
            self.controller.set_preference('file_path', path[0])
            self.file_path.setText(path[0])

    def closeEvent(self, event:QtCore.QEvent):
        self.controller.umount_webviews()
        self.controller.destroy_ui('accounts')
        event.accept()