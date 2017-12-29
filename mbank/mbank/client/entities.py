import uuid
from .value_object import EmailAddress


class Client(object):
    __uuid = None
    __username = None
    __email_address = None
    __first_name = None
    __last_name = None
    __is_company = None
    __password = None

    def __init__(self, username,
                 email, first_name, last_name, is_company, password):
        if not isinstance(email, EmailAddress):
            raise Exception

        self.__username = username
        self.__email_address = email
        self.__first_name = first_name
        self.__last_name = last_name
        self.__is_company = is_company
        self.__password = password

    def set_uuid(self, uuid):
        self.__uuid = uuid

    def get_uuid(self):
        return self.__uuid

    def set_username(self, username):
        self.__username = username

    def get_username(self):
        return self.__username

    def set_email_address(self, email):
        self.__email_address = email

    def get_email_address(self):
        return self.__email_address

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def get_first_name(self):
        return self.__first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def get_last_name(self):
        return self.__last_name

    def set_is_company(self, is_company):
        self.__is_company = is_company

    def get_is_company(self):
        return  self.__is_company

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password
