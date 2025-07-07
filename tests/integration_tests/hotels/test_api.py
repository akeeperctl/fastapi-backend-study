async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",

        # query параметры
        params={
            "date_from": "2025-07-01",
            "date_to": "2025-07-10",
        }
    )

    assert response.status_code == 200