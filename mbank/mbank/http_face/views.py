from django.shortcuts import render, redirect
from django.views.generic import View
from .domain_service import ClientCreateService
from .forms import CreateClientForm
from basehelp.exceptions import InvalidInputsException


class ClientCreateView(View):

    template_name = "register.html"

    def get(self, request, *args, **kwargs):

        create_client_form = CreateClientForm()
        context = {
            'form': create_client_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        is_company = request.POST.get("is_company")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        client_create_service = ClientCreateService()

        try:
            client_create_service.run(
                username,
                email,
                first_name,
                last_name,
                is_company,
                password1,
                password2,
            )
            redirect('home')
        except InvalidInputsException:
            context = {
                'form': client_create_service.get_form()
            }

        return render(request, self.template_name, context)
