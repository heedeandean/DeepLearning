# 챗봇 엔진 전체 동작
from config.DatabaseConfig import *
from utils.Database import Database

# 1. 전처리 객체 생성
from utils.Preprocess import Preprocess
p = Preprocess(word2index_dic='../train_tools/dict/chatbot_dict.bin',
               userdic='../utils/user_dic.tsv')

db = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME)
db.connect()

query = '오전에 탕수육 10개 주문합니다.'
# query = '오늘 오전 13시 2분에 탕수육 주문하고 싶어요'
# query = '안녕하세요'
# query = '자장면 주문할게요'

# 2. 의도 파악
from models.intent.IntentModel import IntentModel
intent = IntentModel(model_name='../models/intent/intent_model.h5', preprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

# 3. 개체명 인식
from models.ner.NerModel import NerModel
ner = NerModel(model_name='../models/ner/ner_model.h5', preprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print('질문 :', query)
print('=' * 40)
print('의도 파악 :', intent_name)
print('개체명 인식 :', predicts)
print('답변 검색에 필요한 NER 태그 :', ner_tags)
print('=' * 40)

# 4. 답변 검색
from utils.FindAnswer import FindAnswer
try:
    f = FindAnswer(db)
    answer_text, answer_image = f.search(intent_name, ner_tags)
    answer = f.tag_to_word(predicts, answer_text)
except Exception as ex:
    print(ex)
    answer = '죄송해요, 무슨 말인지 모르겠어요.'

print('답변 :', answer)
db.close()