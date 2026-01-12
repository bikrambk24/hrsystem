import pytest
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from attendance.models import Attendance

pytestmark = pytest.mark.django_db


def test_clock_in_once_per_day(client):
    User.objects.create_user(
        email="emp@example.com",
        password="Pass12345!",
        role=User.ROLE_EMP,
    )
    client.login(email="emp@example.com", password="Pass12345!")


    r1 = client.post(reverse("clock_in"))
    assert r1.status_code in (301, 302)

    
    r2 = client.post(reverse("clock_in"))
    assert r2.status_code in (301, 302)

    today = timezone.localdate()
    att = Attendance.objects.get(user__email="emp@example.com", date=today)
    assert att.clock_in is not None


def test_clock_out_requires_clock_in(client):
    User.objects.create_user(
        email="emp2@example.com",
        password="Pass12345!",
        role=User.ROLE_EMP,
    )
    client.login(email="emp2@example.com", password="Pass12345!")

    
    r = client.post(reverse("clock_out"))
    assert r.status_code in (301, 302)

    today = timezone.localdate()
    att, _ = Attendance.objects.get_or_create(
        user__email="emp2@example.com",
        date=today,
    )

    assert att.clock_in is None
    assert att.clock_out is None


def test_clock_out_once_per_day(client):
    User.objects.create_user(
        email="emp3@example.com",
        password="Pass12345!",
        role=User.ROLE_EMP,
    )
    client.login(email="emp3@example.com", password="Pass12345!")

    
    r1 = client.post(reverse("clock_in"))
    assert r1.status_code in (301, 302)

    
    r2 = client.post(reverse("clock_out"))
    assert r2.status_code in (301, 302)

    
    r3 = client.post(reverse("clock_out"))
    assert r3.status_code in (301, 302)

    today = timezone.localdate()
    att = Attendance.objects.get(user__email="emp3@example.com", date=today)

    assert att.clock_in is not None
    assert att.clock_out is not None


def test_hr_attendance_page_forbidden_to_employee(client):
    User.objects.create_user(
        email="emp4@example.com",
        password="Pass12345!",
        role=User.ROLE_EMP,
    )
    client.login(email="emp4@example.com", password="Pass12345!")

    res = client.get(reverse("hr_attendance_list"))
    assert res.status_code == 403


def test_hr_attendance_page_accessible_to_hr(client):
    User.objects.create_user(
        email="hr@example.com",
        password="Pass12345!",
        role=User.ROLE_HR,
    )
    client.login(email="hr@example.com", password="Pass12345!")

    res = client.get(reverse("hr_attendance_list"))


    assert res.status_code == 200
