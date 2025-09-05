import os
import torch
from modelscope import AutoModelForCausalLM, AutoTokenizer, snapshot_download

# 设置显存分配策略
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# 清理显存
torch.cuda.empty_cache()

# 指定模型下载路径
model_dir = snapshot_download('AI-ModelScope/Mistral-7B-Instruct-v0.1', revision='v1.0.0', cache_dir='G:/models')

# 加载模型和分词器
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)
model = model.to(device)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

# 示例对话
messages = [
    {"role": "user", "content": "What is your favourite condiment?"},
    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    {"role": "user", "content": "Do you have mayonnaise recipes?"}
]

encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
model_inputs = encodeds.to(device)

# 生成回答
generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
decoded = tokenizer.batch_decode(generated_ids)
print(decoded[0])