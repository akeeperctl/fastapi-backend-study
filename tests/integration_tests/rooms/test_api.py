import pytest


@pytest.mark.parametrize(
    "hotel_id, date_from, date_to, room_count, status_code",
    [
        (1, "2025-07-30", "2025-08-07", 2, 200),
        (2, "2025-07-30", "2025-08-07", 1, 200),
        (3, "2025-07-30", "2025-08-07", 1, 200),
        (4, "2025-07-30", "2025-08-07", 0, 404),
        (5, "2025-07-30", "2025-08-07", 0, 404),
        (-1, "2025-07-30", "2025-08-07", 0, 422),
        (0, "2025-07-30", "2025-08-07", 0, 422),
    ],
)
async def test_get_rooms(hotel_id, date_from, date_to, room_count, status_code, ac):
    response = await ac.get(
        f"hotels/{hotel_id}/rooms",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
    if status_code == 200:
        data = response.json().get("data")
        assert data
        assert len(data) == room_count


# 422 код получается из проверки facilities
# 404 код получается из проверки hotel_id
@pytest.mark.parametrize(
    "hotel_id, description, title, quantity, price, facilities, status_code",
    [
        (1, "Test room desc", "Test room title", 5, 999, [], 200),
        (10, "Test room desc", "Test room title", 5, 999, [], 404),
        (2, "Test room desc", "Test room title", 4, 888, [0], 422),
        (3, "Test room desc", "Test room title", 3, 777, [-1], 422),
        (0, "Test room desc", "Test room title", 2, 666, [], 422),
        (1, "Test room desc", "Test room title", -1, 555, [], 422),
        (1, "Test room desc", "Test room title", 0, 555, [], 422),
        (0, "Test room desc", "Test room title", 1, 0, [], 422),
        (1, "Test room desc", "Test room title", -1, -55, [], 422),
    ],
)
async def test_create_and_delete_room(
    hotel_id, description, title, quantity, price, facilities, status_code, ac
):
    # create
    response = await ac.post(
        f"hotels/{hotel_id}/rooms",
        json={
            "title": title,
            "description": description,
            "price": price,
            "quantity": quantity,
            "facilities_ids": facilities,
        },
    )

    assert response.status_code == status_code
    if status_code == 200:
        result = response.json()
        data = result.get("data")
        status = result.get("status")
        assert data
        assert status == "ok"
        assert isinstance(data, dict)
        room_id = data.get("id")
        assert room_id
        assert data.get("hotel_id") == hotel_id
        assert data.get("description") == description
        assert data.get("title") == title
        assert data.get("quantity") == quantity
        assert data.get("price") == price

        check_response = await ac.get(
            f"hotels/{hotel_id}/rooms/{room_id}",
        )
        assert check_response.status_code == status_code
        check_data = check_response.json().get("data")
        assert check_data
        assert isinstance(check_data, dict)
        assert check_data.get("facilities") == facilities

        # delete
        delete_response = await ac.delete(f"hotels/{hotel_id}/rooms/{room_id}")
        delete_result = delete_response.json()
        assert delete_response.status_code == 200
        assert delete_result.get("status") == "ok"


@pytest.mark.parametrize(
    "hotel_id, room_id, status_code",
    [
        (1, 1, 200),
        (1, 2, 200),
        (2, 3, 200),
        (3, 4, 200),
        (4, 1, 404),
        (3, 2, 404),
    ],
)
async def test_read_room(hotel_id, room_id, status_code, ac):
    response = await ac.get(
        f"hotels/{hotel_id}/rooms/{room_id}",
    )
    assert response.status_code == status_code
    if status_code == 200:
        result = response.json()
        data = result.get("data")
        status = result.get("status")
        assert status
        assert status == "ok"
        assert data
        assert isinstance(data, dict)
        assert data.get("hotel_id") == hotel_id


@pytest.mark.parametrize(
    "hotel_id, room_id, description, title, status_code",
    [
        (1, 1, "Patched1", "Patched2", 200),
        (1, 2, "dsdkm", "Patched3", 200),
        (2, 3, "Shreck", "Patched_xyz", 200),
        (3, 4, "Osel", "", 200),
        (4, 1, "Potato", "Killbox", 404),
        (3, 2, "Pizza", "Shock", 404),
    ],
)
async def test_patch_room(hotel_id, room_id, description, title, status_code, ac):
    get_response = await ac.get(
        f"hotels/{hotel_id}/rooms/{room_id}",
    )
    assert get_response.status_code == status_code
    if status_code != 200:
        return

    result = get_response.json()
    status = result.get("status")
    old_data = result.get("data")
    assert status == "ok"
    assert old_data
    assert isinstance(old_data, dict)

    patch_response = await ac.patch(
        f"hotels/{hotel_id}/rooms/{room_id}",
        json={
            "title": title,
            "description": description,
        },
    )
    assert patch_response.status_code == status_code

    patch_check_response = await ac.get(
        f"hotels/{hotel_id}/rooms/{room_id}",
    )
    assert patch_check_response.status_code == status_code
    patch_check_data = patch_check_response.json().get("data")
    assert patch_check_data
    assert isinstance(patch_check_data, dict)
    assert patch_check_data.get("title") == title
    assert patch_check_data.get("description") == description
    assert patch_check_data.get("quantity") == old_data.get("quantity")
    assert patch_check_data.get("price") == old_data.get("price")


@pytest.mark.parametrize(
    "hotel_id, room_id, description, title, quantity, price, facilities, status_code",
    [
        (1, 1, "Test room desc edit", "Test room title edit", 5, 999, [1, 2], 200),
        (1, 2, "Test room desc edit", "Test room title edit", 2, 323, [3, 1], 200),
        (1, 101, "Test room desc edit", "Test room title edit", 1, 100, [1], 404),
        (1, 3, "Test room desc edit", "Test room title edit", 1, 100, [-1], 422),
        (1, 3, "Test room desc edit", "Test room title edit", 1, 100, [0], 422),
        (1, 3, "Test room desc edit", "Test room title edit", 1, -100, [1, 2], 422),
        (1, 3, "Test room desc edit", "Test room title edit", -1, 100, [1, 2], 422),
    ],
)
async def test_edit_room(
    hotel_id, room_id, description, title, quantity, price, facilities, status_code, ac
):
    put_response = await ac.put(
        f"hotels/{hotel_id}/rooms/{room_id}",
        json={
            "title": title,
            "description": description,
            "price": price,
            "quantity": quantity,
            "facilities_ids": facilities,
        },
    )

    assert put_response.status_code == status_code
    if status_code == 200:
        put_check_response = await ac.get(
            f"hotels/{hotel_id}/rooms/{room_id}",
        )
        assert put_check_response.status_code == status_code

        put_check_data = put_check_response.json().get("data")
        assert put_check_data
        assert isinstance(put_check_data, dict)
        assert put_check_data.get("title") == title
        assert put_check_data.get("description") == description
        assert put_check_data.get("quantity") == quantity
        assert put_check_data.get("price") == price

        _facilities = put_check_data.get("facilities")
        assert _facilities
        assert isinstance(_facilities, list)
        assert len(_facilities) == len(facilities)
        for _facility in _facilities:
            assert isinstance(_facility, dict)
            assert _facility["id"] in facilities
