import json
import faiss
import numpy as np
import gradio as gr
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# 读取 embeddings.json 文件
input_file = "embeddings.json"

with open(input_file, "r", encoding="utf-8") as f:
    embeddings_data = json.load(f)

# 提取嵌入向量和文本
texts = [item['text'] for item in embeddings_data]
embeddings = np.array([item['embedding'] for item in embeddings_data], dtype=np.float32)

# 创建 Faiss 索引
dimension = embeddings.shape[1]  # 嵌入向量的维度
index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离度量创建一个扁平索引
index.add(embeddings)  # 将嵌入向量添加到 Faiss 索引

# 初始化模型用于生成查询嵌入
model_id = "iic/nlp_gte_sentence-embedding_chinese-large"
pipeline_se = pipeline(Tasks.sentence_embedding, model=model_id, sequence_length=512)

# 定义搜索函数
def search_similar(query):
    if not query.strip():  # 如果用户没有输入文本，返回空字符串
        return json.dumps({"error": "Query cannot be empty"}, ensure_ascii=False, indent=4)

    # 提示词工程：调整查询内容
    enhanced_query = f"以下是基于输入语句生成的相关性查询：{query}"

    # 生成查询文本的嵌入向量
    result = pipeline_se(input={"source_sentence": [enhanced_query]})
    query_embedding = np.array(result["text_embedding"], dtype=np.float32).reshape(1, -1)

    # 返回最相似的 6 个结果
    k = 6
    distances, indices = index.search(query_embedding, k)

    # 获取最相似的文本及其相似度
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "rank": i + 1,
            "text": texts[idx],
            "similarity_score": float(distances[0][i])
        })

    return json.dumps({"query": query, "results": results}, ensure_ascii=False, indent=4)

# 创建 Gradio 接口
interface = gr.Interface(
    fn=search_similar,
    inputs=gr.Textbox(label="Enter query text", placeholder="Enter a sentence to search..."),
    outputs=gr.Textbox(label="Search Results (JSON)", placeholder="Results will be displayed here..."),
    live=True
)

# 启动 Gradio 界面
interface.launch()
