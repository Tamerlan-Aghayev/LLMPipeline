from sentence_transformers import SentenceTransformer, util
import torch

class SemanticMatcher:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def semantic_search(self, query, all_schemas):
        query_embedding = self.model.encode(query, convert_to_tensor=True)

        table_embeddings = []
        table_info = []
        column_embeddings = []
        column_info = []

        for schema_name, schema in all_schemas.items():
            for table in schema['tables']:
                table_embeddings.append(self.model.encode(f"{schema_name} {table['name']}", convert_to_tensor=True))
                table_info.append((schema_name, table))

                for column in table['columns']:
                    column_embeddings.append(self.model.encode(f"{schema_name} {table['name']} {column['name']}", convert_to_tensor=True))
                    column_info.append((schema_name, table, column))

        table_embeddings = torch.stack(table_embeddings)
        column_embeddings = torch.stack(column_embeddings)

        table_similarities = util.pytorch_cos_sim(query_embedding, table_embeddings)[0]
        column_similarities = util.pytorch_cos_sim(query_embedding, column_embeddings)[0]

        top_tables = torch.topk(table_similarities, k=min(5, len(table_info)))
        top_columns = torch.topk(column_similarities, k=min(10, len(column_info)))

        result = {
            "tables": [
                {
                    "schema": table_info[i][0],
                    "table": table_info[i][1],
                    "score": score.item()
                } for i, score in zip(top_tables.indices, top_tables.values)
            ],
            "columns": [
                {
                    "schema": column_info[i][0],
                    "table": column_info[i][1],
                    "column": column_info[i][2],
                    "score": score.item()
                } for i, score in zip(top_columns.indices, top_columns.values)
            ]
        }

        return result