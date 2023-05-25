import pytest
from rest_framework import status

from ads.serializers import AdDetailSerializer


@pytest.mark.django_db
def test_retrieve_ad(client, ad, get_token):
    response = client.get(f"/ad/{ad.id}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get(f"/ad/{ad.id}/",
                          HTTP_AUTHORIZATION="Bearer " + get_token)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == AdDetailSerializer(ad).data
