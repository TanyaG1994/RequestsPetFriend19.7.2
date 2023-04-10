from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest

pf = PetFriends()

@pytest.mark.parametrize("name", ["12345", ".,!?", "%&*$"])
def test_add_new_pet_with_invalid_name(name, animal_type='сиамская',
                                     age=1, pet_photo='images/cat.jpg'):
    """Проверяем, что поле name для ввода имени питомца не принимает на ввод числа, знаки препинания, специальные символы"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400




@pytest.mark.parametrize("animal_type", ["245436", "!:?", "%&#$"])
def test_add_new_pet_with_invalid_animal_type(animal_type, name='Bobby', age=2, pet_photo='images/cat.jpg'):
    """Проверяем, что поле name для ввода породы питомца не принимает на ввод числа, знаки препинания, специальные символы"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400




@pytest.mark.parametrize("age", ["sd", "ит", "%&", "?!"])
def test_add_new_pet_with_invalid_age(age, name='Bobby', animal_type='овчарка', pet_photo='images/cat.jpg'):
    """Проверяем, что поле age для ввода возраста питомца не принимает на ввод буквы, специальные символы, занки препинания."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400





def test_add_new_pet_with_no_name(name='', animal_type='сиамская', age=1, pet_photo='images/cat.jpg'):
    """Проверяем, что поле name для ввода имени питомца не может быть не заполненным"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400




def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем, что при указании неверного ключа авторизации, запрос списка питомцев невозможен"""

    auth_key = {'key': '1234jno788poko0990'}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403




def test_add_pet_creat_simple_no_animal_type(name='Vally', animal_type='', age=1):
    """Проверяем, что поле animal_type для ввода породы питомца не может быть не заполненным"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_creat_simple(auth_key, name, animal_type, age)

    assert status == 400




def test_unsuccessful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем, что не возможно обновить информацию о питомце по несуществующему id питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что список питомцев не пуст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, '909jbajcb8292hihi18w28', name, animal_type, age)

        assert status == 400
    else:
        # Исключение, если спиок питомцев пустой
        raise Exception("There is no my pets")




@pytest.mark.parametrize("pet_photo", ["images/cat.jpg", "images/cat1.jpeg", "images/dog.png"])
def test_add_pet_set_photo_valid_data(pet_photo):
    """Проверяем, что можно добавить фото разных форматов питомцу, у которого его нет, по id питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Проверяем, что список питомцев не пуст
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200

    else:
        # если список питомцев пустой, то выкидываем исключение
        raise Exception("There is no my pets")




def test_add_new_pet_with_name_max(name = """SjjEm6QL5kht57PzgqOk4ohKMWKSjMyY3pA9nnr7X2Bctm3KLUiaBA0jgOwqFTrGbbs
F4KSHb3paVJLHHWEzLJA1D4GU2zgUVSsPjijIpPsmuMv24U67uepi48rNGbfbtjaDoKGNAJuhXKKFe952gcMa84tNaMpvxE53K5IXTYaODOlmQnRL32N
bnha2QwONlgvqeO9I9mV16mmAtkm7LZtnVevZY9hkfgz43NLET7Pp7y0VAIDTVrLXjy4e6yIy""", animal_type='сиамская', age=1, pet_photo='images/cat.jpg'):


    """Проверяем, что поле name для ввода имени питомца принимает на ввод троку максимальной длины 256 символов"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name





def test_get_api_key_for_invalid_user(email='Orlov@mail.ru', password='123abc456'):
    """ Проверяем что запрос api ключа возвращает статус 403 при вводе логина и пароля несуществующего пользователя"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
