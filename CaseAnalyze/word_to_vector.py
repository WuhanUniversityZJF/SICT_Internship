from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import json

# 初始化模型
model_id = "iic/nlp_gte_sentence-embedding_chinese-large"
pipeline_se = pipeline(Tasks.sentence_embedding, model=model_id, sequence_length=512)

# 读取文件
input_file = "output.txt"

# 定义不同的段落长度和输出文件名
segment_lengths = [100, 200, 500, 1000]
output_files = ["embedding_01.json", "embedding_02.json", "embedding_03.json", "embedding_04.json"]

# 逐行读取文本并合并为一个长文本
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# 为每个段落长度生成嵌入向量并保存到对应的文件
for i, segment_length in enumerate(segment_lengths):
    # 按每segment_length个字符划分段落
    segments = [text[j:j + segment_length] for j in range(0, len(text), segment_length)]

    # 生成嵌入向量
    embeddings = []
    for segment in segments:
        segment = segment.strip()  # 去掉空白符
        if segment:  # 如果段落不为空
            result = pipeline_se(input={"source_sentence": [segment]})
            embedding = result["text_embedding"]  # 提取嵌入向量
            embeddings.append({
                "text": segment,
                "embedding": embedding[0].tolist()  # 转换为 Python 列表
            })

    # 保存结果到对应的 JSON 文件
    output_file = output_files[i]
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=4)

    print(f"嵌入生成完成，已保存至 {output_file}")
