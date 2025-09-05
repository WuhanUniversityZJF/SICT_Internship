# import os
# from PyQt5.QtCore import QObject
# from paddleocr import PaddleOCR
# import logging
# from colorama import Fore, Style
#
# # 设置 PaddleOCR 日志级别为 ERROR
# logging.getLogger("ppocr").setLevel(logging.ERROR)
#
#
# class OcrQt(QObject):
#     def __init__(self, parent=None):
#         super(OcrQt, self).__init__(parent)
#         self.use_angle = True
#         self.cls = True
#         self.default_lan = "ch"
#         self.result = []
#         self.ls = []
#         self.dic = {}
#
#     def set_task(self, img_path='', use_angle=True, cls=True, lan="ch"):
#         self.img_path = img_path
#         self.use_angle = use_angle
#         self.cls = cls
#         self.default_lan = lan
#
#     def start(self, output_file="output.txt"):
#         # 遍历 img 目录下所有图片并提取文本
#         img_dir = "./imgs/小牛模拟案卷"
#         img_files = sorted([f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
#
#         with open(output_file, "w", encoding="utf-8") as f:
#             for img_file in img_files:
#                 img_path = os.path.join(img_dir, img_file)
#                 print(f"正在处理图片：{img_path}")
#                 self.ocr(img_path, self.use_angle, self.cls, self.default_lan)
#                 self.grouping(f)  # 将提取的文本写入文件
#
#     def ocr(self, img_path, use_angle=True, cls=True, lan="ch", use_gpu=0):
#         ocr = PaddleOCR(use_angle_cls=use_angle, use_gpu=use_gpu, lang=lan)
#         try:
#             result = ocr.ocr(img_path, cls=cls)
#             self.result = result
#         except PermissionError:
#             print(Fore.RED + '权限错误:' + Style.RESET_ALL)
#             exit()
#         except FileNotFoundError:
#             print(Fore.RED + '图片路径错误:' + Style.RESET_ALL, img_path)
#             exit()
#         for line in self.result:
#             ls = [j[0] for i in line for j in i]
#             dic = {}
#             self.ls = ls
#             self.dic = dic
#             for index, info in enumerate(ls):
#                 if index % 2 == 0:
#                     dic[tuple(info)] = ls[index + 1]
#
#     def grouping(self, file_object):
#         max_line_length = 30  # 每行的最大字数限制
#         current_line = ""  # 当前行
#
#         for index, info in enumerate(self.ls):
#             if index % 2 == 1:
#                 while len(info) > max_line_length:
#                     # 如果当前行文本超过最大长度，将其分割
#                     file_object.write(info[:max_line_length] + "\n")
#                     info = info[max_line_length:]  # 剩余部分继续处理
#
#                 # 如果当前行未达到最大长度，继续加入当前行
#                 if len(current_line) + len(info) <= max_line_length:
#                     current_line += info
#                 else:
#                     # 当前行超过最大长度，保存当前行并开始新的一行
#                     file_object.write(current_line + "\n")
#                     current_line = info  # 新的一行从当前文本开始
#
#         # 写入最后一行（如果有内容）
#         if current_line:
#             file_object.write(current_line + "\n")
#
#
# if __name__ == "__main__":
#     # 定义输出文件
#     output_file = "output.txt"
#
#     ocrObj = OcrQt()
#     print('=' * 30, '开始提取所有图片文本', '=' * 30)
#     ocrObj.start(output_file)
#     print(f"所有图片文本已保存到文件 {output_file}")
#

import os
from PyQt5.QtCore import QObject
from paddleocr import PaddleOCR
import logging
from colorama import Fore, Style
import re

# 设置 PaddleOCR 日志级别为 ERROR
logging.getLogger("ppocr").setLevel(logging.ERROR)


class OcrQt(QObject):
    def __init__(self, parent=None):
        super(OcrQt, self).__init__(parent)
        self.use_angle = True
        self.cls = True
        self.default_lan = "ch"
        self.result = []
        self.ls = []
        self.dic = {}

    def set_task(self, img_path='', use_angle=True, cls=True, lan="ch"):
        self.img_path = img_path
        self.use_angle = use_angle
        self.cls = cls
        self.default_lan = lan

    def start(self, output_file="output.txt"):
        # 遍历 img 目录下所有图片并提取文本
        img_dir = "./imgs/小牛模拟案卷"
        img_files = sorted(
            [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))],
            key=lambda x: [int(y) if y.isdigit() else y for y in re.split(r'(\d+)', x)]
        )

        with open(output_file, "w", encoding="utf-8") as f:
            for img_file in img_files:
                img_path = os.path.join(img_dir, img_file)
                print(f"正在处理图片：{img_path}")
                self.ocr(img_path, self.use_angle, self.cls, self.default_lan)
                self.grouping(f)  # 将提取的文本写入文件

    def ocr(self, img_path, use_angle=True, cls=True, lan="ch", use_gpu=0):
        ocr = PaddleOCR(use_angle_cls=use_angle, use_gpu=use_gpu, lang=lan)
        try:
            result = ocr.ocr(img_path, cls=cls)
            self.result = result
        except PermissionError:
            print(Fore.RED + '权限错误:' + Style.RESET_ALL)
            exit()
        except FileNotFoundError:
            print(Fore.RED + '图片路径错误:' + Style.RESET_ALL, img_path)
            exit()
        for line in self.result:
            ls = [j[0] for i in line for j in i]
            dic = {}
            self.ls = ls
            self.dic = dic
            for index, info in enumerate(ls):
                if index % 2 == 0:
                    dic[tuple(info)] = ls[index + 1]

    def grouping(self, file_object):
        max_line_length = 30  # 每行的最大字数限制
        current_line = ""  # 当前行

        for index, info in enumerate(self.ls):
            if index % 2 == 1:
                while len(info) > max_line_length:
                    # 如果当前行文本超过最大长度，将其分割
                    file_object.write(info[:max_line_length] + "\n")
                    info = info[max_line_length:]  # 剩余部分继续处理

                # 如果当前行未达到最大长度，继续加入当前行
                if len(current_line) + len(info) <= max_line_length:
                    current_line += info
                else:
                    # 当前行超过最大长度，保存当前行并开始新的一行
                    file_object.write(current_line + "\n")
                    current_line = info  # 新的一行从当前文本开始

        # 写入最后一行（如果有内容）
        if current_line:
            file_object.write(current_line + "\n")


if __name__ == "__main__":
    # 定义输出文件
    output_file = "output.txt"

    ocrObj = OcrQt()
    print('=' * 30, '开始提取所有图片文本', '=' * 30)
    ocrObj.start(output_file)
    print(f"所有图片文本已保存到文件 {output_file}")