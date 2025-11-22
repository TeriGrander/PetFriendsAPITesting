from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password) 
    assert status == 200
    assert 'key' in result

def test_get_pets_list_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password) 
    status, result = pf.get_pets_list(auth_key)
    assert status == 200
    assert type(result) == dict
    assert len(result['pets']) != 0
    
def test_add_pet_with_valid_data(name='Alice', animal_type='tabby cat', age=6, image='images/cat1.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_pet(auth_key, name, animal_type, age, image)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == str(age)

def test_delete_existing_pet(pet_id='f2be51b3-950e-47d9-858b-47c451038370'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status = pf.delete_pet(auth_key, pet_id)
    _, check = pf.get_pets_list(auth_key, filter='my_pets')
    ids_list = list(map(lambda x: x['id'], check['pets']))
    assert status == 200
    assert pet_id not in ids_list

def test_update_pet_with_valid_data(name='Lissa', animal_type='tabby cat', age=3, image='images/Lissa_the_cat.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_pets_list(auth_key)
    test_pet_id = pets['pets'][0]['id']
    status, result = pf.put_update_pet(auth_key, test_pet_id, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == str(age)