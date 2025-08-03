"""
Student Manager for Educational RAG System

Handles student profiles, progress tracking, and learning path management.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from ..learning_path.generator import LearningPath

logger = logging.getLogger(__name__)

class StudentManager:
    """
    Manager for student data and learning paths.
    
    Features:
    - Student profile management
    - Progress tracking
    - Learning path storage
    - Activity monitoring
    """
    
    def __init__(self, data_dir: str = "data/student_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.students_file = self.data_dir / "students.json"
        self.paths_file = self.data_dir / "learning_paths.json"
        self.progress_file = self.data_dir / "progress.json"
        self.activity_file = self.data_dir / "activity.json"
        
        # Initialize data files
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Initialize data files if they don't exist."""
        files_to_init = [
            (self.students_file, []),
            (self.paths_file, []),
            (self.progress_file, {}),
            (self.activity_file, [])
        ]
        
        for file_path, default_data in files_to_init:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, indent=2, ensure_ascii=False)
    
    def add_student(self, student_data: Dict[str, Any]) -> bool:
        """
        Add a new student to the system.
        
        Args:
            student_data: Student information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            students = self._load_students()
            
            # Check if student already exists
            if any(s.get('student_id') == student_data['student_id'] for s in students):
                logger.warning(f"Student {student_data['student_id']} already exists")
                return False
            
            # Add creation timestamp
            student_data['created_at'] = datetime.now().isoformat()
            student_data['updated_at'] = datetime.now().isoformat()
            
            students.append(student_data)
            self._save_students(students)
            
            logger.info(f"Added student: {student_data['student_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding student: {e}")
            return False
    
    def get_student(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        Get student by ID.
        
        Args:
            student_id: Student ID
            
        Returns:
            Student data or None if not found
        """
        try:
            students = self._load_students()
            for student in students:
                if student.get('student_id') == student_id:
                    return student
            return None
            
        except Exception as e:
            logger.error(f"Error getting student: {e}")
            return None
    
    def get_all_students(self) -> List[Dict[str, Any]]:
        """
        Get all students.
        
        Returns:
            List of all students
        """
        try:
            return self._load_students()
        except Exception as e:
            logger.error(f"Error getting all students: {e}")
            return []
    
    def update_student(self, student_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update student information.
        
        Args:
            student_id: Student ID
            updates: Updated information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            students = self._load_students()
            
            for student in students:
                if student.get('student_id') == student_id:
                    student.update(updates)
                    student['updated_at'] = datetime.now().isoformat()
                    self._save_students(students)
                    
                    logger.info(f"Updated student: {student_id}")
                    return True
            
            logger.warning(f"Student {student_id} not found")
            return False
            
        except Exception as e:
            logger.error(f"Error updating student: {e}")
            return False
    
    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student.
        
        Args:
            student_id: Student ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            students = self._load_students()
            students = [s for s in students if s.get('student_id') != student_id]
            self._save_students(students)
            
            # Also remove associated learning paths and progress
            self._remove_student_data(student_id)
            
            logger.info(f"Deleted student: {student_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting student: {e}")
            return False
    
    def add_learning_path(self, learning_path: LearningPath) -> bool:
        """
        Add a learning path for a student.
        
        Args:
            learning_path: Learning path object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            paths = self._load_learning_paths()
            
            # Convert learning path to dictionary
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
            
            paths.append(path_data)
            self._save_learning_paths(paths)
            
            logger.info(f"Added learning path: {learning_path.path_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding learning path: {e}")
            return False
    
    def get_learning_paths(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get learning paths for a student.
        
        Args:
            student_id: Student ID
            
        Returns:
            List of learning paths
        """
        try:
            paths = self._load_learning_paths()
            return [p for p in paths if p.get('student_id') == student_id]
        except Exception as e:
            logger.error(f"Error getting learning paths: {e}")
            return []
    
    def get_all_learning_paths(self) -> List[LearningPath]:
        """
        Get all learning paths.
        
        Returns:
            List of learning path objects
        """
        try:
            paths_data = self._load_learning_paths()
            learning_paths = []
            
            for path_data in paths_data:
                # Reconstruct objectives
                objectives = []
                for obj_data in path_data['objectives']:
                    from ..learning_path.generator import LearningObjective
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
                learning_paths.append(learning_path)
            
            return learning_paths
            
        except Exception as e:
            logger.error(f"Error getting all learning paths: {e}")
            return []
    
    def update_learning_path_status(self, path_id: str, status: str) -> bool:
        """
        Update learning path status.
        
        Args:
            path_id: Learning path ID
            status: New status
            
        Returns:
            True if successful, False otherwise
        """
        try:
            paths = self._load_learning_paths()
            
            for path in paths:
                if path.get('path_id') == path_id:
                    path['status'] = status
                    path['updated_at'] = datetime.now().isoformat()
                    self._save_learning_paths(paths)
                    
                    logger.info(f"Updated learning path status: {path_id} -> {status}")
                    return True
            
            logger.warning(f"Learning path {path_id} not found")
            return False
            
        except Exception as e:
            logger.error(f"Error updating learning path status: {e}")
            return False
    
    def update_progress(self, student_id: str, progress_data: Dict[str, Any]) -> bool:
        """
        Update student progress.
        
        Args:
            student_id: Student ID
            progress_data: Progress information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            progress = self._load_progress()
            
            if student_id not in progress:
                progress[student_id] = {}
            
            progress[student_id].update(progress_data)
            progress[student_id]['last_updated'] = datetime.now().isoformat()
            
            self._save_progress(progress)
            
            logger.info(f"Updated progress for student: {student_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating progress: {e}")
            return False
    
    def get_progress(self, student_id: str) -> Dict[str, Any]:
        """
        Get student progress.
        
        Args:
            student_id: Student ID
            
        Returns:
            Progress data
        """
        try:
            progress = self._load_progress()
            return progress.get(student_id, {})
        except Exception as e:
            logger.error(f"Error getting progress: {e}")
            return {}
    
    def add_activity(self, activity_data: Dict[str, Any]) -> bool:
        """
        Add activity record.
        
        Args:
            activity_data: Activity information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            activities = self._load_activity()
            
            # Add timestamp
            activity_data['timestamp'] = datetime.now().isoformat()
            
            activities.append(activity_data)
            
            # Keep only recent activities (last 1000)
            if len(activities) > 1000:
                activities = activities[-1000:]
            
            self._save_activity(activities)
            
            logger.info(f"Added activity: {activity_data.get('type', 'unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding activity: {e}")
            return False
    
    def get_recent_activity(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent activity.
        
        Args:
            limit: Number of activities to return
            
        Returns:
            List of recent activities
        """
        try:
            activities = self._load_activity()
            return activities[-limit:] if activities else []
        except Exception as e:
            logger.error(f"Error getting recent activity: {e}")
            return []
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """
        Get active learning sessions.
        
        Returns:
            List of active sessions
        """
        try:
            activities = self._load_activity()
            active_sessions = []
            
            # Find recent activities that indicate active sessions
            recent_activities = activities[-100:] if activities else []
            
            for activity in recent_activities:
                if activity.get('type') in ['login', 'content_view', 'path_start']:
                    # Check if activity is recent (within last 30 minutes)
                    timestamp = datetime.fromisoformat(activity['timestamp'])
                    if (datetime.now() - timestamp).total_seconds() < 1800:
                        active_sessions.append(activity)
            
            return active_sessions
            
        except Exception as e:
            logger.error(f"Error getting active sessions: {e}")
            return []
    
    def _load_students(self) -> List[Dict[str, Any]]:
        """Load students from file."""
        try:
            with open(self.students_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading students: {e}")
            return []
    
    def _save_students(self, students: List[Dict[str, Any]]):
        """Save students to file."""
        try:
            with open(self.students_file, 'w', encoding='utf-8') as f:
                json.dump(students, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving students: {e}")
    
    def _load_learning_paths(self) -> List[Dict[str, Any]]:
        """Load learning paths from file."""
        try:
            with open(self.paths_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading learning paths: {e}")
            return []
    
    def _save_learning_paths(self, paths: List[Dict[str, Any]]):
        """Save learning paths to file."""
        try:
            with open(self.paths_file, 'w', encoding='utf-8') as f:
                json.dump(paths, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving learning paths: {e}")
    
    def _load_progress(self) -> Dict[str, Any]:
        """Load progress from file."""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading progress: {e}")
            return {}
    
    def _save_progress(self, progress: Dict[str, Any]):
        """Save progress to file."""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving progress: {e}")
    
    def _load_activity(self) -> List[Dict[str, Any]]:
        """Load activity from file."""
        try:
            with open(self.activity_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading activity: {e}")
            return []
    
    def _save_activity(self, activities: List[Dict[str, Any]]):
        """Save activity to file."""
        try:
            with open(self.activity_file, 'w', encoding='utf-8') as f:
                json.dump(activities, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving activity: {e}")
    
    def _remove_student_data(self, student_id: str):
        """Remove all data associated with a student."""
        try:
            # Remove learning paths
            paths = self._load_learning_paths()
            paths = [p for p in paths if p.get('student_id') != student_id]
            self._save_learning_paths(paths)
            
            # Remove progress
            progress = self._load_progress()
            if student_id in progress:
                del progress[student_id]
                self._save_progress(progress)
            
            logger.info(f"Removed all data for student: {student_id}")
            
        except Exception as e:
            logger.error(f"Error removing student data: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics."""
        try:
            students = self._load_students()
            paths = self._load_learning_paths()
            progress = self._load_progress()
            activities = self._load_activity()
            
            stats = {
                'total_students': len(students),
                'total_learning_paths': len(paths),
                'students_with_progress': len(progress),
                'total_activities': len(activities),
                'active_sessions': len(self.get_active_sessions())
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {} 