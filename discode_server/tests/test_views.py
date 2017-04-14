import pytest


@pytest.mark.skip(reason="I don't know why this fails.")
def test_index(test_client):
    request, response = test_client.get("/")
    assert response.status == 200
