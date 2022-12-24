from random import randrange
import requests
import vk_api
from database import *
from vk_api.longpoll import VkLongPoll, VkEventType
from configuration import *
from keyboard import *


class VKinderBot:

    def __init__(self):
        self.vk_group = vk_api.VkApi(token=group_token)
        self.vk_user = vk_api.VkApi(token=user_token)
        self.longpoll = VkLongPoll(self.vk_group)  # для работы с сообщениями

    def get_event(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text.lower()
                return msg, event.user_id

    def write_msg(self, user_id, message):
        """МЕТОД ДЛЯ ОТПРАВКИ СООБЩЕНИЙ"""
        self.vk_group.method('messages.send',
                             {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                              'keyboard': keyboard})

    def get_name(self, user_id):
        """ИМЯ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ НАПИСАЛ БОТУ"""
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'v': V}
        repl = requests.get(url, params=params)
        response = repl.json()
        if repl.status_code == HTTP_STATUS:
            information_dict = response['response']
            for i in information_dict:
                for key, value in i.items():
                    first_name = i.get('first_name')
                    return first_name

    def search_users(self, sex, age_from, age_to, city):
        """ПОИСК ЛЮДЕЙ ПО КРИТЕРИЯМ"""
        url = 'https://api.vk.com/method/users.search'
        params = {'access_token': user_token,
                  'v': V,
                  'sex': sex,
                  'age_from': age_from,
                  'age_to': age_to,
                  'hometown': city,
                  'fields': 'is_closed, id, first_name, last_name',
                  'status': '1' or '6',
                  'has_photo': 1,
                  'count': 1000}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        if resp.status_code == HTTP_STATUS:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
            for person_dict in list_1:
                if person_dict.get('is_closed') == False:
                    first_name = person_dict.get('first_name')
                    last_name = person_dict.get('last_name')
                    vk_id = str(person_dict.get('id'))
                    vk_link = 'vk.com/id' + str(person_dict.get('id'))
                    insert_data_users(first_name, last_name, vk_id, vk_link)
                else:
                    continue

    def found_info(self, offset):
        """ВЫВОД ИНФОРМАЦИИ О НАЙДЕННОМ ПОЛЬЗОВАТЕЛЕ"""
        user_info = get_unseen_users(offset)
        list_person = []
        for i in user_info:
            list_person.append(i)
        return f'{list_person[0]} {list_person[1]}, ссылка - {list_person[3]}'

    def get_photos_id(self, id):
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИЙ С СОРТИРОВКОЙ"""
        url = 'https://api.vk.com/method/photos.get'
        params = {'access_token': user_token,
                  'v': V,
                  'owner_id': id,
                  'album_id': 'profile',
                  'extended': 1}
        resp = requests.get(url, params=params)
        dict_photos = dict()
        resp_json = resp.json()
        if resp.status_code == HTTP_STATUS:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
            for photo in list_1:
                photo_id = str(photo.get('id'))
                photo_likes = photo.get('likes')
                photo_comments = photo.get('comments')
                if photo_likes.get('count'):
                    likes = photo_likes.get('count')
                    dict_photos[likes] = photo_id
                if photo_comments.get('count'):
                    comments = photo_comments.get('count')
                    dict_photos[comments] = photo_id
            list_of_ids = sorted(dict_photos.items(), reverse=True)
            return [x[1] for x in list_of_ids[0:3]]

    def get_photo_list(self, offset, id):
        """ПОЛУЧЕНИЕ СПИСКА ФОТО"""
        photo_list = self.get_photos_id(self.person_id(offset))
        if len(photo_list) == 1:
            photo1 = str(f'photo{id}_{photo_list[0]}')
            return [photo1]
        elif len(photo_list) == 2:
            photo1 = str(f'photo{id}_{photo_list[0]}')
            photo2 = str(f'photo{id}_{photo_list[1]}')
            return [photo1, photo2]
        elif len(photo_list) == 3:
            photo1 = str(f'photo{id}_{photo_list[0]}')
            photo2 = str(f'photo{id}_{photo_list[1]}')
            photo3 = str(f'photo{id}_{photo_list[2]}')
            return [photo1, photo2, photo3]

    def send_photo_1(self, user_id, message, offset, id):
        """ОТПРАВКА ПЕРВОЙ ФОТОГРАФИИ"""
        self.vk_group.method('messages.send', {'user_id': user_id,
                                               'access_token': user_token,
                                               'message': message,
                                               'attachment': self.get_photo_list(offset, id)[0],
                                               'random_id': 0})

    def send_photo_2(self, user_id, message, offset, id):
        """ОТПРАВКА ВТОРОЙ ФОТОГРАФИИ"""
        self.vk_group.method('messages.send', {'user_id': user_id,
                                               'access_token': user_token,
                                               'message': message,
                                               'attachment': self.get_photo_list(offset, id)[1],
                                               'random_id': 0})

    def send_photo_3(self, user_id, message, offset, id):
        """ОТПРАВКА ТРЕТЬЕЙ ФОТОГРАФИИ"""
        self.vk_group.method('messages.send', {'user_id': user_id,
                                               'access_token': user_token,
                                               'message': message,
                                               'attachment': self.get_photo_list(offset, id)[2],
                                               'random_id': 0})

    def start_searching(self, user_id, offset):
        """ЗАПУСК ВСЕХ МЕТОДОВ """
        self.write_msg(user_id, self.found_info(offset))
        self.person_id(offset)
        self.get_photos_id(self.person_id(offset))
        self.send_photo_1(user_id, 'Фото №1', offset, self.person_id(offset))
        try:
            self.send_photo_2(user_id, 'Фото №2', offset, self.person_id(offset))
            self.send_photo_3(user_id, 'Фото №3', offset, self.person_id(offset))
        except IndexError:
            self.write_msg(user_id, 'Больше фотографий нет')

    def person_id(self, offset):
        """ВЫВОД ID НАЙДЕННОГО ПОЛЬЗОВАТЕЛЯ"""
        user_info = get_unseen_users(offset)
        list_person = []
        for i in user_info:
            list_person.append(i)
        return str(list_person[2])

    def greeting(self, user_id):
        """ВЫВОД ПРИВЕТСТВИЯ"""
        self.write_msg(user_id,
                       f"Привет, {vk_bot.get_name(user_id)}!\n"
                       "Добро пожаловать в чат-бот Vkinder. Чтобы я мог подобрать для тебя пару, нужно ответить на несколько вопросов. Нажми или напиши 'начать'.\n"
                       "Чтобы закончить поиск, напиши 'пока'\n")

    def like_photo1(self, id, user_id):
        """ПОСТАВИТЬ ЛАЙК НА ФОТО 1"""
        photo_list1 = self.get_photos_id(id)
        url = 'https://api.vk.com/method/likes.add'
        params = {'access_token': user_token,
                  'v': V,
                  'owner_id': id,
                  'type': 'photo',
                  'item_id': int(photo_list1[0])}
        resp = requests.get(url, params=params)
        if resp.status_code == HTTP_STATUS:
            self.write_msg(user_id, 'Лайк поставлен.\n'
                           'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                           'Чтобы закончить поиск, напиши "пока".')

    def like_photo2(self, id, user_id):
        """ПОСТАВИТЬ ЛАЙК НА ФОТО 2"""
        photo_list2 = self.get_photos_id(id)
        url = 'https://api.vk.com/method/likes.add'
        params = {'access_token': user_token,
                  'v': V,
                  'owner_id': id,
                  'type': 'photo',
                  'item_id': int(photo_list2[1])}
        resp = requests.get(url, params=params)
        if resp.status_code == HTTP_STATUS:
            self.write_msg(user_id, 'Лайк поставлен.\n'
                           'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                           'Чтобы закончить поиск, напиши "пока".')
            
    def like_photo3(self, id, user_id):
        """ПОСТАВИТЬ ЛАЙК НА ФОТО 3"""
        photo_list3 = self.get_photos_id(id)
        url = 'https://api.vk.com/method/likes.add'
        params = {'access_token': user_token,
                  'v': V,
                  'owner_id': id,
                  'type': 'photo',
                  'item_id': int(photo_list3[2])}
        resp = requests.get(url, params=params)
        if resp.status_code == HTTP_STATUS:
            self.write_msg(user_id, 'Лайк поставлен.\n'
                           'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                           'Чтобы закончить поиск, напиши "пока".')


vk_bot = VKinderBot()
