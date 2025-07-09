async def test_add_booking(db, logged_in_ac):
    room_id = (await db.rooms.get_all())[0]
    for _ in range(5):
        response = await logged_in_ac.post(
            "/bookings",
            json={
                "room_id": room_id,
                "date_from": "2025-07-01",
                "date_to": "2025-07-10",
            }
        )

        result = response.json()

        assert isinstance(result, dict)
        assert result.get("status") == "ok"
        assert result.get("data")
        assert response.status_code == 200

