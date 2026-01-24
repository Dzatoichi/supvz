import pytest
from httpx import AsyncClient

PERMISSIONS_URL = "/permissions"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, expected_status, expected_msg_part",
    [
        ({"position_id": "not-an-int"}, 422, "valid integer"),
        ({"user_id": "abc"}, 422, "valid integer"),
        ({"position_source": "invalid_source", "position_id": 1}, 422, "Input should be 'system' or 'custom'"),
    ],
    ids=[
        "invalid_position_id_type",
        "invalid_user_id_type",
        "invalid_position_source_enum",
    ],
)
async def test_get_permissions_validation_errors(
    client: AsyncClient,
    params: dict,
    expected_status: int,
    expected_msg_part: str,
):
    """
    Тест: Ошибки валидации query-параметров.
    GET /permissions/?{invalid_params}

    Сценарий:
    1. Отправляем запрос с невалидными параметрами.
    2. Проверяем статус 422.
    3. Ищем ожидаемый текст ошибки в списке всех возвращенных ошибок.
    """
    response = await client.get(PERMISSIONS_URL, params=params)

    assert response.status_code == expected_status

    data = response.json()
    error_messages = data["detail"]

    match_found = any(expected_msg_part.lower() in msg.lower() for msg in error_messages)

    assert match_found
