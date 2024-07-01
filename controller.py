from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets, QtGui

import shutil
import os

import webbrowser
import requests

class Controller(QtCore.QObject):
    def __init__(self, VERSION:str) -> None:
        super().__init__()
        self.ICON:QtGui.QIcon
        self.VERSION = VERSION
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
        self.windows['home'].show()
        self.windows['home'].activateWindow()
        self.windows['home'].setWindowIcon(self.ICON)
        self.windows['home'].setWindowTitle("Maturador de chips")

    def destroy_ui(self, name:str):
        if self.windows.get(name, False):
            win:QtWidgets.QMainWindow = self.windows.get(name)
            win.deleteLater()
    
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
