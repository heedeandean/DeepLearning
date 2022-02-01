from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello(): # view 함수
    return 'Hello Flask'

if __name__ == '__main__':
    app.run()