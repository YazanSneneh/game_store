from rest_framework import serializers
from .models import Game, Order
from core.serializers import UserSerializer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    user = UserSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class PurchaseSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()

    def validate_game_id(self, value):
        if not Game.objects.filter(id=value).exists():
            raise serializers.ValidationError('Game not found')
        return value
