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

# 提示词模板
PROMPT_TEMPLATE = "以下是基于输入语句的相关查询：'{query}'。请返回最相关的结果。"

# 定义搜索函数
def search_similar(query):
    if not query.strip():  # 如果用户没有输入文本，返回空 JSON
        return json.dumps({"error": "Query is empty. Please enter valid text."}, ensure_ascii=False)

    # 使用提示词增强查询
    enhanced_query = PROMPT_TEMPLATE.format(query=query)

    # 生成查询文本的嵌入向量
    result = pipeline_se(input={"source_sentence": [enhanced_query]})
    query_embedding = np.array(result["text_embedding"], dtype=np.float32).reshape(1, -1)

    # 返回最相似的 k 个结果
    k = 6
    distances, indices = index.search(query_embedding, k)

    # 构造 JSON 输出
    search_results = []
    for rank, (idx, distance) in enumerate(zip(indices[0], distances[0]), start=1):
        search_results.append({
            "rank": rank,
            "text": texts[idx],
            "similarity_score": float(distance)
        })

    return json.dumps({"query": query, "results": search_results}, ensure_ascii=False, indent=2)

# 创建 Gradio 接口
interface = gr.Interface(
    fn=search_similar,
    inputs=gr.Textbox(label="Enter your query", placeholder="Type your question or query..."),
    outputs=gr.JSON(label="Search Results"),
    live=True
)

# 启动 Gradio 界面
interface.launch()
