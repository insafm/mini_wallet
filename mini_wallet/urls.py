from django.urls import path
from .views import InitView, WalletAPIView, WalletTransactionAPIView

app_name = 'mini_wallet'

urlpatterns = [
    path('init', InitView.as_view(), name='init_wallet'),
    path('wallet', WalletAPIView.as_view(), name='wallet'),
    path('wallet/<slug:category>', WalletTransactionAPIView.as_view(), name='wallet_transaction'),
]