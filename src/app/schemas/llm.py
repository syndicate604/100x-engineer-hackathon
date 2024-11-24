from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict
import os

class ModelProvider(Enum):
    """Enum for supported model providers"""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    DEEPSEEK = "deepseek"


class Message(BaseModel):
    """Message model for chat interactions"""

    role: str = Field(
        ..., description="Role of the message sender (system/user/assistant)"
    )
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Request model for chat completions"""

    messages: List[Message]


class ChatResponse(BaseModel):
    """Response model for chat completions"""

    model: str
    choices: List[Dict[str, Union[str, Message]]]
    usage: Optional[Dict[str, int]]


class ModelConfig(BaseModel):
    """Configuration for model settings"""

    name: str
    provider: ModelProvider
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: int = Field(default=1024, gt=0)
    stream: bool = False

class APIKeyManager:
    """Manages API keys for different providers"""

    def __init__(self):
        self._keys = {
            ModelProvider.ANTHROPIC: os.getenv("ANTHROPIC_API_KEY", ""),
            ModelProvider.OPENAI: os.getenv("OPENAI_API_KEY", ""),
            ModelProvider.HUGGINGFACE: os.getenv("HuggingFace_API_KEY", ""),
            ModelProvider.DEEPSEEK: os.getenv("DEEPSEEK_API_KEY", ""),
        }

    def get_key(self, provider: ModelProvider) -> str:
        """Get API key for specified provider"""
        key = self._keys.get(provider)
        if not key:
            raise ValueError(f"No API key found for provider: {provider.value}")
        return key