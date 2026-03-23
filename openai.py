import json
import time
from openai import OpenAI


def get_client(ak=None, use_batch_api=False):
    """
    获取百炼 OpenAI client
    :param ak: API key
    :param use_batch_api: 是否使用批量API
    :return: OpenAI client实例
    """
    if ak is None:
        ak = ''  # 默认ak

    base_url = 'https://batch.dashscope.aliyuncs.com/compatible-mode/v1' if use_batch_api else 'https://dashscope.aliyuncs.com/compatible-mode/v1'

    return OpenAI(
        base_url=base_url,
        api_key=ak
    )


class bailian_chatgpt():
    def __init__(self, ak=None, use_batch_api=False):
        self.client = get_client(ak=ak, use_batch_api=use_batch_api)

    def process(self, input, return_json=False, model="qwen-plus", temp=0.7, extra_body=None):
        """
        同步处理单个请求
        :param input: 输入数据，格式为 {"text": "你的问题", "retry": 5}
        :param return_json: 是否将返回结果解析为 JSON
        :param model: 模型名称
        :param temp: 温度参数
        :param extra_body: 额外参数，如 {"enable_thinking": False}
        :return: 模型返回的内容
        """
        text = input["text"]
        retry = input.get("retry", 5)
        is_success = False
        response = None

        while retry > 0 and not is_success:
            try:
                # 构建请求参数
                kwargs = {
                    'model': model,
                    'messages': [{'role': 'user', 'content': text}],
                    'stream': False,
                    'temperature': temp
                }

                # 添加额外参数
                if extra_body is not None:
                    kwargs['extra_body'] = extra_body

                # 调用 API
                completion = self.client.chat.completions.create(**kwargs)
                response = completion.choices[0].message.content
                is_success = True

            except Exception as e:
                print(f"请求失败: {e}")
                retry -= 1
                time.sleep(1)

        if return_json and response is not None:
            try:
                response = json.loads(response)
            except:
                print("Warning: Failed to parse response as JSON")

        return response


if __name__ == "__main__":
    # 简单测试
    model = 'qwen-plus'
    chatgpt = bailian_chatgpt()

    test_input = {
        "text": "你好，请用一句话介绍一下你自己。"
    }

    print(f"测试模型: {model}")
    print("输入:", test_input["text"])
    print("-" * 60)

    response = chatgpt.process(test_input, model=model)
    print("输出:", response)