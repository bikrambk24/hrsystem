from django import forms


class DBSCheckForm(forms.Form):
    dbs_number = forms.CharField(
        max_length=50,
        label="DBS Number"
    )


class BankCheckForm(forms.Form):
    account_name = forms.CharField(
        max_length=100,
        label="Account Name"
    )
    sort_code = forms.CharField(
        max_length=20,
        label="Sort Code (e.g., 11-22-33)"
    )
    account_number = forms.CharField(
        max_length=20,
        label="Account Number"
    )


class HomeOfficeCheckForm(forms.Form):
    visa_ref = forms.CharField(
        max_length=50,
        label="Home Office Visa Reference"
    )


class CreditCheckForm(forms.Form):
    credit_ref = forms.CharField(
        max_length=50,
        label="Credit Reference"
    )
