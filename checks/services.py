import json
from pathlib import Path
from django.conf import settings

MOCK_FILE = Path(settings.BASE_DIR) / "checks" / "mock_data.json"


def load_mock_data():
    with open(MOCK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_record(section: str, employee_id: str):
    data = load_mock_data()
    records = data.get(section, [])

    for r in records:
        if r.get("employee_id") == employee_id:
            return r

    return None


def normalize(s: str) -> str:
    return (s or "").strip().lower()


def check_dbs(employee_profile, dbs_number: str):
    record = find_record("dbs", employee_profile.employee_id)

    if not record:
        return False, "No DBS record found in mock database."

    if normalize(record.get("dbs_number")) != normalize(dbs_number):
        return False, "DBS number does not match."

    if normalize(record.get("full_name")) != normalize(employee_profile.full_name):
        return False, "Name does not match DBS record."

    if normalize(record.get("status")) != "clear":
        return False, "DBS status is not CLEAR."

    return True, "DBS check passed (mock match)."


def check_bank(employee_profile, account_name: str, sort_code: str, account_number: str):
    record = find_record("bank", employee_profile.employee_id)

    if not record:
        return False, "No Bank record found in mock database."

    if normalize(record.get("account_name")) != normalize(account_name):
        return False, "Account name does not match."

    if normalize(record.get("sort_code")) != normalize(sort_code):
        return False, "Sort code does not match."

    if normalize(record.get("account_number")) != normalize(account_number):
        return False, "Account number does not match."

    return True, "Bank check passed (mock match)."


def check_home_office(employee_profile, visa_ref: str):
    record = find_record("home_office", employee_profile.employee_id)

    if not record:
        return False, "No Home Office record found in mock database."

    if normalize(record.get("visa_ref")) != normalize(visa_ref):
        return False, "Visa reference does not match."

    if normalize(record.get("full_name")) != normalize(employee_profile.full_name):
        return False, "Name does not match Home Office record."

    if record.get("right_to_work") is not True:
        return False, "Right-to-work not confirmed."

    return True, "Home Office check passed (mock match)."


def check_credit(employee_profile, credit_ref: str):
    record = find_record("credit", employee_profile.employee_id)

    if not record:
        return False, "No Credit record found in mock database."

    if normalize(record.get("credit_ref")) != normalize(credit_ref):
        return False, "Credit reference does not match."

    band = normalize(record.get("score_band"))

    if band not in ("good", "excellent"):
        return False, f"Credit score band is {record.get('score_band')}."

    return True, "Credit check passed (mock match)."
