import grpc
import sys
sys.path.append('proto')

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

address = 'localhost'
port = 11912

class Client:
    def __init__(self, username):
        self.username = username
        channel = grpc.insecure_channel(f"{address}:{port}")
        self.conn = rpc.ChatServerStub(channel)

    def listen_for_messages(self):
        for note in self.conn.ChatStream(chat.Empty()):
            print(f"[{note.name}] {note.message}")

    def send_message(self, message):
        if message.strip():  # Verifica se a mensagem não está vazia
            n = chat.Note()
            n.name = self.username
            n.message = message
            self.conn.SendNote(n)

if __name__ == "__main__":
    username = input("digite seu nome: ")
    client = Client(username)

    print("digite uma mensagem. Ctrl + C para sair do server")
    try:
        while True:
            message = input()
            client.send_message(message)
    except KeyboardInterrupt:
        print("tu saiu mesmo.")