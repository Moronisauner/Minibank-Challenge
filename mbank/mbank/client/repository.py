from .entities import Client
from .models import ClientModel
from .value_object import EmailAddress
from basehelp.repositories import AbstractRepository


class ClientRepo(AbstractRepository):

    def find_all(self):
        clients_models = ClientModel.objects.all()
        clients_entities = []
        for client in clients_models:
            entity = self.__load_entity(client)
            clients_entities.append(entity)

    def find_by_id(self, id):
        client_model = ClientModel.objects.get(pk=id)
        client = self.__load_entity(client_model)
        return client

    def find_by_email_address(self, email):
        client_model = ClientModel.objects.get(email=email)
        client = self.__load_entity(client_model)
        return client

    def find_by_username(self, username):
        client_model = ClientModel.objects.get(username=username)
        client = self.__load_entity(client_model)
        return client

    def create(self, client):
        client_model = ClientModel(
            #uuid=client.get_uuid(),
            username=client.get_username(),
            email=client.get_email_address(),
            first_name=client.get_first_name(),
            last_name=client.get_last_name(),
            is_company=bool(client.get_is_company()),
        )
        client_model.set_password(client.get_password())
        client_model.save()

    def update(self, client):
        client_model = ClientModel.objects.get(pk=client.get_uuid())
        if client_model.username != client.get_username():
            if ClientModel.objects.get(username=client.get_username()).exists():
                raise Exception
        client_model.username = client.get_username()
        client_model.email = client.get_email_address()
        client_model.first_name = client.get_first_name()
        client_model.last_name = client.get_last_name()
        client_model.is_company = client.get_is_company()
        client_model.save()

    def delete(self, client):
        ClientModel.get(pk=client.get_uuid()).delete()

    def __load_entity(self, client_model):

        client_entity = Client(
            client_model.uuid,
            client_model.username,
            EmailAddress(client_model.email),
            client_model.first_name,
            client_model.last_name,
            client_model.is_company,
        )
        return client_entity
