from elasticsearch import Elasticsearch
from transformers import AutoModel, AutoTokenizer
import numpy as np
import torch

# 配置 Elasticsearch 连接信息
es_host = "localhost"  # Elasticsearch 服务器地址
es_port = 9200         # Elasticsearch 服务端口
index_name = "embeddings"  # 索引名称

# 创建 Elasticsearch 客户端
es = Elasticsearch([{"host": es_host, "port": es_port}])

# 检查连接是否成功
if not es.ping():
    raise ValueError("Connection failed")

print("Connected to Elasticsearch!")

# 指定本地模型路径
model_path = "C:\\Users\\thinkpad\\.cache\\modelscope\\hub\\iic\\nlp_gte_sentence-embedding_chinese-large"

# 加载本地模型和分词器
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)

# 输入文本
input_text = "罚款"

# 计算输入文本的嵌入向量
inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
with torch.no_grad():
    outputs = model(**inputs)
    input_embedding = outputs.last_hidden_state.mean(dim=1).numpy().tolist()[0]

# 定义 KNN 查询
query = {
    "size": 5,  # 返回最相似的 5 个结果
    "query": {
        "knn": {
            "embedding": {  # 指定嵌入字段
                "vector": input_embedding,
                "k": 5,  # 搜索最接近的 5 个向量
                "filter": {
                    "match_all": {}  # 可以添加过滤条件
                }
            }
        }
    }
}

# 执行检索操作
try:
    response = es.search(index=index_name, body=query)
    print("Search Results:")
    for hit in response["hits"]["hits"]:
        print(f"ID: {hit['_id']}")
        print(f"Score: {hit['_score']}")
        print(f"Text: {hit['_source']['text']}")
        print("-" * 50)
except Exception as e:
    print(f"Error during search: {e}")