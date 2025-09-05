# import os
# import json
# from paddleocr import PaddleOCR
# from PyQt5.QtCore import QObject
# import logging
# from colorama import Fore, Style
# import re
#
# # 设置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
# class ImageTextExtractor(QObject):
#     def __init__(self, image_dir, output_file):
#         super().__init__()
#         self.image_dir = image_dir
#         self.output_file = output_file
#         self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 使用PaddleOCR进行文字识别
#
#     def extract_text_from_images(self):
#         # 检查目录是否存在
#         if not os.path.exists(self.image_dir):
#             logger.error(f"{Fore.RED}目录不存在: {self.image_dir}{Style.RESET_ALL}")
#             return
#
#         # 获取目录下的所有图片文件
#         image_files = [f for f in os.listdir(self.image_dir) if f.endswith('.png') and re.match(r'^images_\d+\.png$', f)]
#         image_files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))  # 按页号排序
#
#         results = []
#
#         # 遍历图片文件
#         for image_file in image_files:
#             image_path = os.path.join(self.image_dir, image_file)
#             logger.info(f"{Fore.GREEN}正在处理图片: {image_path}{Style.RESET_ALL}")
#
#             # 使用PaddleOCR提取文字
#             result = self.ocr.ocr(image_path, cls=True)
#             if result:
#                 text = '\n'.join([''.join([line[1][0] for line in block]) for block in result])
#             else:
#                 text = ""
#
#             # 提取页号
#             page_number = int(re.findall(r'\d+', image_file)[0])
#
#             # 将结果保存到列表中
#             results.append({
#                 "page_number": page_number,
#                 "content": text
#             })
#
#         # 将结果保存到JSON文件
#         with open(self.output_file, 'w', encoding='utf-8') as f:
#             json.dump(results, f, ensure_ascii=False, indent=4)
#
#         logger.info(f"{Fore.BLUE}文字提取完成，结果已保存到: {self.output_file}{Style.RESET_ALL}")
#
#
# if __name__ == "__main__":
#     image_directory = r"E:\CaseAnalyze\imgs\小牛模拟案卷"
#     output_json_file = r"E:\CaseAnalyze\output\result.json"
#
#     extractor = ImageTextExtractor(image_directory, output_json_file)
#     extractor.extract_text_from_images()

import os
import json
from paddleocr import PaddleOCR
import logging
from colorama import Fore, Style
import re

# 设置 PaddleOCR 日志级别为 ERROR
logging.getLogger("ppocr").setLevel(logging.ERROR)

class ImageTextExtractor:
    def __init__(self, image_dir, output_file, use_angle=True, cls=True, lang="ch", use_gpu=False):
        self.image_dir = image_dir
        self.output_file = output_file
        self.use_angle = use_angle
        self.cls = cls
        self.lang = lang
        self.use_gpu = use_gpu
        self.ocr = PaddleOCR(use_angle_cls=self.use_angle, use_gpu=self.use_gpu, lang=self.lang)

    def extract_text_from_images(self):
        # 检查目录是否存在
        if not os.path.exists(self.image_dir):
            print(f"{Fore.RED}目录不存在: {self.image_dir}{Style.RESET_ALL}")
            return

        # 获取目录下的所有图片文件并排序
        img_files = sorted(
            [f for f in os.listdir(self.image_dir) if f.endswith(('.png')) and re.match(r'^images_\d+\.png$', f)],
            key=lambda x: int(re.findall(r'\d+', x)[0])
        )

        results = []

        # 遍历图片文件
        for img_file in img_files:
            img_path = os.path.join(self.image_dir, img_file)
            print(f"{Fore.GREEN}正在处理图片: {img_path}{Style.RESET_ALL}")

            # 使用 PaddleOCR 提取文字
            result = self.ocr.ocr(img_path, cls=self.cls)

            # 提取页号
            page_number = int(re.findall(r'\d+', img_file)[0])

            # 将识别结果拼接成字符串
            if result:
                text = '\n'.join([''.join([line[1][0] for line in block]) for block in result])
            else:
                text = ""

            # 将结果保存到列表中
            results.append({
                "page_number": page_number,
                "content": text
            })

        # 将结果保存到 JSON 文件
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print(f"{Fore.BLUE}文字提取完成，结果已保存到: {self.output_file}{Style.RESET_ALL}")


if __name__ == "__main__":
    # 定义图片目录和输出文件
    image_directory = r"E:\CaseAnalyze\imgs\小牛模拟案卷"
    output_json_file = r"E:\CaseAnalyze\output\result.json"

    # 初始化提取器
    extractor = ImageTextExtractor(image_dir=image_directory, output_file=output_json_file)

    # 开始提取文字
    extractor.extract_text_from_images()