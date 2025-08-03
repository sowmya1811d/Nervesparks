"""
Content Embedder for Educational RAG System

Handles text embeddings for educational content using Sentence Transformers.
"""

import logging
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class ContentEmbedder:
    """
    Content embedder for educational materials using Sentence Transformers.
    
    Features:
    - Text embedding generation
    - Batch processing
    - Model management
    - Embedding similarity calculation
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedder with a specific model.
        
        Args:
            model_name: Name of the Sentence Transformer model to use
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
        
        logger.info(f"Initialized embedder with model: {model_name}")
    
    def _load_model(self):
        """Load the Sentence Transformer model."""
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Successfully loaded model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error loading model {self.model_name}: {e}")
            # Fallback to a default model
            try:
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("Loaded fallback model: all-MiniLM-L6-v2")
            except Exception as e2:
                logger.error(f"Error loading fallback model: {e2}")
                raise
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        if not text or not text.strip():
            return np.zeros(self.model.get_sentence_embedding_dimension())
        
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            return np.zeros(self.model.get_sentence_embedding_dimension())
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            Embedding vectors as numpy array
        """
        if not texts:
            return np.array([])
        
        # Filter out empty texts
        valid_texts = [text for text in texts if text and text.strip()]
        
        if not valid_texts:
            return np.zeros((0, self.model.get_sentence_embedding_dimension()))
        
        try:
            embeddings = self.model.encode(valid_texts, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            logger.error(f"Error embedding texts: {e}")
            return np.zeros((len(valid_texts), self.model.get_sentence_embedding_dimension()))
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        try:
            # Normalize embeddings
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Calculate cosine similarity
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def find_most_similar(self, 
                         query_embedding: np.ndarray, 
                         candidate_embeddings: List[np.ndarray],
                         top_k: int = 5) -> List[tuple]:
        """
        Find the most similar embeddings to a query embedding.
        
        Args:
            query_embedding: Query embedding vector
            candidate_embeddings: List of candidate embedding vectors
            top_k: Number of top similar embeddings to return
            
        Returns:
            List of tuples (index, similarity_score) sorted by similarity
        """
        if not candidate_embeddings:
            return []
        
        similarities = []
        for i, candidate in enumerate(candidate_embeddings):
            similarity = self.calculate_similarity(query_embedding, candidate)
            similarities.append((i, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def batch_similarity_search(self,
                               query_embeddings: List[np.ndarray],
                               candidate_embeddings: List[np.ndarray],
                               top_k: int = 5) -> List[List[tuple]]:
        """
        Perform batch similarity search for multiple queries.
        
        Args:
            query_embeddings: List of query embedding vectors
            candidate_embeddings: List of candidate embedding vectors
            top_k: Number of top similar embeddings to return per query
            
        Returns:
            List of results for each query, where each result is a list of (index, similarity_score) tuples
        """
        results = []
        
        for query_embedding in query_embeddings:
            query_results = self.find_most_similar(query_embedding, candidate_embeddings, top_k)
            results.append(query_results)
        
        return results
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors."""
        return self.model.get_sentence_embedding_dimension()
    
    def get_model_info(self) -> dict:
        """Get information about the current model."""
        return {
            'model_name': self.model_name,
            'embedding_dimension': self.get_embedding_dimension(),
            'max_seq_length': self.model.max_seq_length if hasattr(self.model, 'max_seq_length') else None
        }
    
    def change_model(self, new_model_name: str):
        """
        Change to a different embedding model.
        
        Args:
            new_model_name: Name of the new model to load
        """
        try:
            old_model_name = self.model_name
            self.model_name = new_model_name
            self._load_model()
            logger.info(f"Successfully changed model from {old_model_name} to {new_model_name}")
        except Exception as e:
            logger.error(f"Error changing model to {new_model_name}: {e}")
            # Revert to old model
            self.model_name = old_model_name
            self._load_model()
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text before embedding.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Basic preprocessing
        text = text.strip()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Truncate if too long (most models have limits)
        max_length = 512  # Conservative limit
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        return text
    
    def embed_with_preprocessing(self, text: str) -> np.ndarray:
        """
        Preprocess and embed text.
        
        Args:
            text: Raw text to embed
            
        Returns:
            Embedding vector
        """
        preprocessed_text = self.preprocess_text(text)
        return self.embed_text(preprocessed_text)
    
    def embed_texts_with_preprocessing(self, texts: List[str]) -> np.ndarray:
        """
        Preprocess and embed multiple texts.
        
        Args:
            texts: List of raw texts to embed
            
        Returns:
            Embedding vectors
        """
        preprocessed_texts = [self.preprocess_text(text) for text in texts]
        return self.embed_texts(preprocessed_texts) 