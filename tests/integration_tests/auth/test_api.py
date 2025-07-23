import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test1@mail.ru", "test1_password", 200),
        ("test2@mail.ru", "test2_password", 200),
        ("test3@mail.ru", "test3_password", 200),
        ("test3@mail.ru", "test3_password", 409),
        ("xyz_mail_ru", "test3_password", 422),
    ],
)
async def test_register(email, password, status_code, ac):
    response = await ac.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test1@mail.ru", "test1_password", 200),
        ("test2@mail.ru", "test2_password", 200),
        ("test3@mail.ru", "test3_password", 200),
        ("test6@mail.ru", "test6_password", 409),
        ("test2@mail.ru", "test1_password", 403),
    ],
)
async def test_login_getme_logout(email, password, status_code, ac):
    # авторизация
    login_response = await ac.post("/auth/login", json={"email": email, "password": password})

    assert login_response.status_code == status_code

    if status_code == 200:
        access_token = login_response.json().get("data")
        assert login_response.json().get("status") == "ok"
        assert access_token

        # информация о себе 1
        me_response = await ac.get("/auth/me")
        me_data = me_response.json().get("data")
        assert me_data
        assert me_data.get("id")
        assert me_data.get("email") == email
        assert me_data.get("password") is None
        assert me_data.get("hashed_password") is None

        # выход
        logout_response = await ac.post("/auth/logout")
        assert logout_response.json().get("status") == "ok"
        assert logout_response.cookies.get("access_token") is None

        # информация о себе 2
        me_response = await ac.get("/auth/me")
        assert me_response.status_code == 401
