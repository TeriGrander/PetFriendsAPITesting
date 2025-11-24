from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def get_first_of_my_pets_helper() -> tuple:
    """Вспомогательная функция, возвращает код 1 и данные о первом
    питомце в списке, полученном по фильтру my_pets, или код 0 и
    сообщение что по этому фильтру нет питомцев.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pets_list(auth_key, filter='my_pets')
    if len(my_pets['pets']) > 0:
        return 1, my_pets['pets'][0]
    else:
        return 0, 'There is no my pets'


def test_get_api_key_for_valid_user(email=valid_email,
                                    password=valid_password):
    """Проверяем, что при передаче email и пароля существующего
    пользователя успешно возвращается ключ аутентификации.
    (Тест взят из модуля).
    """

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_api_key_invalid_credentials(email='11'+valid_email,
                                         password='11'+valid_password):
    """Проверяем, что при передаче несуществующих email и пароля ключ
    аутентификации не возвращается.
    """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_pets_list_with_valid_key(filter=''):
    """Проверяем, что при передаче корректного ключа аутентификации
    успешно возвращается список питомцев.
    (Тест взят из модуля).
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_pets_list(auth_key)

    assert status == 200
    assert len(result['pets']) != 0


def test_get_pets_list_with_invalid_key():
    """Проверяем, что при передаче некорректного ключа аутентификации
    возвращается код 403, а не список питомцев.
    """

    status, result = pf.get_pets_list({'key': '111'})
    assert status == 403
    assert 'Forbidden' in result


def test_add_pet_with_valid_data(name='Alice', animal_type='tabby cat',
                                 age=6, image='tests/images/cat1.jpg'):
    """Проверяем, что при запросе с корректными данными питомец успешно
    добавляется.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_pet(auth_key, name, animal_type, age, image)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == str(age)


def test_add_pet_negative_age(name='Alice', animal_type='cat',
                              age=-1, image='tests/images/cat1.jpg'):
    """Проверяем, что работает валидация возраста питомца - питомец
    с отрицательным возрастом не добавляется.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.post_add_pet(auth_key, name, animal_type, age, image)

    assert status == 422


def test_delete_existing_pet():
    """Проверяем, что при передаче существующего pet_id питомец успешно
    удаляется.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, test_pet = pf.post_add_pet_simple(auth_key, '111', '111', 11)

    status, _ = pf.delete_pet(auth_key, test_pet['id'])
    _, check = pf.get_pets_list(auth_key, filter='my_pets')
    ids_list = list(map(lambda x: x['id'], check['pets']))

    assert status == 200
    assert test_pet['id'] not in ids_list


def test_delete_non_existing_pet():
    """Проверяем, что при попытке удалить питомца по несуществующему id
    возвращается ошибка.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.delete_pet(auth_key, '111111')

    assert status == 403


def test_update_pet_with_valid_data(name='Lissa',
                                    animal_type='tabby cat',
                                    age=3):
    """Проверяем, что при передаче корректных данных информация о
    питомце успешно обновляется.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    code, first_pet = get_first_of_my_pets_helper()

    if code == 1:
        test_pet_id = first_pet['id']
        status, result = pf.put_update_pet(auth_key, test_pet_id, name,
                                           animal_type, age)
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == str(age)
    else:
        raise Exception("There is no my pets")


def test_update_pet_with_blank_id(name='Lissa', animal_type='cat', age=2):
    """Проверяем, что при передаче пустой строки в pet_id возвращается
    код 404.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.put_update_pet(auth_key, '', name,
                                       animal_type, age)

    assert status == 200
    assert 'name' not in result


def test_add_pet_simple_valid_data(name='Lissa', animal_type='cat', age=2):
    """Проверяем, что при запросе с корректными данными без фото
    питомец успешно добавляется.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == str(age)


def test_add_pet_simple_invalid_key(name='Lissa', animal_type='cat', age=2):
    """Проверяем, что при запросе с некорректным ключом аутентификации
    питомец не добавляется.
    """

    status, result = pf.post_add_pet_simple({'key': '111'}, name,
                                            animal_type, age)

    assert status == 403
    assert 'name' not in result


def test_add_pet_simple_negative_age(name='Lissa', animal_type='cat', age=-2):
    """Проверяем, что работает валидация возраста питомца в запросе на
    добавление питомца без фото - питомец с отрицательным возрастом не
    добавляется.
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_pet_simple(auth_key, name, animal_type, age)

    assert status == 422
    assert name not in result


def test_add_pet_photo_for_existing_pet(image='tests/images/cat2.jpg'):
    """Проверяем, фото добавляется к существующему питомцу без фото."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pets_list(auth_key)
    test_pet = list(filter(lambda x: x['pet_photo'] == '', my_pets['pets']))[0]

    status, result = pf.post_add_pet_photo(auth_key, test_pet['id'], image)

    assert status == 200
    assert result['pet_photo'] != ''


def test_add_pet_photo_for_non_existing_pet(image='tests/images/cat2.jpg'):
    """Проверяем, к несуществующему питомцу фото не добавляется."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_pet_photo(auth_key, '1111', image)

    assert status == 404
    assert 'pet_photo' not in result
