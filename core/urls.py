from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import Dashboard, Wallet, SendCrypto, CreateUser, logout_user, ReceiveCrypto


app_name = 'core'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('wallet/', Wallet.as_view(), name='wallet'),
    path('send/', SendCrypto.as_view(), name='crypto_send'),
    path('receive/', ReceiveCrypto.as_view(), name='crypto_receive'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', CreateUser.as_view(), name='register'),
]
