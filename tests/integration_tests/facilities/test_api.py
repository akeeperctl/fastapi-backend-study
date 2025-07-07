async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities"
    )

    assert response.status_code == 200


async def test_post_facilities(ac, db):
    title = "Сауна"

    response = await ac.post(
        "/facilities",
        json={"title": title}
    )

    facility = (await db.facilities.get_all())[0]

    assert facility.title == title
    assert response.status_code == 200
