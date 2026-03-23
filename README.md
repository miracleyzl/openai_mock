# OpenAI Mock - 简化版 IDEALAB LLM 调用工具

这是一个精简的 IDEALAB 大模型调用工具，提供同步非流式的 LLM API 调用功能。

## 功能特性

- 同步调用 IDEALAB 大模型 API
- 内置重试机制（指数退避策略）
- 支持多种模型（GPT、Qwen、Gemini 等）
- 极简依赖，只需要 `requests` 库
- 支持自定义 AK（Access Key）

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

### 基本用法

```python
from openai import idealab_chatgpt

# 初始化（使用默认 AK）
chatgpt = idealab_chatgpt()

# 调用模型
test_input = {
    "text": "你好，请用一句话介绍一下你自己。"
}

response = chatgpt.process(test_input, model='qwen-plus')
print(response)
```

### 使用自定义 AK

```python
from openai import idealab_chatgpt

# 使用自定义 AK
chatgpt = idealab_chatgpt(ak="your_custom_ak_here")

response = chatgpt.process(
    input={"text": "你的问题"},
    model='gpt-4o-mini-0718',
    temp=0.7
)
```

### 返回 JSON 格式

```python
test_input = {
    "text": "请以JSON格式返回：{\"name\": \"张三\", \"age\": 30}"
}

response = chatgpt.process(test_input, return_json=True)
print(response)  # 自动解析为 Python dict
```

## API 说明

### `idealab_chatgpt` 类

#### 初始化参数

- `ak` (str, optional): IDEALAB API 的 Access Key，默认使用内置 AK

#### `process` 方法

同步处理单个 LLM 请求。

**参数：**
- `input` (dict): 输入数据，格式为 `{"text": "你的问题", "retry": 5}`
  - `text` (str): 必需，要发送给模型的文本内容
  - `retry` (int): 可选，重试次数，默认 5
- `return_json` (bool): 是否将返回结果解析为 JSON，默认 False
- `model` (str): 模型名称，默认 `"gpt-4o-mini-0718"`
- `temp` (float): 温度参数，控制输出随机性，默认 0.7

**返回：**
- `str` 或 `dict`: 模型的返回结果，如果 `return_json=True` 则返回解析后的字典

## 支持的模型

常用模型示例：
- `qwen-flash`
- `qwen-plus`

## 运行测试

```bash
python3 openai.py
```

## 项目结构

```
openai_mock/
├── openai.py           # 主程序文件
├── requirements.txt    # 依赖列表
└── README.md          # 项目说明
```

## 注意事项

1. 默认使用阿里巴巴内部的 IDEALAB API 服务
2. 需要有效的 AK 才能正常调用
3. 内置指数退避重试机制，最多重试 5 次
4. 每次请求后会自动休眠 0.5 秒，避免频率过高

## License

内部使用工具，请勿外传。
