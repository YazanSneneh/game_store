from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Game, Order
from .serializers import GameSerializer, OrderSerializer, PurchaseSerializer
from django.core.paginator import Paginator


class GameListView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        location = request.query_params.get('location', None)
        queryset = Game.objects.all()

        if location:
            queryset = queryset.filter(location=location)

        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)

        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = GameSerializer(page_obj, many=True)

        response_data = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'results': serializer.data
        }
        return Response(response_data, status= status.HTTP_200_OK)


class GameDetailView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        game = get_object_or_404(Game, id=serializer.validated_data['game_id'])

        game_purchased = Order.objects.filter(user=request.user, game=game).exists()

        if game_purchased:
            return Response(
                {"error": "You have already purchased this game."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            user=request.user,
            game=game,
            total_price=game.price
        )

        response_data = {
            'message': 'Purchase successful',
            'order': {
                'id': order.id,
                'game': GameSerializer(game).data,
                'total_price': str(order.total_price),
                'purchase_date': order.purchase_date
            }
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-purchase_date')
