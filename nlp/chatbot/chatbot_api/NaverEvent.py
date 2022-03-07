import requests, json

class NaverEvent:
    def __init__(self, authorization):
        self.authorization_key = authorization

    def textContentComponent(self, text):
        return {
            'textContent': {
                'text': text
            }
        }

    def imageContentComponent(self, imageUrl):
        return {
            'imageContent': {
                'imageUrl': imageUrl
            }
        }

    def send_message(self, user_key, component):
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': self.authorization_key,
        }

        data = {
            'event': 'send',
            'user': user_key,
        }
        data.update(component)

        message = json.dumps(data)
        return requests.post(
            'https://gw.talk.naver.com/chatbot/v1/event',
            headers=headers,
            data=message
        )

    def send_response(self, dst_user_key, bot_resp):
        if bot_resp['AnswerImageUrl'] is not None:
            image = self.imageContentComponent(bot_resp['AnswerImageUrl'])
            self.send_message(user_key=dst_user_key, component=image)

        if bot_resp['Answer'] is not None:
            text = self.textContentComponent(bot_resp['Answer'])
            self.send_message(user_key=dst_user_key, component=text)

        return json.dumps({}), 200