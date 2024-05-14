import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("databases/mainDB.db", isolation_level=None)
        self.cursor = self.connection.cursor()

    def execute(self, query, arguments=[]):
        self.cursor.execute(query, arguments)

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
        self.execute(
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
        self.execute(
            """
                DELETE FROM USER
                WHERE ID = :ID ;
            """,
            {"ID": ID},
        )
