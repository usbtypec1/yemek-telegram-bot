import sqlite3
import datetime
from dataclasses import dataclass


__all__ = ("UsageStatisticsDao",)


@dataclass(frozen=True, slots=True, kw_only=True)
class UsageStatisticsDao:
    connection: sqlite3.Connection
    
    def __post_init__(self) -> None:
        with self.connection:
            self.connection.execute('''
            CREATE TABLE IF NOT EXISTS usages (
                user_id INTEGER NOT NULL,
                chat_id INTEGER NOT NULL,
                timestamp INTEGER NOT NULL
            );
            ''')
        

    def add_usage(self, user_id: int, chat_id: int) -> None:
        now = int(datetime.datetime.now().timestamp())
        statement = (
            "INSERT INTO usages (user_id, chat_id, timestamp) VALUES (?, ?, ?);"
        )
        with self.connection:
            self.connection.execute(statement, (user_id, chat_id, now))
            self.connection.commit()
