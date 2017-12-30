from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.forms.forms import ValidationError
from basehelp.exceptions import InvalidInputsException
from mbank.client.domain_service import ClientCreateService
from mbank.client.forms import CreateClientForm
# from mbank.client.use_case import ClientUseCase
from mbank.domain.use_case import AccountUseCase
from mbank.domain.repository import DomainRepo
from mbank.domain.forms import CreateAccountForm, TransactionForm
from mbank.domain.domain_service import CreateAccountService



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
            redirect('http_face:home')
        except InvalidInputsException:
            context = {
                'form': client_create_service.get_form()
            }

        return render(request, self.template_name, context)

def home(request):
    template_name = 'index.html'
    return render(request, template_name)

@login_required
def dashboard(request):
    account_use_case = AccountUseCase(DomainRepo())
    context = {}
    context['accounts'] = account_use_case.find_all_client_accounts(request.user)
    return render(request, 'dashboard.html', context)


@login_required
def account_details(request, account_uuid):
    repo = DomainRepo()
    account_use_case = AccountUseCase(repo)
    account = account_use_case.find_account_by_uuid(account_uuid)

    if account.get_client_uuid() != request.user.uuid:
        redirect('http_face:dashboard')

    context = {
        'accounts': account_use_case.find_all_client_accounts(request.user),
        'account': account,
        'transactions': account.get_transactions_events()
    }

    form = TransactionForm(request.POST or None)
    if form.is_valid():
        """
        django tem uma falha ao retornar valores de choice_field
        retornando os todos os valores como string, dificultando a comparação
        convertendo a string para o tipo desejado, como float(form.data.get('amount'))
        ou 
        import json
        json.loads(form.data.get('field'))
        
        lembrando que a função json.loads() produz erro ao converter a string "True",
        porem pode ser usando numa string "True".lower()
        """

        if form.data.get('transction_type') == 'True':
            account.deposit(float(form.data.get('amount')))
        elif form.data.get('transction_type') == 'False':
            account.withdraw(float(form.data.get('amount')))
        repo.update(account)
        context['transactions'] = account.get_transactions_events()
    context['form'] = form
    print(context)
    return render(request, 'account_details.html', context)


# @login_required
# def snapshot(request, account_id):
#     account = get_object_or_404(Account, id=account_id)
#     account.takeSnapshot()
#     return redirect('presentation:dashboard')


@login_required
def creating_account(request):
    form = CreateAccountForm(request.POST or None)
    context = {'form':form}
    account_use_case = AccountUseCase(DomainRepo())

    if request.method == 'POST':
        create_account_service = CreateAccountService()
        try:
            account_number = form.data['account_number']
            create_account_service.run(request.user.uuid, account_number)
            redirect('http_face:dashboard')
        except ValidationError:
            context['form'] = create_account_service.get_form()
    context['accounts'] = account_use_case.find_all_client_accounts(request.user)

    return render(request, 'creating_account.html', context)
