# import json
# import faiss
# import numpy as np
# import gradio as gr
#
# # 读取 embeddings.json 文件
# input_file = "embeddings.json"
#
# with open(input_file, "r", encoding="utf-8") as f:
#     embeddings_data = json.load(f)
#
# # 提取嵌入向量和文本
# texts = [item['text'] for item in embeddings_data]
# embeddings = np.array([item['embedding'] for item in embeddings_data], dtype=np.float32)
#
# # 创建 Faiss 索引
# dimension = embeddings.shape[1]  # 嵌入向量的维度
# index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离度量创建一个扁平索引
# index.add(embeddings)  # 将嵌入向量添加到 Faiss 索引
#
#
# # 定义搜索函数
# def search_similar(query):
#     # 使用 Gradio 输入的查询文本来生成查询的嵌入向量（假设已经通过某种模型生成了嵌入）
#     # 这里假设 query_embedding 是已经转换成嵌入的查询向量，实际上你需要使用一个 NLP 模型来生成这个向量。
#     query_embedding = np.random.rand(1, dimension).astype(np.float32)  # 随机生成一个查询嵌入向量（请替换成实际的生成方式）
#
#     k = 3  # 返回最相似的 3 个结果
#     distances, indices = index.search(query_embedding, k)
#
#     # 获取最相似的文本
#     similar_texts = [texts[i] for i in indices[0]]
#     return "\n".join(similar_texts)
#
#
# # 创建 Gradio 接口
# interface = gr.Interface(
#     fn=search_similar,
#     inputs=gr.Textbox(label="Enter query text"),
#     outputs=gr.Textbox(label="Most Similar Texts"),
#     live=True
# )
#
# # 启动 Gradio 界面
# interface.launch()

###############################################################################
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
        return ""

    # 生成查询文本的嵌入向量
    result = pipeline_se(input={"source_sentence": [query]})
    query_embedding = np.array(result["text_embedding"], dtype=np.float32).reshape(1, -1)

    # 返回最相似的 3 个结果
    k = 6
    distances, indices = index.search(query_embedding, k)

    # 获取最相似的文本
    similar_texts = [texts[i] for i in indices[0]]
    return "\n".join(similar_texts)


# 创建 Gradio 接口
interface = gr.Interface(
    fn=search_similar,
    inputs=gr.Textbox(label="Enter query text", placeholder="Enter a sentence to search..."),
    outputs=gr.Textbox(label="Most Similar Texts", placeholder="Results will be displayed here..."),
    live=True
)

# 启动 Gradio 界面
interface.launch()
