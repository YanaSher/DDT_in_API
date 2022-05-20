import pytest


# проверка ошибки ввода фильтра
def test_api_brewery_type_error(openbrewerydb_api):
    response = openbrewerydb_api.get("breweries?by_type=nan")
    #    print("status=", response.status_code)
    assert response.status_code == 400
    print(response.json())
    assert response.json()[
               "errors"] == [
               'Brewery type must include one of these types: ["micro", "nano", "regional", "brewpub", "large", "planning", "bar", "contract", "proprieter", "closed"]']


# проверка фильтра по типу пивоварни
@pytest.mark.parametrize('brewery_type', ["nano", "large", "bar", "contract", "planning"])
def test_api_brewery_type(openbrewerydb_api, brewery_type):
    response = openbrewerydb_api.get(f"breweries?by_type={brewery_type}")
    assert response.status_code == 200
    numbers_of_elements = len(response.json())
    #    print("количество элементов в списке =", numbers_of_elements)
    #    print("весь джсон", response.json())
    for i in range(numbers_of_elements):
        #   print("по индексу" ,response.json()[i]["brewery_type"])
        assert response.json()[i]["brewery_type"] == brewery_type


# проверка автозаполнения
@pytest.mark.parametrize('autocomplete', ["dog", "sea", "dark", "river"])
def test_api_autocomplete_random(openbrewerydb_api, autocomplete):
    response = openbrewerydb_api.get(f"breweries/autocomplete?{autocomplete}")
    assert response.status_code == 200
    numbers_of_elements = len(response.json())
    for i in range(numbers_of_elements):
        assert '{autocomplete}' in response.json()[i]


# проверка что в автозаполнении у пивоварни только два значения
@pytest.mark.parametrize('parametr',
                         ['brewery_type', 'street', 'address_2', 'address_3', 'city', 'state', 'county_province',
                          'postal_code', 'country', 'longitude', 'latitude', 'phone', 'website_url', 'updated_at',
                          'created_at'])
def test_api_autocomplete_2_parametrs(openbrewerydb_api, parametr):
    response = openbrewerydb_api.get("breweries/autocomplete?river")
    assert response.status_code == 200
    numbers_of_elements = len(response.json())
    for i in range(numbers_of_elements):
        assert '{autocomplete}' not in response.json()[i]


# проверка открытия конкретной пивоварни
def test_api_breweries(openbrewerydb_api):
    response = openbrewerydb_api.get("breweries/madtree-brewing-cincinnati")
    assert response.status_code == 200
    len(response.json()) == 17
    response.json()["name"] == "MadTree Brewing"
    response.json()["city"] == "Cincinnati"
