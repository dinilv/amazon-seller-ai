
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_vertexai.llms import VertexAI
from langchain_google_vertexai.chat_models import ChatVertexAI
from langchain_core.prompts.prompt import PromptTemplate 

def get_text_embedding():
    embeddings = VertexAIEmbeddings(
    model_name="textembedding-gecko@latest",
    max_tokens=1024,
    max_output_tokens=1024,
    temperature=0.1,
    top_p=0.8,
    )
    return embeddings

def get_codechat_model():
    query_model = ChatVertexAI(model_name="codechat-bison", max_output_tokens=2048)
    return query_model

def get_query_prompt_template(sql_project,sql_dataset,sql_prompt:str):
    prompt_template = PromptTemplate(
    input_variables=["context", "question", "project", "dataset"],
    template=sql_prompt)
    partial_prompt = prompt_template.partial(project=sql_project,
                                       dataset=sql_dataset)
    return partial_prompt