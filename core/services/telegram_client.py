import requests
from django.conf import settings


class TelegramClient:
    BASE_URL = "https://api.telegram.org/"

    @property
    def url(self):
        return f"{self.BASE_URL}/bot{settings.BOT_TOKEN}"

    def send_message(
        self,
        user_id: int,
        text: str,
        parse_mode: str = None,
        reply_markup=None,
    ):
        """
        Отправляет сообщение пользователю по его user_id.
        :param user_id: ID пользователя в Telegram.
        :param text: Текст сообщения.
        :param parse_mode: Режим форматирования текста (например, "HTML" или "Markdown").
        :param reply_markup: Клавиатура или inline-клавиатура в формате JSON (опционально).
        """

        url = f"{self.url}/sendMessage"
        payload = {
            "chat_id": user_id,
            "text": text,
        }

        if parse_mode:
            payload["parse_mode"] = parse_mode

        if reply_markup:
            payload["reply_markup"] = reply_markup

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None
