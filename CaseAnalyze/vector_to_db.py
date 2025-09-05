import json
import faiss
import numpy as np

# 读取 embeddings.json 文件
input_file = "embeddings.json"

with open(input_file, "r", encoding="utf-8") as f:
    embeddings_data = json.load(f)

# 提取嵌入向量和文本
texts = [item['text'] for item in embeddings_data]
embeddings = np.array([item['embedding'] for item in embeddings_data], dtype=np.float32)

# 输出嵌入向量，查看它们是否有差异
for idx, embedding in enumerate(embeddings):
    print(f"Embedding for {texts[idx]}: {embedding[:10]}...")  # 输出前10个元素

# 创建 Faiss 索引
dimension = embeddings.shape[1]  # 嵌入向量的维度
index = faiss.IndexFlatL2(dimension)  # 使用 L2 距离度量创建一个扁平索引

# 将嵌入向量添加到 Faiss 索引
index.add(embeddings)

# 查询和检索
#query_embedding = embeddings[10:11]  # 使用第一个嵌入向量作为查询
query_embedding = embeddings[17:18]  # 使用第一个嵌入向量作为查询
k = 3  # 返回最相似的 3 个结果

# 搜索相似项
distances, indices = index.search(query_embedding, k)

# 输出搜索结果和距离
print(f"查询的文本: {texts[17]}")
for i in range(k):
    print(f"第{i+1}个最相似的文本: {texts[indices[0][i]]} (距离: {distances[0][i]:.4f})")

