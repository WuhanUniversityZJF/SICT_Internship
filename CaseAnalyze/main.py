# import gradio as gr
# import json
# import random
# import requests
# from openai import OpenAI
#
#
# def get_response(text):
#     #openai_api_key = "sk-ipOShdrs3sZgMQ731XT8uI4bvFOHh6sE1SCkN5iJ186tV9B3"
#     #openai_api_key="sk-1xKIdLe7p48ERfIQpylwuumLEoqt2CJt73sEnJ8eXAQ5mRYo"
#     openai_api_key="sk-e3lf8Jrm6B0NSmwLGHDy84dECWWAFnsZFQoDHbcyhnpf0At7"
#     #openai_api_base = "https://hk.soruxgpt.com/api/api/v1"
#     openai_api_base="https://api.moonshot.cn/v1"
#
#     client = OpenAI(
#         api_key=openai_api_key,
#         base_url=openai_api_base,
#     )
#     ## 流式回答
#     response = client.chat.completions.create(
#         #model="gpt-4o-mini",
#         model="moonshot-v1-8k",
#         messages=[
#             {"role": "system", "content": "你是****手，是一名建筑工程、基建安全、安全生产、工程弱电领域的专家。"},
#             {"role": "user", "content": text}
#         ],
#
#         stream=True,
#     )
#
#     return response
#
#
# conversation_history = []
#
#
# def chat_response(message, history):
#     print(message, history)
#     results = get_response(message)
#     contents = ""
#     for chunk in results:
#         if chunk.choices[0].delta.content is not None:
#             # print(chunk.choices[0].delta.content)
#             contents += chunk.choices[0].delta.content
#             # print(chunk.choices[0].delta.content, end="")
#             yield contents
#
#
# gr.ChatInterface(chat_response, title="GPT提问").launch()
#

# import gradio as gr
# import json
# import random
# import requests
# from openai import OpenAI
# from PyPDF2 import PdfReader
#
#
# def get_response(text):
#     openai_api_key = "sk-e3lf8Jrm6B0NSmwLGHDy84dECWWAFnsZFQoDHbcyhnpf0At7"
#     openai_api_base = "https://api.moonshot.cn/v1"
#
#     client = OpenAI(
#         api_key=openai_api_key,
#         base_url=openai_api_base,
#     )
#     # Streaming response
#     response = client.chat.completions.create(
#         model="moonshot-v1-8k",
#         messages=[
#             {"role": "system", "content": "你是****手，是一名建筑工程、基建安全、安全生产、工程弱电领域的专家。"},
#             {"role": "user", "content": text}
#         ],
#         stream=True,
#     )
#
#     return response
#
#
# conversation_history = []
#
#
# def read_pdf(file):
#     # Extract text from a PDF file
#     pdf_reader = PdfReader(file.name)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text
#
#
# def chat_response_with_pdf(file, message, history):
#     # Read text from PDF
#     pdf_text = read_pdf(file)
#     # Combine PDF text with the user's message
#     combined_message = f"PDF内容：\n{pdf_text}\n\n用户提问：\n{message}"
#     # Get response
#     results = get_response(combined_message)
#     contents = ""
#     for chunk in results:
#         if chunk.choices[0].delta.content is not None:
#             contents += chunk.choices[0].delta.content
#             yield contents
#
#
# interface = gr.Interface(
#     fn=chat_response_with_pdf,
#     inputs=[
#         gr.File(label="Upload PDF File", file_types=[".pdf"]),
#         gr.Textbox(label="Enter your message"),
#         gr.State()
#     ],
#     outputs="text",
#     title="GPT提问 with PDF Support",
# )
#
# interface.launch()


import gradio as gr
import json
import random
import requests
from openai import OpenAI
from PyPDF2 import PdfReader


def get_response(text):
    openai_api_key = "sk-e3lf8Jrm6B0NSmwLGHDy84dECWWAFnsZFQoDHbcyhnpf0At7"
    openai_api_base = "https://api.moonshot.cn/v1"

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )
    # Streaming response
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "你是****手，是一名建筑工程、基建安全、安全生产、工程弱电领域的专家。"},
            {"role": "user", "content": text}
        ],
        stream=True,
    )

    return response


conversation_history = []


def read_pdf(file):
    # Extract text from a PDF file
    pdf_reader = PdfReader(file.name)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def chat_response_with_pdf(file, message):
    # Read text from PDF
    pdf_text = read_pdf(file)
    # Combine PDF text with the user's message
    combined_message = f"PDF内容：\n{pdf_text}\n\n用户提问：\n{message}"
    # Get response
    results = get_response(combined_message)
    contents = ""
    for chunk in results:
        if chunk.choices[0].delta.content is not None:
            contents += chunk.choices[0].delta.content
            yield contents


interface = gr.Interface(
    fn=chat_response_with_pdf,
    inputs=[
        gr.File(label="Upload PDF File", file_types=[".pdf"]),
        gr.Textbox(label="Enter your message")
    ],
    outputs="text",
    title="GPT提问 with PDF Support",
)

interface.launch()
