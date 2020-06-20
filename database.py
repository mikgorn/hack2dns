from typing import *
from pathlib import Path
from sqlite3 import connect

from models import User


class Database:

    _fields = (
        "email",
        "first_name",
        "second_name",
        "patronymic",
        "birthday",
        "address",
        "password",
        "retiree",
        "disabled",
    )

    def __init__(self, dbfile_path: Path):
        self.connection = connect(str(dbfile_path), check_same_thread=False)
        self.c = self.connection.cursor()

    def initialize(self):
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS user  (email text primary key, first_name text, second_name text, patronymic text, birthday datetime, address text, password text, retiree int, disabled int  )"
        )
        self.connection.commit()

    def set_user(self, user: User) -> None:
        self.c.execute(
            "INSERT INTO user (%s) VALUES (%s)"
            % (
                ",".join((self._fields)),
                ",".join([":%s" % f for f in self._fields]),
            ),
            vars(user),
        )
        self.connection.commit()

    def find_by(
        self,
        filter_values: Dict[str, Any],
        need_columns: Optional[Iterable[str]] = None,
    ) -> List[Tuple[Any]]:
        columns: Iterable[
            str
        ] = need_columns if need_columns is not None else {"*"}
        self.c.execute(
            "SELECT %s FROM user WHERE %s"
            % (
                ",".join(columns),
                ",".join(["%s=:%s" % (k, k) for k in filter_values.keys()]),
            ),
            filter_values,
        )
        return self.c.fetchall()

    def get_all_users(self) -> List[User]:
        results = []
        self.c.execute("SELECT * FROM user")
        for raw_data in self.c.fetchall():
            results.append(
                User.create_user_from_sqlite_db(raw_data, self._fields)
            )
        return results

    def get_user_by_email(self, email: str) -> Optional[User]:
        raw_data = self.find_by({"email": email})
        if len(raw_data) > 1:
            raise Exception(
                "More, than one on %s. %s" % (email, str(raw_data))
            )
        elif len(raw_data) == 1:
            return User.create_user_from_sqlite_db(raw_data[0], self._fields)
        return None

    def close(self) -> None:
        self.c.close()
        self.connection.close()


if __name__ == "__main__":
    from datetime import datetime

    u = User(
        first_name="slava",
        second_name="Кривуя",
        patronymic="",
        birthday=datetime.now(),
        password="ficus",
        email="ficus@bk.рФ",
        disabled=False,
        retiree=True,
        address="Ficus",
    )
    u1 = User(
        first_name="slava",
        second_name="Кривуя",
        patronymic="",
        birthday=datetime.now(),
        password="ficus",
        email="ficus1@bk.рФ",
        disabled=False,
        retiree=True,
        address="Ficus",
    )
    d = Database(Path("database2.db"))
    d.initialize()
    d.set_user(u)
    d.set_user(u1)
    print(d.find_by({"email": "ficus@bk.рФ"}))
    print(d.get_all_users())
    print(d.get_user_by_email("ficus@bk.рФ"))
    d.close()
