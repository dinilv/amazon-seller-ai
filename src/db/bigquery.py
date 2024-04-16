# sql imports
from sqlalchemy import *
from sqlalchemy.schema import *
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import Session
from sqlalchemy.dialects import registry
from google.cloud import bigquery
import json

# Register the BigQuery dialect
registry.register('bigquery', 'sqlalchemy_bigquery', 'BigQueryDialect')
# bigquery project details

class BigQueryManager:
    BIGQUERY_PROJECT = "gcpa-415907"
    bq_client = bigquery.Client(project=BIGQUERY_PROJECT)
    
    def __init__(self):
        self.client = bigquery.Client(project=self.BIGQUERY_PROJECT)

    def list_schemas(self,dataset):
        q_tables = self.bq_client.list_tables(dataset=f"{self.BIGQUERY_PROJECT}.{dataset}")
        schemas = []
        for bq_table in q_tables:
            t = self.bq_client.get_table(f"{self.BIGQUERY_PROJECT}.{dataset}.{bq_table.table_id}")
            schema_fields = [f.to_api_repr() for f in t.schema]
            schema = f"The schema for table {bq_table.table_id} is the following: \n```{json.dumps(schema_fields, indent=1)}```"
            schemas.append(schema)
        print(f"Found {len(schemas)} tables in dataset {self.BIGQUERY_PROJECT}:{dataset}")
        return schemas
    
    def execute_query(self,sql_query:str):
        # run query on BQ
        query_job = self.bq_client.query(sql_query)
        results = query_job.result()
        # Assuming results is an iterable containing rows
        formatted_results = []
        for row in results:
            formatted_row = dict(row.items())
            formatted_results.append(formatted_row)

        return formatted_results