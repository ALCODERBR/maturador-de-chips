from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel
from controller import Controller
import requests
import os

class UiThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    load_finished = QtCore.pyqtSignal(int, str, int, float)

    def __init__(self, parent=None):
        self.parent1 = parent
        super().__init__(parent)

    def run(self):
        full_sessions_id = [i for i in os.listdir(os.environ['SESSIONS_PATH']) if i.startswith('@')]
        if not full_sessions_id:
            self.progress.emit(100)
            self.load_finished.emit(0, "", 0, 0)
            return

        progress_bar_increment = (100 - self.parent1.progressBar.value()) / len(full_sessions_id)

        for index, full_session_id in enumerate(full_sessions_id, start=1):
            self.load_finished.emit(index, full_session_id, len(full_sessions_id), progress_bar_increment)

class Ui_start(QtWidgets.QMainWindow):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller

    def setupUi(self):
        self.setObjectName("Ui_start")
        self.setFixedSize(460, 200)
        self.setStyleSheet("background:rgb(26, 26, 26);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(70, 70, 351, 23))
        self.progressBar.setStyleSheet("color:#fff;")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.description = QtWidgets.QLabel(self.centralwidget)
        self.description.setGeometry(QtCore.QRect(170, 120, 141, 16))
        self.description.setStyleSheet("color:#fff;")
        self.description.setObjectName("description")
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.worker = UiThread(self)
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.load_finished.connect(self.create_webview)
        self.worker.start()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Ui_start", "Maturador de chips"))
        self.description.setText(_translate("Ui_start", "carregando configurações ..."))
        
        try:
            requests.get(url='https://example.com')
        except:
            self.controller.show_messagebox(
                self,
                "Maturador de chips",
                'Você não está conectado á internet'
            )
            quit()
        self.progressBar.setProperty("value", 5)

    def update_progress_bar(self, value):
        self.progressBar.setProperty("value", value)

    def create_webview(self, index, full_session_id, total_sessions, progress_bar_increment):
        if full_session_id:
            session_id = full_session_id.replace('@','')
            webview = QtWebEngineWidgets.QWebEngineView(self.controller.windows['accounts'])
            cache_dir = os.path.join(os.environ['SESSIONS_PATH'], full_session_id)
            profile = QtWebEngineWidgets.QWebEngineProfile('cacheWebviews', webview)
            profile.setCachePath(cache_dir)
            profile.setPersistentStoragePath(cache_dir)
            profile.setDownloadPath(cache_dir)
            profile.setPersistentCookiesPolicy(QtWebEngineWidgets.QWebEngineProfile.AllowPersistentCookies)
            profile.setHttpAcceptLanguage("pt-br")
            engine = QtWebEngineWidgets.QWebEnginePage(profile, webview)
            engine.setAudioMuted(True)
            profile.setHttpUserAgent(os.environ['user-agent'])
            webview.setPage(engine)
            webview.load(QtCore.QUrl('https://web.whatsapp.com/'))
            webview.page().loadFinished.connect(lambda ok, index=index, id=session_id, t_sessions=total_sessions: 
                self.on_webview_load_finished(ok, index, id, t_sessions, progress_bar_increment))
            
            self.controller.sessions[session_id] = {
                'id': session_id,
                'index': index,
                'webview': webview,
                'full_session_id': full_session_id
            }
        else:
            self.progressBar.setProperty('value', 100)
            self.controller.destroy_ui('main')
            self.controller.home_ui()
        self.loaded_sessions = 0

    def on_webview_load_finished(self, ok, index, id, t_sessions, progress_bar_increment):
        webview:QtWebEngineWidgets.QWebEngineView = self.controller.sessions[id]['webview']
        channel = QtWebChannel.QWebChannel(webview.page())
        channel.registerObject("controller", self.controller)
        webview.page().setWebChannel(channel)
        webview.page().runJavaScript(open(file="js\qwebchannel.js", mode="r", encoding="utf8").read() )
        webview.page().runJavaScript(open(file="js\login.js", mode="r", encoding="utf8").read().replace("@INSTANCEID", id) )        
        current_value = self.progressBar.value()
        self.loaded_sessions +=1
        self.progressBar.setProperty('value', int(current_value) + int(progress_bar_increment))
        if t_sessions == self.loaded_sessions :
            self.controller.destroy_ui('main')
            self.controller.home_ui()