import socket
import threading
import os


class Server:
    def __init__(self, port):
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = port
        self.ADDRESS = (self.HOST, int(self.PORT))
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)

        self.color = 1

        # 1 = Blue \ 2 = Red
        self.turnColor = 1
        self.bluePlayer = None
        self.redPlayer = None

        self.players = []

        def send_action(action, playerId):
            for player in self.players:
                if playerId != player['player']:
                    print('Enviando ação para o player', player['player'], 'em', player['address'])
                    action_to_send = 'action=' + action
                    player['connection'].send(action_to_send.encode('utf-8'))

        def send_message(message):
            for player in self.players:
                print('Enviando mensagem para o player', player['player'], 'em', player['address'])
                message_to_send = message
                player['connection'].send(message_to_send.encode('utf-8'))

        def send_color_response(playerConnection):
            message_to_send = "color=%s" % str(self.color)
            playerConnection.send(message_to_send.encode('utf-8'))
            self.color = 2

        def end_game(colorWhoGaveUp):
            for player in self.players:
                msgToSend = "endGame=" + colorWhoGaveUp
                player['connection'].send(msgToSend.encode('utf-8'))

        def handle_players(connection, address, player):
            print('Jogador', player, 'conectado ao servidor pelo endereço:', address)
            nickname = ""

            while True:
                message = connection.recv(2048).decode('utf-8')
                split_message = message.split('=')
                match split_message[0]:
                    case 'nickname':
                        nickname = split_message[1]
                        if self.bluePlayer is None:
                            self.bluePlayer = nickname
                        else:
                            self.redPlayer = nickname
                        self.players.append({'player': player, 'connection': connection, 'address': address, 'nickname': nickname})
                        send_color_response(connection)
                    case 'message':
                        message = split_message[1]
                        send_message(message)
                    case 'action':
                        if nickname == split_message[1]:
                            action = nickname + '=' + split_message[2]
                            send_action(action, player)
                    case 'endGame':
                        end_game(split_message[1])

        def start():
            self.server.listen(2)
            for i in range(1, 3):
                print('Servidor aguardando a conexão do jogador', i)
                connection, address = self.server.accept()
                msg = "Conexão estabelecida com o server: " + '192.168.18.43' + " na porta: " + str(8080)
                connection.send(msg.encode())
                player = i
                thread = threading.Thread(target=handle_players, args=(connection, address, player))
                thread.start()

        os.system('cls')
        start()
