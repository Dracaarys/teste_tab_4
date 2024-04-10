import grpc
import time
from concurrent import futures
import sys
sys.path.append('proto')  # Adiciona o diretório 'proto' ao caminho de importação
import chat_pb2 as chat  # Importa chat_pb2 do diretório 'proto'
import chat_pb2_grpc as rpc

class ChatServer(rpc.ChatServerServicer):
    def __init__(self):
        self.chats = []
        self.client_stubs = set()  # Usamos um conjunto para evitar clientes duplicados

    def ChatStream(self, request_iterator, context):
        lastindex = 0
        while True:
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: chat.Note, context):
        print("[{}] {}".format(request.name, request.message))
        self.chats.append(request)
        
        # Envia a mensagem para todos os clientes conectados
        for stub in self.client_stubs:
            stub.SendNote(request)
        return chat.Empty()

    def join_chat(self, context):
        self.client_stubs.add(context)
        print("algum individuo entrou.")

    def leave_chat(self, context):
        self.client_stubs.remove(context)
        print("vc saiu.")

if __name__ == '__main__':
    port = 11912
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_server = ChatServer()
    rpc.add_ChatServerServicer_to_server(chat_server, server)
    print('serve iniciou ...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    
    try:
        while True:
            time.sleep(64 * 64 * 100)
    except KeyboardInterrupt:
        server.stop(0)
