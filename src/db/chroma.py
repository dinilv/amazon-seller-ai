from langchain.schema.vectorstore import VectorStoreRetriever
from langchain.vectorstores.chroma import Chroma

class ChromaVectorStoreManager:
    def __init__(self):
        self.vector_stores = {}

    def create_vector_store(self, database_id, schemas, embeddings):       
        # Create a vector store from the collection
        vector_store = Chroma.from_texts(schemas, embedding=embeddings)
        n_docs = len(vector_store.get()['ids'])
        print(f"The vector store has {n_docs} documents")
        # Add the vector store to the dictionary with the database ID as the key
        self.vector_stores[database_id] = vector_store

    def get_vector_store(self, database_id:str) -> VectorStoreRetriever:
        # Return the vector store for the specified database ID
        vector_store=self.vector_stores.get(database_id)
        n_docs = len(vector_store.get()['ids'])
        print(f"The vector store has {n_docs} documents")
        return vector_store
    
    def get_documents(self,retriever: VectorStoreRetriever, question: str) -> str:
        # Return only the first document
        output = ""
        for d in retriever.get_relevant_documents(question):
            output += d.page_content
            output += "\n"
        return output
    
    def get_vector_documents(self, database_id: str, question: str) -> str:
        vector_store=self.get_vector_store(database_id)
        retriever = vector_store.as_retriever(search_kwargs={'k': 1})
        docs=self.get_documents(retriever,question)
        return docs
