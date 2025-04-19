import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()

@pytest.mark.django_db
def test_login_success(client):
    User.objects.create_user(username='testuser', password='testpass')

    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpass'
    }
    response = client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    assert 'user' in response.data

@pytest.mark.django_db
def test_login_failure(client):
    User.objects.create_user(username='testuser', password='testpass')

    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'wrong_pass'
    }
    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST