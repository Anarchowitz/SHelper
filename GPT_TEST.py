
from openai import OpenAI

client = OpenAI(
    api_key="sk-ai31tunnel-jJbl5JiPBgCygbIwCRpUFnK3PP0VHe8M", # Ключ из нашего сервиса
    base_url="https://api.aitunnel.ru/v1/",
)

completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "Скажи интересный факт"}],
    max_tokens=1025,
    model="gpt-4o-mini"
)
#ChatCompletionMessage(content='Знаете ли вы, что бананы на самом деле являются ягодами, а например, клубника — нет? В ботанике ягода определяется как плод, образующийся из одного цветка с одним яйцеклеткой, и бананы подходят под это определение. Клубника же является сборным плодом, который формируется из нескольких пестиков.', refusal='', role='assistant', audio=None, function_call=None, tool_calls=None)


print(completion.choices[0].message)