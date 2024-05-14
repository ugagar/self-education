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
