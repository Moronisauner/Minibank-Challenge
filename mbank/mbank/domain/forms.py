from django import forms
from mbank.domain.value_object import AccountNumber, InvalidAccountNumber


class CreateAccountForm(forms.Form):
    account_number = forms.CharField()

    def clean_account_number(self):
        account_number = ''
        try:
            account_number = AccountNumber(self.cleaned_data['account_number'])
        except InvalidAccountNumber:
            raise forms.ValidationError("Numero de Conta inválido. Siga o padrão '00-000' !")

class TransactionForm(forms.Form):
    T_CHOICES = (
        (True, 'Deposito'),
        (False, 'Retirar'),
    )
    transction_type = forms.ChoiceField(choices=T_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control custom-select'})
    )
    amount = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
