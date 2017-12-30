from .entities import Client
from .forms import CreateClientForm
from .use_case import ClientUseCase
from .models import ClientModel
from .repository import ClientRepo
from .value_object import EmailAddress
from basehelp.exceptions import InvalidInputsException


class ClientCreateService(object):

    __client_create_form = None

    def run(self, username, email, first_name, last_name, is_company, password1, password2):
        inputs = {
            'username': username,
            'email_address': email,
            'first_name': first_name,
            'last_name': last_name,
            'is_company': is_company,
            'password1': password1,
            'password2': password2,
        }

        client_create_form = CreateClientForm(inputs)
        self.__client_create_form = client_create_form

        if client_create_form.is_valid():
            client_use_case = ClientUseCase(ClientRepo())
            try:
                client = ClientModel.objects.get(username=username)
                client = ClientModel.objects.get(email=email)
            except ClientModel.DoesNotExist:
                new_client = Client(
                    username=username,
                    email=EmailAddress(email),
                    first_name=first_name,
                    last_name=last_name,
                    is_company=is_company,
                    password=password1
                )
                client_use_case.create(new_client)
        else:
            raise InvalidInputsException

    def get_form(self):
        return self.__client_create_form
