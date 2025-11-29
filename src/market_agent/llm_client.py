from __future__ import annotations
from typing import Protocol
import os
from huggingface_hub import InferenceClient


class LLMClient(Protocol):
    """
    A minimal and vendor-neutral interface for summarisation.
    Keeps the agent decoupled from the model/provider.
    """

class HuggingFaceSummariser:
    """
    Light wrapper around HF Inference API for financial-style summaries.
    Model and token come from environment variables.
    """
    def __init__(self) -> None:
        model = os.getenv("LLM_MODEL", "google/gemma-2b-it")
        token = os.getenv("HF_API_TOKEN")

        if not token:
            raise RuntimeError("HF_API_TOKEN not set")

        self.client = InferenceClient(model=model, token=token)

    def summarise(self, text: str) -> str:
        prompt = (
            "You are a concise financial analyst. "
            "Provide an executive summary of the following market movements "
            "in 4–6 bullet points, written in clear business English:\n\n"
            f"{text}\n"
        )

        resp = self.client.text_generation(
            prompt,
            max_new_tokens=200,
            temperature=0.3,
        )
        return resp.strip()