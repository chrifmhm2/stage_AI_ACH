from django import forms
from .models import Bank, Account

class TransactionForm(forms.Form):
    bank = forms.ModelChoiceField(queryset=Bank.objects.all(), label="Choose Bank")
    account = forms.ModelChoiceField(queryset=Account.objects.all(), label="Choose Account")  # Affiche tous les comptes
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")
    account_id = forms.ChoiceField(choices=[('OLD_ACNT_NUM', 'OLD_ACNT_NUM'), ('ACNT_NUM', 'ACNT_NUM'), ('OLD_RIB', 'OLD_RIB'), ('NEW_RIB', 'NEW_RIB')], label="Account ID")
