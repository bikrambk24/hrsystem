from django.urls import path

from .views import check_page


urlpatterns = [
    path(
        "employee/<int:employee_pk>/<str:check_type>/",
        check_page,
        name="check_page",
    ),
]
