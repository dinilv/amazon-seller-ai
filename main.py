from flask import Flask
from src.app.sales_prompt.handler import SalesPromptHandler
from src.db.bigquery import BigQueryManager 
from src.db.chroma import ChromaVectorStoreManager 
from src.utils.dataset_resolver import resolve_all_dataset
from src.utils.vertex_ai import get_text_embedding
from flask import jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
bq_manager=BigQueryManager()
chroma_vector_store=ChromaVectorStoreManager()
sp_handler=SalesPromptHandler(bq_manager,chroma_vector_store)
datasets = resolve_all_dataset()
embeddings=get_text_embedding()
for dataset in datasets:
    schemas=bq_manager.list_schemas(dataset)
    chroma_vector_store.create_vector_store(dataset,schemas,embeddings)

@app.route('/seller/<seller_id>/prompt', methods=['POST'])
def route_handler(seller_id):
    return sp_handler.process(seller_id)
@app.route('/health-check')
def health_check():
    return jsonify({'status': 'healthy'}), 200
@app.route('/')
def default():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True)
