"""Bottle server for the bot."""
import os
import requests
from bottle import (
    Bottle, response, request as bottle_request
)
from dotenv import load_dotenv

load_dotenv()


class BotHandlerMixin:
    """Bot handler mixin."""

    BOT_URL = None

    def get_chat_id(self, data):
        """Extract chat id from telegram request."""
        chat_id = data['message']['chat']['id']

        return chat_id

    def get_message(self, data):
        """Extract message id from telegram request."""
        message_text = data['message']['text']

        return message_text

    def send_message(self, prepared_data):
        """Prepare data(should be json).

        Includes(min):
        1.chat_id
        2.text
        """
        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)


class TelegramBot(BotHandlerMixin, Bottle):
    """Telegram bot."""

    BOT_URL = os.getenv("BOT_URL")

    def __init__(self, *args, **kwargs):
        """Set up mixin."""
        super(TelegramBot, self).__init__()
        self.route('/', callback=self.post_handler, method="POST")

    def change_text_message(self, text):
        """Turn our message backwards."""
        return text[::-1]

    def prepare_data_for_answer(self, data):
        """Create response."""
        message = self.get_message(data)
        chat_id = self.get_chat_id(data)
        answer = self.change_text_message(message)

        json_data = {
            "chat_id": chat_id,
            "text": answer,
        }

        return json_data

    def post_handler(self):
        """Handle post/text."""
        data = bottle_request.json
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)

        return response


if __name__ == '__main__':
    app = TelegramBot()
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"))
