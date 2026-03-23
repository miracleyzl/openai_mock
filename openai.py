import json
import requests
import traceback
import time
AK = "" # 填入AK
class IDEALABChat:
    def __init__(self, ak=None):
        self.chat_url = "https://idealab.alibaba-inc.com/api/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f'Bearer {ak}',
            "X-AK": f'{ak}'
        }

    def chat_completion_with_retry(self, **kwargs):
        """同步调用，内置重试逻辑"""
        use_messages = []
        messages = kwargs.get("messages", [])
        model = kwargs.get("model", "qwen-plus")
        stream = kwargs.get("stream", False)
        temperature = kwargs.get("temperature", 0.6)
        frequencyPenalty = kwargs.get("frequency_penalty", None)
        stop = kwargs.get("stop", None)
        functions = kwargs.get("functions", None)
        function_call = kwargs.get("function_call", None)
        max_tokens = kwargs.pop("max_tokens", 4096)

        for message in messages:
            if not("valid" in message.keys() and message["valid"] == False):
                use_messages.append(message)

        json_data = {
            "model": model,
            "temperature": temperature,
            "frequency_penalty": frequencyPenalty,
            "messages": use_messages,
            "max_tokens": max_tokens,
            **kwargs
        }
        if stop is not None:
            json_data.update({"stop": stop})
        if functions is not None:
            json_data.update({"functions": functions})
        if function_call is not None:
            json_data.update({"function_call": function_call})

        # 内置重试逻辑，最多重试5次
        retry_times = 5
        last_exception = None

        for attempt in range(retry_times):
            try:
                response = requests.post(
                    self.chat_url,
                    headers=self.headers,
                    json=json_data,
                    timeout=300
                )
                result = response.json()
                time.sleep(0.5)
                return result
            except Exception as e:
                last_exception = e
                print(f"Attempt {attempt + 1}/{retry_times} failed: {e}")
                if attempt < retry_times - 1:
                    wait_time = min(5 * (2 ** attempt), 40)  # 指数退避，最长40秒
                    time.sleep(wait_time)

        # 所有重试都失败
        print("Unable to generate ChatCompletion response")
        print(f"OpenAI calling Exception: {last_exception}\n{traceback.format_exc()}")
        raise last_exception


class idealab_chatgpt():
    def __init__(self, ak=None):
        self.instance = IDEALABChat(ak=ak)

    def process(self, input, return_json=False, model="gpt-4o-mini-0718", temp=0.7):
        """同步处理单个请求"""
        messages = [{"role": "user", "content": [{"type": "text", "text": input["text"]}]}]
        retry = input.get("retry", 5)
        is_success = False
        response = None

        while retry > 0 and not is_success:
            kwargs = {
                'messages': messages,
                'model': model,
                'stream': False,
                'temperature': temp,
                'seed': 0
            }
            # 关闭gemini的思考部分
            if "gemini" in model:
                kwargs['extendParams'] = {
                    "thinkingConfig": {
                        "thinkingBudget": 128
                    }
                }
            try:
                res = self.instance.chat_completion_with_retry(**kwargs)
                response = res['choices'][0]['message']['content']
                is_success = True
            except:
                traceback.print_exc()
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
    chatgpt = idealab_chatgpt()

    test_input = {
        "text": "你好，请用一句话介绍一下你自己。"
    }

    print(f"测试模型: {model}")
    print("输入:", test_input["text"])
    print("-" * 60)

    response = chatgpt.process(test_input, model=model)
    print("输出:", response)
