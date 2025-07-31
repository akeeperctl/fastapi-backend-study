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
    "title, status_code",
    [
        ("Золотой унитаз", 200),
        ("Золотой унитаз", 409),
        (500100, 422),
        ([500100], 422),
        ("Xbox", 200),
        ("PlayStation", 200),
    ]
)
async def test_post_facilities(title, status_code, ac):
    response = await ac.post("/facilities", json={"title": title})
    result = response.json()

    assert response.status_code == status_code
    if status_code == 200:
        data = result.get("data")
        assert result.get("status") == "ok"
        assert data
        assert isinstance(data, dict)
        assert data.get("title") == title
