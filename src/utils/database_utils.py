import mysql.connector
class QueryExecutor:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        
    def execute_query(self, sql_query):
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
        )
        cursor = connection.cursor()
        
        try:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return True, result
        except mysql.connector.Error as e:
            return False, str(e)
        finally:
            cursor.close()
            connection.close()