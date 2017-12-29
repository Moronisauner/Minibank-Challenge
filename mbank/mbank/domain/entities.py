from basehelp.exceptions import InvalidInputsException
from .events import CreateAccountEvent, DepositEvent, WithdrawEvent
from .value_object import AccountNumber, InvalidAccountNumber
import datetime, uuid



class Account(object):
    __uuid = None
    __account_number = None
    __client_uuid = None
    __balance = None
    __last_snapshot_version = None
    __events = None
    __snapshot = None

    def __init__(self, client_uuid, account_number):
        try:
            _account_number = AccountNumber(account_number)
        except InvalidAccountNumber:
            raise InvalidInputsException
        self.set_account_number(_account_number)
        self.set_uuid(uuid.uuid4())
        self.set_client_uuid(client_uuid)
        self.set_balance(0)
        self.__events = []
        self.set_account_number(account_number)
        create_account_event = CreateAccountEvent()
        create_account_event.set_client_uuid(client_uuid)
        create_account_event.set_account_number(account_number)
        self._add_event(create_account_event)

    def set_uuid(self, uuid):
        self.__uuid = uuid

    def get_uuid(self):
        return self.__uuid

    def set_account_number(self, account_number):
        self.__account_number = account_number

    def get_account_number(self):
        return self.__account_number

    def set_client_uuid(self, client_uuid):
        self.__client_uuid = client_uuid

    def get_client_uuid(self):
        return self.__client_uuid

    def set_balance(self, amount):
        self.__balance = amount

    def get_balance(self):
        return self.__balance

    def set_last_snapshot_version(self, last_version):
        self.__last_snapshot_version = last_version

    def get_last_snaphot_version(self):
        return self.__last_snapshot_version

    def set_events(self, events):
        self.__events = events

    def get_events(self):
        return self.__events

    def _add_event(self, event):
        if event.get_version() is None:
            event.set_version(self.next_event_version())
        event.set_account_uuid(self.get_uuid())
        event.set_client_uuid(self.get_client_uuid())
        self.__events.append(event)

    def set_snapshot(self, snaphot):
        self.__snapshot = snaphot

    def get_snapshot(self):
        return self.__snapshot

    def _apply_withdraw(self, event):
        self.__balance -= event.get_amount()

    def _apply_deposit(self, event):
        self.__balance += event.get_amount()

    def _apply(self, event):
        if isinstance(event, DepositEvent):
            self._apply_deposit(event)
        elif isinstance(event, WithdrawEvent):
            self._apply_withdraw(event)

    def apply(self, event_or_events, many=False):

        if many:
            for e in event_or_events:
                self._apply(e)
                self._add_event(e)
        else:
            self._apply(event_or_events)
            self._add_event(event_or_events)

    def deposit(self, amount):
        event = DepositEvent()
        event.set_version(self.next_event_version())
        event.set_amount(amount)
        self.apply(event)

    def withdraw(self, amount):
        event = WithdrawEvent()
        event.set_version(self.next_event_version())
        event.set_amount(amount)
        self.apply(event)

    def next_event_version(self):
        if len(self.get_events()) == 0:
            return 0
        else:
            return (self.get_events()[-1].get_version() or 0) + 1
