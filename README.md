Minibank-Challenge
====
Django, CQRS, Event Sourcing, DDD

O projeto mescla aplica os conceitos de CQRS, Event Sourcing e DDD com os recursos do Django. Ainda há pequenas falhas que serão corrigidas, porem essas falhas não interferem na arquitetura hexagonal.

Os módudos armazenam:
as entidades no arquivo entities.py
os repositorios no aquivo repository.py
os modelos usados pelo ORM no aquivo models.py
os Use Case no arquivo use_case.py
os serviços em domain_service.py
os objetos de valor em value_object.py
os demais arquivos são para uso do framework


Install
=======

    virtualenv minibank --python=python3
    cd minibank
    . bin/activate
    pip install -r requeriments.txt


Autenticação
==========
autenticação padrão do Django, porém a persistencia é feita por repository.py que cuida desta tarefa.

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

CQRS
==========
 
Commands

mbank.domain.repository.py
```py
    def _prepare_to_save(self, event):
        """
        converte adequadamente a subclasse de Event para ser armazenada
        no banco de dados
        :param event:
        :return: EventModel
        """
        if not issubclass(event.__class__, Event):
            raise Exception

        if isinstance(event, WithdrawEvent):
            return EventModel(
                event_type='WithdrawEvent',
                account_uuid=event.get_account_uuid(),
                client_uuid=event.get_client_uuid(),
                body=json.dumps({
                    'amount': event.get_amount(),
                    'desc': event.get_desc(),
                }),
                version=event.get_version(),
                created_at = event.get_created_at(),
            )
        elif isinstance(event, DepositEvent):
            return EventModel(
                event_type='DepositEvent',
                account_uuid=event.get_account_uuid(),
                client_uuid=event.get_client_uuid(),
                body=json.dumps({
                    'amount': event.get_amount(),
                    'desc': event.get_desc(),
                }),
                version=event.get_version(),
                created_at = event.get_created_at(),
            )
        elif isinstance(event, CreateAccountEvent):
            return EventModel(
                event_type='CreateAccountEvent',
                account_uuid=event.get_account_uuid(),
                client_uuid=event.get_client_uuid(),
                body=json.dumps({
                    'account_number': event.get_account_number(),
                }),
                version=event.get_version(),
                created_at = event.get_created_at(),
            )
```



Querys

mbank.domain.repository.py
```py

    def create(self, account):
        account_events = account.get_events()
        for e in account_events:
            if EventModel.objects.filter(
                    account_uuid=e.get_account_uuid(),
                    version=e.get_version()).exists() == True:
                break
            event_model = self._prepare_to_save(e)
            event_model.save()

    def __load_entity(self, events_model):
        """
        Converte uma lista de EventModel para um Account
        :param events_model:
        :return Account
        """
        events = []
        account_number = None
        client_uuid = None
        account_uuid = None

        for e in events_model:
            if e.event_type == 'CreateAccountEvent':
                event = self._load_create_account_event(e)
                account_number = event.get_account_number()
                account_uuid = event.get_account_uuid()
                client_uuid = event.get_client_uuid()
                events.append(event)
            elif e.event_type == 'DepositEvent':
                event = self._load_deposit_event(e)
                events.append(event)

            elif e.event_type == 'WithdrawEvent':
                event = self._load_withdraw_event(e)
                events.append(event)
        acc = Account(client_uuid, account_number)
        acc.set_uuid(account_uuid)
        acc.set_events([])
        acc.apply(events, True)
        return acc
```
 
 
Banco de Dados
==========
Configure o banco de dados postgres 

mbank.settings.py
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'minibank', # nome da base de dados
        'HOST': 'localhost', # servidor
        'PORT': '5432', # porta padrao postgres
        'USER': 'postgres', # usuario com privilegios de super usuario
        'PASSWORD': 'minhasenha' # senha do usuario
    }
}
```
