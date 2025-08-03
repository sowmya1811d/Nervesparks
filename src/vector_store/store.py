"""
Vector Store for Educational RAG System

Handles vector database operations using Chroma for storing and retrieving educational content.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import chromadb
from chromadb.config import Settings
import numpy as np

from ..content_processor.chunker import ContentChunk
from .embedder import ContentEmbedder

logger = logging.getLogger(__name__)

class VectorStore:
    """
    Vector store for educational content using Chroma.
    
    Features:
    - Content storage and retrieval
    - Metadata filtering
    - Semantic search
    - Hybrid search (semantic + keyword)
    - Relevance scoring
    """
    
    def __init__(self, 
                 persist_directory: str = "data/vector_store",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize embedder
        self.embedder = ContentEmbedder(model_name=embedding_model)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="educational_content",
            metadata={"description": "Educational content vector store"}
        )
        
        logger.info(f"Initialized vector store at {self.persist_directory}")
    
    def add_content(self, chunks: List[ContentChunk]) -> List[str]:
        """
        Add content chunks to the vector store.
        
        Args:
            chunks: List of content chunks to add
            
        Returns:
            List of chunk IDs that were added
        """
        if not chunks:
            return []
        
        # Prepare data for Chroma
        documents = []
        metadatas = []
        ids = []
        
        for chunk in chunks:
            # Create document text
            doc_text = f"Title: {chunk.parent_document}\n\n{chunk.content}"
            
            # Create metadata
            metadata = {
                'chunk_id': chunk.chunk_id,
                'parent_document': chunk.parent_document,
                'chunk_type': chunk.chunk_type,
                'subject': chunk.metadata.get('subject', 'unknown'),
                'difficulty_level': chunk.metadata.get('difficulty_level', 'unknown'),
                'content_type': chunk.metadata.get('content_type', 'unknown'),
                'start_position': chunk.start_position,
                'end_position': chunk.end_position
            }
            
            # Add additional metadata
            for key, value in chunk.metadata.items():
                if key not in metadata and isinstance(value, (str, int, float, bool)):
                    metadata[key] = value
            
            documents.append(doc_text)
            metadatas.append(metadata)
            ids.append(chunk.chunk_id)
        
        # Add to collection
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(chunks)} chunks to vector store")
            return ids
        except Exception as e:
            logger.error(f"Error adding chunks to vector store: {e}")
            return []
    
    def search(self, 
               query: str, 
               n_results: int = 10,
               filters: Optional[Dict[str, Any]] = None,
               search_type: str = "semantic") -> List[Dict[str, Any]]:
        """
        Search for relevant content.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filters: Metadata filters
            search_type: Type of search ("semantic", "keyword", "hybrid")
            
        Returns:
            List of search results with content and metadata
        """
        try:
            if search_type == "semantic":
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where=filters
                )
            elif search_type == "keyword":
                # For keyword search, we'll use a simple approach
                # In a real implementation, you might use BM25 or similar
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where=filters
                )
            elif search_type == "hybrid":
                # Hybrid search combining semantic and keyword
                semantic_results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results * 2,
                    where=filters
                )
                
                # Re-rank based on keyword matching
                results = self._hybrid_rerank(semantic_results, query, n_results)
            else:
                raise ValueError(f"Unknown search type: {search_type}")
            
            # Format results
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    result = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'id': results['ids'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []
    
    def _hybrid_rerank(self, 
                       semantic_results: Dict[str, Any], 
                       query: str, 
                       n_results: int) -> Dict[str, Any]:
        """Re-rank semantic results using keyword matching."""
        if not semantic_results['documents']:
            return semantic_results
        
        # Calculate keyword scores
        query_terms = set(query.lower().split())
        scored_results = []
        
        for i, doc in enumerate(semantic_results['documents'][0]):
            doc_terms = set(doc.lower().split())
            keyword_overlap = len(query_terms.intersection(doc_terms))
            semantic_score = 1 - semantic_results['distances'][0][i]  # Convert distance to similarity
            
            # Combine scores (you can adjust weights)
            hybrid_score = 0.7 * semantic_score + 0.3 * (keyword_overlap / len(query_terms))
            
            scored_results.append({
                'index': i,
                'hybrid_score': hybrid_score,
                'semantic_score': semantic_score,
                'keyword_score': keyword_overlap / len(query_terms)
            })
        
        # Sort by hybrid score
        scored_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        # Reconstruct results
        top_indices = [r['index'] for r in scored_results[:n_results]]
        
        reranked_results = {
            'documents': [[semantic_results['documents'][0][i] for i in top_indices]],
            'metadatas': [[semantic_results['metadatas'][0][i] for i in top_indices]],
            'ids': [[semantic_results['ids'][0][i] for i in top_indices]],
            'distances': [[1 - r['hybrid_score'] for r in scored_results[:n_results]]]
        }
        
        return reranked_results
    
    def get_by_metadata(self, 
                        filters: Dict[str, Any], 
                        n_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get content by metadata filters.
        
        Args:
            filters: Metadata filters
            n_results: Number of results to return
            
        Returns:
            List of content matching the filters
        """
        try:
            results = self.collection.get(
                where=filters,
                limit=n_results
            )
            
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'])):
                    result = {
                        'content': results['documents'][i],
                        'metadata': results['metadatas'][i],
                        'id': results['ids'][i]
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error getting content by metadata: {e}")
            return []
    
    def get_similar_content(self, 
                           content_id: str, 
                           n_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get content similar to a specific piece of content.
        
        Args:
            content_id: ID of the content to find similar items for
            n_results: Number of similar results to return
            
        Returns:
            List of similar content
        """
        try:
            # Get the target content
            target_content = self.collection.get(ids=[content_id])
            
            if not target_content['documents']:
                return []
            
            # Search for similar content
            results = self.collection.query(
                query_texts=target_content['documents'],
                n_results=n_results + 1,  # +1 to account for the original
                exclude_ids=[content_id]
            )
            
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    result = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'id': results['ids'][0][i],
                        'similarity': 1 - results['distances'][0][i]
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error getting similar content: {e}")
            return []
    
    def update_content(self, chunk_id: str, new_content: str, new_metadata: Dict[str, Any]):
        """
        Update existing content in the vector store.
        
        Args:
            chunk_id: ID of the chunk to update
            new_content: New content text
            new_metadata: New metadata
        """
        try:
            # Delete existing content
            self.collection.delete(ids=[chunk_id])
            
            # Add updated content
            self.collection.add(
                documents=[new_content],
                metadatas=[new_metadata],
                ids=[chunk_id]
            )
            
            logger.info(f"Updated content with ID: {chunk_id}")
            
        except Exception as e:
            logger.error(f"Error updating content: {e}")
    
    def delete_content(self, chunk_ids: List[str]):
        """
        Delete content from the vector store.
        
        Args:
            chunk_ids: List of chunk IDs to delete
        """
        try:
            self.collection.delete(ids=chunk_ids)
            logger.info(f"Deleted {len(chunk_ids)} chunks from vector store")
            
        except Exception as e:
            logger.error(f"Error deleting content: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        try:
            count = self.collection.count()
            
            # Get sample of content for analysis
            sample_results = self.collection.get(limit=1000)
            
            stats = {
                'total_chunks': count,
                'subjects': {},
                'content_types': {},
                'difficulty_levels': {},
                'chunk_types': {}
            }
            
            if sample_results['metadatas']:
                for metadata in sample_results['metadatas']:
                    # Count subjects
                    subject = metadata.get('subject', 'unknown')
                    stats['subjects'][subject] = stats['subjects'].get(subject, 0) + 1
                    
                    # Count content types
                    content_type = metadata.get('content_type', 'unknown')
                    stats['content_types'][content_type] = stats['content_types'].get(content_type, 0) + 1
                    
                    # Count difficulty levels
                    difficulty = metadata.get('difficulty_level', 'unknown')
                    stats['difficulty_levels'][difficulty] = stats['difficulty_levels'].get(difficulty, 0) + 1
                    
                    # Count chunk types
                    chunk_type = metadata.get('chunk_type', 'unknown')
                    stats['chunk_types'][chunk_type] = stats['chunk_types'].get(chunk_type, 0) + 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting vector store statistics: {e}")
            return {}
    
    def clear_all(self):
        """Clear all content from the vector store."""
        try:
            self.client.delete_collection("educational_content")
            self.collection = self.client.create_collection(
                name="educational_content",
                metadata={"description": "Educational content vector store"}
            )
            logger.info("Cleared all content from vector store")
            
        except Exception as e:
            logger.error(f"Error clearing vector store: {e}")
    
    def export_data(self, output_path: str):
        """
        Export vector store data to a file.
        
        Args:
            output_path: Path to save the exported data
        """
        try:
            # Get all data
            all_data = self.collection.get()
            
            export_data = {
                'documents': all_data['documents'],
                'metadatas': all_data['metadatas'],
                'ids': all_data['ids'],
                'exported_at': str(Path().absolute())
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported vector store data to {output_path}")
            
        except Exception as e:
            logger.error(f"Error exporting vector store data: {e}")
    
    def import_data(self, import_path: str):
        """
        Import vector store data from a file.
        
        Args:
            import_path: Path to the file containing data to import
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Add imported data
            self.collection.add(
                documents=import_data['documents'],
                metadatas=import_data['metadatas'],
                ids=import_data['ids']
            )
            
            logger.info(f"Imported vector store data from {import_path}")
            
        except Exception as e:
            logger.error(f"Error importing vector store data: {e}") 