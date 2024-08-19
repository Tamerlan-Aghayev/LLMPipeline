import json
from openai import OpenAI
from src.schema.schema_extractor import SchemaExtractor

class QueryGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
        self.prompt = f'''You are a SQL Expert, and you need to create queries based on given prompt. There is a must-to-follow rules:
                            1. Do not include any explanations, comments, or other symbols, especially symbols like ``` or ```sql.
                            2. Return ONLY the SQL query, do not use formatting around.
                            3. Ensure the query is syntactically correct and optimized.
                            4. Use the most relevant schema, table, and column names from the provided details.
                            5. Support complex queries including JOINs, subqueries, and aggregations as needed.
                            6. For example, if there is a data to retrieve from a specific table, write Select * FROM schema_name.table_name
                            
                            Here is schema structure: {SchemaExtractor.read_file_content("schemas.json")}
                            '''
    def generate_sql_query(self, user_query, semantic_results):
        question = f"""Generate a SQL query for this user request: "{user_query}"
                    Use these schema details:
                    {json.dumps(semantic_results, indent=2)}                    
                    """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()

    def correct_query(self, sql_query, error_message, semantic_results):
        question = f"""Correct this SQL query that produced an error:

                                SQL Query: {sql_query}
                                Error: {error_message}
                                Use these schema details:
                                {json.dumps(semantic_results, indent=2)}
                                """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()