"""
Learning Path Generator for Educational RAG System

Handles personalized learning path generation based on student profiles and progress.
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

from .planner import LearningPathPlanner
from .assessor import LearningStyleAssessor
from ..vector_store.store import VectorStore

logger = logging.getLogger(__name__)

@dataclass
class LearningObjective:
    """Represents a learning objective."""
    id: str
    title: str
    description: str
    subject: str
    difficulty_level: str
    prerequisites: List[str]
    estimated_duration: int  # in minutes
    content_ids: List[str]

@dataclass
class LearningPath:
    """Represents a personalized learning path."""
    student_id: str
    path_id: str
    title: str
    description: str
    objectives: List[LearningObjective]
    estimated_total_duration: int
    difficulty_progression: List[str]
    subjects: List[str]
    created_at: datetime
    updated_at: datetime
    status: str  # 'active', 'completed', 'paused'

class LearningPathGenerator:
    """
    Generator for personalized learning paths.
    
    Features:
    - Student profile analysis
    - Learning style accommodation
    - Competency-based sequencing
    - Adaptive difficulty adjustment
    - Progress tracking integration
    """
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.planner = LearningPathPlanner(vector_store)
        self.assessor = LearningStyleAssessor()
        
        # Learning path templates
        self.path_templates = {
            'beginner': {
                'duration_range': (30, 90),
                'objectives_per_path': (3, 6),
                'difficulty_progression': ['beginner', 'beginner', 'intermediate']
            },
            'intermediate': {
                'duration_range': (60, 180),
                'objectives_per_path': (4, 8),
                'difficulty_progression': ['intermediate', 'intermediate', 'advanced']
            },
            'advanced': {
                'duration_range': (120, 300),
                'objectives_per_path': (5, 10),
                'difficulty_progression': ['advanced', 'advanced', 'expert']
            }
        }
    
    def generate_learning_path(self, 
                              student_profile: Dict[str, Any],
                              subjects: List[str],
                              target_duration: Optional[int] = None) -> LearningPath:
        """
        Generate a personalized learning path for a student.
        
        Args:
            student_profile: Student profile with preferences and progress
            subjects: List of subjects to include in the path
            target_duration: Target duration in minutes (optional)
            
        Returns:
            Personalized learning path
        """
        # Assess learning style
        learning_style = self.assessor.assess_learning_style(student_profile)
        
        # Determine path level based on student profile
        path_level = self._determine_path_level(student_profile)
        
        # Get available content for subjects
        available_content = self._get_available_content(subjects, student_profile)
        
        # Plan learning objectives
        objectives = self.planner.plan_objectives(
            available_content=available_content,
            student_profile=student_profile,
            learning_style=learning_style,
            path_level=path_level,
            target_duration=target_duration
        )
        
        # Create learning path
        path = self._create_learning_path(
            student_id=student_profile['student_id'],
            objectives=objectives,
            learning_style=learning_style,
            path_level=path_level
        )
        
        logger.info(f"Generated learning path for student {student_profile['student_id']}")
        return path
    
    def _determine_path_level(self, student_profile: Dict[str, Any]) -> str:
        """Determine the appropriate path level for the student."""
        # Consider multiple factors
        factors = {
            'beginner': 0,
            'intermediate': 0,
            'advanced': 0
        }
        
        # Factor 1: Current skill level
        current_level = student_profile.get('current_level', 'beginner')
        factors[current_level] += 2
        
        # Factor 2: Previous performance
        avg_performance = student_profile.get('average_performance', 0.5)
        if avg_performance > 0.8:
            factors['advanced'] += 1
        elif avg_performance > 0.6:
            factors['intermediate'] += 1
        else:
            factors['beginner'] += 1
        
        # Factor 3: Learning pace
        learning_pace = student_profile.get('learning_pace', 'normal')
        if learning_pace == 'fast':
            factors['advanced'] += 1
        elif learning_pace == 'slow':
            factors['beginner'] += 1
        
        # Factor 4: Time availability
        time_availability = student_profile.get('time_availability', 'medium')
        if time_availability == 'high':
            factors['advanced'] += 1
        elif time_availability == 'low':
            factors['beginner'] += 1
        
        # Return the level with highest score
        return max(factors, key=factors.get)
    
    def _get_available_content(self, 
                              subjects: List[str], 
                              student_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get available content for the specified subjects."""
        available_content = []
        
        for subject in subjects:
            # Get content by subject and difficulty level
            filters = {
                'subject': subject,
                'difficulty_level': {'$in': ['beginner', 'intermediate', 'advanced']}
            }
            
            content = self.vector_store.get_by_metadata(filters, n_results=100)
            available_content.extend(content)
        
        # Filter out content the student has already completed
        completed_content = student_profile.get('completed_content', [])
        available_content = [
            content for content in available_content 
            if content['id'] not in completed_content
        ]
        
        return available_content
    
    def _create_learning_path(self,
                             student_id: str,
                             objectives: List[LearningObjective],
                             learning_style: Dict[str, Any],
                             path_level: str) -> LearningPath:
        """Create a learning path from planned objectives."""
        # Calculate total duration
        total_duration = sum(obj.estimated_duration for obj in objectives)
        
        # Determine difficulty progression
        difficulty_progression = self.path_templates[path_level]['difficulty_progression']
        
        # Get unique subjects
        subjects = list(set(obj.subject for obj in objectives))
        
        # Create path ID
        path_id = f"path_{student_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create path title and description
        title = f"Personalized Learning Path - {', '.join(subjects)}"
        description = f"Custom learning path designed for {learning_style['primary_style']} learners"
        
        return LearningPath(
            student_id=student_id,
            path_id=path_id,
            title=title,
            description=description,
            objectives=objectives,
            estimated_total_duration=total_duration,
            difficulty_progression=difficulty_progression,
            subjects=subjects,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status='active'
        )
    
    def adapt_learning_path(self, 
                           learning_path: LearningPath,
                           student_progress: Dict[str, Any]) -> LearningPath:
        """
        Adapt a learning path based on student progress.
        
        Args:
            learning_path: Current learning path
            student_progress: Student progress data
            
        Returns:
            Adapted learning path
        """
        # Analyze progress
        progress_analysis = self._analyze_progress(student_progress)
        
        # Determine if adaptation is needed
        if progress_analysis['needs_adaptation']:
            # Get updated content
            available_content = self._get_available_content(
                learning_path.subjects,
                {'student_id': learning_path.student_id, 'completed_content': student_progress.get('completed_content', [])}
            )
            
            # Re-plan objectives
            student_profile = {
                'student_id': learning_path.student_id,
                'current_level': progress_analysis['current_level'],
                'learning_pace': progress_analysis['learning_pace'],
                'time_availability': progress_analysis['time_availability']
            }
            
            learning_style = self.assessor.assess_learning_style(student_profile)
            
            new_objectives = self.planner.plan_objectives(
                available_content=available_content,
                student_profile=student_profile,
                learning_style=learning_style,
                path_level=progress_analysis['path_level'],
                target_duration=learning_path.estimated_total_duration
            )
            
            # Update learning path
            learning_path.objectives = new_objectives
            learning_path.estimated_total_duration = sum(obj.estimated_duration for obj in new_objectives)
            learning_path.updated_at = datetime.now()
            
            logger.info(f"Adapted learning path {learning_path.path_id}")
        
        return learning_path
    
    def _analyze_progress(self, student_progress: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze student progress to determine adaptation needs."""
        analysis = {
            'needs_adaptation': False,
            'current_level': 'intermediate',
            'learning_pace': 'normal',
            'time_availability': 'medium',
            'path_level': 'intermediate'
        }
        
        # Analyze completion rate
        completion_rate = student_progress.get('completion_rate', 0.5)
        if completion_rate < 0.3:
            analysis['needs_adaptation'] = True
            analysis['current_level'] = 'beginner'
            analysis['learning_pace'] = 'slow'
        elif completion_rate > 0.8:
            analysis['needs_adaptation'] = True
            analysis['current_level'] = 'advanced'
            analysis['learning_pace'] = 'fast'
        
        # Analyze performance
        avg_performance = student_progress.get('average_performance', 0.5)
        if avg_performance < 0.4:
            analysis['needs_adaptation'] = True
            analysis['current_level'] = 'beginner'
        elif avg_performance > 0.8:
            analysis['needs_adaptation'] = True
            analysis['current_level'] = 'advanced'
        
        # Determine path level
        if analysis['current_level'] == 'beginner':
            analysis['path_level'] = 'beginner'
        elif analysis['current_level'] == 'advanced':
            analysis['path_level'] = 'advanced'
        else:
            analysis['path_level'] = 'intermediate'
        
        return analysis
    
    def get_learning_path_recommendations(self, 
                                        student_profile: Dict[str, Any],
                                        n_recommendations: int = 3) -> List[Dict[str, Any]]:
        """
        Get learning path recommendations for a student.
        
        Args:
            student_profile: Student profile
            n_recommendations: Number of recommendations to generate
            
        Returns:
            List of learning path recommendations
        """
        recommendations = []
        
        # Get available subjects
        available_subjects = self._get_available_subjects()
        
        # Generate different path combinations
        for i in range(n_recommendations):
            # Select random subjects
            import random
            selected_subjects = random.sample(available_subjects, min(3, len(available_subjects)))
            
            # Generate path
            try:
                path = self.generate_learning_path(
                    student_profile=student_profile,
                    subjects=selected_subjects
                )
                
                recommendation = {
                    'path_id': path.path_id,
                    'title': path.title,
                    'description': path.description,
                    'subjects': path.subjects,
                    'estimated_duration': path.estimated_total_duration,
                    'difficulty_level': path.difficulty_progression[0],
                    'objectives_count': len(path.objectives)
                }
                
                recommendations.append(recommendation)
                
            except Exception as e:
                logger.error(f"Error generating recommendation {i}: {e}")
                continue
        
        return recommendations
    
    def _get_available_subjects(self) -> List[str]:
        """Get list of available subjects from vector store."""
        try:
            stats = self.vector_store.get_statistics()
            return list(stats.get('subjects', {}).keys())
        except Exception as e:
            logger.error(f"Error getting available subjects: {e}")
            return ['mathematics', 'science', 'computer_science', 'literature']
    
    def save_learning_path(self, learning_path: LearningPath, file_path: str):
        """Save learning path to file."""
        try:
            path_data = {
                'student_id': learning_path.student_id,
                'path_id': learning_path.path_id,
                'title': learning_path.title,
                'description': learning_path.description,
                'objectives': [
                    {
                        'id': obj.id,
                        'title': obj.title,
                        'description': obj.description,
                        'subject': obj.subject,
                        'difficulty_level': obj.difficulty_level,
                        'prerequisites': obj.prerequisites,
                        'estimated_duration': obj.estimated_duration,
                        'content_ids': obj.content_ids
                    }
                    for obj in learning_path.objectives
                ],
                'estimated_total_duration': learning_path.estimated_total_duration,
                'difficulty_progression': learning_path.difficulty_progression,
                'subjects': learning_path.subjects,
                'created_at': learning_path.created_at.isoformat(),
                'updated_at': learning_path.updated_at.isoformat(),
                'status': learning_path.status
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(path_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved learning path to {file_path}")
            
        except Exception as e:
            logger.error(f"Error saving learning path: {e}")
    
    def load_learning_path(self, file_path: str) -> LearningPath:
        """Load learning path from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                path_data = json.load(f)
            
            # Reconstruct objectives
            objectives = []
            for obj_data in path_data['objectives']:
                objective = LearningObjective(
                    id=obj_data['id'],
                    title=obj_data['title'],
                    description=obj_data['description'],
                    subject=obj_data['subject'],
                    difficulty_level=obj_data['difficulty_level'],
                    prerequisites=obj_data['prerequisites'],
                    estimated_duration=obj_data['estimated_duration'],
                    content_ids=obj_data['content_ids']
                )
                objectives.append(objective)
            
            # Reconstruct learning path
            learning_path = LearningPath(
                student_id=path_data['student_id'],
                path_id=path_data['path_id'],
                title=path_data['title'],
                description=path_data['description'],
                objectives=objectives,
                estimated_total_duration=path_data['estimated_total_duration'],
                difficulty_progression=path_data['difficulty_progression'],
                subjects=path_data['subjects'],
                created_at=datetime.fromisoformat(path_data['created_at']),
                updated_at=datetime.fromisoformat(path_data['updated_at']),
                status=path_data['status']
            )
            
            logger.info(f"Loaded learning path from {file_path}")
            return learning_path
            
        except Exception as e:
            logger.error(f"Error loading learning path: {e}")
            raise 