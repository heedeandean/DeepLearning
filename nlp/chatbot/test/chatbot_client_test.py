import socket
import json

host = '127.0.0.1' # 챗봇 엔진 서버 IP 주소
port = 5050

while True:
    print('질문 : ')
    query = input() # 질문 입력
    if(query == 'exit'):
        exit(0)
    print('-' * 40)

    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    json_data = {
        'Query': query,
        'BotType': 'MyService'
    }
    message = json.dumps(json_data) # json -> str
    mySocket.send(message.encode())

    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data) # str -> json
    print('답변 : ')
    print(ret_data['Answer'])
    print('\n')

    mySocket.close() # 소켓은 사용 뒤 반드시 닫기! DB도 마찬가지


