from requests import get, post
import unittest

URL = "http://" + "127.0.0.1" + ":" + "7777"


def add_book():
    header = {"Content-type": "application/json"}
    cookies = {"session": "admin"}
    data = {
        "available": 1,
        "title": "The Book",
        "writer": "I'm writer",
        "publisher": "We Publish books",
        "amount": 3,
        "field": "IT",
        "category": "IT",
    }

    response = post(
        url=URL + "/admin/books/add", cookies=cookies, json=data, headers=header
    )
    if response.status_code == 200:
        return True
    else:
        return response.text


class SampleTest(unittest.TestCase):
    def test_add_book(self):
        result = add_book()
        print(result)
        self.assertTrue(result == True)


if __name__ == "__main__":
    unittest.main()
