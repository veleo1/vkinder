from main import vk_bot, offset
from database import creating_database, insert_data_seen_users, get_seen_user

if __name__ == '__main__':
    while True:
        msg, user_id = vk_bot.get_event()
        if msg == 'начать':
            vk_bot.greeting(user_id)
            sex: int = 0
            vk_bot.write_msg(user_id, 'Введи пол (1 - женский, 2 - мужской)')
            while True:
                msg, user_id = vk_bot.get_event()
                try:
                    if msg == '1' or msg == '2':
                        sex: int = int(msg)
                    else:
                        raise ValueError
                except ValueError:
                    vk_bot.write_msg(user_id, 'Введи корректный пол')
                else:
                    break
            age_from: int = 0
            vk_bot.write_msg(user_id, 'Введи минимальный возраст')
            while True:
                msg, user_id = vk_bot.get_event()
                try:
                    if int(msg) <= 0:
                        raise ValueError
                    else:
                        age_from = int(msg)
                except ValueError:
                    vk_bot.write_msg(user_id, 'Введи корректный возраст')
                else:
                    break
            age_to: int = 0
            vk_bot.write_msg(user_id, 'Введи максимальный возраст')
            while True:
                msg, user_id = vk_bot.get_event()
                try:
                    if int(msg) <= 0 or int(msg) < age_from:
                        raise ValueError
                    else:
                        age_to = int(msg)
                except ValueError:
                    vk_bot.write_msg(user_id, 'Введи корректный возраст')
                else:
                    break
            vk_bot.write_msg(user_id, 'Введи город')
            msg, user_id = vk_bot.get_event()
            city: str = msg
            creating_database()
            vk_bot.search_users(sex, age_from, age_to, city)
            vk_bot.start_searching(user_id, offset)
            insert_data_seen_users(vk_bot.person_id(offset))
            vk_bot.write_msg(user_id, 'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                                      'Чтобы поставить лайк фото, напиши номер фото.\n'
                                      'Чтобы закончить поиск, напиши "пока".')
        elif msg == 'далее':
            for i in range(0, 1000):
                offset += 1
                vk_bot.start_searching(user_id, offset)
                insert_data_seen_users(vk_bot.person_id(offset))
                vk_bot.write_msg(user_id, 'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                                      'Чтобы поставить лайк фото, напиши номер фото.\n'
                                      'Чтобы закончить поиск, напиши "пока".')
                break
        elif msg == '1' or msg == '2' or msg == '3':
            vk_bot.like_photo(get_seen_user(), user_id, msg)
        elif msg == 'пока':
            vk_bot.write_msg(user_id, "Пока((")
        else:
            vk_bot.greeting(user_id)
