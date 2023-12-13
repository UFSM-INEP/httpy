import httpy
import json


def test_get_one():
    response = httpy.get_one('https://reqres.in/api/users/1')

    response.raise_for_status()

    print(json.dumps(response.json(), indent=4))


def test_get_multiple():
    urls = [f'https://reqres.in/api/users/{i}' for i in range(1, 11)]

    responses = httpy.get_multiple(urls)

    for response in responses:
        response.raise_for_status()

        print(json.dumps(response.json(), indent=4))
