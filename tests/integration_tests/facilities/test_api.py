async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200


async def test_post_facilities(ac, db):
    title = "Сауна"

    response = await ac.post("/facilities", json={"title": title})

    result = response.json()

    assert result["data"]["title"] == title
    assert result["status"] == "ok"
    assert response.status_code == 200
