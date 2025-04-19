import pytest
from store.models import Game
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_game_creation():
    game = Game.objects.create(
        title='Test Game',
        description='Test Description',
        price=49.99,
        location='JO'
    )
    assert game.title == 'Test Game'
    assert str(game) == 'Test Game'


@pytest.mark.django_db
def test_game_price_validation():
    with pytest.raises(ValidationError):
        game = Game(
            title='Test Game',
            description='Test Description',
            price=-10,
            location='JO'
        )
        game.full_clean()
