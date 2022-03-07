import requests, json

authorization_key = 'g7GhK/0pR9WsHd/hCUak' # 보내기 API 인증키
headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Authorization': authorization_key,
}

user_key = ''
data = { # type(dict)
    "event": "send",
    "user": user_key,
    "textContent": {"text": "hello world :D"}
}

message = json.dumps(data) # type(str)
response = requests.post(
    'https://gw.talk.naver.com/chatbot/v1/event',
    headers=headers,
    data=message
)
print(response.status_code)
print(response.text)