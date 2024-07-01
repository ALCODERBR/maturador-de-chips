from PyQt5 import QtWidgets 
import sys

from controller import Controller
import argparse

import ui
import os

parser = argparse.ArgumentParser(description='aquecedor de chips WhatsApp')
parser.add_argument('-o', '--output-default',action='store_true', help='Usar a saída padrão do terminal')
parser.add_argument('-f', '--output-file', type=str, help='Escolha o arquivo de saída para terminal', default=os.path.join(os.getcwd(), 'logs.log'))
parser.add_argument('-w', '--web-engine-flags', type=str, help='Mais informações em https://doc.qt.io/qt-6/qtwebengine-debugging.html', default='')
parser.add_argument('-s', '--session-path', type=str, help='Caminho onde sessão do WhatsApp está armazenada', default=os.path.join(os.getcwd(), 'WhatsApp'))
args = parser.parse_args()

os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = args.web_engine_flags

if not os.path.exists(args.session_path):
    os.mkdir(args.session_path)

os.environ['SESSIONS_PATH'] = args.session_path

if not args.output_default:
    sys.stdout = open(file=args.output_file, mode='a', encoding='utf8')
    

controller = Controller("1.0.0")

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    controller.setProgramIcon('icons/icon.ico')
    controller.windows.update({
        'accounts': ui.Ui_accounts(),
        'main': ui.Ui_start(controller),
        'home': ui.Ui_home()
    })
    controller.start_ui()
    app.destroyed.connect(lambda _: controller.delete_sessions() )
    app.exec()