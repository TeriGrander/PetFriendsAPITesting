import requests
import json

class PetFriends():
    '''API библиотека к веб приложению Pet Friends'''
    def __init__(self) -> None:
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> tuple[int, json]:
        '''Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключом пользователя, найденного по указанным email и паролю.'''
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    
    def get_pets_list(self, auth_key: json, filter: str = '') -> tuple[int, json]:
        '''Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список собственных питомцев'''
        header = {'auth_key': auth_key['key']}
        params = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=header, params=params)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result