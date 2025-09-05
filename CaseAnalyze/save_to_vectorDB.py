# import numpy as np
# import faiss
# from sklearn.feature_extraction.text import CountVectorizer
#
# # 读取文本文件
# with open('output.txt', 'r', encoding='utf-8') as f:
#     texts = f.readlines()
#
# # 使用CountVectorizer将文本转换为向量
# vectorizer = CountVectorizer()
# vectors = vectorizer.fit_transform(texts).toarray().astype('float32')
#
# # 创建FAISS索引
# dimension = vectors.shape[1]  # 向量的维度
# index = faiss.IndexFlatL2(dimension)  # 使用L2距离度量
# index.add(vectors)  # 将向量添加到索引中
#
# # 示例：进行查询
# query_text = "生产日志"
# #query_text = "1212"
# query_vector = vectorizer.transform([query_text]).toarray().astype('float32')
# k = 5  # 检索最相似的5个文本
# distances, indices = index.search(query_vector, k)
#
# # 输出查询结果
# print("Query:", query_text)
# print("Most similar texts:")
# for i, idx in enumerate(indices[0]):
#     print(f"{i+1}. {texts[idx].strip()} (Distance: {distances[0][i]:.4f})")


import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


# 步骤1：读取文件中的文本内容
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


# 步骤2：使用 TF-IDF 进行文本向量化
def text_to_vectors(texts):
    # 使用 TF-IDF 向量化文本
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(texts)
    # 将稀疏矩阵转换为密集的 NumPy 数组
    dense_vectors = vectors.toarray()
    # 归一化向量（可选）
    return normalize(dense_vectors, axis=1)


def store_vectors_in_faiss(vectors):
    # 获取向量的维度
    dim = vectors.shape[1]
    # 创建一个 FAISS 索引
    index = faiss.IndexFlatL2(dim)  # 使用 L2 距离度量
    # 对向量进行归一化之前，确保它们是 float32 类型
    vectors = vectors.astype(np.float32)
    faiss.normalize_L2(vectors)  # 对向量进行归一化
    # 将向量添加到索引中
    index.add(vectors)
    return index


# 步骤4：主函数
def main():
    # 读取文件内容
    file_path = 'output.txt'
    texts = read_text_file(file_path)

    # 将文本转换为向量
    vectors = text_to_vectors(texts)

    # 存储向量到 FAISS 向量数据库
    index = store_vectors_in_faiss(vectors)

    print(f"成功将 {len(texts)} 条文本数据存储到 FAISS 向量数据库！")

    # 可选：查询示例，搜索相似文本
    query = vectors[0:1]  # 使用第一条文本作为查询

    D, I = index.search(query.astype(np.float32), k=5)  # 查询最相似的 5 条记录
    print("查询结果：")
    for i, idx in enumerate(I[0]):
        print(f"第 {i + 1} 条相似文本的索引: {idx}, 距离: {D[0][i]}")


if __name__ == '__main__':
    main()
