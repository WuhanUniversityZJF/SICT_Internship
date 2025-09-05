import json
import faiss
import numpy as np
import gradio as gr
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# 初始化模型用于生成查询嵌入
model_id_embedding = "iic/nlp_gte_sentence-embedding_chinese-large"
pipeline_se = pipeline(Tasks.sentence_embedding, model=model_id_embedding, sequence_length=512)

# 创建 Faiss 索引
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]  # 嵌入向量的维度
    index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离度量创建一个扁平索引
    index.add(embeddings)  # 将嵌入向量添加到 Faiss 索引
    return index

# 计算两个文本之间的相似度
def calculate_similarity(text1, text2):
    if not text1.strip() or not text2.strip():  # 如果任意一个文本为空，返回错误消息
        return json.dumps({"error": "Both texts must be non-empty."}, ensure_ascii=False)

    # 生成两个文本的嵌入向量
    result1 = pipeline_se(input={"source_sentence": [text1]})
    result2 = pipeline_se(input={"source_sentence": [text2]})

    embedding1 = np.array(result1["text_embedding"], dtype=np.float32).reshape(1, -1)
    embedding2 = np.array(result2["text_embedding"], dtype=np.float32).reshape(1, -1)

    # 计算 L2 距离
    distance = np.linalg.norm(embedding1 - embedding2)  # L2 范数计算两个向量之间的距离
    similarity = 1 / (1 + distance)  # 将 L2 距离转换为相似度

    # 返回相似度结果
    return json.dumps({
        "text1": text1,
        "text2": text2,
        "similarity": similarity
    }, ensure_ascii=False, indent=2)

# 创建 Gradio 接口
def create_gradio_interface():
    interface = gr.Interface(
        fn=calculate_similarity,
        inputs=[gr.Textbox(label="Enter text 1", placeholder="Type the first text..."),
                gr.Textbox(label="Enter text 2", placeholder="Type the second text...")],
        outputs=gr.JSON(label="Similarity Result"),
        live=True
    )
    interface.launch()

# 启动 Gradio 界面
create_gradio_interface()
