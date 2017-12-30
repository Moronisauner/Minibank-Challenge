from mbank.domain.use_case import AccountUseCase
from mbank.domain.repository import DomainRepo
from mbank.domain.entities import Account
from mbank.domain.forms import  CreateAccountForm

class CreateAccountService(object):

    __account_create_form = None

    def run(self, client_uuid, account_number):
        inputs = {
            'client_uuid': client_uuid,
            'account_number': account_number
        }

        create_account_form = CreateAccountForm(inputs)
        __account_create_form = create_account_form
        if create_account_form.is_valid():

            account_use_case = AccountUseCase(DomainRepo())
            account = Account(client_uuid, account_number)
            print('>>>>>>>>', account, '<<<<<<<<<<')
            account_use_case.create(account)

    def get_form(self):
        return self.__account_create_form
