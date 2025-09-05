# from transformers import T5Tokenizer, T5ForConditionalGeneration
#
# # 加载T5模型和分词器
# tokenizer = T5Tokenizer.from_pretrained('t5-small')
# model = T5ForConditionalGeneration.from_pretrained('t5-small')
#
# # 读取文本文件
# with open('output.txt', 'r', encoding='utf-8') as f:
#     texts = f.readlines()
#
# # 定义生成摘要的函数
# def generate_summary_t5(text):
#     inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
#     summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary
#
# # 对文件中的每段文本生成摘要
# summaries = []
# for text in texts:
#     summary = generate_summary_t5(text)
#     summaries.append(summary)
#
# # 输出摘要
# for i, summary in enumerate(summaries):
#     print(f"Summary {i+1}: {summary}")
#

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# 读取文本文件
with open('output.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# 创建PlaintextParser对象
parser = PlaintextParser.from_string(text, Tokenizer("english"))

# 选择摘要算法，这里使用LSA算法
summarizer = Summarizer(Stemmer("english"))
summarizer.stop_words = get_stop_words("english")

# 生成摘要，指定摘要的句子数量
summary_sentences = summarizer(parser.document, 5)  # 生成5个句子的摘要

# 输出摘要
summary_text = ' '.join([str(sentence) for sentence in summary_sentences])
print(summary_text)