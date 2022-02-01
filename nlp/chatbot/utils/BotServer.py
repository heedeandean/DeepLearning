import socket

class BotServer:
    def __init__(self, srv_port, listen_num):
        # 멤버변수
        self.port = srv_port
        self.listen = listen_num # 동시에 연결을 수락할 클라이언트 수
        self.mySock = None

    # 래퍼 함수
    def create_sock(self):
        self.mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP/IP 소켓 생성
        self.mySock.bind(('0.0.0.0', int(self.port)))
        self.mySock.listen(int(self.listen))
        return self.mySock

    def ready_for_client(self):
        return self.mySock.accept()

    def get_sock(self):
        return self.mySock
