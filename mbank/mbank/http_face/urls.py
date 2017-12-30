from django.urls import path, re_path
from mbank.http_face import views
from django.contrib.auth.views import login, logout

app_name = 'http_face'
urlpatterns = [
    path('', views.home, name='home'),
    path('cadastre-se/', views.ClientCreateView.as_view(), name='register'),
    path('entrar/', login, {'template_name': 'login.html'}, name='login'),
    path('sair/', logout, {'next_page': 'http_face:home'}, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/criar-conta/',
        views.creating_account, name='add_account'),
    path('dashboard/account_details/<uuid:account_uuid>/',
        views.account_details, name='account_details'),
]
