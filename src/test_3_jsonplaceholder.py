import pytest
from allpairspy import AllPairs


# негативные проверки для пользователей
@pytest.mark.parametrize('userID', [-3, 0, 'b', 13],
                         ids=["negative", "zero", "letter", "out_of_range"])
def test_api_empty_response_on_user_id(userID, jsonplaceholder_api):
    response = jsonplaceholder_api.get(f"users/{userID}")
    assert response.status_code == 404
    assert response.json() == {}


# позитивные проверки для пользователей
@pytest.mark.parametrize('userID', [1, 3, 6, 10])
def test_api_response_on_user_id(userID, jsonplaceholder_api):
    response = jsonplaceholder_api.get(f"users/{userID}")
    assert response.status_code == 200
    numbers_of_elements = len(response.json())
    assert numbers_of_elements == 8
    assert response.json()["id"] == userID


# проверка создания поста
@pytest.mark.parametrize("title, body, userID", [
    value_list for value_list in AllPairs([
        ["New_post", "", "nuts", "nuts1234567890~!@#$%^&*()_+"],
        ["New_body", "", "squirrel loves nuts", "465~!@#$%^&*()_+|}{|/*-+312"],
        [1, 6, 13, 21]
    ])
])
def test_created_post(jsonplaceholder_api, title, body, userID):
    response = jsonplaceholder_api.post("posts", data={'title': title, 'body': body, 'userId': userID})
#    print(response.json())
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()["userId"] == f'{userID}'
    assert response.json()["title"] == title
    assert response.json()["body"] == body

# проверка изменения поста
@pytest.mark.parametrize("id, title, body, userID", [
    value_list for value_list in AllPairs([
        [1, 5, 10],
        ["Edit_post", "Edit_nuts", "Edit_nuts1234567890~!@#$%^&*()_+"],
        ["Edit_body", "Edit_squirrel loves nuts", "Edit_465~!@#$%^&*()_+|}{|/*-+312"],
        [1, 6, 13]
    ])
])
def test_update_post(jsonplaceholder_api, id, title, body, userID):
    response = jsonplaceholder_api.put(f"posts/{id}", data={'title': title, 'body': body, 'userId': userID})
#    print(response.json())
    assert response.status_code == 200
    assert response.json()["id"] == id
    assert response.json()["userId"] == f'{userID}'
    assert response.json()["title"] == title
    assert response.json()["body"] == body

# проверка пограничных значений
@pytest.mark.parametrize("resourcse, expected", [
    ("posts", 100),
    ("comments", 500),
    ("albums", 100),
    ("photos", 5000),
    ("todos", 200),
    ("users", 10)
])
def test_get_max_number(jsonplaceholder_api, resourcse, expected):
    response = jsonplaceholder_api.get(f"{resourcse}")
    assert response.status_code == 200
    numbers_of_elements = len(response.json())
    assert numbers_of_elements == expected
