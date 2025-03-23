from typing import Any

from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from rest_framework.request import Request

from core.constants import ACCEPTED_URLS_WITHOUT_ROLE
from users.models import User


class TelegramUserAuth:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        request.current_user = None
        url = request.path

        if (
            url in ACCEPTED_URLS_WITHOUT_ROLE or url.startswith(("/admin", "/api/v1/users"))
        ):
            return self.get_response(request)

        user_id, error = self._get_user_id(request)
        if error:
            return self.json_response(*user_id)
        user, error = self._get_user_instance(user_id)
        if error:
            return self.json_response(*user)
        request.current_user = user
        return self.get_response(request)

    @staticmethod
    def json_response(message: dict, status: int) -> JsonResponse:
        return JsonResponse(message, status=status)

    def _get_user_id(
        self, request: Request
    ) -> str | tuple[dict[str, str], Any]:
        user_id = request.headers.get("User-Id")
        if not user_id:
            return (
                {"message": "Доступ запрещен"},
                HttpResponseForbidden.status_code,
            ), True
        return user_id, False

    def _get_user_instance(
        self, user_id: str
    ) -> User | tuple[dict[str, str], Any]:
        try:
            user = get_object_or_404(User, user_id=user_id)
            return user, False
        except User.DoesNotExist:
            return (
                {"message": "Пользователь не зарегистрирован"},
                HttpResponseNotFound.status_code,
            ), True
