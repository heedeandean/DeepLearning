import threading
import json

from config.DatabaseConfig import *
from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from utils.FindAnswer import FindAnswer
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel

# 1. 전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.tsv')

# 2. 의도 파악
intent = IntentModel(model_name='models/intent/intent_model.h5', preprocess=p)

# 3. 개체명 인식
ner = NerModel(model_name='models/ner/ner_model.h5', preprocess=p)

# 챗봇 클라이언트의 서버 연결이 수락되는 순간 실행
def to_client(conn, addr, params):
    db = params['db']
    try:
        db.connect()

        read = conn.recv(2048) # 수신 데이터가 있을 때까지 blocking; 최대 2048byte 만큼 데이터 수신
        print('============================')
        print('Connection from: %s' % str(addr))

        if read is None or not read:
            print('클라이언트 연결 끊어짐')
            exit(0) # 스레드 강제 종료

        recv_json_data = json.loads(read.decode()) # str(챗봇 클라이언트로부터 수신된 데이터) -> json
        print('데이터 수신 :', recv_json_data)
        query = recv_json_data['Query']

        # 2. 의도 파악
        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]

        # 3. 개체명 인식
        ner_predicts = ner.predict(query)
        ner_tags = ner.predict_tags(query)

        # 4. 답변 검색
        try:
            f = FindAnswer(db)
            answer_text, answer_image = f.search(intent_name, ner_tags)
            answer = f.tag_to_word(ner_predicts, answer_text)

        except:
            answer = '죄송해요 무슨 말인지 모르겠어요. 조금 더 공부할게요.'
            answer_image = None

        send_json_data_str = {
            'Query': query,
            'Answer': answer,
            'AnswerImageUrl': answer_image,
            'Intent': intent_name,
            'NER': str(ner_predicts)
        }

        message = json.dumps(send_json_data_str) # json -> str (Why? 소켓 통신은 객체형태로(json) 데이터 송신이 불가능)
        conn.send(message.encode()) # 서버 -> 클라이언트

    except Exception as ex:
        print(ex)

    finally:
        if db is not None:
            db.close()
        conn.close() # 스레드 함수 실행 종료

if __name__ == '__main__':
    db = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME)
    print('DB 접속')

    port = 5050
    listen = 100
    bot = BotServer(port, listen)
    bot.create_sock()
    print('bot start')

    # 무한 루프를 돌면서 챗봇 클라이언트 연결을 기다림
    while True:
        conn, addr = bot.ready_for_client()
        params = {'db': db}

        client = threading.Thread(target=to_client, args=(conn, addr, params)) # 스레드 생성
        client.start() # 스레드 시작




