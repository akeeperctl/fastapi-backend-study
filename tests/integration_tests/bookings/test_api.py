import pytest


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
async def delete_all_bookings(ac):
    get_response = await ac.get(
        "/bookings"
    )
    bookings = get_response.json().get("data")
    assert bookings
    assert len(bookings) > 0

    for i in bookings:

        id = i.get("id")
        assert id

        delete_response = await ac.delete(f"/bookings/{id}")
        assert delete_response.status_code == 200
        assert delete_response.json().get("status") == "ok"

    response = await ac.get(
        "/bookings"
    )
    bookings = response.json().get("data")
    assert isinstance(bookings, list)
    assert len(bookings) == 0


@pytest.mark.parametrize("room_id, date_from, date_to, status_code, bookings_count", [
    (1, "2025-07-01", "2025-07-10", 200, 1),
    (1, "2025-07-02", "2025-07-11", 200, 2),
    (1, "2025-07-03", "2025-07-12", 200, 3)
])
async def test_add_and_get_my_booking(
        room_id, date_from, date_to, status_code, bookings_count,
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

    assert response.status_code == status_code
    if status_code == 200:
        result = response.json()
        data = result.get("data")

        assert data
        assert isinstance(result, dict)
        assert isinstance(data, dict)

    # получение созданных бронирований
    response = await logged_in_ac.get(
        "bookings/me"
    )

    assert response.status_code == status_code
    if status_code == 200:
        result = response.json()
        data = result.get("data")

        assert isinstance(result, dict)
        assert isinstance(data, list)
        assert len(data) == bookings_count
