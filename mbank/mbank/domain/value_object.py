import re


class InvalidAccountNumber(Exception):
    pass


class AccountNumber(object):

    __value = None

    def __init__(self, number):
        if re.match(r'^\d{2}-\d{3}$', number):
            self.__value = number
        else:
            raise InvalidAccountNumber
