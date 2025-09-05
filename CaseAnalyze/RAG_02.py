import json
import faiss
import numpy as np
import gradio as gr
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# 读取 embeddings.json 文件
def load_embeddings(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        embeddings_data = json.load(f)
    texts = [item['text'] for item in embeddings_data]
    embeddings = np.array([item['embedding'] for item in embeddings_data], dtype=np.float32)
    return texts, embeddings

# 创建 Faiss 索引
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]  # 嵌入向量的维度
    index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离度量创建一个扁平索引
    index.add(embeddings)  # 将嵌入向量添加到 Faiss 索引
    return index

# 初始化模型用于生成查询嵌入
#model_id_embedding = "maple77/xiaobu-embedding-v2"
model_id_embedding = "iic/nlp_gte_sentence-embedding_chinese-large"
pipeline_se = pipeline(Tasks.sentence_embedding, model=model_id_embedding)

# 初始化 LLM 模型（选择适合文本生成的模型）
model_id_llm = "Qwen/Qwen2.5-0.5B-Instruct"
pipeline_llm = pipeline(Tasks.text_generation, model=model_id_llm)

# 提示词模板
PROMPT_TEMPLATE = "以下是基于输入语句的相关查询：'{query}'。请返回最相关的结果。"

def search_similar(query, texts, index):
    if not query.strip():  # 如果用户没有输入文本，返回空 JSON
        return json.dumps({"error": "Query is empty. Please enter valid text."}, ensure_ascii=False)

    # 使用提示词增强查询
    enhanced_query = PROMPT_TEMPLATE.format(query=query)

    # 生成查询文本的嵌入向量
    result = pipeline_se(input={"source_sentence": [enhanced_query]})
    query_embedding = np.array(result["text_embedding"], dtype=np.float32).reshape(1, -1)

    # 检索不同数量的相似结果
    k_values = [100, 200, 500, 1000]
    best_result = None
    best_similarity = -float('inf')

    for k in k_values:
        distances, indices = index.search(query_embedding, k)
        # 找到最相似的结果
        most_similar_idx = indices[0][0]
        most_similar_distance = distances[0][0]
        similarity = 1 / (1 + most_similar_distance)  # 将Faiss返回的L2距离转换为相似度

        if similarity > best_similarity:
            best_similarity = similarity
            best_result = {
                "text": texts[most_similar_idx],
                "similarity": similarity
            }

    # 构造 LLM 的输入提示
    llm_prompt = f"以下是与用户问题相关的内容：\n\n检索内容：\n{best_result['text']}\n\n用户问题：{query}\n\n请根据这些信息回答是或者不是："

    # 使用 LLM 生成回答
    llm_result = pipeline_llm(input=llm_prompt, max_length=5000)
    answer = llm_result["text"]

    # 构造 JSON 输出
    return json.dumps({
        "query": query,
        "most_similar_context": best_result["text"],
        "similarity": best_result["similarity"],
        "generated_answer": answer
    }, ensure_ascii=False, indent=2)

# 加载四个不同的嵌入向量文件
embeddings_data_files = ["embedding_01.json", "embedding_02.json", "embedding_03.json", "embedding_04.json"]
interfaces = []

for i, file in enumerate(embeddings_data_files):
    texts, embeddings = load_embeddings(file)
    index = create_faiss_index(embeddings)

    # 为每个文件创建一个Gradio接口
    interface = gr.Interface(
        fn=lambda query, texts=texts, index=index: search_similar(query, texts, index),
        inputs=gr.Textbox(label=f"Enter your query for {file}", placeholder="Type your question or query..."),
        outputs=gr.JSON(label="Search Results"),
        live=True
    )

    interfaces.append(interface)

# 启动所有 Gradio 界面
gr.TabbedInterface(interfaces).launch()
