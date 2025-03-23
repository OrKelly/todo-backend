from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiParameter


class CustomAutoSchema(AutoSchema):
    global_params = [
        OpenApiParameter(
            name="User-Id",
            type=int,
            location=OpenApiParameter.HEADER,
            description="ID текущего пользователя",
        ),
    ]

    def get_override_parameters(self):
        params = super().get_override_parameters()
        params.extend(self.global_params)
        return params
