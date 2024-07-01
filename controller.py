from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets, QtGui
import json

import shutil
import os

import webbrowser
import requests

class Controller(QtCore.QObject):
    def __init__(self, VERSION:str) -> None:
        super().__init__()
        self.ICON:QtGui.QIcon
        self.VERSION = VERSION
        self.home_display_connected_phones_numbers = {}
        self.windows = {}
        self.sessions = {}
    
    def accounts_ui(self):
        self.windows['accounts'].setupUi(self)
        self.windows['accounts'].show()
        self.windows['accounts'].activateWindow()
        self.windows['accounts'].setWindowIcon(self.ICON)
        self.windows['accounts'].setWindowTitle("Maturador de chips")

    def start_ui(self):
        self.windows['main'].setupUi()
        self.windows['main'].show()
        self.windows['main'].activateWindow()
        self.windows['main'].setWindowIcon(self.ICON)
        self.windows['main'].setWindowTitle("Maturador de chips")

    def home_ui(self):
        self.windows['home'].setupUi(self)
        self.windows['home'].show()
        self.windows['home'].activateWindow()
        self.windows['home'].setWindowIcon(self.ICON)
        self.windows['home'].setWindowTitle("Maturador de chips")

    def work_ui(self):
        self.windows['work'].setupUi(self)
        self.windows['work'].show()
        self.windows['work'].activateWindow()
        self.windows['work'].setWindowIcon(self.ICON)
        self.windows['work'].setWindowTitle("Maturador de chips")

    def destroy_ui(self, name:str):
        if self.windows.get(name, False):
            win:QtWidgets.QMainWindow = self.windows.get(name)
            win.deleteLater()
            self.windows.pop(name)
    
    # TODO
    def start_maturation(self,  parent:QtWidgets.QWidget):
        accounts_phone_numbers = [self.sessions[x]['phone'] for x in self.sessions if self.sessions[x].get('phone', False) and not self.sessions[x].get('marked_remove', False)]
        accounts_phone_numbers = list(set(accounts_phone_numbers))
        if not accounts_phone_numbers or len(accounts_phone_numbers) < 2:
              return self.show_messagebox(
                   parent,
                   "Maturador de Chips",
                   "A quantidade de contas minima para iniciar maturação não foi atigindo.\nConecte 2 contas ou mais e tente novamente."  
        )
        self.windows['home'].hide()
        self.work_ui()

    def maturation_status_update(self, sender, receiver, message, time):
        row_position = self.windows['work'].table.rowCount()
        self.windows['work'].table.insertRow(row_position)
        self.windows['work'].table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(sender))
        self.table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(receiver))
        self.table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(message))
        self.windows['work'].table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(time))
    
    def show_version(self, parent:QtWidgets.QWidget):
            message_box = QtWidgets.QMessageBox(parent)
            message_box.setStyleSheet("background-color:#fff;")
            try:
                response = requests.get("https://api.github.com/repos/C0D3RBR/maturador-de-chips/releases/latest")
                if response.json()['tag_name'] == self.VERSION:
                    message_box.about(
                        message_box,
                        f'versão do software',
                        f'{self.VERSION} (versão mais recente)'
                    )
                else :
                    message_box.about(
                        message_box,
                        f'versão do software',
                        f'{self.VERSION} (nova atualização {response.json()["tag_name"]} disponível )'
                    )
                    webbrowser.open("https://api.github.com/repos/C0D3RBR/maturador-de-chips/releases/latest")
                                
            except:
                message_box.about(
                    message_box,
                    f'versão do software',
                    f'{self.VERSION} (não foi possível buscar por atualizações)'
                )

    def show_messagebox(self, parent:QtWidgets.QMainWindow, title:str, text:str):
            message_box = QtWidgets.QMessageBox(parent)
            message_box.setStyleSheet("background-color:#fff;")
            message_box.about(
                message_box,
                title,
                text
            )

    def get_preference(self, name:str, default):
            if QtCore.QSettings('_preference').value(name):
                return  QtCore.QSettings('_preference').value(name)
            return self.set_preference(name, default)

    def set_preference(self, name:str, value):
            QtCore.QSettings('_preference').setValue(name, value)
            return value

    def umount_webviews(self):
         for session_id in self.sessions:
            session = self.sessions[session_id]
            if not session.get('marked_remove', False):
                webview:QtWebEngineWidgets.QWebEngineView = session['webview']
                webview.page().deleteLater()
                webview.page().profile().deleteLater()

    def delete_sessions(self):
         for session_id in self.sessions:
            session = self.sessions[session_id]
            if session.get('marked_remove', False):
                shutil.rmtree(os.path.join(
                    os.environ['SESSIONS_PATH'],
                    session['full_session_id']
        ))
    
    def setProgramIcon(self, path):
        self.ICON = QtGui.QIcon(path)

    @QtCore.pyqtSlot(str)
    def new_account(self, account_data:str):
        account_data = json.loads(account_data)
        row_position = self.windows['home'].tableWidget.rowCount()
        self.windows['home'].tableWidget.insertRow(row_position)

        item = QtWidgets.QTableWidgetItem(account_data['session_id'])
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        item.setForeground(QtGui.QBrush(QtGui.QColor("white")))
        font = QtGui.QFont("Arial Black", 7)
        item.setFont(font)

        self.windows['home'].tableWidget.setItem(row_position, 0, item)
        item = QtWidgets.QTableWidgetItem(account_data['phone'])
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        item.setForeground(QtGui.QBrush(QtGui.QColor("white")))
        font = QtGui.QFont("Arial Black", 7)
        item.setFont(font)
        self.windows['home'].tableWidget.setItem(row_position, 1, item)

        self.sessions[account_data['session_id']]['phone'] = account_data['phone']
        self.home_display_connected_phones_numbers.update({
            account_data['phone']:account_data['session_id']
        })