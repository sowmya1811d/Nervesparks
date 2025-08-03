"""
Content Chunker for Educational RAG System

Handles intelligent chunking of educational content for optimal vector storage and retrieval.
"""

import re
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from .processor import ContentMetadata

logger = logging.getLogger(__name__)

@dataclass
class ContentChunk:
    """Represents a chunk of educational content."""
    content: str
    chunk_id: str
    metadata: Dict[str, Any]
    chunk_type: str
    start_position: int
    end_position: int
    parent_document: str

class ContentChunker:
    """
    Intelligent content chunker for educational materials.
    
    Features:
    - Semantic-aware chunking
    - Preservation of context
    - Metadata preservation
    - Overlap management
    """
    
    def __init__(self, 
                 max_chunk_size: int = 1000,
                 chunk_overlap: int = 200,
                 min_chunk_size: int = 100):
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        
        # Chunking strategies for different content types
        self.chunking_strategies = {
            'lesson': self._chunk_lesson,
            'tutorial': self._chunk_tutorial,
            'concept': self._chunk_concept,
            'exercise': self._chunk_exercise,
            'assessment': self._chunk_assessment
        }
    
    def chunk_content(self, content: str, metadata: ContentMetadata) -> List[ContentChunk]:
        """
        Chunk content based on its type and characteristics.
        
        Args:
            content: The content to chunk
            metadata: Content metadata
            
        Returns:
            List of content chunks
        """
        content_type = metadata.content_type
        
        # Use specific strategy if available
        if content_type in self.chunking_strategies:
            return self.chunking_strategies[content_type](content, metadata)
        else:
            # Default chunking strategy
            return self._chunk_generic(content, metadata)
    
    def _chunk_lesson(self, content: str, metadata: ContentMetadata) -> List[ContentChunk]:
        """Chunk lesson content with section preservation."""
        chunks = []
        
        # Split by sections (headers, etc.)
        sections = self._split_by_sections(content)
        
        for i, section in enumerate(sections):
            if len(section.strip()) < self.min_chunk_size:
                continue
                
            # Further split large sections
            if len(section) > self.max_chunk_size:
                sub_chunks = self._split_by_sentences(section)
                for j, sub_chunk in enumerate(sub_chunks):
                    chunk = ContentChunk(
                        content=sub_chunk.strip(),
                        chunk_id=f"{metadata.title}_lesson_{i}_{j}",
                        metadata={
                            'subject': metadata.subject,
                            'difficulty_level': metadata.difficulty_level,
                            'content_type': 'lesson',
                            'section': i,
                            'subsection': j
                        },
                        chunk_type='lesson_section',
                        start_position=content.find(sub_chunk),
                        end_position=content.find(sub_chunk) + len(sub_chunk),
                        parent_document=metadata.title
                    )
                    chunks.append(chunk)
            else:
                chunk = ContentChunk(
                    content=section.strip(),
                    chunk_id=f"{metadata.title}_lesson_{i}",
                    metadata={
                        'subject': metadata.subject,
                        'difficulty_level': metadata.difficulty_level,
                        'content_type': 'lesson',
                        'section': i
                    },
                    chunk_type='lesson_section',
                    start_position=content.find(section),
                    end_position=content.find(section) + len(section),
                    parent_document=metadata.title
                )
                chunks.append(chunk)
        
        return chunks
    
    def _chunk_tutorial(self, content: str, metadata: ContentMetadata) -> List[ContentChunk]:
        """Chunk tutorial content with step preservation."""
        chunks = []
        
        # Split by steps or numbered items
        steps = self._split_by_steps(content)
        
        for i, step in enumerate(steps):
            if len(step.strip()) < self.min_chunk_size:
                continue
                
            chunk = ContentChunk(
                content=step.strip(),
                chunk_id=f"{metadata.title}_tutorial_{i}",
                metadata={
                    'subject': metadata.subject,
                    'difficulty_level': metadata.difficulty_level,
                    'content_type': 'tutorial',
                    'step': i + 1
                },
                chunk_type='tutorial_step',
                start_position=content.find(step),
                end_position=content.find(step) + len(step),
                parent_document=metadata.title
            )
            chunks.append(chunk)
        
        return chunks
    
    def _chunk_concept(self, content: str, metadata: ContentMetadata) -> List[ContentChunk]:
        """Chunk concept content with definition and explanation preservation."""
        chunks = []
        
        # Split by paragraphs or logical sections
        paragraphs = self._split_by_paragraphs(content)
        
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph.strip()) < self.min_chunk_size:
                continue
                
            chunk = ContentChunk(
                content=paragraph.strip(),
                chunk_id=f"{metadata.title}_concept_{i}",
                metadata={
                    'subject': metadata.subject,
                    'difficulty_level': metadata.difficulty_level,
                    'content_type': 'concept',
                    'paragraph': i + 1
                },
                chunk_type='concept_paragraph',
                start_position=content.find(paragraph),
                end_position=content.find(paragraph) + len(paragraph),
                parent_document=metadata.title
            )
            chunks.append(chunk)
        
        return chunks
    
    def _chunk_exercise(self, content: str, metadata: ContentMetadata) -> List[ContentChunk]:
        """Chunk exercise content with problem preservation."""
        chunks = []
        
        # Split by individual problems or exercises
        problems = self._split_by_problems(content)
        
        for i, problem in enumerate(problems):
            if len(problem.strip()) < self.min_chunk_size:
                continue
                
            chunk = ContentChunk(
                content=problem.strip(),
                chunk_id=f"{metadata.title}_exercise_{i}",
                metadata={
                    'subject': metadata.subject,
                    'difficulty_level': metadata.difficulty_level,
                    'content_type': 'exercise',
                    'problem': i + 1
                },
                chunk_type='exercise_problem',
                start_position=content.find(problem),
                end_position=content.find(problem) + len(problem),
                parent_document=metadata.title
            )
            chunks.append(chunk)
        
        return chunks
    
    def _chunk_assessment(self, content: str, metadata: ContentMetadata) -> List[ContentChunk]:
        """Chunk assessment content with question preservation."""
        chunks = []
        
        # Split by questions
        questions = self._split_by_questions(content)
        
        for i, question in enumerate(questions):
            if len(question.strip()) < self.min_chunk_size:
                continue
                
            chunk = ContentChunk(
                content=question.strip(),
                chunk_id=f"{metadata.title}_assessment_{i}",
                metadata={
                    'subject': metadata.subject,
                    'difficulty_level': metadata.difficulty_level,
                    'content_type': 'assessment',
                    'question': i + 1
                },
                chunk_type='assessment_question',
                start_position=content.find(question),
                end_position=content.find(question) + len(question),
                parent_document=metadata.title
            )
            chunks.append(chunk)
        
        return chunks
    
    def _chunk_generic(self, content: str, metadata: ContentMetadata) -> List[ContentChunk]:
        """Generic chunking strategy for unknown content types."""
        chunks = []
        
        # Split by sentences with overlap
        sentences = self._split_by_sentences(content)
        
        current_chunk = ""
        chunk_id = 0
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.max_chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunk = ContentChunk(
                        content=current_chunk.strip(),
                        chunk_id=f"{metadata.title}_generic_{chunk_id}",
                        metadata={
                            'subject': metadata.subject,
                            'difficulty_level': metadata.difficulty_level,
                            'content_type': metadata.content_type,
                            'chunk_id': chunk_id
                        },
                        chunk_type='generic',
                        start_position=content.find(current_chunk),
                        end_position=content.find(current_chunk) + len(current_chunk),
                        parent_document=metadata.title
                    )
                    chunks.append(chunk)
                
                current_chunk = sentence + " "
                chunk_id += 1
        
        # Add the last chunk
        if current_chunk.strip():
            chunk = ContentChunk(
                content=current_chunk.strip(),
                chunk_id=f"{metadata.title}_generic_{chunk_id}",
                metadata={
                    'subject': metadata.subject,
                    'difficulty_level': metadata.difficulty_level,
                    'content_type': metadata.content_type,
                    'chunk_id': chunk_id
                },
                chunk_type='generic',
                start_position=content.find(current_chunk),
                end_position=content.find(current_chunk) + len(current_chunk),
                parent_document=metadata.title
            )
            chunks.append(chunk)
        
        return chunks
    
    def _split_by_sections(self, content: str) -> List[str]:
        """Split content by sections (headers, etc.)."""
        # Look for headers (lines starting with #, numbers, etc.)
        section_pattern = r'(?:^|\n)(?:#{1,6}\s+|^\d+\.\s+|^[A-Z][A-Z\s]+$|^[A-Z][a-z]+:)'
        sections = re.split(section_pattern, content, flags=re.MULTILINE)
        return [s.strip() for s in sections if s.strip()]
    
    def _split_by_steps(self, content: str) -> List[str]:
        """Split content by steps or numbered items."""
        # Look for numbered steps
        step_pattern = r'(?:^|\n)(?:\d+\.\s+|Step\s+\d+:|^\d+\)\s+)'
        steps = re.split(step_pattern, content, flags=re.MULTILINE)
        return [s.strip() for s in steps if s.strip()]
    
    def _split_by_paragraphs(self, content: str) -> List[str]:
        """Split content by paragraphs."""
        paragraphs = re.split(r'\n\s*\n', content)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _split_by_problems(self, content: str) -> List[str]:
        """Split content by individual problems or exercises."""
        # Look for problem indicators
        problem_pattern = r'(?:^|\n)(?:Problem\s+\d+|Exercise\s+\d+|^\d+\.\s+)'
        problems = re.split(problem_pattern, content, flags=re.MULTILINE)
        return [p.strip() for p in problems if p.strip()]
    
    def _split_by_questions(self, content: str) -> List[str]:
        """Split content by questions."""
        # Look for question indicators
        question_pattern = r'(?:^|\n)(?:\d+\.\s+[^.]*\?|Question\s+\d+:|^\d+\)\s+[^)]*\?)'
        questions = re.split(question_pattern, content, flags=re.MULTILINE)
        return [q.strip() for q in questions if q.strip()]
    
    def _split_by_sentences(self, content: str) -> List[str]:
        """Split content by sentences."""
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', content)
        return [s.strip() for s in sentences if s.strip()]
    
    def get_chunk_statistics(self, chunks: List[ContentChunk]) -> Dict[str, Any]:
        """Get statistics about the chunks."""
        if not chunks:
            return {}
        
        chunk_sizes = [len(chunk.content) for chunk in chunks]
        
        stats = {
            'total_chunks': len(chunks),
            'average_chunk_size': sum(chunk_sizes) / len(chunk_sizes),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes),
            'chunk_types': {},
            'subjects': {},
            'difficulty_levels': {}
        }
        
        for chunk in chunks:
            # Count chunk types
            chunk_type = chunk.chunk_type
            stats['chunk_types'][chunk_type] = stats['chunk_types'].get(chunk_type, 0) + 1
            
            # Count subjects
            subject = chunk.metadata.get('subject', 'unknown')
            stats['subjects'][subject] = stats['subjects'].get(subject, 0) + 1
            
            # Count difficulty levels
            difficulty = chunk.metadata.get('difficulty_level', 'unknown')
            stats['difficulty_levels'][difficulty] = stats['difficulty_levels'].get(difficulty, 0) + 1
        
        return stats 