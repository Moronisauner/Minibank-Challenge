from .entities import Account
from .events import Event, Snapshot, WithdrawEvent, DepositEvent, CreateAccountEvent
from .models import EventModel
from basehelp.repositories import AbstractRepository
import json, uuid


class DomainRepo(AbstractRepository):

    def find_all(self):
        """
        :return: [Account]
        """
        values = EventModel.objects.values('account_uuid')
        result = []
        for account_uuid in values:
            result.append(self.find_by_id(account_uuid.get('account_uuid')))
        return result

    def find_by_id(self, account_uuid):
        """
        :param account_uuid:
        :return: Account
        """
        events = EventModel.objects.filter(account_uuid=account_uuid) .order_by('version')
        acc = self.__load_entity(events)
        return acc

    def find_by_client_uuid(self, client_uuid):
        """

        :param client_uuid:
        :return: [Account]
        """
        values = EventModel.objects.filter(event_type='CreateAccountEvent', client_uuid=client_uuid).values('account_uuid')
        result = []
        for account_uuid in values:
            result.append(self.find_by_id(account_uuid.get('account_uuid')))
        return result

    def create(self, account):
        account_events = account.get_events()
        for e in account_events:
            if EventModel.objects.filter(
                    account_uuid=e.get_account_uuid(),
                    version=e.get_version()).exists() == True:
                break
            event_model = self._prepare_to_save(e)
            event_model.save()

    def update(self, account):
        # TODO fazer isso de forma mais inteligente
        # por enquanto o metodo apenas deixa de salvar EventModels
        # que foram salvos anteriomente

        account_events = account.get_events()
        for e in account_events:
            if EventModel.objects.filter(
                    account_uuid=e.get_account_uuid(),
                    version=e.get_version()).exists():
                continue
            event_model = self._prepare_to_save(e)
            event_model.save()

    def delete(self, account_uuid):
        EventModel.objects.filter(account_uuid=account_uuid).delete()

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
                version=event.get_version()
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
                version=event.get_version()
            )
        elif isinstance(event, CreateAccountEvent):
            return EventModel(
                event_type='CreateAccountEvent',
                account_uuid=event.get_account_uuid(),
                client_uuid=event.get_client_uuid(),
                body=json.dumps({
                    'account_number': event.get_account_number()
                }),
                version=event.get_version()
            )

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

    def _load_create_account_event(self, event_model):
        data = json.loads(event_model.body)
        account_number = data.get('account_number')
        account_uuid = event_model.account_uuid
        event = CreateAccountEvent()
        event.set_account_number(account_number)
        event.set_account_uuid(account_uuid)
        event.set_client_uuid(event_model.client_uuid)
        event.set_version(event_model.version)
        return event

    def _load_deposit_event(self, event_model):
        data = json.loads(event_model.body)
        amount = data.get('amount')
        desc = data.get('desc')
        account_uuid = event_model.account_uuid
        client_uuid = event_model.client_uuid

        event = DepositEvent()
        event.set_client_uuid(client_uuid)
        event.set_account_uuid(account_uuid)
        event.set_version(event_model.version)
        event.set_amount(amount)
        event.set_desc(desc)
        return event

    def _load_withdraw_event(self, event_model):
        data = json.loads(event_model.body)
        amount = data.get('amount')
        desc = data.get('desc')
        account_uuid = event_model.account_uuid
        client_uuid = event_model.client_uuid

        event = WithdrawEvent()
        event.set_client_uuid(client_uuid)
        event.set_account_uuid(account_uuid)
        event.set_version(event_model.version)
        event.set_amount(amount)
        event.set_desc(desc)
        return event
