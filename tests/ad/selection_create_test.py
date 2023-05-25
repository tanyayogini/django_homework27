import pytest
from rest_framework import status


@pytest.mark.django_db
def test_create_selection(client, ad, get_token):
    expected_response = {
        "id": 1,
        "owner": "test",
        "name": "test_selection",
        "items": [ad.id]
    }

    data = {
        "name": "test_selection",
        "items": [ad.id]
    }

    response = client.post("/selection/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post("/selection/",
                           data,
                           content_type='application/json',
                           HTTP_AUTHORIZATION="Bearer " + get_token)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_response
