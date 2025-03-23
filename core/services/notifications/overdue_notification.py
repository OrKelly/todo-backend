from core.services.telegram_client import TelegramClient
from tasks.models import Task


class OverdueNotificationMessageCreateService:
    def __init__(self, task: Task):
        self.task = task
        self.telegram_client = TelegramClient()

    def notify(self):
        text = self._get_notification_text()
        self.telegram_client.send_message(
            user_id=self.task.user.user_id, text=text, parse_mode="HTML"
        )

    def _get_notification_text(self) -> str:
        return f"""
        <b>Внимание!</b> Вы забыли выполнить задачу <b>{self.task.title}</b>!
        Вам лучше исправиться, пока я не начал злиться!
        """
