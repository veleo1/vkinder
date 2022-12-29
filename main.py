from random import randrange
import requests
import vk_api
from database import insert_data_users, get_unseen_users
from vk_api.longpoll import VkLongPoll, VkEventType
from configuration import V, group_token, user_token
from keyboard import keyboard

offset: int = 0


class VKinderBot:

    def __init__(self):
        self.vk_group = vk_api.VkApi(token=group_token)
        self.vk_user = vk_api.VkApi(token=user_token)
        self.longpoll = VkLongPoll(self.vk_group)  # для работы с сообщениями

    def get_event(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg: str = event.text.lower()
                return msg, event.user_id

    def write_msg(self, user_id: int, message: str) -> None:
        """МЕТОД ДЛЯ ОТПРАВКИ СООБЩЕНИЙ"""
        self.vk_group.method('messages.send',
                             {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                              'keyboard': keyboard})

    def get_name(self, user_id: int) -> str:
        """ИМЯ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ НАПИСАЛ БОТУ"""
        url: str = 'https://api.vk.com/method/users.get'
        params: dict = {'access_token': user_token,
                        'user_ids': user_id,
                        'v': V}
        reply = requests.get(url, params=params)
        response = reply.json()
        if reply.status_code == 200:
            information_list: list = response['response']
            for item in information_list:
                for key, value in item.items():
                    first_name: str = item.get('first_name')
                    return first_name

    def search_users(self, sex: int, age_from: int, age_to: int, city: str) -> None:
        """ПОИСК ЛЮДЕЙ ПО КРИТЕРИЯМ"""
        url: str = 'https://api.vk.com/method/users.search'
        params: dict = {'access_token': user_token,
                        'v': V,
                        'sex': sex,
                        'age_from': age_from,
                        'age_to': age_to,
                        'hometown': city,
                        'fields': 'is_closed, id, first_name, last_name',
                        'status': '1' or '6',
                        'has_photo': 1,
                        'count': 1000}
        reply = requests.get(url, params=params)
        response = reply.json()
        if reply.status_code == 200:
            list_of_found_users: dict = response['response']
            info_about_one_user: list = list_of_found_users['items']
            for item_about_one_user in info_about_one_user:
                if not item_about_one_user.get('is_closed'):
                    first_name: str = item_about_one_user.get('first_name')
                    last_name: str = item_about_one_user.get('last_name')
                    vk_id: int = item_about_one_user.get('id')
                    insert_data_users(first_name, last_name, vk_id)
                else:
                    continue

    def found_info(self, offset: int) -> str:
        """ВЫВОД ИНФОРМАЦИИ О НАЙДЕННОМ ПОЛЬЗОВАТЕЛЕ"""
        user_info: tuple = get_unseen_users(offset)
        info_about_person: list = []
        for i in user_info:
            info_about_person.append(i)
        return f'{info_about_person[0]} {info_about_person[1]}, ссылка - vk.com/id{info_about_person[2]}'

    def get_photos_id(self, id: int) -> list:
        """ПОЛУЧЕНИЕ ID ФОТОГРАФИЙ С СОРТИРОВКОЙ"""
        url: str = 'https://api.vk.com/method/photos.get'
        params: dict = {'access_token': user_token,
                        'v': V,
                        'owner_id': id,
                        'album_id': 'profile',
                        'extended': 1}
        reply = requests.get(url, params=params)
        photos_dictionary: dict = dict()
        response = reply.json()
        if reply.status_code == 200:
            list_of_found_photos: dict = response['response']
            info_about_one_photo: list = list_of_found_photos['items']
            for photo in info_about_one_photo:
                photo_id: str = str(photo.get('id'))
                photo_likes: dict = photo.get('likes')
                photo_comments: dict = photo.get('comments')
                if photo_likes.get('count'):
                    likes: int = photo_likes.get('count')
                    photos_dictionary[likes] = photo_id
                if photo_comments.get('count'):
                    comments: int = photo_comments.get('count')
                    photos_dictionary[comments] = photo_id
            list_of_ids: list = sorted(photos_dictionary.items(), reverse=True)
            return [photoid[1] for photoid in list_of_ids[0:3]]

    def get_photo_list(self, offset: int, id: int) -> list:
        """ПОЛУЧЕНИЕ СПИСКА ФОТО"""
        list_id: list = self.get_photos_id(self.person_id(offset))
        photo_list: list = []
        for num_id in range(len(list_id)):
            photo_list.append(f"photo{id}_{list_id[num_id]}")
        return photo_list

    def send_photo(self, user_id: int, offset: int, id: int) -> None:
        """ОТПРАВКА ФОТОГРАФИЙ"""
        for num_photo in range(len(self.get_photo_list(offset, id))):
            message: str = f'Фото №{num_photo + 1}'
            self.vk_group.method('messages.send', {'user_id': user_id,
                                                   'access_token': user_token,
                                                   'message': message,
                                                   'attachment': self.get_photo_list(offset, id)[num_photo],
                                                   'random_id': 0})

    def start_searching(self, user_id: int, offset: int) -> None:
        """ЗАПУСК ВСЕХ МЕТОДОВ """
        self.write_msg(user_id, self.found_info(offset))
        self.person_id(offset)
        self.get_photos_id(self.person_id(offset))
        self.send_photo(user_id, offset, self.person_id(offset))

    def person_id(self, offset: int) -> int:
        """ВЫВОД ID НАЙДЕННОГО ПОЛЬЗОВАТЕЛЯ"""
        user_info: tuple = get_unseen_users(offset)
        list_person: list = []
        for info_item in user_info:
            list_person.append(info_item)
        return list_person[2]

    def greeting(self, user_id: int) -> None:
        """ВЫВОД ПРИВЕТСТВИЯ"""
        self.write_msg(user_id,
                       f"Привет, {vk_bot.get_name(user_id)}!\n"
                       "Добро пожаловать в чат-бот Vkinder. Чтобы я мог подобрать для тебя пару, нужно ответить на несколько вопросов. Нажми или напиши 'начать'.\n"
                       "Чтобы закончить поиск, напиши 'пока'.")

    def like_photo(self, id: int, user_id: int, msg: str) -> None:
        """ПОСТАВИТЬ ЛАЙК НА ФОТО"""
        url: str = 'https://api.vk.com/method/likes.add'
        params: dict = {'access_token': user_token,
                  'v': V,
                  'owner_id': id,
                  'type': 'photo',
                  'item_id': [photo for i, photo in enumerate(self.get_photos_id(id), 1) if int(i) == int(msg)]}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            self.write_msg(user_id, 'Лайк поставлен.\n'
                                    'Жми на кнопку "Далее", чтобы продолжить поиск.\n'
                                    'Чтобы закончить поиск, напиши "пока".')

            
vk_bot = VKinderBot()
