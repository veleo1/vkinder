import psycopg2

connection = psycopg2.connect(
    user='postgres',
    password='postgres',
    database='vkinder',
)

connection.autocommit = True


def create_table_users():
    """СОЗДАНИЕ ТАБЛИЦЫ USERS (НАЙДЕННЫЕ ПОЛЬЗОВАТЕЛИ)"""
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id serial,
                first_name varchar(50) NOT NULL,
                last_name varchar(50) NOT NULL,
                vk_id varchar(50) NOT NULL PRIMARY KEY)
                ;"""
        )
    print("Таблица USERS создана")


def create_table_seen_users():
    """СОЗДАНИЕ ТАБЛИЦЫ SEEN_USERS (ПРОСМОТРЕННЫЕ ПОЛЬЗОВАТЕЛИ)"""
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS seen_users(
            id serial,
            vk_id varchar(50) PRIMARY KEY);"""
        )
    print("Таблица SEEN_USERS создана")


def get_seen_user():
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT vk_id from seen_users
            ORDER BY ID DESC 
            LIMIT 1;
            """
        )
        return cursor.fetchone()


def insert_data_users(first_name, last_name, vk_id):
    """ВСТАВКА ДАННЫХ В ТАБЛИЦУ USERS"""
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (first_name, last_name, vk_id)
            VALUES ('{first_name}', '{last_name}', '{vk_id}');"""
        )


def insert_data_seen_users(vk_id):
    """ВСТАВКА ДАННЫХ В ТАБЛИЦУ SEEN_USERS"""
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO seen_users (vk_id) 
            VALUES ('{vk_id}')
            ;"""
        )


def get_unseen_users(offset):
    """ВЫБОРКА ИЗ НЕПРОСМОТРЕННЫХ ЛЮДЕЙ"""
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT u.first_name, u.last_name, u.vk_id, su.vk_id FROM users u
                        LEFT JOIN seen_users su
                        ON u.vk_id = su.vk_id
                        WHERE su.vk_id IS NULL
                        OFFSET '{offset}'
                        ;"""
        )
        return cursor.fetchone()


def drop_users():
    """УДАЛЕНИЕ ТАБЛИЦЫ USERS"""
    with connection.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS users CASCADE;"""
        )
        print('Таблица USERS удалена')


def creating_database():
    drop_users()
    create_table_users()
    create_table_seen_users()
