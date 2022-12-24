from main import *
from database import *

if __name__ == '__main__':
    while True:
        msg, user_id = vk_bot.get_event()
        if msg == 'начать':
            vk_bot.greeting(user_id)
            sex = 0
            while not msg == 'ж' or msg == 'м':
                vk_bot.write_msg(user_id, 'Введи пол (м - мужской, ж - женский)')
                msg, user_id = vk_bot.get_event()
                if msg == 'ж':
                    sex = 1
                    break
                elif msg == 'м':
                    sex = 2
                    break
                else:
                    vk_bot.write_msg(user_id, 'Введите корректный пол')
            age_from = 0
            vk_bot.write_msg(user_id, 'Введи минимальный возраст')
            while True:
                msg, user_id = vk_bot.get_event()
                try:
                    if int(msg) <= 0:
                        raise ValueError
                    else:
                        age_from = int(msg)
                except ValueError:
                    vk_bot.write_msg(user_id, 'Введите корректный возраст')
                else:
                    break
            age_to = 0
            vk_bot.write_msg(user_id, 'Введи максимальный возраст')
            while True:
                msg, user_id = vk_bot.get_event()
                try:
                    if int(msg) <= 0 or int(msg) < age_from:
                        raise ValueError
                    else:
                        age_to = int(msg)
                except ValueError:
                    vk_bot.write_msg(user_id, 'Введите корректный возраст')
                else:
                    break
            vk_bot.write_msg(user_id, 'Введи город')
            msg, user_id = vk_bot.get_event()
            city = msg
            creating_database()
            vk_bot.search_users(sex, age_from, age_to, city)
            vk_bot.start_searching(user_id, offset)
            insert_data_seen_users(vk_bot.person_id(offset))
            vk_bot.write_msg(user_id, 'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                                      'Чтобы поставить лайк фото, напиши номер фото (1, 2 или 3).\n'
                                      'Чтобы закончить поиск, напиши "пока".')
        elif msg == 'далее':
            for i in range(0, 1000):
                offset += 1
                vk_bot.start_searching(user_id, offset)
                insert_data_seen_users(vk_bot.person_id(offset))
                vk_bot.write_msg(user_id, 'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                                      'Чтобы поставить лайк фото, напиши номер фото (1, 2 или 3).\n'
                                      'Чтобы закончить поиск, напиши "пока".')
                break
        elif msg == '1':
            vk_bot.like_photo1(get_seen_user(), user_id)
        elif msg == '2':
            vk_bot.like_photo2(get_seen_user(), user_id)
        elif msg == '3':
            vk_bot.like_photo3(get_seen_user(), user_id)
        elif msg == 'пока':
            vk_bot.write_msg(user_id, "Пока((")
        else:
            vk_bot.greeting(user_id)
