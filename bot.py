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
            # vk_bot.search_users(1, 25, 28, 'Пермь')
            vk_bot.start_searching(user_id, offset)
            insert_data_seen_users(vk_bot.person_id(offset))  # убрать
            vk_bot.write_msg(user_id, 'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                                      'Чтобы поставить лайк фото, напиши номер фото (1, 2 или 3)')
            # msg, user_id = vk_bot.get_event()
        elif msg == 'далее':
            for i in range(0, 1000):
                offset += 1
                vk_bot.start_searching(user_id, offset)
                insert_data_seen_users(vk_bot.person_id(offset))  # убрать
                vk_bot.write_msg(user_id, 'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                                          'Чтобы поставить лайк фото, напиши номер фото (1, 2 или 3)')
                break
                # msg, user_id = vk_bot.get_event()
                # if msg == '1':
                #     vk_bot.like_photo1(get_seen_user(), user_id)
                # if msg == '2':
                #     vk_bot.like_photo2(get_seen_user(), user_id)
                # if msg == '3':
                #     vk_bot.like_photo3(get_seen_user(), user_id)
                # else:
                #     continue
        elif msg == '1':
            vk_bot.like_photo1(get_seen_user(), user_id)
        elif msg == '2':
            vk_bot.like_photo2(get_seen_user(), user_id)
        elif msg == '3':
            vk_bot.like_photo3(get_seen_user(), user_id)
        # else:
        #     break

        elif msg == 'пока':
            vk_bot.write_msg(user_id, "Пока((")
        else:
            vk_bot.greeting(user_id)

            # # Производим отбор анкет
            # for i in range(len(result)):
            #     dating_user, blocked_user = check_db_user(result[i][3])
            #     # Ждем пользовательский ввод
            #     write_msg(user_id, '1 - Добавить, 2 - Заблокировать, 0 - Далее, \nq - выход из поиска')
            #     msg_text, user_id = loop_bot()
            #     if msg_text == '0':
            #         # Проверка на последнюю запись
            #         if i >= len(result) - 1:
            #             show_info()
            #     # Добавляем пользователя в избранное
            #     elif msg_text == '1':
            #         # Проверка на последнюю запись
            #         if i >= len(result) - 1:
            #             show_info()
            #             break
            #         # Пробуем добавить анкету в БД
            #         try:
            #             add_user(user_id, result[i][3], result[i][1],
            #                      result[i][0], city, result[i][2], current_user_id.id)
            #             # Пробуем добавить фото анкеты в БД
            #             add_user_photos(user_id, sorted_user_photo[0][1],
            #                             sorted_user_photo[0][0], current_user_id.id)
            #         except AttributeError:
            #             write_msg(user_id, 'Вы не зарегистрировались!\n Введите Vkinder для перезагрузки бота')
            #             break
            #     # Добавляем пользователя в черный список
            #     elif msg_text == '2':
            #         # Проверка на последнюю запись
            #         if i >= len(result) - 1:
            #             show_info()
            #         # Блокируем
            #         add_to_black_list(user_id, result[i][3], result[i][1],
            #                           result[i][0], city, result[i][2],
            #                           sorted_user_photo[0][1],
            #                           sorted_user_photo[0][0], current_user_id.id)
            #     elif msg_text.lower() == 'q':
            #         write_msg(user_id, 'Введите Vkinder для активации бота')
            #         break

            # # Переходим в избранное
            # elif msg_text == '2':
            #     go_to_favorites(user_id)
            #
            # # Переходим в черный список
            # elif msg_text == '0':
            #     go_to_blacklist(user_id)
