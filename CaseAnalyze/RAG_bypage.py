# import json
# import faiss
# import numpy as np
# import gradio as gr
# from modelscope.pipelines import pipeline
# from modelscope.utils.constant import Tasks
#
# # 读取 result_with_embeddings.json 文件
# def load_embeddings(input_file):
#     with open(input_file, "r", encoding="utf-8") as f:
#         embeddings_data = json.load(f)
#     texts = [item['content'] for item in embeddings_data]  # 每页的文本内容
#     embeddings = np.array([item['embedding'] for item in embeddings_data], dtype=np.float32)  # 每页的嵌入向量
#     return texts, embeddings
#
# # 创建 Faiss 索引
# def create_faiss_index(embeddings):
#     dimension = embeddings.shape[1]  # 嵌入向量的维度
#     index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离度量创建一个扁平索引
#     index.add(embeddings)  # 将嵌入向量添加到 Faiss 索引
#     return index
#
# # 初始化模型用于生成查询嵌入
# model_id_embedding = "iic/nlp_gte_sentence-embedding_chinese-large"
# pipeline_se = pipeline(Tasks.sentence_embedding, model=model_id_embedding, sequence_length=512)
#
# # 初始化 LLM 模型（选择适合文本生成的模型）
# model_id_llm = "Qwen/Qwen2.5-0.5B-Instruct"
# pipeline_llm = pipeline(Tasks.text_generation, model=model_id_llm)
#
# # 提示词模板
# PROMPT_TEMPLATE = "以下是基于输入语句的相关查询：'{query}'。请返回最相关的结果。"
#
# # 搜索最相似的页面
# def search_similar(query, texts, index):
#     if not query.strip():  # 如果用户没有输入文本，返回空 JSON
#         return json.dumps({"error": "Query is empty. Please enter valid text."}, ensure_ascii=False)
#
#     # 使用提示词增强查询
#     enhanced_query = PROMPT_TEMPLATE.format(query=query)
#
#     # 生成查询文本的嵌入向量
#     result = pipeline_se(input={"source_sentence": [enhanced_query]})
#     query_embedding = np.array(result["text_embedding"], dtype=np.float32).reshape(1, -1)
#
#     # 检索最相似的页面
#     k = 1  # 检索最相似的1个页面
#     distances, indices = index.search(query_embedding, k)
#     most_similar_idx = indices[0][0]
#     most_similar_distance = distances[0][0]
#     similarity = 1 / (1 + most_similar_distance)  # 将Faiss返回的L2距离转换为相似度
#
#     # 构造 LLM 的输入提示
#     llm_prompt = f"以下是与用户问题相关的内容：\n\n检索内容：\n{texts[most_similar_idx]}\n\n用户问题：{query}\n\n请根据这些信息回答："
#
#     # 使用 LLM 生成回答
#     llm_result = pipeline_llm(input=llm_prompt, max_length=5000)
#     answer = llm_result["text"]
#
#     # 构造 JSON 输出
#     return json.dumps({
#         "query": query,
#         "most_similar_context": texts[most_similar_idx],
#         "similarity": similarity,
#         "generated_answer": answer
#     }, ensure_ascii=False, indent=2)
#
# # 加载嵌入向量文件
# input_file = "E:\\CaseAnalyze\\output\\result_with_embeddings.json"
# texts, embeddings = load_embeddings(input_file)
# index = create_faiss_index(embeddings)
#
# # 创建 Gradio 接口
# interface = gr.Interface(
#     fn=lambda query: search_similar(query, texts, index),
#     inputs=gr.Textbox(label="Enter your query", placeholder="Type your question or query..."),
#     outputs=gr.JSON(label="Search Results"),
#     live=True
# )
#
# # 启动 Gradio 界面
# interface.launch()

import json
import faiss
import numpy as np
import gradio as gr
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


# 读取 result_with_embeddings.json 文件，并排除 page_number=14 的条目
def load_embeddings(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        embeddings_data = json.load(f)

    # 过滤掉 page_number=14 的条目
    filtered_data = [item for item in embeddings_data if item.get("page_number") != 14]

    texts = [item['content'] for item in filtered_data]  # 每页的文本内容
    embeddings = np.array([item['embedding'] for item in filtered_data], dtype=np.float32)  # 每页的嵌入向量
    return texts, embeddings


# 创建 Faiss 索引
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]  # 嵌入向量的维度
    index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离度量创建一个扁平索引
    index.add(embeddings)  # 将嵌入向量添加到 Faiss 索引
    return index


# 初始化模型用于生成查询嵌入
model_id_embedding = "iic/nlp_gte_sentence-embedding_chinese-large"
pipeline_se = pipeline(Tasks.sentence_embedding, model=model_id_embedding, sequence_length=512)

# 初始化 LLM 模型（选择适合文本生成的模型）
model_id_llm = "Qwen/Qwen2.5-0.5B-Instruct"
pipeline_llm = pipeline(Tasks.text_generation, model=model_id_llm)

# 提示词模板
PROMPT_TEMPLATE = "以下是基于输入语句的相关查询：'{query}'。请返回最相关的结果。"


# 搜索最相似的页面
def search_similar(query, texts, index):
    if not query.strip():  # 如果用户没有输入文本，返回空 JSON
        return json.dumps({"error": "Query is empty. Please enter valid text."}, ensure_ascii=False)

    # 使用提示词增强查询
    enhanced_query = PROMPT_TEMPLATE.format(query=query)

    # 生成查询文本的嵌入向量
    result = pipeline_se(input={"source_sentence": [enhanced_query]})
    query_embedding = np.array(result["text_embedding"], dtype=np.float32).reshape(1, -1)

    # 检索最相似的页面
    k = 1  # 检索最相似的1个页面
    distances, indices = index.search(query_embedding, k)
    most_similar_idx = indices[0][0]
    most_similar_distance = distances[0][0]
    similarity = 1 / (1 + most_similar_distance)  # 将Faiss返回的L2距离转换为相似度

    # 构造 LLM 的输入提示
    llm_prompt = f"以下是与用户问题相关的内容：\n\n检索内容：\n{texts[most_similar_idx]}\n\n用户问题：{query}\n\n请根据这些信息回答："

    # 使用 LLM 生成回答
    llm_result = pipeline_llm(input=llm_prompt, max_length=5000)
    answer = llm_result["text"]

    # 构造 JSON 输出
    return json.dumps({
        "query": query,
        "most_similar_context": texts[most_similar_idx],
        "similarity": similarity,
        "generated_answer": answer
    }, ensure_ascii=False, indent=2)


# 加载嵌入向量文件，并排除 page_number=14 的条目
input_file = "E:\\CaseAnalyze\\output\\result_with_embeddings.json"
texts, embeddings = load_embeddings(input_file)
index = create_faiss_index(embeddings)

# 创建 Gradio 接口
interface = gr.Interface(
    fn=lambda query: search_similar(query, texts, index),
    inputs=gr.Textbox(label="Enter your query", placeholder="Type your question or query..."),
    outputs=gr.JSON(label="Search Results"),
    live=True
)

# 启动 Gradio 界面
interface.launch()