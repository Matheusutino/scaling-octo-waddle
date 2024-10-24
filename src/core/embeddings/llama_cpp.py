import numpy as np
from typing import List, Dict, Any
import llama_cpp
from huggingface_hub import hf_hub_download
from tqdm import tqdm
from src.core.utils import get_value_by_key_json
from src.core.embeddings.base_embeddings import BaseEmbeddings

class LlamaCppEmbeddings(BaseEmbeddings):
    """
    A class to handle the generation and aggregation of token-level embeddings
    using LlamaCpp and manual pooling.

    Attributes:
        llm (llama_cpp.Llama): The Llama model instance.
        model_path (str): Path to the Llama model file.
    """

    def __init__(self, repo_id: str, filename: str, n_ctx: int = 512):
        """
        Initializes the EmbeddingAggregator by downloading the specified model.

        Args:
            repo_id (str): The Hugging Face repository ID of the model.
            filename (str): The filename of the model to download.
        """
        # Download the model file
        n_ctx = get_value_by_key_json(file_path="configs/context_lenght.json", key = repo_id)
        self.model_path = hf_hub_download(repo_id=repo_id, filename=filename)
        self.llm = llama_cpp.Llama(model_path = self.model_path, 
                                   n_ctx = n_ctx, 
                                   n_gpu_layers = -1, 
                                #    verbose = True, 
                                   pooling_type = llama_cpp.LLAMA_POOLING_TYPE_MEAN,
                                   embedding=True)

    def max_pooling(self, token_embeddings: List[List[float]]) -> np.ndarray:
        """
        Computes the maximum of token-level embeddings to produce a sequence-level embedding.

        Args:
            token_embeddings (List[List[float]]): A list of embeddings for each token.

        Returns:
            np.ndarray: The max pooled embedding for the entire sequence.
        """
        token_embeddings_array = np.array(token_embeddings)
        return np.max(token_embeddings_array, axis=0)

    def average_pooling(self, token_embeddings: List[List[float]]) -> np.ndarray:
        """
        Computes the average of token-level embeddings to produce a sequence-level embedding.

        Args:
            token_embeddings (List[List[float]]): A list of embeddings for each token.

        Returns:
            np.ndarray: The averaged embedding for the entire sequence.
        """
        token_embeddings_array = np.array(token_embeddings)
        return np.mean(token_embeddings_array, axis=0)

    def concatenate_pooling(self, token_embeddings: List[List[float]]) -> np.ndarray:
        """
        Computes both average and max pooled embeddings and concatenates them.

        Args:
            token_embeddings (List[List[float]]): A list of embeddings for each token.

        Returns:
            np.ndarray: The concatenated embeddings from average and max pooling.
        """
        avg_embedding = self.average_pooling(token_embeddings)
        max_embedding = self.max_pooling(token_embeddings)
        return np.concatenate((avg_embedding, max_embedding))

    def get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generates and aggregates embeddings for a list of input texts, applying average pooling immediately.

        Args:
            texts (List[str]): A list of strings for which to generate and aggregate embeddings.

        Returns:
            List[np.ndarray]: A list of aggregated sequence-level embeddings.
        """
        # Initialize a list to store aggregated embeddings
        # embeddings = []

        # # Generate and aggregate embeddings for each text
        # for text in tqdm(texts, desc="Generating embeddings"):
        #     # Generate embedding data for the current text
        #     embedding_data = self.llm.create_embedding(text)
        #     print(np.array(embedding_data).shape)
            
        #     # Apply average pooling to the embedding and store the result
        #     pooled_embedding = self.average_pooling(embedding_data['embedding'])
        #     print(pooled_embedding.shape)
        #     embeddings.append(pooled_embedding)

        # return np.array(embeddings)

        # texts = ["Hello, world!", "Goodbye, world!"]

        embeddings = []

        for text in tqdm(texts, desc="Generating embeddings"):
            embedding = self.llm.embed(text)
            embeddings.append(embedding)

        return embeddings


