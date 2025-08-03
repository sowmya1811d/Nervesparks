"""
Content Processor for Educational RAG System

Handles the ingestion, preprocessing, and initial processing of educational content.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
from dataclasses import dataclass

from .chunker import ContentChunker
from .categorizer import ContentCategorizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ContentMetadata:
    """Metadata for educational content."""
    title: str
    subject: str
    difficulty_level: str
    content_type: str
    learning_objectives: List[str]
    prerequisites: List[str]
    estimated_duration: int  # in minutes
    tags: List[str]
    source_url: Optional[str] = None
    author: Optional[str] = None
    last_updated: Optional[str] = None

class ContentProcessor:
    """
    Main content processor for educational materials.
    
    Handles:
    - Content ingestion from various sources
    - Preprocessing and cleaning
    - Metadata extraction
    - Content categorization
    - Chunking for vector storage
    """
    
    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.chunker = ContentChunker()
        self.categorizer = ContentCategorizer()
        
        # Supported file types
        self.supported_extensions = {'.txt', '.md', '.pdf', '.docx', '.json', '.csv'}
        
    def process_content(self, content_path: str, metadata: Optional[ContentMetadata] = None) -> Dict[str, Any]:
        """
        Process educational content from a file or directory.
        
        Args:
            content_path: Path to content file or directory
            metadata: Optional metadata for the content
            
        Returns:
            Dictionary containing processed content and metadata
        """
        content_path = Path(content_path)
        
        if content_path.is_file():
            return self._process_single_file(content_path, metadata)
        elif content_path.is_dir():
            return self._process_directory(content_path)
        else:
            raise ValueError(f"Path {content_path} does not exist")
    
    def _process_single_file(self, file_path: Path, metadata: Optional[ContentMetadata] = None) -> Dict[str, Any]:
        """Process a single content file."""
        logger.info(f"Processing file: {file_path}")
        
        # Read content based on file type
        content = self._read_content(file_path)
        
        # Extract metadata if not provided
        if metadata is None:
            metadata = self._extract_metadata(file_path, content)
        
        # Categorize content
        category = self.categorizer.categorize(content, metadata)
        
        # Chunk content
        chunks = self.chunker.chunk_content(content, metadata)
        
        # Prepare processed content
        processed_content = {
            'file_path': str(file_path),
            'content': content,
            'metadata': metadata.__dict__,
            'category': category,
            'chunks': chunks,
            'processed_at': pd.Timestamp.now().isoformat()
        }
        
        # Save processed content
        self._save_processed_content(processed_content, file_path.stem)
        
        return processed_content
    
    def _process_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Process all supported files in a directory."""
        logger.info(f"Processing directory: {dir_path}")
        
        processed_files = []
        
        for file_path in dir_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                try:
                    processed = self._process_single_file(file_path)
                    processed_files.append(processed)
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
        
        return {
            'directory': str(dir_path),
            'processed_files': processed_files,
            'total_files': len(processed_files)
        }
    
    def _read_content(self, file_path: Path) -> str:
        """Read content from various file types."""
        extension = file_path.suffix.lower()
        
        if extension == '.txt' or extension == '.md':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif extension == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return json.dumps(data, indent=2)
        
        elif extension == '.csv':
            df = pd.read_csv(file_path)
            return df.to_string()
        
        elif extension == '.pdf':
            # For PDF files, we'll use a simple text extraction
            # In a real implementation, you'd use PyPDF2 or similar
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                logger.warning("PyPDF2 not available, skipping PDF file")
                return ""
        
        elif extension == '.docx':
            # For DOCX files, we'll use python-docx
            try:
                from docx import Document
                doc = Document(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            except ImportError:
                logger.warning("python-docx not available, skipping DOCX file")
                return ""
        
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    def _extract_metadata(self, file_path: Path, content: str) -> ContentMetadata:
        """Extract metadata from file and content."""
        # Basic metadata extraction
        title = file_path.stem.replace('_', ' ').title()
        
        # Try to extract subject from filename or content
        subject = self._extract_subject(file_path, content)
        
        # Estimate difficulty level based on content analysis
        difficulty_level = self._estimate_difficulty(content)
        
        # Determine content type
        content_type = self._determine_content_type(file_path, content)
        
        # Extract learning objectives (basic implementation)
        learning_objectives = self._extract_learning_objectives(content)
        
        return ContentMetadata(
            title=title,
            subject=subject,
            difficulty_level=difficulty_level,
            content_type=content_type,
            learning_objectives=learning_objectives,
            prerequisites=[],
            estimated_duration=30,  # Default 30 minutes
            tags=[],
            source_url=None,
            author=None,
            last_updated=None
        )
    
    def _extract_subject(self, file_path: Path, content: str) -> str:
        """Extract subject from filename or content."""
        # Simple subject extraction based on filename patterns
        filename = file_path.stem.lower()
        
        subjects = {
            'math': ['math', 'mathematics', 'algebra', 'calculus', 'geometry'],
            'science': ['science', 'physics', 'chemistry', 'biology'],
            'history': ['history', 'historical'],
            'literature': ['literature', 'english', 'writing'],
            'computer_science': ['programming', 'coding', 'computer', 'software']
        }
        
        for subject, keywords in subjects.items():
            if any(keyword in filename for keyword in keywords):
                return subject
        
        return 'general'
    
    def _estimate_difficulty(self, content: str) -> str:
        """Estimate difficulty level based on content analysis."""
        # Simple difficulty estimation based on content length and complexity
        word_count = len(content.split())
        
        if word_count < 500:
            return 'beginner'
        elif word_count < 2000:
            return 'intermediate'
        else:
            return 'advanced'
    
    def _determine_content_type(self, file_path: Path, content: str) -> str:
        """Determine the type of educational content."""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['quiz', 'test', 'assessment']):
            return 'assessment'
        elif any(word in content_lower for word in ['exercise', 'practice', 'problem']):
            return 'exercise'
        elif any(word in content_lower for word in ['tutorial', 'guide', 'how-to']):
            return 'tutorial'
        elif any(word in content_lower for word in ['concept', 'theory', 'definition']):
            return 'concept'
        else:
            return 'lesson'
    
    def _extract_learning_objectives(self, content: str) -> List[str]:
        """Extract learning objectives from content."""
        # Basic implementation - look for common objective patterns
        objectives = []
        
        # Look for patterns like "Students will learn..." or "Learning objectives:"
        lines = content.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(phrase in line_lower for phrase in ['students will', 'learning objective', 'objective:', 'goal:']):
                objectives.append(line.strip())
        
        return objectives[:5]  # Limit to 5 objectives
    
    def _save_processed_content(self, processed_content: Dict[str, Any], filename: str):
        """Save processed content to disk."""
        output_file = self.output_dir / f"{filename}_processed.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_content, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved processed content to {output_file}")
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get statistics about processed content."""
        processed_files = list(self.output_dir.glob("*_processed.json"))
        
        stats = {
            'total_processed_files': len(processed_files),
            'subjects': {},
            'difficulty_levels': {},
            'content_types': {}
        }
        
        for file_path in processed_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                metadata = data['metadata']
                
                # Count subjects
                subject = metadata.get('subject', 'unknown')
                stats['subjects'][subject] = stats['subjects'].get(subject, 0) + 1
                
                # Count difficulty levels
                difficulty = metadata.get('difficulty_level', 'unknown')
                stats['difficulty_levels'][difficulty] = stats['difficulty_levels'].get(difficulty, 0) + 1
                
                # Count content types
                content_type = metadata.get('content_type', 'unknown')
                stats['content_types'][content_type] = stats['content_types'].get(content_type, 0) + 1
        
        return stats 