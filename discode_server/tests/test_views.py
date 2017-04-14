async def test_index(test_client):
    request, response = await test_client.get("/")
    assert response.status == 200
