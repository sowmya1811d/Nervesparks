"""
Content Categorizer for Educational RAG System

Handles intelligent categorization of educational content based on its characteristics.
"""

import re
import logging
from typing import Dict, Any, List
from .processor import ContentMetadata

logger = logging.getLogger(__name__)

class ContentCategorizer:
    """
    Intelligent content categorizer for educational materials.
    
    Features:
    - Subject classification
    - Difficulty level assessment
    - Content type identification
    - Learning objective extraction
    - Prerequisite identification
    """
    
    def __init__(self):
        # Subject keywords for classification
        self.subject_keywords = {
            'mathematics': [
                'algebra', 'calculus', 'geometry', 'trigonometry', 'statistics',
                'probability', 'number theory', 'linear algebra', 'differential equations',
                'mathematical', 'equation', 'formula', 'theorem', 'proof'
            ],
            'physics': [
                'mechanics', 'thermodynamics', 'electromagnetism', 'optics',
                'quantum physics', 'relativity', 'force', 'energy', 'motion',
                'wave', 'particle', 'field', 'momentum', 'acceleration'
            ],
            'chemistry': [
                'organic chemistry', 'inorganic chemistry', 'biochemistry',
                'analytical chemistry', 'molecule', 'atom', 'bond', 'reaction',
                'compound', 'element', 'solution', 'acid', 'base', 'catalyst'
            ],
            'biology': [
                'cell biology', 'genetics', 'ecology', 'evolution', 'anatomy',
                'physiology', 'microbiology', 'organism', 'species', 'ecosystem',
                'dna', 'protein', 'enzyme', 'metabolism', 'photosynthesis'
            ],
            'computer_science': [
                'programming', 'algorithm', 'data structure', 'software engineering',
                'artificial intelligence', 'machine learning', 'database', 'network',
                'operating system', 'compiler', 'code', 'function', 'class'
            ],
            'history': [
                'ancient', 'medieval', 'modern', 'civilization', 'empire',
                'war', 'revolution', 'culture', 'society', 'politics', 'economics'
            ],
            'literature': [
                'novel', 'poetry', 'drama', 'fiction', 'non-fiction', 'author',
                'character', 'plot', 'theme', 'symbolism', 'metaphor', 'narrative'
            ],
            'economics': [
                'microeconomics', 'macroeconomics', 'supply', 'demand', 'market',
                'inflation', 'unemployment', 'gdp', 'trade', 'monetary policy'
            ]
        }
        
        # Content type patterns
        self.content_type_patterns = {
            'lesson': [
                r'lesson', r'chapter', r'unit', r'topic', r'concept',
                r'introduction', r'overview', r'background'
            ],
            'tutorial': [
                r'tutorial', r'guide', r'how.?to', r'step.?by.?step',
                r'instructions', r'procedure', r'method'
            ],
            'exercise': [
                r'exercise', r'practice', r'problem', r'worksheet',
                r'activity', r'assignment', r'homework'
            ],
            'assessment': [
                r'quiz', r'test', r'exam', r'assessment', r'evaluation',
                r'question', r'multiple choice', r'true.?false'
            ],
            'concept': [
                r'definition', r'concept', r'theory', r'principle',
                r'fundamental', r'basic', r'core'
            ]
        }
        
        # Difficulty indicators
        self.difficulty_indicators = {
            'beginner': [
                'basic', 'fundamental', 'introduction', 'overview', 'simple',
                'elementary', 'prerequisite', 'foundation'
            ],
            'intermediate': [
                'intermediate', 'advanced', 'complex', 'detailed', 'comprehensive',
                'application', 'analysis', 'synthesis'
            ],
            'advanced': [
                'advanced', 'expert', 'specialized', 'research', 'theoretical',
                'sophisticated', 'cutting.?edge', 'state.?of.?the.?art'
            ]
        }
    
    def categorize(self, content: str, metadata: ContentMetadata) -> Dict[str, Any]:
        """
        Categorize educational content based on its characteristics.
        
        Args:
            content: The content to categorize
            metadata: Content metadata
            
        Returns:
            Dictionary containing categorization results
        """
        # Analyze content characteristics
        subject = self._classify_subject(content, metadata)
        content_type = self._classify_content_type(content, metadata)
        difficulty = self._classify_difficulty(content, metadata)
        learning_objectives = self._extract_learning_objectives(content)
        prerequisites = self._extract_prerequisites(content)
        
        return {
            'subject': subject,
            'content_type': content_type,
            'difficulty_level': difficulty,
            'learning_objectives': learning_objectives,
            'prerequisites': prerequisites,
            'confidence_scores': {
                'subject': self._calculate_subject_confidence(content, subject),
                'content_type': self._calculate_content_type_confidence(content, content_type),
                'difficulty': self._calculate_difficulty_confidence(content, difficulty)
            }
        }
    
    def _classify_subject(self, content: str, metadata: ContentMetadata) -> str:
        """Classify the subject of the content."""
        content_lower = content.lower()
        
        # Check metadata first
        if metadata.subject and metadata.subject != 'general':
            return metadata.subject
        
        # Analyze content for subject keywords
        subject_scores = {}
        
        for subject, keywords in self.subject_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in content_lower:
                    score += 1
            
            if score > 0:
                subject_scores[subject] = score
        
        # Return the subject with the highest score
        if subject_scores:
            return max(subject_scores, key=subject_scores.get)
        
        return 'general'
    
    def _classify_content_type(self, content: str, metadata: ContentMetadata) -> str:
        """Classify the type of educational content."""
        content_lower = content.lower()
        
        # Check metadata first
        if metadata.content_type:
            return metadata.content_type
        
        # Analyze content for type patterns
        type_scores = {}
        
        for content_type, patterns in self.content_type_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, content_lower, re.IGNORECASE)
                score += len(matches)
            
            if score > 0:
                type_scores[content_type] = score
        
        # Return the type with the highest score
        if type_scores:
            return max(type_scores, key=type_scores.get)
        
        return 'lesson'  # Default to lesson
    
    def _classify_difficulty(self, content: str, metadata: ContentMetadata) -> str:
        """Classify the difficulty level of the content."""
        content_lower = content.lower()
        
        # Check metadata first
        if metadata.difficulty_level:
            return metadata.difficulty_level
        
        # Analyze content for difficulty indicators
        difficulty_scores = {}
        
        for difficulty, indicators in self.difficulty_indicators.items():
            score = 0
            for indicator in indicators:
                if indicator in content_lower:
                    score += 1
            
            if score > 0:
                difficulty_scores[difficulty] = score
        
        # Return the difficulty with the highest score
        if difficulty_scores:
            return max(difficulty_scores, key=difficulty_scores.get)
        
        # Fallback to content length analysis
        word_count = len(content.split())
        if word_count < 500:
            return 'beginner'
        elif word_count < 2000:
            return 'intermediate'
        else:
            return 'advanced'
    
    def _extract_learning_objectives(self, content: str) -> List[str]:
        """Extract learning objectives from content."""
        objectives = []
        
        # Look for common objective patterns
        objective_patterns = [
            r'learning objective[s]?:?\s*(.+)',
            r'students? will learn:?\s*(.+)',
            r'objective[s]?:?\s*(.+)',
            r'goal[s]?:?\s*(.+)',
            r'by the end of this.*?students? will:?\s*(.+)'
        ]
        
        for pattern in objective_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            objectives.extend(matches)
        
        # Clean and limit objectives
        cleaned_objectives = []
        for obj in objectives:
            obj = obj.strip()
            if len(obj) > 10 and len(obj) < 200:  # Reasonable length
                cleaned_objectives.append(obj)
        
        return cleaned_objectives[:5]  # Limit to 5 objectives
    
    def _extract_prerequisites(self, content: str) -> List[str]:
        """Extract prerequisites from content."""
        prerequisites = []
        
        # Look for prerequisite patterns
        prerequisite_patterns = [
            r'prerequisite[s]?:?\s*(.+)',
            r'before.*?you should.*?:?\s*(.+)',
            r'required knowledge:?\s*(.+)',
            r'assuming.*?:?\s*(.+)'
        ]
        
        for pattern in prerequisite_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            prerequisites.extend(matches)
        
        # Clean prerequisites
        cleaned_prerequisites = []
        for prereq in prerequisites:
            prereq = prereq.strip()
            if len(prereq) > 5 and len(prereq) < 150:
                cleaned_prerequisites.append(prereq)
        
        return cleaned_prerequisites[:3]  # Limit to 3 prerequisites
    
    def _calculate_subject_confidence(self, content: str, subject: str) -> float:
        """Calculate confidence score for subject classification."""
        if subject == 'general':
            return 0.3
        
        content_lower = content.lower()
        keywords = self.subject_keywords.get(subject, [])
        
        if not keywords:
            return 0.5
        
        matches = 0
        for keyword in keywords:
            if keyword in content_lower:
                matches += 1
        
        return min(matches / len(keywords), 1.0)
    
    def _calculate_content_type_confidence(self, content: str, content_type: str) -> float:
        """Calculate confidence score for content type classification."""
        content_lower = content.lower()
        patterns = self.content_type_patterns.get(content_type, [])
        
        if not patterns:
            return 0.5
        
        matches = 0
        for pattern in patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                matches += 1
        
        return min(matches / len(patterns), 1.0)
    
    def _calculate_difficulty_confidence(self, content: str, difficulty: str) -> float:
        """Calculate confidence score for difficulty classification."""
        content_lower = content.lower()
        indicators = self.difficulty_indicators.get(difficulty, [])
        
        if not indicators:
            return 0.5
        
        matches = 0
        for indicator in indicators:
            if indicator in content_lower:
                matches += 1
        
        return min(matches / len(indicators), 1.0)
    
    def get_categorization_statistics(self, categorizations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about categorizations."""
        if not categorizations:
            return {}
        
        stats = {
            'total_items': len(categorizations),
            'subjects': {},
            'content_types': {},
            'difficulty_levels': {},
            'average_confidence': {
                'subject': 0.0,
                'content_type': 0.0,
                'difficulty': 0.0
            }
        }
        
        total_subject_confidence = 0
        total_type_confidence = 0
        total_difficulty_confidence = 0
        
        for cat in categorizations:
            # Count subjects
            subject = cat.get('subject', 'unknown')
            stats['subjects'][subject] = stats['subjects'].get(subject, 0) + 1
            
            # Count content types
            content_type = cat.get('content_type', 'unknown')
            stats['content_types'][content_type] = stats['content_types'].get(content_type, 0) + 1
            
            # Count difficulty levels
            difficulty = cat.get('difficulty_level', 'unknown')
            stats['difficulty_levels'][difficulty] = stats['difficulty_levels'].get(difficulty, 0) + 1
            
            # Sum confidence scores
            confidence_scores = cat.get('confidence_scores', {})
            total_subject_confidence += confidence_scores.get('subject', 0.0)
            total_type_confidence += confidence_scores.get('content_type', 0.0)
            total_difficulty_confidence += confidence_scores.get('difficulty', 0.0)
        
        # Calculate average confidence scores
        if categorizations:
            stats['average_confidence']['subject'] = total_subject_confidence / len(categorizations)
            stats['average_confidence']['content_type'] = total_type_confidence / len(categorizations)
            stats['average_confidence']['difficulty'] = total_difficulty_confidence / len(categorizations)
        
        return stats 