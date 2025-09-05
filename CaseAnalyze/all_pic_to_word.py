import os
import cv2
from paddleocr import PPStructure,save_structure_res
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx
from copy import deepcopy
# 中文测试图
table_engine = PPStructure(recovery=True,lang='ch')

#image_path = './imgs/小牛模拟案卷'
image_path='E:\\CaseAnalyze\\imgs\\小牛模拟案卷'
save_folder = './txt'
def img2docx(img_path):
    text=[]
    imgs=os.listdir(img_path)
    for img_name in imgs:
        print(os.path.join(img_path,img_name))
        img = cv2.imread(os.path.join(img_path,img_name))
        result = table_engine(img)

        save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

        h, w, _ = img.shape
        res = sorted_layout_boxes(result, w)
        convert_info_docx(img, res, save_folder, os.path.basename(img_path).split('.')[0])

        for line in res:
            line.pop('img')
            print(line)
            for pra in line['res']:
                text.append(pra['text'])
            text.append('\n')
        with open('txt/res.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(text))
img2docx(image_path)
