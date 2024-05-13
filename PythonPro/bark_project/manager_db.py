from sqlite3 import connect


template_create_table_query = """
CREATE TABLE IF NOT EXISTS {table_name}
(
    {table_columns}
);
"""

template_insert_table_query = """
INSERT INTO {table_name}
({column_names})
VALUES ({column_values});
"""

template_delete_data_from_table_query = """
DELETE FROM {table_name}
WHERE {delete_criteria}
"""

template_select_query = """
SELECT {columns} FORM {table_name}
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

    def insert_table(self, table_name, data):
        column_names = ", ".join(data.keys())
        placeholders = ", ".join("?"*len(data))
        insert_table_query = template_insert_table_query.format(table_name=table_name,
                                                                column_names=column_names,
                                                                column_values=placeholders)
        column_values = tuple(data.values())
        self._execute(insert_table_query, column_values)

    def delete_data_by_equal(self, table_name, criteria):
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        delete_query = template_delete_data_from_table_query.format(table_name=table_name,
                                                                    delete_criteria=delete_criteria)
        self._execute(delete_query, tuple(criteria.values()))

    def select_data(self, table_name, columns=None, criteria=None, order_by=None):
        criteria = criteria or {}
        columns = columns or ["*"]

        query = template_select_query.format(table_name=table_name,
                                             columns=", ".join(columns))

        criteria_value = tuple(criteria.values())
        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            query += f"WHERE {select_criteria}"

        if order_by:
            query += f"ORDER BY {order_by}"

        self._execute(query, criteria_value)

    def __del__(self):
        self.connection.close()
