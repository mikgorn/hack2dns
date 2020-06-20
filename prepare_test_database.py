from typing import *
from datetime import datetime

import config
from database import Database
from models import User, Roles
from utils import get_password_hash


def main():
    u1 = User(
        first_name="Андрей",
        second_name="Фикусов",
        patronymic="",
        birthday=datetime.fromtimestamp(646577281),
        password=get_password_hash("1111"),
        email="andreyivanov01@тестовая-зона.рф",
        disabled=False,
        retiree=True,
        address="Санкт-Петербург",
        role=Roles.USER,
    )

    u2 = User(
        first_name="Петр",
        second_name="Черков",
        patronymic="Андреевич",
        birthday=datetime.fromtimestamp(1277297462),
        password=get_password_hash("1111"),
        email="petrsergeev02@тестовая-зона.рф",
        disabled=False,
        retiree=False,
        address="Москва",
        role=Roles.USER,
    )

    u3 = User(
        first_name="Кирилл",
        second_name="Ким",
        patronymic="",
        birthday=datetime.fromtimestamp(1025009572),
        password=get_password_hash("админ"),
        email="кириллким03@тестовая-зона.рф",
        disabled=False,
        retiree=False,
        address="Санкт-Петербург",
        role=Roles.ADMIN,
    )

    u4 = User(
        first_name="Андрей",
        second_name="Самокатов",
        patronymic="Павлович",
        birthday=datetime.fromtimestamp(1025709572),
        password=get_password_hash("1111"),
        email="xn--80aidqrt@тестовая-зона.рф",
        disabled=False,
        retiree=False,
        address="Санкт-Петербург",
        role=Roles.USER,
    )

    db = Database(config.DB_PATH)
    db.initialize()
    db.set_user(u1)
    db.set_user(u2)
    db.set_user(u3)
    db.set_user(u4)


if __name__ == "__main__":
    main()
