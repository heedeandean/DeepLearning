from flask import Flask, request, jsonify
app = Flask(__name__)

# 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json()
    print('='*100)
    print(body)

    responseBody = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'simpleText': {
                        'text': '안녕'
                    }
                }
            ]
        }
    }
    return jsonify(responseBody)

# 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print('='*100)
    print(body)

    responseBody = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'simpleImage': {
                        'imageUrl': 'https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg',
                        'altText': '안녕'
                    }
                }
            ]
        }
    }
    return jsonify(responseBody)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)