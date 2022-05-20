import pytest


# проверка рандомного изображения собаки
def test_get_random_dog(dog_api):
    response = dog_api.get("breeds/image/random")
    #    print(response.status_code)
    assert response.status_code == 200
    #    print(response.json()["status"])
    assert response.json()["status"] == 'success'
    #    print(response.json()["message"])
    assert 'message' in response.json()


# проверка ошибки ввода породы
def test_get_breed_error(dog_api):
    response = dog_api.get(f"breed/houn/images/random")
    assert response.status_code == 404
    assert response.json()["status"] == 'error'
    assert response.json()["message"] == 'Breed not found (master breed does not exist)'


# проверка рандомных изображений определенных пород
@pytest.mark.parametrize('breed', ["akita", "boxer", "husky", "saluki", "papillon"])
def test_get_bread_image_random(dog_api, breed):
    response = dog_api.get(f"breed/{breed}/images/random")
    assert response.status_code == 200
    assert response.json()["status"] == 'success'
    assert 'message' in response.json()


# проверка корректного отображения запрашивоемого количества изображений
@pytest.mark.parametrize('number_of_images', [i for i in range(1, 51)])
def test_get_few_random_images_dog(dog_api, number_of_images):
    response = dog_api.get(f"breeds/image/random/{number_of_images}")
    final_len = len(response.json()["message"])
    #    print("nomer=", number_of_images)
    #    print(final_len)
    assert final_len == number_of_images


# проверка наличия изображения
@pytest.mark.parametrize('url',
                         ["breed/hound/images/random", "breed/hound/afghan/images/random", "breeds/image/random"])
def test_get_bread_have_image(dog_api, url):
    response = dog_api.get(f"{url}")
    assert response.status_code == 200
    assert response.json()["status"] == 'success'
    assert '.jpg' in response.json()["message"]


# проверка подпород
@pytest.mark.parametrize("breed, expected", [
    ("hound", ['afghan', 'basset', 'blood', 'english', 'ibizan', 'plott', 'walker']),
    ("bulldog", ['boston', 'english', 'french']),
    ("mastiff", ['bull', 'english', 'tibetan']),
    ("pointer", ['german', 'germanlonghair']),
    ("retriever", ['chesapeake', 'curly', 'flatcoated', 'golden'])
])
def test_get_bread_sub(dog_api, breed, expected):
    response = dog_api.get(f"breed/{breed}/list")
    assert response.status_code == 200
    assert response.json()["status"] == 'success'
    #    print(response.json()["message"])
    #    print(expected)
    assert response.json()["message"] == expected
