from django.urls import reverse

ACCEPTED_URLS_WITHOUT_ROLE = {
    reverse("api-docs"),
    reverse("swagger"),
}
