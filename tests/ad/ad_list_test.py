import pytest
from rest_framework import status

from ads.serializers import AdListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client):
    ads = AdFactory.create_batch(5)
    expected_response = {
        "count": 5,
        "next": None,
        "previous": None,
        "results": AdListSerializer(ads, many=True).data}

    response = client.get("/ad/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response
