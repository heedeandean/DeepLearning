from konlpy.tag import Komoran

class Preprocess:
    def __init__(self, userdic=None):
        self.komoran = Komoran(userdic=userdic) # 형태소 분석기

        # 제외할 품사 (관계언, 기호, 어미, 접미사) 정의
        # 참조 : https://docs.komoran.kr/firststep/postypes.html
        self.exclusion_tags = [ # 클래스 멤버변수
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',
            'JX', 'JC',
            'SF', 'SP', 'SS', 'SE', 'SO',
            'EP', 'EF', 'EC', 'ETN', 'ETM',
            'XSN', 'XSV', 'XSA'
        ]

    def pos(self, sentence): # 래퍼 함수
        return self.komoran.pos(sentence)

    def get_keywords(self, pos, without_tag=False):
        f = lambda x: x in self.exclusion_tags
        word_list = []
        for p in pos:
            if f(p[1]) is False:
                word_list.append(p if without_tag is False else p[0])
        return word_list

