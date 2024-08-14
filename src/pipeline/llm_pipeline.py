from src.schema.schema_extractor import SchemaExtractor
from src.semantic_search.semantic_matcher import SemanticMatcher
from src.query_generation.query_generator import QueryGenerator
from src.utils.database_utils import QueryExecutor


class LLMPipeline:
    def __init__(self, config):
        self.config = config
        self.schema_extractor = SchemaExtractor(
            config['mysql']['host'],
            config['mysql']['user'],
            config['mysql']['password']
        )
        self.semantic_matcher = SemanticMatcher()
        self.query_generator = QueryGenerator(config["google"]["api_key"])
        self.query_executor = QueryExecutor(
            config['mysql']['host'],
            config['mysql']['user'],
            config['mysql']['password']
        )

    def run(self, user_query):
        all_schemas = self.schema_extractor.extract_schemas(self.config['schemas_to_extract'])
        self.schema_extractor.save_schemas(all_schemas, 'schemas.json')

        semantic_results = self.semantic_matcher.semantic_search(user_query, all_schemas)

        sql_query = self.query_generator.generate_sql_query(user_query, semantic_results)

        success, result = self.query_executor.execute_query(sql_query)

        if not success:
            corrected_query = self.query_generator.correct_query(sql_query, result, semantic_results)
            success, result = self.query_executor.execute_query(corrected_query)
            corrected_success, corrected_result=self.query_executor.execute_query(corrected_query)
            return corrected_success, corrected_result, corrected_query
        return success, result, sql_query