from django.urls import path
from .views import GameListView, GameDetailView, PurchaseView, OrderHistoryView

urlpatterns = [
    path('games/', GameListView.as_view(), name='game-list'),
    path('games/<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path('orders/', OrderHistoryView.as_view(), name='order-history'),
]