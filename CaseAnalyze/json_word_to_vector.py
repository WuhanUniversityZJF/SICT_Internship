# import json
# import os
# from modelscope.pipelines import pipeline
# from modelscope import Tasks
# import logging
# from colorama import Fore, Style
#
# # 设置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# class TextEmbeddingProcessor:
#     def __init__(self, input_json, output_json):
#         self.input_json = input_json
#         self.output_json = output_json
#         self.pipeline_se = self.load_model()
#
#     def load_model(self):
#         # 加载 ModelScope 的 sentence_embedding 模型
#         model_id = "iic/nlp_gte_sentence-embedding_chinese-large"
#         logger.info(f"{Fore.GREEN}加载 sentence_embedding 模型: {model_id}{Style.RESET_ALL}")
#         return pipeline(Tasks.sentence_embedding, model=model_id, sequence_length=512)
#
#     def process_text_embeddings(self):
#         # 读取输入的 JSON 文件
#         if not os.path.exists(self.input_json):
#             logger.error(f"{Fore.RED}文件不存在: {self.input_json}{Style.RESET_ALL}")
#             return
#
#         with open(self.input_json, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#
#         # 遍历每一页的内容，计算向量并更新数据
#         for page in data:
#             text = page.get("content", "")
#             logger.info(f"{Fore.BLUE}处理页号: {page['page_number']}, 文本长度: {len(text)}{Style.RESET_ALL}")
#
#             # 使用 sentence_embedding 模型计算向量
#             try:
#                 # 根据模型要求调整输入格式
#                 input_data = {"source_sentence": text}  # 使用 source_sentence 作为键
#                 embedding = self.pipeline_se(input_data)[0]
#                 page["embedding"] = embedding.tolist()  # 将向量保存为列表格式
#             except Exception as e:
#                 logger.error(f"{Fore.RED}处理页号 {page['page_number']} 时出错: {e}{Style.RESET_ALL}")
#                 page["embedding"] = None  # 如果出错，设置为 None
#
#         # 将更新后的数据保存到新的 JSON 文件
#         with open(self.output_json, 'w', encoding='utf-8') as f:
#             json.dump(data, f, ensure_ascii=False, indent=4)
#
#         logger.info(f"{Fore.GREEN}处理完成，结果已保存到: {self.output_json}{Style.RESET_ALL}")
#
#
# if __name__ == "__main__":
#     # 输入和输出的 JSON 文件路径
#     input_json_file = r"E:\CaseAnalyze\output\result.json"  # 原始 JSON 文件
#     output_json_file = r"E:\CaseAnalyze\output\result_with_embeddings.json"  # 更新后的 JSON 文件
#
#     # 初始化处理器并开始处理
#     processor = TextEmbeddingProcessor(input_json=input_json_file, output_json=output_json_file)
#     processor.process_text_embeddings()


import json
import os
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import logging
from colorama import Fore, Style

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TextEmbeddingProcessor:
    def __init__(self, input_json, output_json):
        self.input_json = input_json
        self.output_json = output_json
        self.pipeline_se = self.load_model()

    def load_model(self):
        # 加载 ModelScope 的 sentence_embedding 模型
        model_id = "iic/nlp_gte_sentence-embedding_chinese-large"
        logger.info(f"{Fore.GREEN}加载 sentence_embedding 模型: {model_id}{Style.RESET_ALL}")
        return pipeline(Tasks.sentence_embedding, model=model_id, sequence_length=512)

    def process_text_embeddings(self):
        # 读取输入的 JSON 文件
        if not os.path.exists(self.input_json):
            logger.error(f"{Fore.RED}文件不存在: {self.input_json}{Style.RESET_ALL}")
            return

        with open(self.input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 遍历每一页的内容，计算向量并更新数据
        for page in data:
            text = page.get("content", "")
            logger.info(f"{Fore.BLUE}处理页号: {page['page_number']}, 文本长度: {len(text)}{Style.RESET_ALL}")

            # 使用 sentence_embedding 模型计算向量
            try:
                # 确保输入格式为列表
                input_data = {"source_sentence": [text]}  # 使用列表格式
                result = self.pipeline_se(input=input_data)
                embedding = result["text_embedding"][0]  # 提取嵌入向量
                page["embedding"] = embedding.tolist()  # 将向量保存为列表格式
            except Exception as e:
                logger.error(f"{Fore.RED}处理页号 {page['page_number']} 时出错: {e}{Style.RESET_ALL}")
                page["embedding"] = None  # 如果出错，设置为 None

        # 将更新后的数据保存到新的 JSON 文件
        with open(self.output_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logger.info(f"{Fore.GREEN}处理完成，结果已保存到: {self.output_json}{Style.RESET_ALL}")


if __name__ == "__main__":
    # 输入和输出的 JSON 文件路径
    input_json_file = r"E:\CaseAnalyze\output\result.json"  # 原始 JSON 文件
    output_json_file = r"E:\CaseAnalyze\output\result_with_embeddings.json"  # 更新后的 JSON 文件

    # 初始化处理器并开始处理
    processor = TextEmbeddingProcessor(input_json=input_json_file, output_json=output_json_file)
    processor.process_text_embeddings()