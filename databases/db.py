import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("databases/mainDB.db")
        self.cursor = self.connection.cursor()

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
        return self.fetchone()

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
        self.commit()

    def delete_user(self, ID: int):
        self.execute(
            """
                DELETE FROM USER
                WHERE ID = :ID ;
            """,
            {"ID": ID},
        )
        self.commit()
