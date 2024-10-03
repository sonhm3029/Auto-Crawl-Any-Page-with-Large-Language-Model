from abc import ABC, abstractmethod
from typing import Dict
from pydantic import BaseModel

class BaseExtractor(ABC):
    def __init__(self, json_format: BaseModel = None):
        self.json_format = json_format
        
    
    @abstractmethod
    def parse_prompt(self, context: str = None) -> str:
        """Given the website body is the context, place it into prompt"""
        pass
    
    def extract(self, website_body: str = ""):
        """Extract the query selector

        Raises:
            NotImplementedError
        """
        parsed_prompt = self.parse_prompt(website_body)
        return self._extract(parsed_prompt)
        
    @abstractmethod
    def _extract(self, parsed_prompt: str):
        """This method should implement extraction logic after parsing"""
        pass