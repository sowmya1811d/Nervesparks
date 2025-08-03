"""
Learning Path Planner for Educational RAG System

Handles planning of learning objectives based on available content and student profiles.
"""

import logging
from typing import List, Dict, Any, Optional
import random
from ..vector_store.store import VectorStore
from .generator import LearningObjective

logger = logging.getLogger(__name__)

class LearningPathPlanner:
    """
    Planner for learning objectives and content sequencing.
    
    Features:
    - Content-based objective planning
    - Prerequisite analysis
    - Difficulty progression
    - Learning style accommodation
    - Duration optimization
    """
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        
        # Planning parameters
        self.min_objectives_per_path = 3
        self.max_objectives_per_path = 10
        self.min_duration_per_objective = 15  # minutes
        self.max_duration_per_objective = 60  # minutes
    
    def plan_objectives(self,
                       available_content: List[Dict[str, Any]],
                       student_profile: Dict[str, Any],
                       learning_style: Dict[str, Any],
                       path_level: str,
                       target_duration: Optional[int] = None) -> List[LearningObjective]:
        """
        Plan learning objectives based on available content and student profile.
        
        Args:
            available_content: Available content from vector store
            student_profile: Student profile and preferences
            learning_style: Learning style assessment
            path_level: Target path level
            target_duration: Target duration in minutes
            
        Returns:
            List of planned learning objectives
        """
        # Group content by subject and difficulty
        content_groups = self._group_content_by_subject_and_difficulty(available_content)
        
        # Determine number of objectives based on path level and target duration
        n_objectives = self._determine_objective_count(path_level, target_duration)
        
        # Plan objectives for each subject
        all_objectives = []
        
        for subject, difficulty_groups in content_groups.items():
            subject_objectives = self._plan_subject_objectives(
                subject=subject,
                difficulty_groups=difficulty_groups,
                student_profile=student_profile,
                learning_style=learning_style,
                path_level=path_level,
                n_objectives=n_objectives // len(content_groups)  # Distribute objectives across subjects
            )
            all_objectives.extend(subject_objectives)
        
        # If we don't have enough objectives, add more from available subjects
        if len(all_objectives) < n_objectives:
            additional_objectives = self._add_additional_objectives(
                available_content=available_content,
                existing_objectives=all_objectives,
                target_count=n_objectives,
                student_profile=student_profile,
                learning_style=learning_style
            )
            all_objectives.extend(additional_objectives)
        
        # Sort objectives by difficulty and prerequisites
        sorted_objectives = self._sort_objectives_by_difficulty_and_prerequisites(all_objectives)
        
        return sorted_objectives[:n_objectives]
    
    def _group_content_by_subject_and_difficulty(self, 
                                                content: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Group content by subject and difficulty level."""
        groups = {}
        
        for item in content:
            subject = item['metadata'].get('subject', 'general')
            difficulty = item['metadata'].get('difficulty_level', 'intermediate')
            
            if subject not in groups:
                groups[subject] = {}
            
            if difficulty not in groups[subject]:
                groups[subject][difficulty] = []
            
            groups[subject][difficulty].append(item)
        
        return groups
    
    def _determine_objective_count(self, path_level: str, target_duration: Optional[int]) -> int:
        """Determine the number of objectives based on path level and target duration."""
        base_counts = {
            'beginner': 4,
            'intermediate': 6,
            'advanced': 8
        }
        
        base_count = base_counts.get(path_level, 6)
        
        if target_duration:
            # Estimate based on target duration
            avg_duration_per_objective = 30  # minutes
            estimated_count = max(3, target_duration // avg_duration_per_objective)
            return min(estimated_count, self.max_objectives_per_path)
        
        return min(base_count, self.max_objectives_per_path)
    
    def _plan_subject_objectives(self,
                                subject: str,
                                difficulty_groups: Dict[str, List[Dict[str, Any]]],
                                student_profile: Dict[str, Any],
                                learning_style: Dict[str, Any],
                                path_level: str,
                                n_objectives: int) -> List[LearningObjective]:
        """Plan objectives for a specific subject."""
        objectives = []
        
        # Determine difficulty progression for this subject
        difficulty_progression = self._get_difficulty_progression(path_level)
        
        for difficulty in difficulty_progression:
            if difficulty in difficulty_groups and len(objectives) < n_objectives:
                # Select content for this difficulty level
                content_for_difficulty = difficulty_groups[difficulty]
                
                # Filter content based on learning style
                filtered_content = self._filter_content_by_learning_style(
                    content_for_difficulty, learning_style
                )
                
                if filtered_content:
                    # Create objectives from filtered content
                    difficulty_objectives = self._create_objectives_from_content(
                        content=filtered_content,
                        subject=subject,
                        difficulty=difficulty,
                        student_profile=student_profile,
                        max_objectives=n_objectives - len(objectives)
                    )
                    objectives.extend(difficulty_objectives)
        
        return objectives
    
    def _get_difficulty_progression(self, path_level: str) -> List[str]:
        """Get difficulty progression based on path level."""
        progressions = {
            'beginner': ['beginner', 'beginner', 'intermediate'],
            'intermediate': ['intermediate', 'intermediate', 'advanced'],
            'advanced': ['advanced', 'advanced', 'expert']
        }
        return progressions.get(path_level, ['intermediate', 'advanced'])
    
    def _filter_content_by_learning_style(self, 
                                         content: List[Dict[str, Any]], 
                                         learning_style: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter content based on learning style preferences."""
        primary_style = learning_style.get('primary_style', 'visual')
        
        # Content type preferences by learning style
        style_preferences = {
            'visual': ['lesson', 'tutorial', 'concept'],
            'auditory': ['lesson', 'tutorial'],
            'kinesthetic': ['exercise', 'tutorial', 'assessment']
        }
        
        preferred_types = style_preferences.get(primary_style, ['lesson', 'tutorial'])
        
        # Filter content by preferred types
        filtered_content = []
        for item in content:
            content_type = item['metadata'].get('content_type', 'lesson')
            if content_type in preferred_types:
                filtered_content.append(item)
        
        # If no preferred content found, return all content
        if not filtered_content:
            return content
        
        return filtered_content
    
    def _create_objectives_from_content(self,
                                       content: List[Dict[str, Any]],
                                       subject: str,
                                       difficulty: str,
                                       student_profile: Dict[str, Any],
                                       max_objectives: int) -> List[LearningObjective]:
        """Create learning objectives from content."""
        objectives = []
        
        # Shuffle content to add variety
        random.shuffle(content)
        
        for i, item in enumerate(content[:max_objectives]):
            # Extract content information
            content_text = item['content']
            metadata = item['metadata']
            
            # Create objective title and description
            title = self._generate_objective_title(subject, difficulty, i + 1)
            description = self._extract_description_from_content(content_text)
            
            # Estimate duration based on content length and difficulty
            estimated_duration = self._estimate_objective_duration(content_text, difficulty)
            
            # Create objective
            objective = LearningObjective(
                id=f"obj_{subject}_{difficulty}_{i}",
                title=title,
                description=description,
                subject=subject,
                difficulty_level=difficulty,
                prerequisites=[],  # Could be enhanced with prerequisite analysis
                estimated_duration=estimated_duration,
                content_ids=[item['id']]
            )
            
            objectives.append(objective)
        
        return objectives
    
    def _generate_objective_title(self, subject: str, difficulty: str, index: int) -> str:
        """Generate a title for a learning objective."""
        subject_names = {
            'mathematics': 'Mathematics',
            'physics': 'Physics',
            'chemistry': 'Chemistry',
            'biology': 'Biology',
            'computer_science': 'Computer Science',
            'history': 'History',
            'literature': 'Literature',
            'economics': 'Economics'
        }
        
        difficulty_names = {
            'beginner': 'Fundamentals',
            'intermediate': 'Intermediate Concepts',
            'advanced': 'Advanced Topics',
            'expert': 'Expert Level'
        }
        
        subject_name = subject_names.get(subject, subject.title())
        difficulty_name = difficulty_names.get(difficulty, difficulty.title())
        
        return f"{subject_name} - {difficulty_name} (Part {index})"
    
    def _extract_description_from_content(self, content: str) -> str:
        """Extract a description from content."""
        # Simple extraction - take first few sentences
        sentences = content.split('.')
        if len(sentences) > 2:
            description = '. '.join(sentences[:2]) + '.'
        else:
            description = content[:200] + '...' if len(content) > 200 else content
        
        return description.strip()
    
    def _estimate_objective_duration(self, content: str, difficulty: str) -> int:
        """Estimate duration for an objective based on content and difficulty."""
        # Base duration on content length
        word_count = len(content.split())
        base_duration = max(15, word_count // 50)  # Rough estimate: 50 words per minute
        
        # Adjust for difficulty
        difficulty_multipliers = {
            'beginner': 0.8,
            'intermediate': 1.0,
            'advanced': 1.3,
            'expert': 1.5
        }
        
        multiplier = difficulty_multipliers.get(difficulty, 1.0)
        estimated_duration = int(base_duration * multiplier)
        
        # Ensure within bounds
        return max(self.min_duration_per_objective, 
                  min(estimated_duration, self.max_duration_per_objective))
    
    def _add_additional_objectives(self,
                                  available_content: List[Dict[str, Any]],
                                  existing_objectives: List[LearningObjective],
                                  target_count: int,
                                  student_profile: Dict[str, Any],
                                  learning_style: Dict[str, Any]) -> List[LearningObjective]:
        """Add additional objectives to reach target count."""
        additional_objectives = []
        
        # Get subjects not yet covered
        covered_subjects = {obj.subject for obj in existing_objectives}
        all_subjects = set(item['metadata'].get('subject', 'general') for item in available_content)
        uncovered_subjects = all_subjects - covered_subjects
        
        # Create objectives for uncovered subjects
        for subject in uncovered_subjects:
            if len(existing_objectives) + len(additional_objectives) >= target_count:
                break
            
            subject_content = [item for item in available_content 
                             if item['metadata'].get('subject') == subject]
            
            if subject_content:
                # Create a simple objective for this subject
                content_item = random.choice(subject_content)
                
                objective = LearningObjective(
                    id=f"obj_{subject}_additional_{len(additional_objectives)}",
                    title=f"{subject.title()} - Introduction",
                    description=self._extract_description_from_content(content_item['content']),
                    subject=subject,
                    difficulty_level='beginner',
                    prerequisites=[],
                    estimated_duration=30,
                    content_ids=[content_item['id']]
                )
                
                additional_objectives.append(objective)
        
        return additional_objectives
    
    def _sort_objectives_by_difficulty_and_prerequisites(self, 
                                                        objectives: List[LearningObjective]) -> List[LearningObjective]:
        """Sort objectives by difficulty level and prerequisites."""
        # Define difficulty order
        difficulty_order = ['beginner', 'intermediate', 'advanced', 'expert']
        
        # Sort by difficulty first
        def difficulty_key(obj):
            try:
                return difficulty_order.index(obj.difficulty_level)
            except ValueError:
                return len(difficulty_order)  # Unknown difficulties go last
        
        sorted_objectives = sorted(objectives, key=difficulty_key)
        
        return sorted_objectives
    
    def validate_learning_path(self, objectives: List[LearningObjective]) -> Dict[str, Any]:
        """Validate a learning path for coherence and completeness."""
        validation = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'total_duration': 0,
            'subjects_covered': set(),
            'difficulty_levels': set()
        }
        
        if not objectives:
            validation['is_valid'] = False
            validation['issues'].append("No objectives defined")
            return validation
        
        # Check each objective
        for i, objective in enumerate(objectives):
            # Check duration
            if objective.estimated_duration < self.min_duration_per_objective:
                validation['warnings'].append(
                    f"Objective {i+1} duration ({objective.estimated_duration} min) is below minimum"
                )
            
            if objective.estimated_duration > self.max_duration_per_objective:
                validation['warnings'].append(
                    f"Objective {i+1} duration ({objective.estimated_duration} min) is above maximum"
                )
            
            # Track statistics
            validation['total_duration'] += objective.estimated_duration
            validation['subjects_covered'].add(objective.subject)
            validation['difficulty_levels'].add(objective.difficulty_level)
        
        # Check overall path
        if validation['total_duration'] < 30:
            validation['warnings'].append("Total duration is very short")
        
        if len(validation['subjects_covered']) == 1:
            validation['warnings'].append("Path covers only one subject")
        
        if len(objectives) < self.min_objectives_per_path:
            validation['issues'].append(f"Too few objectives ({len(objectives)})")
            validation['is_valid'] = False
        
        if len(objectives) > self.max_objectives_per_path:
            validation['warnings'].append(f"Many objectives ({len(objectives)})")
        
        return validation 