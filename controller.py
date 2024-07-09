from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets, QtGui
from whatsapp import WhatsApp
import json

import shutil
import os

import webbrowser
import requests

class Controller(QtCore.QObject):
    show_messagebox_signal = QtCore.pyqtSignal(str, str, str)
    stop_maturation_signal =  QtCore.pyqtSignal()

    def __init__(self, VERSION:str) -> None:
        super().__init__()
        self.stop_maturation_signal.connect(lambda: self.stop_maturation() )
        self.show_messagebox_signal.connect(lambda win_id, title, text:
                self.show_messagebox(self.windows[win_id], title, text) )
        self.home_display_connected_phones_numbers = {}
        self.session_id_of_accounts_blocked = []
        self.whatssap_work:WhatsApp = None
        self.VERSION = VERSION
        self.ICON:QtGui.QIcon
        self.sessions = {}
        self.windows = {}
    
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
                   "A quantidade de contas minima para iniciar maturação não foi atigindo.\nConecte 2 contas ou mais e tente iniciar novamente."  
        )

        message_method = self.get_preference("MessageMethod", 0, int)
        file_path = self.get_preference("file_path", '')
        api_token = self.get_preference('token', '')

        if (message_method == 0 and (not file_path or not os.path.exists(file_path) or not open(file=file_path, mode='r', encoding='utf8').readlines() )) :
            return self.show_messagebox(
                    parent,
                    "Maturador de Chips",
                    "Arquivo para entrada de mensagens não foi selecionado ou está vazio."  
            )

        elif message_method == 1 and not api_token :
            return self.show_messagebox(
                    parent,
                    "Maturador de Chips",
                    "Token de autenticação para api.openai.com está vazio."  
        )

        if self.get_preference('MinInterval', 67, int) >= self.get_preference('MaxInterval', 90, int):
            MinInterval = self.get_preference('MinInterval', 67, int)
            MaxInterval = self.get_preference('MaxInterval', 90, int)
            return self.show_messagebox(
                    parent,
                    "Maturador de Chips",
                    f"Intervalo entre ações escolhido não é valido ({MinInterval} á {MaxInterval})"  
        )

        file_content = open(file=file_path, mode='r', encoding='utf8').readlines() if message_method == 0 else []
        self.whatssap_work = WhatsApp(self, message_method, file_content, api_token, accounts_phone_numbers)
        self.work_ui()
        self.whatssap_work.start()
        self.windows['home'].hide()

    def maturation_status_update(self, sender, receiver, message, time):
        row_position = self.windows['work'].table.rowCount()
        self.windows['work'].table.insertRow(row_position)
        self.windows['work'].table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(sender))
        self.windows['work'].table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(receiver))
        self.windows['work'].table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(message))
        self.windows['work'].table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(time))

    def stop_maturation(self):
        self.windows['work'].hide()
        self.whatssap_work.terminate()
        self.home_ui()
    
    def show_version(self, parent:QtWidgets.QWidget):
            message_box = QtWidgets.QMessageBox(parent)
            message_box.setStyleSheet("background-color:#fff;")
            try:
                response = requests.get("https://api.github.com/repos/ALCODERBR/maturador-de-chips/releases/latest")
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
                    webbrowser.open("https://api.github.com/repos/ALCODERBR/maturador-de-chips/releases/latest")
                                
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

    def get_preference(self, name:str, default, value_type = str):
            preference_path = os.path.join(os.getcwd() , '_preference' )
            if QtCore.QSettings(preference_path, QtCore.QSettings.IniFormat).value(name, type=value_type):
                return  QtCore.QSettings(preference_path, QtCore.QSettings.IniFormat).value(name, type=value_type)
            return self.set_preference(name, default)

    def set_preference(self, name:str, value):
            preference_path = os.path.join(os.getcwd() , '_preference' )
            QtCore.QSettings(preference_path,  QtCore.QSettings.IniFormat).setValue(name, value)
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

    @QtCore.pyqtSlot(str)
    def account_blocked(self, account_data:str):
        account_data = json.loads(account_data)
        account_data['phone'] =  self.sessions[account_data['session_id']].pop('phone')
        self.session_id_of_accounts_blocked.append(account_data['session_id'])
        self.home_display_connected_phones_numbers.pop(account_data['phone'])
