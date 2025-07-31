import pytest


async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    result = response.json()

    assert response.status_code == 200
    data = result.get("data")
    assert result.get("status") == "ok"
    assert data
    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.parametrize(
    "title, created_status_code, deleted_status_code",
    [
        ("Золотой унитаз", 200, 200),
        (500100, 422, 0),
        ([500100], 422, 0),
        ("", 422, 0),
        ("Xbox", 200, 200),
        ("PlayStation", 200, 200),
        ("PlayStation", 200, 200),
    ]
)
async def test_create_and_delete_facilities(title, created_status_code, deleted_status_code, ac):
    # create
    response = await ac.post("/facilities", json={"title": title})
    result = response.json()

    assert response.status_code == created_status_code
    if created_status_code == 200:
        data = result.get("data")
        assert result.get("status") == "ok"
        assert data
        assert isinstance(data, dict)
        assert data.get("title") == title
        facility_id = data.get("id")
        assert facility_id

        # delete
        response = await ac.delete(f"/facilities/{facility_id}")
        result = response.json()

        assert response.status_code == deleted_status_code
        if deleted_status_code == 200:
            assert result.get("status") == "ok"


@pytest.mark.parametrize(
    "title, status_code",
    [
        ("Золотой унитаз", 200),
        ("Золотой унитаз", 409),
        (500100, 422),
        ([500100], 422),
        ("", 422),
        ("Xbox", 200),
        ("PlayStation", 200),
        ("PlayStation", 409),
    ]
)
async def test_create_facilities(title, status_code, ac):
    # create
    response = await ac.post("/facilities", json={"title": title})
    result = response.json()

    assert response.status_code == status_code
    if status_code == 200:
        data = result.get("data")
        assert result.get("status") == "ok"
        assert data
        assert isinstance(data, dict)
        assert data.get("title") == title
        facility_id = data.get("id")
        assert facility_id
