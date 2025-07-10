import pytest

from conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2025-07-01", "2025-07-10", 200),
    (1, "2025-07-02", "2025-07-11", 200),
    (1, "2025-07-03", "2025-07-12", 200),
    (1, "2025-07-04", "2025-07-13", 200),
    (1, "2025-07-05", "2025-07-14", 200),
    (1, "2025-07-06", "2025-07-15", 404),
    (1, "2025-07-07", "2025-07-16", 404),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        logged_in_ac
):
    response = await logged_in_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        result = response.json()
        assert isinstance(result, dict)
        assert result.get("status") == "ok"
        assert result.get("data")


@pytest.fixture(scope="session")
async def delete_all_bookings():
    async for db_ in get_db_null_pool():
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, bookings_count", [
    (1, "2025-07-01", "2025-07-10", 1),
    (1, "2025-07-02", "2025-07-11", 2),
    (1, "2025-07-03", "2025-07-12", 3)
])
async def test_add_and_get_my_booking(
        room_id, date_from, date_to, bookings_count,
        logged_in_ac, delete_all_bookings
):
    # создание новых бронирований
    response = await logged_in_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == 200

    result = response.json()
    data = result.get("data")

    assert data
    assert isinstance(result, dict)
    assert isinstance(data, dict)

    # получение созданных бронирований
    response = await logged_in_ac.get("bookings/me")

    result = response.json()
    data = result.get("data")

    assert isinstance(result, dict)
    assert isinstance(data, list)
    assert len(data) == bookings_count
