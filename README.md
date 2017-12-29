Minibank-Challenge
====
Django, CQRS, Event Sourcing, DDD


Install
=======

    virtualenv minibank --python=python3
    cd minibank
    . bin/activate
    pip install -r requeriments.txt


Autenticação
==========
 autenticação padrão do Django, porém a persistencia é feita por repository.py que cuida desta tarefa

mbank.client.repository.py
```py
class ClientRepo(AbstractRepository):
    def create(self, client):
        client_model = ClientModel(
            username=client.get_username(),
            email=client.get_email_address(),
            first_name=client.get_first_name(),
            last_name=client.get_last_name(),
            is_company=bool(client.get_is_company()),
        )
        client_model.set_password(client.get_password())
        client_model.save()
        
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
```

