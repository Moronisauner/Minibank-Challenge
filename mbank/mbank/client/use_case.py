from .repository import ClientRepo
from .entities import Client

class ClientUseCase(object):
    _repo = None
    _cfo = None # Email do CFO da agencia do cliente

    def __init__(self, repo):
        self._repo = repo

    def create(self, client):
        self._repo.create(client)

    def update(self, client):
        self._repo.update(client)

    def delete(self, client):
        self._repo.delete(client)

    def find_by_username(self, username):
        return self._repo.find_by_username(username)

    def find_by_email(self, email):
        return self._repo.find_by_email_address(email)
