"""Model encoder."""
from typing import List, Annotated
from pydantic import BaseModel, ConfigDict, PrivateAttr
import torch
from transformers import AutoModel, AutoTokenizer, PreTrainedTokenizer, PreTrainedModel
from .env_settings import MODEL_NAME

def mean_pooling(
    model_output: torch.Tensor,
    attention_mask: torch.Tensor
    ) -> torch.Tensor:
    """Mean pooling function."""
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    num = torch.sum(token_embeddings * input_mask_expanded, 1)
    den = torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    return num / den

def get_hf_model() -> PreTrainedModel:
    """Get huggingface model."""
    return AutoModel.from_pretrained(MODEL_NAME, trust_remote_code=True)

def get_hf_tokenizer() -> PreTrainedTokenizer:
    """Get huggingface tokenizer."""
    return AutoTokenizer.from_pretrained(MODEL_NAME)

class Encoder(BaseModel):
    """Encoder."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _tokenizer: Annotated[PreTrainedTokenizer, PrivateAttr(default_factory=get_hf_tokenizer)]
    _model: Annotated[PreTrainedModel, PrivateAttr(default_factory=get_hf_model)]

    async def encode(self, documents: List[str]) -> List[List[float]]:
        """Encode."""
        inputs = self._tokenizer(
            documents,
            padding=True,
            truncation=True,
            return_tensors="pt"
            )

        with torch.no_grad():
            op = self._model(**inputs)

        return (
            mean_pooling(op, inputs["attention_mask"])
            .detach()
            .cpu()
            .numpy()
            .tolist()
        )
