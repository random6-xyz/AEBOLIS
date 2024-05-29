import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("databases/mainDB.db", isolation_level=None)
        self.cursor = self.connection.cursor()

    # common command execute function
    def execute(self, query, arguments=[]):
        self.cursor.execute(query, arguments)
        result = self.cursor.fetchall()
        if not result and "INSERT" in query:
            return self.cursor.lastrowid
        return result

    def executemany(self, query, arguments):
        self.cursor.executemany(query, arguments)
        return self.cursor.fetchall()

    def execute_only(self, query, arguments=[]):
        self.cursor.execute(query, arguments)

    # TODO: @imStillDebugging Remove this useless function
    def commit(self):
        self.connection.commit()

    def select_account_info(self, ID: int) -> tuple:
        self.execute_only(
            """
                SELECT *
                FROM USER
                WHERE ID = :ID ;
            """,
            {"ID": ID},
        )
        return self.cursor.fetchone()

    def insert_account_info(
        self, ID: int, NAME: str, HASHED_PASSWORD: str, SALT: str, IS_CONFIRMED: int
    ) -> None:
        self.execute_only(
            """
                INSERT INTO USER(ID, NAME, HASHED_PASSWORD, SALT, IS_ADMIN, IS_CONFIRMED)
                VALUES (:ID, :NAME, :HASHED_PASSWORD, :SALT, 0, :IS_CONFIRMED) ;
            """,
            {
                "ID": ID,
                "NAME": NAME,
                "HASHED_PASSWORD": HASHED_PASSWORD,
                "SALT": SALT,
                "IS_CONFIRMED": IS_CONFIRMED,
            },
        )

    def delete_user(self, ID: int):
        self.execute_only(
            """
                DELETE FROM USER
                WHERE ID = :ID ;
            """,
            {"ID": ID},
        )

    def confirm_user(self, ID: int):
        self.execute_only(
            """
                UPDATE USER
                SET IS_CONFIRMED = 1
                WHERE ID = :ID ;
            """,
            {"ID": ID},
        )

    def reject_user(self, ID: int):
        self.execute_only(
            """
                UPDATE USER
                SET IS_CONFIRMED = 0
                WHERE ID = :ID ;
            """,
            {"ID": ID},
        )

    def select_public_account_info(self) -> tuple:
        self.execute_only(
            """
                SELECT ID, NAME, IS_ADMIN, IS_CONFIRMED
                FROM USER
                WHERE IS_ADMIN = 1
                ORDER BY ID ASC;
            """
        )
        user_data = list(self.cursor.fetchall())
        self.execute_only(
            """
                SELECT ID, NAME, IS_ADMIN, IS_CONFIRMED
                FROM USER
                WHERE IS_CONFIRMED IS NULL
                ORDER BY ID ASC;
            """
        )
        user_data.extend(list(self.cursor.fetchall()))

        self.execute_only(
            """
                SELECT ID, NAME, IS_ADMIN, IS_CONFIRMED
                FROM USER
                WHERE IS_CONFIRMED IS NOT NULL
                AND IS_ADMIN = 0
                ORDER BY ID ASC;
            """
        )

        user_data.extend(list(self.cursor.fetchall()))

        return tuple(user_data)

    def select_book_apply_list(self, STUDENT_NUMBER: int) -> tuple:
        self.execute_only(
            """
                SELECT 
                STUDENT_NUMBER, TITLE, PUBLISHER, WRITER, REASON, CONFIRM
                FROM USERAPPLYS
                WHERE STUDENT_NUMBER = :STUDENT_NUMBER 
                ORDER BY ID DESC;
            """,
            {"STUDENT_NUMBER": STUDENT_NUMBER},
        )
        return self.cursor.fetchall()

    def select_book_checkout_list(self, STUDENT_NUMBER: int) -> tuple:
        self.execute_only(
            """
                SELECT STUDENT_NUMBER, TITLE, RETURN, TIME
                FROM CHECKOUT_HISTORY
                WHERE STUDENT_NUMBER = :STUDENT_NUMBER 
                ORDER BY RETURN ASC, ID DESC;
            """,
            {"STUDENT_NUMBER": STUDENT_NUMBER},
        )
        return self.cursor.fetchall()

    def return_book(self, STUDENT_NUMBER: int, TIME: str) -> None:
        self.execute_only(
            """
                UPDATE CHECKOUT_HISTORY
                SET RETURN = 1
                WHERE STUDENT_NUMBER = :STUDENT_NUMBER
                AND TIME = :TIME
            """,
            {"STUDENT_NUMBER": STUDENT_NUMBER, "TIME": TIME},
        )

    def select_profile_data(self, ID: int) -> tuple:
        self.execute_only(
            """
                SELECT NAME, ID, IS_ADMIN
                FROM USER
                WHERE ID = :ID;
            """,
            {"ID": ID},
        )
        profile_data = list(self.cursor.fetchone())
        profile_data[2] = "Admin" if (profile_data[2] == 1) else "User"
        return profile_data
