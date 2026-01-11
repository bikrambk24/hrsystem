import pytest
from django.urls import reverse
from accounts.models import User

pytestmark = pytest.mark.django_db


def create_user(email, password, role):
    return User.objects.create_user(
        email=email,
        password=password,
        role=role,
    )


def test_hr_redirects_to_hr_dashboard(client):
    create_user("hr@example.com", "Pass12345!", User.ROLE_HR)
    client.login(email="hr@example.com", password="Pass12345!")

    res = client.get(reverse("dashboard"))

    assert res.status_code in (301, 302) 
    assert "/employees/hr/dashboard/" in res["Location"]


def test_team_lead_redirects_to_teamlead_dashboard(client):
    create_user("tl@example.com", "Pass12345!", User.ROLE_TL)
    client.login(email="tl@example.com", password="Pass12345!")

    res = client.get(reverse("dashboard"))

    assert res.status_code in (301, 302)
    assert "/employees/teamlead/dashboard/" in res["Location"]


def test_employee_redirects_to_employee_dashboard(client):
    create_user("emp@example.com", "Pass12345!", User.ROLE_EMP)
    client.login(email="emp@example.com", password="Pass12345!")

    res = client.get(reverse("dashboard"))

    assert res.status_code in (301, 302)
    assert "/employees/employee/dashboard/" in res["Location"]


def test_employee_forbidden_on_hr_pages(client):
    create_user("emp2@example.com", "Pass12345!", User.ROLE_EMP)
    client.login(email="emp2@example.com", password="Pass12345!")

    
    res = client.get(reverse("hr_employee_list"))

    assert res.status_code == 403


def test_hr_can_access_hr_employee_list(client):
    create_user("hr2@example.com", "Pass12345!", User.ROLE_HR)
    client.login(email="hr2@example.com", password="Pass12345!")

    res = client.get(reverse("hr_employee_list"))

    
    assert res.status_code == 200


def test_anonymous_redirected_to_login_for_hr_page(client):
    res = client.get(reverse("hr_employee_list"))

    
    assert res.status_code in (301, 302)
    assert "/accounts/login/" in res["Location"]
