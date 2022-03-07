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
    print('body :', body)

    try:
        if bot_type == 'TEST':
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)

        elif bot_type == 'KAKAO':
            pass
            # print('KAKAO BODY :', body)
            # utterance = body['userRequest']['utterance']
            # ret = get_answer_from_engine(bottype=bot_type, query=utterance)
            #
            # from

        elif bot_type == 'NAVER':
            user_key = body['user']
            event = body['event']

            from NaverEvent import NaverEvent
            authorization_key = '<보내기 API 인증키>'
            naverEvent = NaverEvent(authorization_key)

            if event == 'open':
                print('채팅방에 유저가 들어왔습니다.')
                return json.dumps({}), 200

            elif event == 'leave':
                print('채팅방에서 유저가 나갔습니다.')
                return json.dumps({}), 200

            elif event == 'send':
                print('사용자 -> 챗봇 send')
                user_text = body['textContent']['text']
                ret = get_answer_from_engine(bottype=bot_type, query=user_text)
                return naverEvent.send_response(user_key, ret)

            return json.dumps({}), 200

        else:
            abort(404)

    except Exception as ex:
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)