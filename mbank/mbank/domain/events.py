from basehelp.exceptions import CannotChangeValueException
import datetime


class Event(object):
    __version = None
    __created_at = None
    __account_uuid = None
    __client_uuid = None

    # def __init__(self, version=None, created_at=None,):
    #     if self.__version is None and version:
    #         self.set_version(version)
    #     elif self.get_version() != version:
    #         raise CannotChangeValueException
    #
    #     if self.get_created_at() is None:
    #         self.set_created()
    #     elif self.get_created_at() != created_at:
    #         raise CannotChangeValueException
    #     else:
    #         self.set_created(created_at)

    def set_version(self, version):
        if self.__version is None:
            self.__version = version
        else:
            raise CannotChangeValueException

    def get_version(self):
        return self.__version

    def set_created_at(self, created_at=None):
        if self.__created_at is None and created_at is None:
            self.__created_at = datetime.datetime.now()
        elif self.get_created_at() is None and created_at:
            assert isinstance(created_at, datetime.datetime)
            self.__created_at = created_at
        else:
            raise CannotChangeValueException

    def get_created_at(self):
        return self.__created_at

    def set_account_uuid(self, id):
        self.__account_uuid = id

    def get_account_uuid(self):
        return self.__account_uuid

    def set_client_uuid(self, id):
        self.__client_uuid = id

    def get_client_uuid(self):
        return self.__client_uuid

class TransactionEvent(Event):
    __amount = None
    __desc = ''

    def __init__(self, desc=None):
        if desc:
            self.set_desc(desc)

    def set_amount(self,amount):
        self.__amount = amount

    def get_amount(self):
        return self.__amount

    def set_desc(self, desc):
        self.__desc = desc

    def get_desc(self):
        return self.__desc


class DepositEvent(TransactionEvent):
    pass

class WithdrawEvent(TransactionEvent):
    pass

# class CreateClientEvent(Event):
#     __username = None
#     __email_address = None
#     __first_name = None
#     __last_name = None
#     __is_company = None
#     __password = None
#
#     def set_username(self, username):
#         self.__username = username
#
#     def get_username(self):
#         return self.__username
#
#     def set_email_address(self, email):
#         self.__email_address = email
#
#     def get_email_address(self):
#         return self.__email_address
#
#     def set_first_name(self, first_name):
#         self.__first_name = first_name
#
#     def get_first_name(self):
#         return self.__first_name
#
#     def set_last_name(self, last_name):
#         self.__last_name = last_name
#
#     def get_last_name(self):
#         return self.__last_name
#
#     def set_is_company(self, is_company):
#         self.__is_company = is_company
#
#     def get_is_company(self):
#         return self.__is_company
#
#     def set_password(self, password):
#         self.__password = password
#
#     def get_password(self):
#         return self.__password


class CreateAccountEvent(Event):
    __account_number = None
    __balance = None

    # def __init__(self, account_number, client_uuid=None):
    #     self.set_account_number(account_number)
    #     if client_uuid:
    #         self.set_client_uuid(client_uuid)

    def set_account_number(self, account_number):
        self.__account_number = account_number

    def get_account_number(self):
        return self.__account_number

    def set_balance(self, amount):
        self.__balance = amount

    def get_balance(self):
        return self.__balance


# class ChangeAttributeValueEvent(Event):
#     __attibute = None
#     __new_value = None
#
#     def __init__(self, attr, value):
#         self.set_attribute(attr)
#         self.set_new_value(value)
#
#     def set_attribute(self, attr):
#         self.__attibute = attr
#
#     def get_attribute(self):
#         return self.__attibute
#
#     def set_new_value(self, value):
#         self.__new_value = value
#
#     def get_new_value(self):
#         return self.__new_value


class Snapshot(Event):
    __balance = None
    __last_event_varsion = None

    def __init__(self, account):
        super(Snapshot, self).__init__()
        last_version = account.get_last_snaphot_version()
        if last_version is None:
            last_version = 0
        self.set_version(last_version + 1)
        self.set_balance(account.get_balance())
        self.set_last_event_version(account.get_events()[-1].get_version())

    def set_balance(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def set_last_event_varsion(self, version):
        self.__last_event_varsion = version

    def get_last_event_varsion(self):
        return self.__last_event_varsion

