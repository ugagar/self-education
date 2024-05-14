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





