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
        "field": ["IT", "Novel"],
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
        "category": ["Math", "Art"],
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
    data = {"title": "The Book"}

    response = post(
        url=URL + "/admin/books/delete", cookies=cookies, json=data, headers=header
    )
    if response.status_code == 200:
        return True
    else:
        return response.text


def checkout_book():
    header = {"Content-type": "application/json"}
    cookies = {"session": "user"}
    data = {"title": "The Book"}

    response = post(url=URL + "/checkout", json=data, headers=header, cookies=cookies)
    if response.status_code == 200:
        return True
    else:
        return response.text


def apply_book():
    header = {"Content-type": "application/json"}
    cookies = {"session": "user"}
    data = {
        "title": "Apply Book",
        "writer": "I'm writer",
        "publisher": "We Publish books",
        "reason": "I have to read",
    }

    response = post(url=URL + "/apply", json=data, headers=header, cookies=cookies)
    if response.status_code == 200:
        return True
    else:
        return response.text


def admin_delete_apply_book():
    header = {"Content-type": "application/json"}
    cookies = {"session": "admin"}
    data = {
        "title": "Apply Book",
        "student_number": "22222222",
        "method": "delete",
    }

    response = post(
        url=URL + "/admin/apply", json=data, headers=header, cookies=cookies
    )
    if response.status_code == 200:
        return True
    else:
        return response.text


def admin_modify_apply_book():
    header = {"Content-type": "application/json"}
    cookies = {"session": "admin"}
    data = {
        "title": "Apply Book",
        "student_number": "22222222",
        "method": "confirm",
    }

    response = post(
        url=URL + "/admin/apply", json=data, headers=header, cookies=cookies
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

    def test_apply_book(self):
        result = apply_book()
        print(result)
        self.assertTrue(result == True)

    def test_admin_delete_apply_book(self):
        result = admin_delete_apply_book()
        print(result)
        self.assertTrue(result == True)

    def test_admin_modify_apply_book(self):
        result = admin_modify_apply_book()
        print(result)
        self.assertTrue(result == True)


if __name__ == "__main__":
    unittest.main()
