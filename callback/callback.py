#!/usr/bin/env python

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'

def post_text(reply_token, text):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {ENTER_ACCESS_TOKEN}"
    }
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": text
                }
            ]
    }
    requests.post(REPLY_ENDPOINT, headers=header, data=json.dumps(payload))

