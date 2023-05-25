import pytest
from rest_framework import status

from ads.serializers import AdDetailSerializer


@pytest.mark.django_db
def test_create_ad(client, get_token):
    expected_response = {
        "id": 1,
        "author": None,
        "category": None,
        "name": "test_create_ad",
        "price": 0,
        "description": None,
        "is_published": False,
        "image": None
    }

    data = {
        "name": "test_create_ad",
        "price": 0
    }

    response = client.post("/ad/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post("/ad/",
                           data,
                           content_type='application/json',
                           HTTP_AUTHORIZATION="Bearer " + get_token)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_response

