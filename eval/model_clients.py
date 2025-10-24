
import os
from dataclasses import dataclass
from typing import List

@dataclass
class ModelConfig:
    provider: str   # 'openai' | 'anthropic' | 'google' | 'openrouter' | 'huggingface'
    model: str
    temperature: float = 0.6
    max_tokens: int = 1024

class ModelClient:
    """Base client interface."""
    def __init__(self, cfg: ModelConfig):
        self.cfg = cfg

    def generate(self, prompt: str, n: int = 1) -> List[str]:
        raise NotImplementedError

class OpenAIClient(ModelClient):
    def __init__(self, cfg: ModelConfig):
        super().__init__(cfg)
        try:
            from openai import OpenAI  # type: ignore
            self._client = OpenAI()
        except Exception as e:
            raise RuntimeError("openai package not installed") from e

    def generate(self, prompt: str, n: int = 1) -> List[str]:
        # Using the latest OpenAI API
        completion = self._client.chat.completions.create(
            model=self.cfg.model,
            messages=[{"role":"user","content":prompt}],
            temperature=self.cfg.temperature,
            n=n,
            max_tokens=self.cfg.max_tokens,
        )
        outs = []
        for choice in completion.choices:
            outs.append(choice.message.content)
        return outs

class AnthropicClient(ModelClient):
    def __init__(self, cfg: ModelConfig):
        super().__init__(cfg)
        try:
            import anthropic  # type: ignore
            self._client = anthropic.Anthropic()  # needs ANTHROPIC_API_KEY
        except Exception as e:
            raise RuntimeError("anthropic package not installed") from e

    def generate(self, prompt: str, n: int = 1) -> List[str]:
        outs = []
        for _ in range(n):
            msg = self._client.messages.create(
                model=self.cfg.model,
                max_tokens=self.cfg.max_tokens,
                temperature=self.cfg.temperature,
                messages=[{"role":"user","content":prompt}],
            )
            text = "".join(getattr(block, "text", "") for block in getattr(msg, "content", []))
            outs.append(text)
        return outs

class GoogleClient(ModelClient):
    def __init__(self, cfg: ModelConfig):
        super().__init__(cfg)
        try:
            import google.generativeai as genai  # type: ignore
            api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_TOKEN")
            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel(cfg.model)
        except Exception as e:
            raise RuntimeError("google-generativeai package not installed or API key missing") from e

    def generate(self, prompt: str, n: int = 1) -> List[str]:
        outs = []
        for _ in range(n):
            resp = self._model.generate_content(prompt)
            outs.append(getattr(resp, "text", "") or "")
        return outs

class OpenRouterClient(ModelClient):
    def __init__(self, cfg: ModelConfig):
        super().__init__(cfg)
        try:
            from openai import OpenAI  # type: ignore
            self._client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.environ.get("OPENROUTER_API_KEY")
            )
        except Exception as e:
            raise RuntimeError("openai package not installed or OpenRouter API key missing") from e

    def generate(self, prompt: str, n: int = 1) -> List[str]:
        # Using OpenRouter API with OpenAI client
        completion = self._client.chat.completions.create(
            model=self.cfg.model,
            messages=[{"role":"user","content":prompt}],
            temperature=self.cfg.temperature,
            n=n,
            max_tokens=self.cfg.max_tokens,
        )
        outs = []
        for choice in completion.choices:
            outs.append(choice.message.content)
        return outs

class HuggingFaceClient(ModelClient):
    def __init__(self, cfg: ModelConfig):
        super().__init__(cfg)
        try:
            from openai import OpenAI  # type: ignore
            self.api_key = os.environ.get("HUGGINGFACE_API_KEY")
            if not self.api_key:
                raise RuntimeError("HUGGINGFACE_API_KEY not set")
            # Use OpenAI-compatible client with new Hugging Face router
            self._client = OpenAI(
                base_url="https://router.huggingface.co/v1",
                api_key=self.api_key
            )
        except Exception as e:
            raise RuntimeError("openai package not installed or HuggingFace API key missing") from e

    def generate(self, prompt: str, n: int = 1) -> List[str]:
        # Using new Hugging Face Inference Providers API
        completion = self._client.chat.completions.create(
            model=self.cfg.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.cfg.temperature,
            n=n,
            max_tokens=self.cfg.max_tokens,
        )
        outs = []
        for choice in completion.choices:
            outs.append(choice.message.content)
        return outs

def get_client(cfg: ModelConfig) -> ModelClient:
    p = cfg.provider.lower()
    if p == "openai":
        return OpenAIClient(cfg)
    if p == "anthropic":
        return AnthropicClient(cfg)
    if p == "google":
        return GoogleClient(cfg)
    if p == "openrouter":
        return OpenRouterClient(cfg)
    if p == "huggingface":
        return HuggingFaceClient(cfg)
    raise ValueError(f"Unknown provider {cfg.provider}")
