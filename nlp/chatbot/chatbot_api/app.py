from flask import Flask, request, jsonify, abort
import socket
import json

host = '127.0.0.1'
port = 5050

app = Flask(__name__)

def get_answer_from_engine(bottype, query):
    mySocket = socket.socket()
    mySocket.connect((host, port))

    json_data = {
        'Query': query,
        'BotType': bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)

    mySocket.close()

    return ret_data

@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()
    print('body =', body)

    try:
        if bot_type == 'TEST':
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)

        elif bot_type == 'KAKAO':
            pass

        elif bot_type == 'NAVER':
            pass

        else:
            abort(404)

    except Exception as ex:
        abort(500)

if __name__ == '__main__':
    app.run(debug=True)
