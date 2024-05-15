import sys
from datetime import datetime

from ..manager_db import DatabaseManager

db = DatabaseManager("bookmarks.db")


class CreateBookmarksTableCommand:
    @staticmethod
    def execute():
        columns = {"id": "integer primary key autoincrement",
                   "title": "text not null",
                   "ulr": "text not null",
                   "notes": "text",
                   "date_added": "text not null"}
        db.create_table(table_name="bookmarks", columns=columns)


class AddBookmarkCommand:
    @staticmethod
    def execute(data):
        data["date_added"] = datetime.utcnow().isoformat()
        db.insert_table(table_name="bookmarks", data=data)
        return "Successful added new bookmarks"


class ListBookmarksCommand:
    def __init__(self, criteria=None,order_by="date_added"):
        self.order_by = order_by
        self.criteria = criteria

    def execute(self):
        result = db.select_data(table_name="bookmarks",
                                criteria=self.criteria,
                                order_by=self.order_by)
        return result.fetchall()


class DeleteBookmarkCommand:
    @staticmethod
    def execute(data):
        db.delete_data_by_equal(table_name="bookmarks",
                                criteria={id: data})
        return "Bookmark delete"


class QuitCommand:
    @staticmethod
    def execute():
        sys.exit()
