from openai import OpenAI
class LLM:
    def __init__(self, model_name,base_url,api_key):
        self.model_name=model_name
        self.base_url=base_url
        self.api_key=api_key
        self.client=OpenAI(base_url=self.base_url,api_key=self.api_key)
    def call_llm(self,inputs:list[dict],tools:list[dict]|None=None):
        response= self.client.chat.completions.create(
            model=self.model_name,
            messages=inputs,
            tools=tools or []
        )
        return response.choices[0].message
