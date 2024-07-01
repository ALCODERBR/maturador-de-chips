from plyer import notification
from openai import OpenAI
import requests
import random

from PyQt5 import QtCore, QtWebEngineWidgets
import controller
import datetime
import time
import os

class MessageGenerator:
    def _file(file_content) -> str:
            return True , random.choice(file_content)
    
    def _lorem() -> str:
            return True , requests.get('https://baconipsum.com/api/?type=all-meat-filler&paras=1').json()[0]
    
    def _openAI(api_key) -> str:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-instruct",
            messages=[
                {"role": "system", "content": "OLá eu sou um assistente de conversação."},
                {"role": "user", "content": "Gere uma mensagem ou pergunta em portugues."}
            ],
            temperature=0.33,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return True, completion['choices'][0]['message']['content']
        
    def generate(cls, source_type: int, file_content:list=[], api_key: str = None) -> tuple[bool, str]:
        try:
             match source_type:
                  case 0: return cls._file(file_content)
                  case 1: return cls._openAI(api_key)
                  case _: return cls._lorem()
        
        except Exception as e:
            return False, str(e)

class WhatsApp(QtCore.QThread):
    def __init__(self, controller, message_method:int, file_content:list, api_token:str, accounts_phone_numbers:list) -> None:
        super().__init__()

        self.controller = controller # type: controller.Controller
        self.ContinueOnBlock = self.controller.get_preference('ContinueOnBlock', False) == 'true'
        self.shutdown = self.controller.get_preference('Shutdown', False) == 'true'
        self.ChangeAfterMessages = self.controller.get_preference('ChangeAfterMessages', 3)
        self.MinInterval = self.controller.get_preference('MinInterval', 67)
        self.MaxInterval = self.controller.get_preference('MaxInterval', 90)
        self.MaxMessages = self.controller.get_preference('MaxMessages', 10)
        self.accounts_phone_numbers = accounts_phone_numbers
        self.message_method = message_method
        self.current_sender_session = None
        self.file_content = file_content
        self.current_sender_count = 0
        self.api_token = api_token

    def run(self):
        for x in range(0, self.MaxMessages):

            if not self.current_sender_session or self.current_sender_count == self.ChangeAfterMessages:
                while True:
                    session_id = random.choice(list(self.controller.sessions.keys()))
                    session = self.controller.sessions[session_id]

                    if session.get('phone', False) and not session.get('marked_remove', False) and not session['id'] in self.controller.session_id_of_accounts_blocked :
                        self.current_sender_session = session
                        break
                self.current_sender_count = 0
            
            current_sender_phone_number = self.current_sender_session['phone']
            accounts_phone_numbers_copy = self.accounts_phone_numbers.copy()
            accounts_phone_numbers_copy.remove(current_sender_phone_number)
            receiver_phone_number = random.choice(accounts_phone_numbers_copy)
            message = MessageGenerator.generate(
                MessageGenerator, self.message_method,  self.file_content, self.api_token)
            
            if not message[0]:
                notification.notify(
                    title="Erro ao criar mensagem",
                    message=f"{message[1] if len(message[1]) < 255 else  message[1][:255]}"  ,
                    app_icon="icons/icon.ico")
                continue

            webview = self.current_sender_session['webview']
            script_js = open(file='js/send_message.js', mode='r', encoding='utf8').read()
            webview.page().runJavaScript(
                script_js.replace('@MESSAGE', message[1] ).replace('@PHONE', receiver_phone_number)) 
            time.sleep(9)
            
            if  self.current_sender_session['id'] in self.controller.session_id_of_accounts_blocked:
                self.accounts_phone_numbers.remove(current_sender_phone_number)
                self.current_sender_session = None
                if self.ContinueOnBlock and len(self.accounts_phone_numbers) >= 2 :
                    notification.notify(
                        title="Conta desconectada",
                        message=f"+{current_sender_phone_number} foi bloqueado ou desconectado."  ,
                        app_icon="icons/icon.ico")
                    continue
                
                else:
                    self.controller.show_messagebox_signal.emit(
                            'home',
                            '"Conta desconectada',
                            f"+{current_sender_phone_number} foi bloqueado ou desconectado."
                    )
                    return self.controller.stop_maturation_signal.emit()
            
            self.controller.maturation_status_update(
                sender=current_sender_phone_number,
                receiver=receiver_phone_number,
                message=message[1],
                time=datetime.datetime.now().strftime("%H:%M:%S"))
            
            
            self.current_sender_count += 1
            interval = random.randint(self.MinInterval, self.MaxInterval)
            time.sleep(interval)


        if self.shutdown:
            os.system("shutdown /s /t 30")

        self.controller.show_messagebox_signal.emit(
            'home',
            "Maturador de chips",
            "maturação dos chips concluída com sucesso!")
        return self.controller.stop_maturation_signal.emit()