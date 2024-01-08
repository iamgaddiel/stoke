from django.contrib import admin
from .models import UserWallet, TransactionHistory


admin.site.register(UserWallet)
admin.site.register(TransactionHistory)
