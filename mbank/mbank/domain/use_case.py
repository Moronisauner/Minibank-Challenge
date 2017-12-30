from .repository import DomainRepo
from .entities import Account
from django.core.mail import send_mail


class AccountUseCase(object):
    _repo = None

    def __init__(self, repo):
        self._repo = repo

    def create(self, account):
        self._repo.create(account)
        send_mail(
            'Criada uma nova conta',
            'Um cliente criou uma nova conta bancária',
            'sistema@mail.com',
            ['cfo_da_conta@mail.com'],
            fail_silently=False,
        )

    def update(self, account):
        self._repo.update(account)

    def delete(self, account):
        self._repo.delete(account)

    def find_all_client_accounts(self, client):
        if isinstance(client, Account):
            return self._repo.find_by_client_uuid(client.get_uuid())
        else:
            return self._repo.find_by_client_uuid(client.uuid)

    def find_account_by_uuid(self, account_uuid):
        return self._repo.find_by_account_uuid(account_uuid)

    # def find_by_email(self, email):
    #     return self._repo.find_by_email_address(email)
