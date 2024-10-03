from typing import Dict
from openai import OpenAI
from pydantic import BaseModel
import json
from llm_extractor import BaseExtractor
import os




PROMPT = """
## Given the website html:
{context}

## Find me the css query selector of the element that contain the following information:
{list_fields}
"""




class OpenAIExtractor(BaseExtractor):
    def __init__(
        self,
        json_format: BaseModel = None,
        list_extract_fields: str = None,
        api_key: str = None,
        model_name: str = "gpt-4o-mini",
        prompt: str = PROMPT
    ):
        super().__init__(json_format)
        self.prompt = prompt
        self.api_key = api_key or os.environ["OPENAI_API_KEY"]
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.list_extract_fields = list_extract_fields
        
    def parse_prompt(self, context: str = None) -> str:
        res =  self.prompt.replace("{context}", context)
        return res.replace("{list_fields}", self.list_extract_fields)
    
    def _extract(self, website_body: str = ""):
        completion = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=[{
                "role": "user",
                "content": self.parse_prompt(website_body)
            }],
            response_format=self.json_format
        )
        json_response = json.loads(completion.choices[0].message.content)
        
        return json_response