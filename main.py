from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

#環境変数取得
token = 'nzYnRJXfglQdIxWnFSp4CPkQ9eTVAWlSthIqs6P6FLVgKfo+FlBAthkhNmELfAlmmx7yH+ZEtFojzpY36qGQVL1e+ar++1cl+yMjX00j0u2uEQ8+dCOyBV6ZUBxYyZRg7cCaynZpe93g2OJxSmDPcwdB04t89/1O/w1cDnyilFU='
secret = 'ee73a91ea2873974ed5d63a6db562019'

YOUR_CHANNEL_ACCESS_TOKEN = os.environ[token]
YOUR_CHANNEL_SECRET = os.environ[secret]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
