from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4



class UserWallet(models.Model):
    COIN = [
        ('btc', 'btc'),
        ('ltc', 'ltc'),
        ('eth', 'eth'),
    ]

    id = models.UUIDField(default=uuid4, editable=False, primary_key=True, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    balance = models.FloatField()
    address = models.CharField(max_length=50)
    currency = models.CharField(max_length=200, choices=COIN, default=COIN[0][0])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} | {self.currency.upper()} | {self.address}'

    def get_total_balance(self) -> int:
        total = 0
        user_transactions = self.objects.filter(user=self.user)
        for i in user_transactions:
            total + i.balance
        return total


class TransactionHistory(models.Model):
    COIN = [
        ('btc', 'btc'),
        ('ltc', 'ltc'),
        ('eth', 'eth'),
    ]

    TRANSACTION_TYPE = [
        ('out', 'out'),
        ('in', 'in'),
    ]
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True, unique=True)
    transaction_ref = models.CharField(max_length=50, unique=True)
    # wallet = models.ForeignKey(to=UserWallet, on_delete=models.CASCADE)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=3)
    currency = models.CharField(max_length=200, choices=COIN, default=COIN[0][0])
    from_address =  models.CharField(max_length=100)
    to_address =  models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Currency: {self.currency} | Ref: {self.transaction_ref} | Sent From: {self.from_address} | Sent To: {self.to_address}'
    
    def get_total_received(self) -> int:
        total = 0
        user_transactions = self.objects.filter(transaction_type='in')
        for i in user_transactions:
            total + i.amount
        return total

    def get_total_sent(self):
        pass
