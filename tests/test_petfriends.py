from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password) # type: ignore
    assert status == 200
    assert 'key' in result

def test_get_pets_list_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password) # type: ignore
    status, result = pf.get_pets_list(auth_key) # type: ignore
    assert status == 200
    assert type(result) == dict
    assert len(result['pets']) != 0
    