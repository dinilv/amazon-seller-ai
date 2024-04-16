from flask import jsonify, request
from ...db.bigquery import BigQueryManager 
from ...db.chroma import ChromaVectorStoreManager 
from ...utils.dataset_resolver import resolve_sales_dataset
from ...utils.vertex_ai import get_codechat_model
from ...utils.vertex_ai import get_query_prompt_template
from langchain.schema import StrOutputParser
from operator import itemgetter

class SalesPromptHandler:
    def __init__(self, bigquery_manager: BigQueryManager,chroma_vector_store: ChromaVectorStoreManager):
        self.bigquery_manager = bigquery_manager
        self.chroma_vector_store = chroma_vector_store
        self.codechat_model=get_codechat_model()
        self.BIGQUERY_PROJECT = "gcpa-415907"
        self.SQL_PROMPT = """You are a SQL and BigQuery expert.

            Your job is to create a query for BigQuery in SQL.

            The following paragraph contains the schema of the table used for a query. It is encoded in JSON format.

            {context}

            Create a BigQuery SQL query for the following user input, using the above table.

            Follow these restrictions strictly:
            - Only return the SQL code.
            - Do not add backticks or any markup. Only write the query as output. NOTHING ELSE.
            - In FROM, always use the full table path, using `{project}` as project and `{dataset}` as dataset.
            - Always transform country names to full uppercase. For instance, if the country is Japan, you should use JAPAN in the query.
            - Always cast any date field to DATE(field)

            User input: {question}

            SQL query:
            """
        
    def process(self, seller_id):
        # Retrieve JSON data from the request body
        data = request.get_json()

        # Extract geo and text parameters from the JSON data
        geo = data.get('geo')
        text = data.get('text')
        project = data.get('project')
        if not project:
            # The 'project' key does not exist or its value is empty
            project=self.BIGQUERY_PROJECT 
        dataset=resolve_sales_dataset(geo).lower()
        
        # prompt modelling
        prompt_template = get_query_prompt_template(project,dataset,self.SQL_PROMPT)
        
        # model pipeline
        context = self.chroma_vector_store.get_vector_documents(dataset,text)
        docs = {"context": lambda x: context}
        question = {"question": itemgetter("input")}
        query_chain = docs | question | prompt_template | self.codechat_model
        query = query_chain | StrOutputParser()
        x={"input": {text}}
        
        # query generation
        sql_query=query.invoke(x)
        sql_query = sql_query.strip()[6:-3]

        # execute sql query
        results=self.bigquery_manager.execute_query(sql_query)
        sql_query=str(sql_query.replace('\n', ''))

        print(f"SQL {sql_query} documents")
        response_data = {
            'query': sql_query,
            'results': results

        }


        return jsonify(response_data)
