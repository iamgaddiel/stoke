from typing import Any
from uuid import uuid4
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db.models.query import Q

from .models import TransactionHistory, UserWallet
from .forms import SendCryptoModelForm





def get_random_text(legnth: int) -> str:
    return uuid4().hex[:legnth]


class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'core/dashboard.html'

    def get_queryset(self) -> QuerySet[Any]:
        return TransactionHistory.objects.filter(pk=self.request.user.pk)


class Wallet(LoginRequiredMixin, ListView):
    template_name = 'core/wallet.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        return UserWallet.objects.filter(user=self.request.user.pk)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user_wallets = self.get_queryset()
        eth_wallet_address = user_wallets.get(currency='eth').address
        btc_wallet_address = user_wallets.get(currency='btc').address
        ltc_wallet_address = user_wallets.get(currency='ltc').address

        all_sent_transaction = TransactionHistory.objects.filter(
            Q(from_address=eth_wallet_address) | 
            Q(from_address=btc_wallet_address) | 
            Q(from_address=ltc_wallet_address) 
        ).order_by('-created_at')

        all_received_transaction = TransactionHistory.objects.filter(
            Q(to_address=eth_wallet_address) | 
            Q(to_address=btc_wallet_address) | 
            Q(to_address=ltc_wallet_address) 
        ).order_by('-created_at')

        # Get Total User Wallet Balance
        total_balance = 0.0
        for wallet in user_wallets: total_balance += wallet.balance

        total_sent_amount = 0.0
        for transaction in all_sent_transaction: total_sent_amount += transaction.amount

        total_received_amount = 0.0
        for transaction in all_received_transaction: total_received_amount += transaction.amount

        
        # Contexts]------------------------------------------
        # Sent Transactions
        context['all_sent_transactions'] = all_sent_transaction
        context['sent_eth_transactions'] = TransactionHistory.objects.filter(from_address=eth_wallet_address).order_by('-created_at')
        context['sent_btc_transactions'] = TransactionHistory.objects.filter(from_address=btc_wallet_address).order_by('-created_at')
        context['sent_ltc_transactions'] = TransactionHistory.objects.filter(from_address=ltc_wallet_address).order_by('-created_at')

        # Received Transactions
        context['all_received_transaction'] = all_received_transaction
        context['received_eth_transactions'] = TransactionHistory.objects.filter(to_address=eth_wallet_address).order_by('-created_at')
        context['received_btc_transactions'] = TransactionHistory.objects.filter(to_address=btc_wallet_address).order_by('-created_at')
        context['received_ltc_transactions'] = TransactionHistory.objects.filter(to_address=ltc_wallet_address).order_by('-created_at')
        
        # Totals
        context['total_balance'] = total_balance
        context['total_sent_amount'] = total_sent_amount
        context['total_received_amount'] = total_received_amount
        return context


class SendCrypto(LoginRequiredMixin, CreateView):
    template_name = 'core/crypto_send.html'
    form_class = SendCryptoModelForm

    def get_queryset(self) -> QuerySet[Any]:
        return UserWallet.objects.filter(user=self.request.user.pk)

    def get_success_url(self) -> str:
        return resolve_url('core:wallet')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        try:
            send_amount = int(form.cleaned_data.get('amount'))
            currency = form.data.get('currency')
            address = form.data.get('address')
            wallet = UserWallet.objects.get(user=self.request.user.pk, currency=currency)
            recipient_wallet = UserWallet.objects.get(address=address)

            # check if send_amount is less than user wallet balance
            if send_amount > wallet.balance:
                return render(
                        self.request, 
                        'core/crypto_send.html', 
                        {
                            'form': form, 
                            'error': f'Insufficient {currency.upper()} balance', 
                            'wallets': UserWallet.objects.filter(user=self.request.user.pk)
                        }
                    )
        
            # deduct send_amount from user wallet balance
            wallet.balance -= send_amount
            wallet.save()

            # add send_amount from user to recipient's balance
            recipient_wallet.balance += send_amount
            recipient_wallet.save()

            form.instance.transaction_ref = get_random_text(20)
            form.instance.transaction_type = 'out'
            form.instance.from_address = wallet.address
            form.instance.to_address = address
            form.instance.currency = currency
            
            return super().form_valid(form)
        
        except UserWallet.DoesNotExist:
            return render(
                        self.request, 
                        'core/crypto_send.html', 
                        {
                            'form': form, 
                            'error': f'Invalid wallet address', 
                            'wallets': UserWallet.objects.filter(user=self.request.user.pk)
                        }
                    )

    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['wallets'] = UserWallet.objects.filter(user=self.request.user.pk)
        return context


class ReceiveCrypto(LoginRequiredMixin, ListView):
    template_name = 'core/crypto_receive.html'

    def get_queryset(self) -> QuerySet[Any]:
        return UserWallet.objects.filter(user=self.request.user.pk)


class CreateUser(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'core/register.html'
    success_url = '/login'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        # Create 3 User Wallets
        user = form.save()
        # ETH Wallet--------------------------------
        UserWallet.objects.create(
            user=user,
            balance=0.0,
            address=uuid4(),
            currency='eth',
        )
        # BTC Wallet--------------------------------
        UserWallet.objects.create(
            user=user,
            balance=0.0,
            address=uuid4(),
            currency='btc',
        )
        # LTH Wallet--------------------------------
        UserWallet.objects.create(
            user=user,
            balance=0.0,
            address=uuid4(),
            currency='ltc',
        )
        return super().form_valid(form)

def logout_user(request):
    logout(request)
    return redirect('core:login')