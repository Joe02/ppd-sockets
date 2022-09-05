import sys
from threading import Thread

from PySide2 import QtWidgets

from game import UI
from server import *


class UserName(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.userNameBox = QtWidgets.QLineEdit()
        self.serverIpBox = QtWidgets.QLineEdit()
        self.serverPortBox = QtWidgets.QLineEdit()

        self.userNameBox.setPlaceholderText("Nome")
        self.serverIpBox.setPlaceholderText("Endereço do server")
        self.serverIpBox.setText(str(socket.gethostbyname(socket.gethostname())))
        self.serverPortBox.setPlaceholderText("Porta do server")
        self.serverPortBox.setText("8080")

        self.joinButton = QtWidgets.QPushButton("Entrar (2º jogador)")
        self.hostButton = QtWidgets.QPushButton("Hostear (1º jogador)")
        self.joinButton.clicked.connect(lambda: self.enterGame(self))
        self.hostButton.clicked.connect(lambda: self.hostGame())

        self.userIpLabel = QtWidgets.QLineEdit()
        self.userIpLabel.setEnabled(False)
        self.userIpLabel.setText("Seu endereço: " + str(socket.gethostbyname(socket.gethostname())))

        self.userPortLabel = QtWidgets.QLineEdit()
        self.userPortLabel.setEnabled(False)
        self.userPortLabel.setText("Porta de Host padrão: 8080")

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.userNameBox)
        self.layout.addWidget(self.serverIpBox)
        self.layout.addWidget(self.serverPortBox)

        self.layout.addWidget(self.joinButton)
        self.layout.addWidget(self.hostButton)
        self.layout.addWidget(self.userIpLabel)
        self.layout.addWidget(self.userPortLabel)

        self.setLayout(self.layout)

    @staticmethod
    def enterGame(self):
        self.window = QtWidgets.QMainWindow()
        self.initGame()

    def hostGame(self):
        t1 = Thread(target=self.initServer)
        t1.start()
        t2 = Thread(target=self.initGame())
        t2.start()

    def initServer(self):
        self.server = Server(self.serverPortBox.text())

    def initGame(self):
        self.ui = UI(self.userNameBox.text(), self.serverIpBox.text(), self.serverPortBox.text())
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UserName().show()
    sys.exit(app.exec_())
