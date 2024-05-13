from sqlite3 import connect


template_create_table_query = """
CREATE TABLE IF NOT EXISTS {table_name}
(
    {table_columns}
);
"""


class DatabaseManager:
    connection = None

    def __init__(self, database_path):
        self.connection = connect(database_path)

    def _execute(self, statement, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name, columns):
        columns_with_types = [f"{column_name} {data_type}" for column_name, data_type in columns.items()]
        string_columns = ",\n".join(columns_with_types)
        create_table_query = template_create_table_query.format(table_name=table_name,
                                                                table_columns=string_columns)
        self._execute(create_table_query)

    def __del__(self):
        self.connection.close()
