from app.core.singleton_meta import SingletonMeta
from app.repositories.fake_user_repository import FakeUserDb


class CheckUserDb(metaclass=SingletonMeta):

    @staticmethod
    async def check_user_db(username: str):
        fake_user_db = FakeUserDb()
        any_user_db = await fake_user_db.get_fake_user_by_name(username)
        return any_user_db
