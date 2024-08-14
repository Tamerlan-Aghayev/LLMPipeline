import mysql.connector
import json

class SchemaExtractor:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def extract_schemas(self, schemas=None):
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        cursor = connection.cursor()

        if not schemas:
            cursor.execute("SHOW DATABASES")
            schemas = [schema[0] for schema in cursor.fetchall() if schema[0] not in ['information_schema', 'mysql', 'performance_schema', 'sys']]

        all_schemas = {}

        for schema_name in schemas:
            cursor.execute(f"USE {schema_name}")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            schema = {"tables": []}

            for table in tables:
                table_name = table[0]
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()

                table_schema = {
                    "name": table_name,
                    "columns": [
                        {
                            "name": column[0],
                            "type": column[1].split('(')[0].upper()
                        } for column in columns
                    ]
                }

                schema["tables"].append(table_schema)

            all_schemas[schema_name] = schema

        cursor.close()
        connection.close()

        return all_schemas

    def save_schemas(self, schemas, filename):
        with open(filename, 'w') as f:
            json.dump(schemas, f, indent=2)