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
        self.execute(
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
                "IS_CONFIRMED": ("NULL" if (IS_CONFIRMED is None) else IS_CONFIRMED),
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
