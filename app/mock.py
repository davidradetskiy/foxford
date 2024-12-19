from app.dao import create_user


async def create_mock_users():
    users = [
        {"name": "Mishail Fedorov", "code": "0000"},
        {"name": "Yaroslav Ivanov", "code": "1111"},
    ]
    for user in users:
        await create_user(user)
