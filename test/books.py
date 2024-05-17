from requests import post
import unittest
from pandas import read_excel

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


# TODO: @random6 Add fronted
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


# TODO: @random6 Add fronted
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


# TODO: @random6 Add fronted
def checkout_book():
    header = {"Content-type": "application/json"}
    cookies = {"session": "user"}
    data = {"title": "The Book"}

    response = post(url=URL + "/checkout", json=data, headers=header, cookies=cookies)
    if response.status_code == 200:
        return True
    else:
        return response.text


# TODO: @random6 Add fronted
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


# TODO: @random6 Add fronted
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


def process_xlsx(file_name):
    xlsx = read_excel("./upload/" + file_name, "Sheet1")
    book_list = []

    for _, row in xlsx.iterrows():
        book_list.append(
            [
                row["책 제목"],
                row["지은이"],
                row["출판사"],
                row["수량"],
                1 if row["대출여부"] == "가능" else 0,
                row["분야"],
            ]
        )

    return book_list


def upload_xlsx():
    cookies = {"session": "admin"}
    files = {"file": open("./upload/books.xlsx", "rb")}

    response = post(url=URL + "/admin/books/upload", files=files, cookies=cookies)
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

    def test_process_xlsx(slef):
        result = process_xlsx("books.xlsx")
        print(result)

    def test_upload_xlsx(self):
        result = upload_xlsx()
        print(result)
        self.assertTrue(result == True)


if __name__ == "__main__":
    unittest.main()
