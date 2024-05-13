from requests import get, post
import unittest

URL = "http://" + "127.0.0.1" + ":" + "7777"


# Add book to userbooks DB
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


def modify_books():
    header = {"Content-type": "application/json"}
    cookies = {"session": "admin"}
    data = {
        "old_title": "The Book",
        "available": 1,
        "title": "New Book",
        "writer": "I'm writer",
        "publisher": "We Publish books",
        "amount": 3,
        "field": "IT",
        "category": "IT",
    }

    response = post(
        url=URL + "/admin/books/modify", cookies=cookies, json=data, headers=header
    )
    if response.status_code == 200:
        return True
    else:
        return response.text


def delete_book():
    header = {"Content-type": "application/json"}
    cookies = {"session": "admin"}
    data = {"title": "New Book"}

    response = post(
        url=URL + "/admin/books/delete", cookies=cookies, json=data, headers=header
    )
    if response.status_code == 200:
        return True
    else:
        return response.text


def checkout_book():
    header = {"Content-type": "application/json"}
    data = {"title": "The Book"}

    response = post(url=URL + "/checkout", json=data, headers=header)
    if response.status_code == 200:
        return True
    else:
        return response.text


class SampleTest(unittest.TestCase):
    def test_add_book(self):
        result = add_book()
        print(result)
        self.assertTrue(result == True)

    def test_modify_book(self):
        result = modify_books()
        print(result)
        self.assertTrue(result == True)

    def test_delete_book(self):
        result = delete_book()
        print(result)
        self.assertTrue(result == True)

    def test_checkout_book(self):
        result = checkout_book()
        print(result)
        self.assertTrue(result == True)


if __name__ == "__main__":
    unittest.main()
