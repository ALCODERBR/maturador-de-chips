from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel
import os

from controller import Controller


class Ui_accounts(QtWidgets.QMainWindow):
    def setupUi(self, controller:Controller):
        self.controller = controller
        self.menuBar_actions = [QtWidgets.QAction, QtWidgets.QAction]
        self.setObjectName("MainWindow")
        self.setFixedSize(843, 573)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll.setGeometry(QtCore.QRect(710, 10, 121, 521))
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("scroll")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 119, 519))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scroll.setWidget(self.scrollAreaWidgetContents)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(20, 20, 661, 501))
        self.stackedWidget.setObjectName("stackedWidget")

        self.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 843, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuOp_es = QtWidgets.QMenu(self.menuBar)
        self.menuOp_es.setObjectName("menuOp_es")
        self.menuOp_es.setTitle("Opções")
        self.menuBar.addMenu(self.menuOp_es)
        self.menuBar_actions[0] = QtWidgets.QAction("", self)
        self.menuBar_actions[1] = QtWidgets.QAction("", self)
        [self.menuOp_es.addAction(action) for action in self.menuBar_actions]
        self.setMenuBar(self.menuBar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuBar_actions[0].setText("Criar nova instancia")
        self.menuBar_actions[0].triggered.connect(self.create_new_session)

        self.menuBar_actions[1].setText("Deletar instancia atual")
        self.menuBar_actions[1].setEnabled(False)
        self.menuBar_actions[1].triggered.connect(self.session_delete)

        self.menuOp_es.setTitle(_translate("MainWindow", "opções "))


        self.menuBar_actions[1].setText("Deletar instancia atual")
        current_tab_button_index = None
        
        for index, session_id in enumerate(start=0, iterable=self.controller.sessions):
            session = self.controller.sessions[session_id]
            if not session.get('marked_remove', False):
                self.stackedWidget.addWidget(session['webview'])
                pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
                pushButton.setText(session['id'])
                pushButton.setMinimumHeight(30)
                pushButton.setMaximumHeight(30)
                pushButton.setStyleSheet('''
                    QPushButton {
                        background-color: #6ab8b8;
                        color: white;
                        font-size: 13px;
                        width: 50px;
                        height: 20px;
                        margin-right: 5px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                ''') 
                self.verticalLayout.addWidget(pushButton)
                pushButton.clicked.connect(lambda _,  index=index: self.switch_tab(index) )
                self.controller.sessions[session_id]['pushButton'] = pushButton
                self.menuBar_actions[1].setEnabled(True)

                if not isinstance(current_tab_button_index, int):
                    current_tab_button_index = index            
        
        if isinstance(current_tab_button_index, int):
            self.switch_tab(current_tab_button_index)
        self.verticalLayout.addStretch()

    def switch_tab(self, index):
        buttons = []
        for session_id in self.controller.sessions:
            session = self.controller.sessions[session_id]
            if not session.get('marked_remove', False):
                buttons.append(session['pushButton'])
            else:
                buttons.append(None)

        self.stackedWidget.setCurrentIndex(index)
        for iterator_index, button in enumerate(start=0, iterable=buttons):
            if iterator_index == index:
                button.setStyleSheet('''
                    QPushButton {
                        background-color: #4f6b6b;
                        color: white;
                        font-size: 13px;
                        width: 50px;
                        height: 20px;
                        margin-right: 5px;
                        border-radius: 5px;
                    } '''
            )
        
            elif button:
                button.setStyleSheet('''
                    QPushButton {
                        background-color: #6ab8b8;
                        color: white;
                        font-size: 13px;
                        width: 50px;
                        height: 20px;
                        margin-right: 5px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
            ''') 

    def create_new_session(self):
        while True:
            ask_result = QtWidgets.QInputDialog.getText(
                self,
                'Maturador de chips',
                "Qual o nome você quer definir para essa instância?")
            
            if not ask_result[1]:
                return
        
            elif not ask_result[0] or ask_result[0].isspace():
                QtWidgets.QMessageBox.critical(self, "Maturador de chips","Instâncias devem obrigatoriamente possuir nomes ")
            
            elif len(ask_result[0]) > 15:
                QtWidgets.QMessageBox.critical(self, "Maturador de chips","nomes de instâncias não podem possuir mais que 15 caracteres")
            
            elif os.path.exists(os.path.join("sessions", f"id{ask_result[0]}")):
                QtWidgets.QMessageBox.critical(self, "Maturador de chips", f"{ask_result[0]} já existe, escolha outro.")
            
            else:
                break
        
        full_session_id = "@" + ask_result[0] 
        session_id =  ask_result[0] 
        webview = QtWebEngineWidgets.QWebEngineView(self)
        cache_dir = os.path.join(os.environ['SESSIONS_PATH'], full_session_id)
        profile = QtWebEngineWidgets.QWebEngineProfile('cacheWebviews', webview)
        profile.setCachePath(cache_dir)
        profile.setPersistentStoragePath(cache_dir)
        profile.setDownloadPath(cache_dir)
        profile.setPersistentCookiesPolicy(QtWebEngineWidgets.QWebEngineProfile.AllowPersistentCookies)
        profile.setHttpAcceptLanguage("pt-br")
        profile.setHttpUserAgent(os.environ['user-agent'])
        engine = QtWebEngineWidgets.QWebEnginePage(profile, webview)
        webview.setPage(engine)
        webview.load(QtCore.QUrl('https://web.whatsapp.com/'))
        webview.page().loadFinished.connect(lambda ok, session_id=session_id, index=len( self.controller.sessions) : self.on_webview_load_finished(session_id, index))
        index = self.stackedWidget.addWidget(webview)
        pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        pushButton.setText(session_id)
        pushButton.setMinimumHeight(30)
        pushButton.setMaximumHeight(30)

        pushButton.setStyleSheet('''
                QPushButton {
                    background-color: #6ab8b8;
                    color: white;
                    font-size: 13px;
                    width: 50px;
                    height: 20px;
                    margin-right: 5px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
        ''')
        
        pushButton.clicked.connect(lambda _, session_id=session_id, index=index: self.switch_tab(session_id, index) )
        self.controller.sessions[session_id] = {
            'webview': webview,
            'pushButton': pushButton,
            'index': len( self.controller.sessions),
            'id': session_id,
            'full_session_id': full_session_id

        }
        return self.setupUi(self.controller)

    def session_delete(self):
         for session_id in self.controller.sessions:
            session = self.controller.sessions[session_id]
            if session['webview'] == self.stackedWidget.currentWidget():
                webview:QtWebEngineWidgets.QWebEngineView = session['webview']
                webview.page().deleteLater()
                webview.page().profile().deleteLater()
                session['marked_remove'] = True
                return self.setupUi(self.controller)

    def on_webview_load_finished(self, id, index):
        webview:QtWebEngineWidgets.QWebEngineView = self.controller.sessions[id]['webview']
        channel = QtWebChannel.QWebChannel(webview.page())
        channel.registerObject("controller", self.controller)
        webview.page().setWebChannel(channel)
        webview.page().runJavaScript(open(file="js\qwebchannel.js", mode="r", encoding="utf8").read() )
        webview.page().runJavaScript(open(file="js\login.js", mode="r", encoding="utf8").read().replace("@INSTANCEID", id) )