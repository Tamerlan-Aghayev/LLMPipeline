import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class QueryGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_sql_query(self, user_query, semantic_results):
        prompt = f"""Generate a SQL query for this user request: "{user_query}"

                    Use these schema details:
                    {json.dumps(semantic_results, indent=2)}

                    Rules:
                    1. Return ONLY the SQL query.
                    2. Ensure the query is syntactically correct and optimized.
                    3. Use the most relevant schema, table, and column names from the provided details.
                    4. Support complex queries including JOINs, subqueries, and aggregations as needed.
                    5. Do not include any explanations, comments, or formatting symbols like ```.
                    6. For example, if there is a data to retrieve from a specific table, write Select * FROM schema_name.table_name

                    """

        print(prompt)
        response = self.model.generate_content([prompt])
        return response.text.strip()
    

    def correct_query(self, sql_query, error_message, semantic_results):
        correction_prompt = f"""Correct this SQL query that produced an error:

                                SQL Query: {sql_query}
                                Error: {error_message}
                                Use these schema details:
                                {json.dumps(semantic_results, indent=2)}

                                Rules:
                                1. Return ONLY the corrected SQL query.
                                2. Ensure the query is syntactically correct and resolves the error.
                                3. Maintain the original query's intent.
                                4. Do not include any explanations, comments, or formatting symbols like ```.
                                5. For example, if there is a data to retrieve from a specific table, write Select * FROM schema_name.table_name
                                """


        response = self.model.generate_content([correction_prompt])
        return response.text.strip()