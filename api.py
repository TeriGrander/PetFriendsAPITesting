import requests
import json


class PetFriends():
    '''API библиотека к веб приложению Pet Friends'''
    def __init__(self) -> None:
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус
        запроса и результат в формате JSON с уникальным ключом
        пользователя, найденного по указанным email и паролю.
        """

        endpoint_url = 'api/key'
        headers = {
            'email': email,
            'password': password
        }

        res = requests.get(self.base_url + endpoint_url, headers=headers)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except Exception:
            result = res.text
        return status, result

    def get_pets_list(self, auth_key: json, filter: str = '') -> json:
        """Метод делает запрос к API сервера и возвращает статус
        запроса и результат в формате JSON со списком найденных
        питомцев, совпадающих с фильтром. На данный момент фильтр
        может иметь либо пустое значение - получить список всех
        питомцев, либо 'my_pets' - получить список собственных питомцев.
        """

        endpoint_url = 'api/pets'
        header = {'auth_key': auth_key['key']}
        params = {'filter': filter}

        res = requests.get(self.base_url + endpoint_url,
                           headers=header,
                           params=params)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except Exception:
            result = res.text
        return status, result

    def post_add_pet(self, auth_key: json, pet_name: str,
                     pet_type: str, pet_age: int, pet_image: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и
        возвращает статус запроса на сервер и результат в формате JSON
        с данными добавленного питомца.
        """

        endpoint_url = 'api/pets'
        header = {'auth_key': auth_key['key']}
        data = {
                'name': pet_name,
                'animal_type': pet_type,
                'age': pet_age
                }
        pet_photo = {'pet_photo': (pet_image, open(pet_image, 'rb'),
                                   'image/jpeg')}

        res = requests.post(self.base_url + endpoint_url,
                            headers=header,
                            data=data,
                            files=pet_photo)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except Exception:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по
        указанному ID и возвращает статус запроса.
        """

        endpoint_url = 'api/pets' + '/' + pet_id
        header = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + endpoint_url, headers=header)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except Exception:
            result = res.text
        return status, result

    def put_update_pet(self, auth_key: json, pet_id: str,
                       pet_name: str, pet_type: str, pet_age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных
        питомца по указанному ID и возвращает статус запроса и result
        в формате JSON с обновлённыи данными питомца.
        """

        endpoint_url = 'api/pets' + '/' + pet_id
        header = {'auth_key': auth_key['key']}
        params = {'name': pet_name, 'age': pet_age, 'animal_type': pet_type}

        res = requests.put(self.base_url + endpoint_url,
                           headers=header,
                           data=params)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except Exception:
            result = res.text
        return status, result

    def post_add_pet_simple(self, auth_key: json, pet_name: str,
                            pet_type: str, pet_age: int) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце без
        фото и возвращает статус запроса на сервер и результат в
        формате JSON с данными добавленного питомца.
        """

        endpoint_url = 'api/create_pet_simple'
        header = {'auth_key': auth_key['key']}
        data = {
                'name': pet_name,
                'animal_type': pet_type,
                'age': pet_age
                }

        res = requests.post(self.base_url + endpoint_url,
                            headers=header,
                            data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except Exception:
            result = res.text
        return status, result

    def post_add_pet_photo(self, auth_key: json,
                           pet_id: str, pet_image: str) -> json:
        """Метод отправляет запрос на сервер о добавлении фото питомца
        по указанному id питомца и возвращает статус запроса на сервер
        и результат в формате JSON с данными питомца, для которого
        добавлено фото.
        """

        endpoint_url = 'api/pets/set_photo' + '/' + pet_id
        header = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_image, open(pet_image, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + endpoint_url,
                            headers=header,
                            files=file)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except Exception:
            result = res.text
        return status, result
