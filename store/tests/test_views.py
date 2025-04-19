import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from store.models import Game

User = get_user_model()

# Fixture: create authenticated client
@pytest.fixture
def authenticated_client(db):
    user = User.objects.create_user(
        username='testuser',
        password='testpass'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client

# Fixture: create sample games
@pytest.fixture
def sample_games():
    Game.objects.create(
        title='Game 1',
        description='Desc 1',
        price=10,
        location='JO'
    )
    Game.objects.create(
        title='Game 2',
        description='Desc 2',
        price=20,
        location='SA'
    )


@pytest.mark.django_db
def test_game_list(authenticated_client, sample_games):
    url = reverse('game-list')
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2

@pytest.mark.django_db
def test_game_list_filter(authenticated_client, sample_games):
    url = reverse('game-list')
    response = authenticated_client.get(url, {'location': 'JO'})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['location'] == 'JO'


@pytest.mark.django_db
def test_game_detail_success(authenticated_client):
    game = Game.objects.create(
        title='Test Game',
        description='Test Description',
        price=15,
        location='JO'
    )

    url = reverse('game-detail', args=[game.pk])
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Test Game'
    assert response.data['location'] == 'JO'
    assert response.data['price'] == 15.0


@pytest.mark.django_db
def test_game_detail_not_found(authenticated_client):
    url = reverse('game-detail', args=[999999])  # non-existent pk
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

import pytest
from django.urls import reverse
from rest_framework import status
from store.models import Game, Order

@pytest.mark.django_db
def test_purchase_success(authenticated_client):
    game = Game.objects.create(
        title='New Game',
        description='Test Desc',
        price=30,
        location='JO'
    )

    url = reverse('purchase')
    data = {'game_id': game.id}

    response = authenticated_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'Purchase successful'
    assert response.data['order']['game']['title'] == 'New Game'
    assert Order.objects.count() == 1

@pytest.mark.django_db
def test_purchase_already_bought(authenticated_client):
    game = Game.objects.create(
        title='Old Game',
        description='Test Desc',
        price=25,
        location='SA'
    )

    # Simulate already purchased
    Order.objects.create(user=authenticated_client.handler._force_user, game=game, total_price=25)

    url = reverse('purchase')
    data = {'game_id': game.id}

    response = authenticated_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'already purchased' in response.data['error'].lower()
    assert Order.objects.count() == 1
