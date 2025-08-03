"""
Learning Style Assessor for Educational RAG System

Handles learning style identification and accommodation for personalized learning.
"""

import logging
from typing import Dict, Any, List
import random

logger = logging.getLogger(__name__)

class LearningStyleAssessor:
    """
    Assessor for learning styles and preferences.
    
    Features:
    - Learning style identification
    - Preference analysis
    - Accommodation strategies
    - Multi-modal support
    """
    
    def __init__(self):
        # Learning style definitions
        self.learning_styles = {
            'visual': {
                'description': 'Learns best through visual aids, diagrams, and spatial organization',
                'preferences': ['diagrams', 'charts', 'videos', 'images', 'mind maps'],
                'strengths': ['spatial reasoning', 'visual memory', 'pattern recognition'],
                'challenges': ['verbal instructions', 'auditory-only content']
            },
            'auditory': {
                'description': 'Learns best through listening, discussion, and verbal communication',
                'preferences': ['discussions', 'lectures', 'podcasts', 'verbal explanations'],
                'strengths': ['verbal memory', 'listening comprehension', 'oral communication'],
                'challenges': ['visual-only content', 'silent reading']
            },
            'kinesthetic': {
                'description': 'Learns best through hands-on activities, movement, and physical interaction',
                'preferences': ['experiments', 'hands-on activities', 'role-playing', 'physical movement'],
                'strengths': ['physical coordination', 'tactile memory', 'practical application'],
                'challenges': ['passive learning', 'theoretical content']
            },
            'reading_writing': {
                'description': 'Learns best through reading, writing, and text-based activities',
                'preferences': ['reading', 'note-taking', 'writing', 'text-based materials'],
                'strengths': ['text comprehension', 'written expression', 'analytical thinking'],
                'challenges': ['visual content', 'hands-on activities']
            }
        }
        
        # Assessment questions for learning style identification
        self.assessment_questions = [
            {
                'id': 'q1',
                'question': 'When learning something new, I prefer to:',
                'options': {
                    'visual': 'See diagrams, charts, or visual aids',
                    'auditory': 'Listen to explanations or discussions',
                    'kinesthetic': 'Try it out hands-on or through movement',
                    'reading_writing': 'Read about it or take notes'
                }
            },
            {
                'id': 'q2',
                'question': 'I remember information best when:',
                'options': {
                    'visual': 'I can see it in pictures or diagrams',
                    'auditory': 'I hear it explained or discussed',
                    'kinesthetic': 'I physically do it or experience it',
                    'reading_writing': 'I read it or write it down'
                }
            },
            {
                'id': 'q3',
                'question': 'When solving problems, I typically:',
                'options': {
                    'visual': 'Draw diagrams or visualize the solution',
                    'auditory': 'Talk through the problem out loud',
                    'kinesthetic': 'Use physical objects or move around',
                    'reading_writing': 'Write out the steps or make lists'
                }
            },
            {
                'id': 'q4',
                'question': 'I enjoy learning activities that involve:',
                'options': {
                    'visual': 'Watching videos, looking at images, or creating mind maps',
                    'auditory': 'Group discussions, listening to podcasts, or verbal explanations',
                    'kinesthetic': 'Hands-on experiments, role-playing, or physical activities',
                    'reading_writing': 'Reading books, taking notes, or writing essays'
                }
            },
            {
                'id': 'q5',
                'question': 'When studying, I prefer to:',
                'options': {
                    'visual': 'Use color-coded notes, diagrams, or visual organizers',
                    'auditory': 'Discuss topics with others or listen to recorded lectures',
                    'kinesthetic': 'Use flashcards, act out concepts, or take frequent breaks',
                    'reading_writing': 'Read textbooks, write summaries, or create outlines'
                }
            }
        ]
    
    def assess_learning_style(self, student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess learning style based on student profile and preferences.
        
        Args:
            student_profile: Student profile with preferences and history
            
        Returns:
            Learning style assessment with primary and secondary styles
        """
        # Check if student has completed a learning style assessment
        if 'learning_style_assessment' in student_profile:
            return self._analyze_assessment_results(student_profile['learning_style_assessment'])
        
        # Use profile data to infer learning style
        return self._infer_learning_style_from_profile(student_profile)
    
    def _analyze_assessment_results(self, assessment_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze results from a learning style assessment."""
        scores = {
            'visual': 0,
            'auditory': 0,
            'kinesthetic': 0,
            'reading_writing': 0
        }
        
        # Calculate scores from assessment responses
        for question_id, response in assessment_results.items():
            if response in scores:
                scores[response] += 1
        
        # Determine primary and secondary styles
        sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_style = sorted_styles[0][0]
        secondary_style = sorted_styles[1][0] if len(sorted_styles) > 1 else primary_style
        
        # Calculate confidence scores
        total_responses = sum(scores.values())
        primary_confidence = scores[primary_style] / total_responses if total_responses > 0 else 0
        secondary_confidence = scores[secondary_style] / total_responses if total_responses > 0 else 0
        
        return {
            'primary_style': primary_style,
            'secondary_style': secondary_style,
            'scores': scores,
            'primary_confidence': primary_confidence,
            'secondary_confidence': secondary_confidence,
            'style_description': self.learning_styles[primary_style]['description'],
            'preferences': self.learning_styles[primary_style]['preferences'],
            'strengths': self.learning_styles[primary_style]['strengths'],
            'challenges': self.learning_styles[primary_style]['challenges']
        }
    
    def _infer_learning_style_from_profile(self, student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Infer learning style from student profile data."""
        scores = {
            'visual': 0,
            'auditory': 0,
            'kinesthetic': 0,
            'reading_writing': 0
        }
        
        # Analyze content preferences
        content_preferences = student_profile.get('content_preferences', {})
        
        # Visual indicators
        if content_preferences.get('videos', 0) > 0:
            scores['visual'] += content_preferences['videos']
        if content_preferences.get('diagrams', 0) > 0:
            scores['visual'] += content_preferences['diagrams']
        if content_preferences.get('images', 0) > 0:
            scores['visual'] += content_preferences['images']
        
        # Auditory indicators
        if content_preferences.get('podcasts', 0) > 0:
            scores['auditory'] += content_preferences['podcasts']
        if content_preferences.get('discussions', 0) > 0:
            scores['auditory'] += content_preferences['discussions']
        if content_preferences.get('lectures', 0) > 0:
            scores['auditory'] += content_preferences['lectures']
        
        # Kinesthetic indicators
        if content_preferences.get('experiments', 0) > 0:
            scores['kinesthetic'] += content_preferences['experiments']
        if content_preferences.get('hands_on', 0) > 0:
            scores['kinesthetic'] += content_preferences['hands_on']
        if content_preferences.get('interactive', 0) > 0:
            scores['kinesthetic'] += content_preferences['interactive']
        
        # Reading/Writing indicators
        if content_preferences.get('reading', 0) > 0:
            scores['reading_writing'] += content_preferences['reading']
        if content_preferences.get('note_taking', 0) > 0:
            scores['reading_writing'] += content_preferences['note_taking']
        if content_preferences.get('writing', 0) > 0:
            scores['reading_writing'] += content_preferences['writing']
        
        # Analyze learning behavior
        learning_behavior = student_profile.get('learning_behavior', {})
        
        # Time spent on different activities
        if learning_behavior.get('time_on_videos', 0) > learning_behavior.get('time_on_text', 0):
            scores['visual'] += 1
        if learning_behavior.get('time_on_audio', 0) > learning_behavior.get('time_on_text', 0):
            scores['auditory'] += 1
        if learning_behavior.get('time_on_interactive', 0) > learning_behavior.get('time_on_text', 0):
            scores['kinesthetic'] += 1
        if learning_behavior.get('time_on_text', 0) > 0:
            scores['reading_writing'] += 1
        
        # Performance patterns
        performance_patterns = student_profile.get('performance_patterns', {})
        
        if performance_patterns.get('visual_tasks', 0) > performance_patterns.get('text_tasks', 0):
            scores['visual'] += 1
        if performance_patterns.get('audio_tasks', 0) > performance_patterns.get('text_tasks', 0):
            scores['auditory'] += 1
        if performance_patterns.get('hands_on_tasks', 0) > performance_patterns.get('text_tasks', 0):
            scores['kinesthetic'] += 1
        if performance_patterns.get('text_tasks', 0) > 0:
            scores['reading_writing'] += 1
        
        # If no clear indicators, use default
        if sum(scores.values()) == 0:
            scores['visual'] = 1  # Default to visual
        
        # Determine primary and secondary styles
        sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_style = sorted_styles[0][0]
        secondary_style = sorted_styles[1][0] if len(sorted_styles) > 1 else primary_style
        
        return {
            'primary_style': primary_style,
            'secondary_style': secondary_style,
            'scores': scores,
            'primary_confidence': 0.6,  # Lower confidence for inferred styles
            'secondary_confidence': 0.4,
            'style_description': self.learning_styles[primary_style]['description'],
            'preferences': self.learning_styles[primary_style]['preferences'],
            'strengths': self.learning_styles[primary_style]['strengths'],
            'challenges': self.learning_styles[primary_style]['challenges'],
            'inferred': True
        }
    
    def get_accommodation_strategies(self, learning_style: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Get accommodation strategies for a learning style.
        
        Args:
            learning_style: Learning style assessment results
            
        Returns:
            Dictionary of accommodation strategies
        """
        primary_style = learning_style['primary_style']
        secondary_style = learning_style.get('secondary_style', primary_style)
        
        strategies = {
            'content_presentation': self._get_content_presentation_strategies(primary_style),
            'interaction_methods': self._get_interaction_strategies(primary_style),
            'assessment_approaches': self._get_assessment_strategies(primary_style),
            'study_techniques': self._get_study_techniques(primary_style),
            'multi_modal_support': self._get_multi_modal_strategies(primary_style, secondary_style)
        }
        
        return strategies
    
    def _get_content_presentation_strategies(self, style: str) -> List[str]:
        """Get content presentation strategies for a learning style."""
        strategies = {
            'visual': [
                'Use diagrams, charts, and infographics',
                'Include relevant images and visual aids',
                'Create mind maps and concept maps',
                'Use color coding for organization',
                'Provide visual summaries and flowcharts'
            ],
            'auditory': [
                'Include audio explanations and podcasts',
                'Provide verbal instructions and discussions',
                'Use group discussions and peer teaching',
                'Include audio feedback and explanations',
                'Provide verbal summaries and key points'
            ],
            'kinesthetic': [
                'Include hands-on activities and experiments',
                'Provide interactive simulations and games',
                'Use role-playing and physical demonstrations',
                'Include movement-based learning activities',
                'Provide tactile learning materials'
            ],
            'reading_writing': [
                'Provide comprehensive text-based materials',
                'Include note-taking opportunities',
                'Use written summaries and key points',
                'Provide reading guides and outlines',
                'Include writing assignments and reflections'
            ]
        }
        
        return strategies.get(style, strategies['visual'])
    
    def _get_interaction_strategies(self, style: str) -> List[str]:
        """Get interaction strategies for a learning style."""
        strategies = {
            'visual': [
                'Visual feedback and progress indicators',
                'Interactive diagrams and charts',
                'Visual quizzes and assessments',
                'Screen sharing and visual demonstrations'
            ],
            'auditory': [
                'Verbal feedback and discussions',
                'Audio-based interactions',
                'Group discussions and debates',
                'Voice-based navigation and commands'
            ],
            'kinesthetic': [
                'Hands-on interactive activities',
                'Physical movement and gestures',
                'Touch-based interactions',
                'Real-time feedback and adjustments'
            ],
            'reading_writing': [
                'Text-based interactions and responses',
                'Written feedback and comments',
                'Text-based quizzes and assessments',
                'Written discussions and forums'
            ]
        }
        
        return strategies.get(style, strategies['visual'])
    
    def _get_assessment_strategies(self, style: str) -> List[str]:
        """Get assessment strategies for a learning style."""
        strategies = {
            'visual': [
                'Visual quizzes with diagrams and charts',
                'Image-based assessments',
                'Visual problem-solving tasks',
                'Diagram creation and analysis'
            ],
            'auditory': [
                'Oral presentations and discussions',
                'Audio-based assessments',
                'Verbal problem-solving tasks',
                'Group discussion assessments'
            ],
            'kinesthetic': [
                'Hands-on practical assessments',
                'Physical demonstrations and tasks',
                'Interactive simulations and games',
                'Real-world application projects'
            ],
            'reading_writing': [
                'Written essays and reports',
                'Text-based quizzes and tests',
                'Written problem-solving tasks',
                'Research and writing assignments'
            ]
        }
        
        return strategies.get(style, strategies['visual'])
    
    def _get_study_techniques(self, style: str) -> List[str]:
        """Get study techniques for a learning style."""
        techniques = {
            'visual': [
                'Create visual study guides and mind maps',
                'Use color-coded notes and highlighters',
                'Watch educational videos and documentaries',
                'Create diagrams and flowcharts',
                'Use visual mnemonics and memory aids'
            ],
            'auditory': [
                'Read aloud and discuss with others',
                'Listen to educational podcasts and lectures',
                'Participate in study groups and discussions',
                'Use verbal mnemonics and rhymes',
                'Record and listen to your own explanations'
            ],
            'kinesthetic': [
                'Use flashcards and physical study aids',
                'Act out concepts and scenarios',
                'Take frequent breaks and move around',
                'Use hands-on study materials',
                'Apply concepts through real-world practice'
            ],
            'reading_writing': [
                'Take detailed notes and summaries',
                'Write out key concepts and definitions',
                'Create written study guides and outlines',
                'Practice through writing exercises',
                'Use text-based mnemonics and lists'
            ]
        }
        
        return techniques.get(style, techniques['visual'])
    
    def _get_multi_modal_strategies(self, primary_style: str, secondary_style: str) -> List[str]:
        """Get multi-modal strategies combining primary and secondary styles."""
        strategies = []
        
        # Combine strategies from both styles
        primary_strategies = self._get_content_presentation_strategies(primary_style)
        secondary_strategies = self._get_content_presentation_strategies(secondary_style)
        
        # Select top strategies from each
        strategies.extend(primary_strategies[:2])
        strategies.extend(secondary_strategies[:1])
        
        # Add multi-modal specific strategies
        strategies.extend([
            'Provide content in multiple formats simultaneously',
            'Allow students to choose their preferred format',
            'Use progressive disclosure (start with preferred, add others)',
            'Create hybrid activities that engage multiple styles'
        ])
        
        return strategies
    
    def get_assessment_questions(self) -> List[Dict[str, Any]]:
        """Get learning style assessment questions."""
        return self.assessment_questions
    
    def generate_random_assessment(self) -> Dict[str, str]:
        """Generate random assessment responses for testing."""
        responses = {}
        for question in self.assessment_questions:
            question_id = question['id']
            options = list(question['options'].keys())
            responses[question_id] = random.choice(options)
        return responses 