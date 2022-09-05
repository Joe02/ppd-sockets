from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton, QTextEdit, QMainWindow, QLineEdit, QLabel
import socket
import os
from threading import Thread

redString = "#ff0000"
blueString = "#0000ff"


class UI(QMainWindow):
    def __init__(self, name, server, port):
        super(UI, self).__init__()

        self.playerColor = 0

        self.gameState = 1
        self.socketClient = None
        self.messageToSend = ""

        os.system('cls')

        uic.loadUi("game.ui", self)

        # Board / 1 = Blue / 2 = Red
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.boardButtons = []

        #  1 = Blue / 2 = Remove blue
        #  3 = Red / 4 = Remove red
        # -1 = Lost blue / -2 = Lost red
        self.turn = 1

        # Amount of pieces by color
        self.red = 9
        self.blue = 9

        # Give up button
        self.giveUpButton = self.findChild(QPushButton, "giveUpButton")
        self.giveUpButton.clicked.connect(lambda: self.sendEndGameMessage())
        self.giveUpButton.setStyleSheet("color: white")

        self.playerColorLabel = self.findChild(QLabel, "playerColor")
        self.currentTurnColor = self.findChild(QLabel, "currentTurnColor")
        self.setCurrentTurnColor()
        self.bluePiecesLeft = self.findChild(QLabel, "bluePiecesLeftNumber")
        self.redPiecesLeft = self.findChild(QLabel, "redPiecesLeftNumber")
        self.setPiecesLeftLabels()

        # Displayed to game start
        self.piecesLeft = 18

        # Name of player
        self.name = name

        # Messages editText
        self.serverMessages = self.findChild(QTextEdit, "serverMessages")
        self.serverMessages.setEnabled(False)

        # Player message box
        self.userMessageField = self.findChild(QLineEdit, "playerMessageBox")
        self.sendMessageButton = self.findChild(QPushButton, "sendMessageButton")
        self.sendMessageButton.clicked.connect(lambda: self.sendMessage())

        # 1st Button
        self.oneButton = self.findChild(QPushButton, "oneButton")
        self.oneButton.clicked.connect(lambda: self.paintButton(self.oneButton, 0))
        self.boardButtons.append(self.oneButton)

        # 2nd Button
        self.twoButton = self.findChild(QPushButton, "twoButton")
        self.twoButton.clicked.connect(lambda: self.paintButton(self.twoButton, 1))
        self.boardButtons.append(self.twoButton)

        # 3rd Button
        self.threeButton = self.findChild(QPushButton, "threeButton")
        self.threeButton.clicked.connect(lambda: self.paintButton(self.threeButton, 2))
        self.boardButtons.append(self.threeButton)

        # 4th Button
        self.fourButton = self.findChild(QPushButton, "fourButton")
        self.fourButton.clicked.connect(lambda: self.paintButton(self.fourButton, 3))
        self.boardButtons.append(self.fourButton)

        # 5th Button
        self.fiveButton = self.findChild(QPushButton, "fiveButton")
        self.fiveButton.clicked.connect(lambda: self.paintButton(self.fiveButton, 4))
        self.boardButtons.append(self.fiveButton)

        # 6th Button
        self.sixButton = self.findChild(QPushButton, "sixButton")
        self.sixButton.clicked.connect(lambda: self.paintButton(self.sixButton, 5))
        self.boardButtons.append(self.sixButton)

        # 7th Button
        self.sevenButton = self.findChild(QPushButton, "sevenButton")
        self.sevenButton.clicked.connect(lambda: self.paintButton(self.sevenButton, 6))
        self.boardButtons.append(self.sevenButton)

        # 8th Button
        self.eightButton = self.findChild(QPushButton, "eightButton")
        self.eightButton.clicked.connect(lambda: self.paintButton(self.eightButton, 7))
        self.boardButtons.append(self.eightButton)

        # 9th Button
        self.nineButton = self.findChild(QPushButton, "nineButton")
        self.nineButton.clicked.connect(lambda: self.paintButton(self.nineButton, 8))
        self.boardButtons.append(self.nineButton)

        # 10 Button
        self.tenButton = self.findChild(QPushButton, "tenButton")
        self.tenButton.clicked.connect(lambda: self.paintButton(self.tenButton, 9))
        self.boardButtons.append(self.tenButton)

        # 11th Button
        self.elevenButton = self.findChild(QPushButton, "elevenButton")
        self.elevenButton.clicked.connect(lambda: self.paintButton(self.elevenButton, 10))
        self.boardButtons.append(self.elevenButton)

        # 12th Button
        self.twelveButton = self.findChild(QPushButton, "twelveButton")
        self.twelveButton.clicked.connect(lambda: self.paintButton(self.twelveButton, 11))
        self.boardButtons.append(self.twelveButton)

        # 13th Button
        self.thirteenButton = self.findChild(QPushButton, "thirteenButton")
        self.thirteenButton.clicked.connect(lambda: self.paintButton(self.thirteenButton, 12))
        self.boardButtons.append(self.thirteenButton)

        # 14th Button
        self.fourteenButton = self.findChild(QPushButton, "fourteenButton")
        self.fourteenButton.clicked.connect(lambda: self.paintButton(self.fourteenButton, 13))
        self.boardButtons.append(self.fourteenButton)

        # 15th Button
        self.fifteenButton = self.findChild(QPushButton, "fifteenButton")
        self.fifteenButton.clicked.connect(lambda: self.paintButton(self.fifteenButton, 14))
        self.boardButtons.append(self.fifteenButton)

        # 16th Button
        self.sixteenButton = self.findChild(QPushButton, "sixteenButton")
        self.sixteenButton.clicked.connect(lambda: self.paintButton(self.sixteenButton, 15))
        self.boardButtons.append(self.sixteenButton)

        # 17th Button
        self.seventeenButton = self.findChild(QPushButton, "seventeenButton")
        self.seventeenButton.clicked.connect(lambda: self.paintButton(self.seventeenButton, 16))
        self.boardButtons.append(self.seventeenButton)

        # 18th Button
        self.eighteenButton = self.findChild(QPushButton, "eighteenButton")
        self.eighteenButton.clicked.connect(lambda: self.paintButton(self.eighteenButton, 17))
        self.boardButtons.append(self.eighteenButton)

        # 19th Button
        self.nineteenButton = self.findChild(QPushButton, "nineteenButton")
        self.nineteenButton.clicked.connect(lambda: self.paintButton(self.nineteenButton, 18))
        self.boardButtons.append(self.nineteenButton)

        # 20th Button
        self.twentyButton = self.findChild(QPushButton, "twentyButton")
        self.twentyButton.clicked.connect(lambda: self.paintButton(self.twentyButton, 19))
        self.boardButtons.append(self.twentyButton)

        # 21th Button
        self.twentyOneButton = self.findChild(QPushButton, "twentyOneButton")
        self.twentyOneButton.clicked.connect(lambda: self.paintButton(self.twentyOneButton, 20))
        self.boardButtons.append(self.twentyOneButton)

        # 22th Button
        self.twentyTwoButton = self.findChild(QPushButton, "twentyTwoButton")
        self.twentyTwoButton.clicked.connect(lambda: self.paintButton(self.twentyTwoButton, 21))
        self.boardButtons.append(self.twentyTwoButton)

        # 23th Button
        self.twentyThreeButton = self.findChild(QPushButton, "twentyThreeButton")
        self.twentyThreeButton.clicked.connect(lambda: self.paintButton(self.twentyThreeButton, 22))
        self.boardButtons.append(self.twentyThreeButton)

        # 24th Button
        self.twentyFourButton = self.findChild(QPushButton, "twentyFourButton")
        self.twentyFourButton.clicked.connect(lambda: self.paintButton(self.twentyFourButton, 23))
        self.boardButtons.append(self.twentyFourButton)

        self.server = server
        self.port = port

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server, int(self.port)))
        self.nickToSend = 'nickname=' + name
        self.client.send(self.nickToSend.encode('utf-8'))

        t1 = Thread(target=self.checkForMessages)
        t1.start()

        # Show the game
        self.show()

    def setPiecesLeftLabels(self):
        self.redPiecesLeft.setText(str(self.red))
        self.bluePiecesLeft.setText(str(self.blue))

    def setCurrentTurnColor(self):
        if self.turn == -2 or self.turn == 1 or self.turn == 2:
            self.currentTurnColor.setText("Azul")
        else:
            self.currentTurnColor.setText("Vermelho")

    def checkForMessages(self):
        while True:
            message = self.client.recv(2048).decode('utf-8')
            if len(str(message)) != 0:
                self.onMessageReceived(message)

    def sendMessage(self):
        msg = "message=" + self.name + ": " + self.userMessageField.text()
        self.client.sendall(msg.encode('utf-8'))
        self.userMessageField.setText("")

    def sendAction(self, index):
        action = "action=" + self.name + "=" + str(index)
        self.client.sendall(action.encode('utf-8'))

    def onMessageReceived(self, msg):
        newMessage = msg.split("=")
        if newMessage[0] == "action":
            splittedNewMessage = newMessage[2].split()
            self.clickedButton(splittedNewMessage[0])
        elif newMessage[0] == "endGame":
            if newMessage[1] == "Azul":
                self.messageToSend = "\n\nO jogador Vermelho venceu!\n\n"
            else:
                self.messageToSend = "\n\nO jogador Azul venceu!\n\n"
            self.serverMessages.insertPlainText(self.messageToSend)
            self.gameState = 0
        elif newMessage[0] == "color":
            self.playerColor = int(newMessage[1])
            if self.playerColor == 1:
                self.playerColorLabel.setText("Azul")
                self.playerColorLabel.setStyleSheet("color: blue")
                self.giveUpButton.setStyleSheet("QPushButton {background-color: blue; color: white}")
            else:
                self.playerColorLabel.setText("Vermelho")
                self.playerColorLabel.setStyleSheet("color: red")
                self.giveUpButton.setStyleSheet("QPushButton {background-color: red; color: white}")

        else:
            self.messageToSend = msg + "\n"
            self.serverMessages.insertPlainText(self.messageToSend)

    def clickedButton(self, index):
        integerIndex = int(index)
        for index in range(0, 24):
            if integerIndex == index:
                self.onClickFromServer(self.boardButtons[index], index)

    def onClickFromServer(self, button, index):
        if self.gameState == 0:
            return
        pieceContainsColor = str(button.palette().button().color().name()) == blueString or \
                             str(button.palette().button().color().name()) == redString

        if self.turn == 1 and not pieceContainsColor:

            # Paint blue
            self.board[index] = 1
            button.setStyleSheet("background-color: blue")

            self.piecesLeft -= 1
            if self.piecesLeft > 0:
                self.turn = 3
            else:
                self.turn = 4

            if self.madeTrail("blue", index):
                self.turn = -2

            self.setCurrentTurnColor()

        elif self.turn == 3 and not pieceContainsColor:

            # Paint red
            self.board[index] = 2
            button.setStyleSheet("background-color: red")

            self.piecesLeft -= 1
            if self.piecesLeft > 0:
                self.turn = 1
            else:
                self.turn = 2

            if self.madeTrail("red", index):
                self.turn = -1
            self.setCurrentTurnColor()

        elif self.turn == 2 or self.turn == 4 and pieceContainsColor:

            if self.turn == 2 and str(button.palette().button().color().name()) == blueString:
                self.turn = 1
            elif self.turn == 4 and str(button.palette().button().color().name()) == redString:
                self.turn = 3
            else:
                return

            # Remove piece
            self.board[index] = 0
            button.setStyleSheet("background-color: white")
            # self.setCurrentTurnColor()

        else:
            if self.turn == -1:
                print()
                self.blue -= 1
                self.setPiecesLeftLabels()
                if self.blue < 3:
                    self.displayWinner(self)

                self.turn = 1
                button.setStyleSheet("background-color: white")
                self.board[index] = 0

            elif self.turn == -2:
                self.red -= 1
                self.setPiecesLeftLabels()
                if self.red < 3:
                    self.displayWinner(self)

                self.turn = 3
                button.setStyleSheet("background-color: white")
                self.board[index] = 0

            self.setCurrentTurnColor()

    def paintButton(self, button, index):
        if self.gameState != 0:
            pieceContainsColor = str(button.palette().button().color().name()) == blueString or \
                                 str(button.palette().button().color().name()) == redString

            if self.turn == 1 and not pieceContainsColor and self.playerColor == 1:

                # Paint blue
                self.board[index] = 1
                button.setStyleSheet("background-color: blue")

                self.piecesLeft -= 1
                if self.piecesLeft > 0:
                    self.turn = 3
                else:
                    self.turn = 4

                if self.madeTrail("blue", index):
                    self.turn = -2

                self.sendAction(index)

                self.setCurrentTurnColor()

            elif self.turn == 3 and not pieceContainsColor and self.playerColor == 2:

                # Paint red
                self.board[index] = 2
                button.setStyleSheet("background-color: red")
                self.sendAction(index)

                self.piecesLeft -= 1
                if self.piecesLeft > 0:
                    self.turn = 1
                else:
                    self.turn = 2

                if self.madeTrail("red", index):
                    self.turn = -1

                self.setCurrentTurnColor()

            elif self.turn == 2 or self.turn == 4 and pieceContainsColor:

                if self.turn == 2 and str(
                        button.palette().button().color().name()) == blueString and self.playerColor == 1:
                    self.turn = 1
                    self.sendAction(index)
                elif self.turn == 4 and str(
                        button.palette().button().color().name()) == redString and self.playerColor == 2:
                    self.turn = 3
                    self.sendAction(index)
                else:
                    return

                # Remove piece
                self.board[index] = 0
                button.setStyleSheet("background-color: white")

                # self.setCurrentTurnColor()

            else:
                if self.turn == -1 and self.playerColor == 2:
                    self.blue -= 1
                    self.setPiecesLeftLabels()
                    if self.blue < 3:
                        self.displayWinner("Vermelho")

                    self.turn = 1
                    button.setStyleSheet("background-color: white")
                    # self.paintButton(button, index)
                    self.sendAction(index)
                    self.board[index] = 0

                elif self.turn == -2 and self.playerColor == 1:
                    self.red -= 1
                    self.setPiecesLeftLabels()
                    if self.red < 3:
                        self.displayWinner("Azul")

                    self.turn = 3
                    print(button.styleSheet())
                    button.setStyleSheet("background-color: white")
                    # self.paintButton(button, index)
                    self.sendAction(index)
                    self.board[index] = 0

                self.setCurrentTurnColor()

    def sendEndGameMessage(self):
        if self.gameState != 0:
            endGameMsg = "endGame=" + self.playerColorLabel.text()
            print(endGameMsg)
            self.client.sendall(endGameMsg.encode('utf-8'))

    def displayWinner(self, winnerColor):
        self.messageToSend = "O jogador %s venceu!" % str(winnerColor)
        self.serverMessages.insertPlainText(self.messageToSend)
        self.gameState = 0

    def madeTrail(self, color, index):
        # Vertical lines
        if color == "blue":
            return self.checkForTrail(1, index)

        # Horizontal lines
        else:
            return self.checkForTrail(2, index)

    def checkForTrail(self, colorId, index):
        if self.board[0] == colorId and self.board[9] == colorId and self.board[21] == colorId and (
                index == 0 or index == 9 or index == 21):
            return True
        if self.board[3] == colorId and self.board[10] == colorId and self.board[18] == colorId and (
                index == 3 or index == 10 or index == 18):
            return True
        if self.board[6] == colorId and self.board[11] == colorId and self.board[15] == colorId and (
                index == 6 or index == 11 or index == 15):
            return True
        if self.board[1] == colorId and self.board[4] == colorId and self.board[7] == colorId and (
                index == 1 or index == 4 or index == 7):
            return True
        if self.board[16] == colorId and self.board[19] == colorId and self.board[22] == colorId and (
                index == 16 or index == 19 or index == 22):
            return True
        if self.board[8] == colorId and self.board[12] == colorId and self.board[17] == colorId and (
                index == 8 or index == 12 or index == 17):
            return True
        if self.board[5] == colorId and self.board[13] == colorId and self.board[20] == colorId and (
                index == 5 or index == 13 or index == 20):
            return True
        if self.board[2] == colorId and self.board[14] == colorId and self.board[23] == colorId and (
                index == 2 or index == 14 or index == 23):
            return True
        if self.board[0] == colorId and self.board[1] == colorId and self.board[2] == colorId and (
                index == 0 or index == 1 or index == 2):
            return True
        if self.board[3] == colorId and self.board[4] == colorId and self.board[5] == colorId and (
                index == 3 or index == 4 or index == 5):
            return True
        if self.board[6] == colorId and self.board[7] == colorId and self.board[8] == colorId and (
                index == 6 or index == 7 or index == 8):
            return True
        if self.board[9] == colorId and self.board[10] == colorId and self.board[11] == colorId and (
                index == 9 or index == 10 or index == 11):
            return True
        if self.board[12] == colorId and self.board[13] == colorId and self.board[14] == colorId and (
                index == 12 or index == 13 or index == 14):
            return True
        if self.board[15] == colorId and self.board[16] == colorId and self.board[17] == colorId and (
                index == 15 or index == 16 or index == 17):
            return True
        if self.board[18] == colorId and self.board[19] == colorId and self.board[20] == colorId and (
                index == 18 or index == 19 or index == 20):
            return True
        if self.board[21] == colorId and self.board[22] == colorId and self.board[23] == colorId and (
                index == 21 or index == 22 or index == 23):
            return True
        return False
