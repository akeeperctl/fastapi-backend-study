import pytest
from loguru import logger


@pytest.mark.parametrize(
    "date_from, date_to, hotels_count, status_code",
    [
        ("2025-07-01", "2025-09-28", 3, 200),
    ]
)
async def test_get_hotels(date_from, date_to, hotels_count, status_code, ac):
    response = await ac.get(
        "/hotels",
        # query параметры
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code

    result = response.json()
    hotels = result.get("data")

    assert result.get("status") == "ok"
    assert hotels
    assert isinstance(hotels, list)
    assert len(hotels) == hotels_count


# TODO
# create
@pytest.mark.parametrize(
    "title, location, status, status_code",
    [
        ("Отель 5 звезд у моря", "Сочи", "ok", 200),
        ("Отель 5 звезд у песка", "Дубай", "ok", 200),
    ]
)
async def test_create_and_delete_hotel(title, location, status, status_code, ac):
    # create
    create_response = await ac.post(
        "/hotels",
        json={
            "title": title,
            "location": location
        },
    )
    create_result = create_response.json()
    create_data = create_result.get("data")
    assert create_response.status_code == status_code
    assert create_result.get("status") == status
    assert create_data
    assert isinstance(create_data, dict)
    assert create_data.get("title") == title
    assert create_data.get("location") == location
    created_hotel_id = create_data.get("id")
    assert created_hotel_id
    logger.debug(f"Создан отель {created_hotel_id}")

    # delete
    delete_response = await ac.delete(
        f"/hotels/{created_hotel_id}",
    )
    assert delete_response.status_code == status_code
    assert delete_response.json().get("status") == status
    logger.debug(f"Удален отель {created_hotel_id}")


# read
@pytest.mark.parametrize(
    "hotel_id, status_code",
    [
        (1, 200),
        (2, 200),
        (3, 200),
        (4, 404),
        (5, 404),
        (6, 404),
        (-1, 422),
        (0, 422),
    ]
)
async def test_get_hotel(hotel_id, status_code, ac):
    response = await ac.get(
        f"/hotels/{hotel_id}",
    )
    assert response.status_code == status_code
    if status_code == 200:
        result = response.json()
        data = result.get("data")
        assert data
        assert isinstance(data, dict)
        assert result.get("status") == "ok"


@pytest.mark.parametrize(
    "hotel_id, title, location, status_code",
    [
        (1, "Тестовое название отеля", "Тестовый город", 200),
        (2, "Домик у моря 5 звезд", "Сочи", 200),
        (3, "Дом правды", "Алтай", 200),
        (4, "Отель 5 звезд Императрица", "Санкт-Петербург", 404),
        (-1, "Тестовое название отеля", "Тестовый город", 422),
        (0, "Тестовое название отеля", "Тестовый город", 422),
    ]
)
async def test_edit_hotel(hotel_id, title, location, status_code, ac):
    # edit
    edit_response = await ac.put(
        f"/hotels/{hotel_id}",
        json={
            "title": title,
            "location": location,
        }
    )
    assert edit_response.status_code == status_code
    if status_code == 200:
        assert edit_response.json().get("status") == "ok"

        # check
        check_response = await ac.get(
            f"/hotels/{hotel_id}",
        )
        assert check_response.status_code == status_code
        if status_code == 200:
            check_data = check_response.json().get("data")
            assert check_data
            assert isinstance(check_data, dict)
            assert check_data.get("title") == title
            assert check_data.get("location") == location


@pytest.mark.parametrize(
    "hotel_id, title, location, status_code",
    [
        (1, "Тестовое название отеля", "Тестовый город", 200),
        (2, "Домик у моря 5 звезд", "Сочи", 200),
        (3, "Дом правды", "Алтай", 200),
        (4, "Отель 5 звезд Императрица", "Санкт-Петербург", 404),
        (-1, "Тестовое название отеля", "Тестовый город", 422),
        (0, "Тестовое название отеля", "Тестовый город", 422),
    ]
)
async def test_patch_hotel(hotel_id, title, location, status_code, ac):
    # старые данные
    old_response = await ac.get(
        f"/hotels/{hotel_id}",
    )
    assert old_response.status_code == status_code
    if status_code != 200:
        return

    old_data = old_response.json().get("data")
    assert old_data
    assert isinstance(old_data, dict)

    # patch
    patch_response = await ac.patch(
        f"/hotels/{hotel_id}",
        json={
            "title": title,
        }
    )
    assert patch_response.status_code == status_code
    if status_code == 200:
        assert patch_response.json().get("status") == "ok"

        # check
        check_response = await ac.get(
            f"/hotels/{hotel_id}",
        )
        assert check_response.status_code == status_code
        if status_code == 200:
            check_data = check_response.json().get("data")
            assert check_data
            assert isinstance(check_data, dict)
            assert check_data.get("title") == title
            assert check_data.get("location") == old_data.get("location") and check_data.get("location") is not None
