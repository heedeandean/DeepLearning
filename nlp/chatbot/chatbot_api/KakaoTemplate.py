class KakaoTemplate:
    def __init__(self):
        self.version = '2.0'

    def simpleTextComponent(self, text):
        return {
            'simpleText': {'text': text}
        }

    def simpleImageComponent(self, imageUrl, altText):
        return {
            'simpleImage': {'imageUrl': imageUrl, 'altText': altText}
        }

    def send_response(self, bot_resp):
        responseBody = {
            'version': self.version,
            'template': {
                'outputs': []
            }
        }

        # 이미지 답변 -> 텍스트 답변
        if bot_resp['AnswerImageUrl'] is not None:
            responseBody['template']['outputs'].append(self.simpleImageComponent(bot_resp['AnswerImageUrl'], ''))

        if bot_resp['Answer'] is not None:
            responseBody['template']['outputs'].append(self.simpleTextComponent(bot_resp['Answer']))

        return responseBody