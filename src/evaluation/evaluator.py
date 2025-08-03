"""
System Evaluator for Educational RAG System

Handles system evaluation, performance metrics, and quality assessment.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class SystemEvaluator:
    """
    Evaluator for system performance and quality metrics.
    
    Features:
    - Retrieval performance evaluation
    - Learning effectiveness assessment
    - System performance monitoring
    - Quality metrics calculation
    """
    
    def __init__(self, output_dir: str = "data/evaluation"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Evaluation metrics
        self.metrics = {
            'retrieval': {},
            'learning': {},
            'system': {},
            'quality': {}
        }
    
    def evaluate_retrieval_performance(self, 
                                     query_results: List[Dict[str, Any]],
                                     ground_truth: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Evaluate retrieval performance.
        
        Args:
            query_results: Retrieved results from the system
            ground_truth: Ground truth relevant documents (optional)
            
        Returns:
            Dictionary containing retrieval metrics
        """
        metrics = {
            'total_queries': len(query_results),
            'average_results_per_query': 0,
            'relevance_scores': [],
            'coverage_metrics': {}
        }
        
        if query_results:
            # Calculate average results per query
            total_results = sum(len(result.get('results', [])) for result in query_results)
            metrics['average_results_per_query'] = total_results / len(query_results)
            
            # Calculate relevance scores
            relevance_scores = []
            for result in query_results:
                for item in result.get('results', []):
                    if 'distance' in item:
                        relevance = 1 - item['distance']
                        relevance_scores.append(relevance)
            
            if relevance_scores:
                metrics['relevance_scores'] = {
                    'average': sum(relevance_scores) / len(relevance_scores),
                    'min': min(relevance_scores),
                    'max': max(relevance_scores),
                    'median': sorted(relevance_scores)[len(relevance_scores) // 2]
                }
            
            # Calculate coverage metrics
            all_subjects = set()
            all_difficulties = set()
            
            for result in query_results:
                for item in result.get('results', []):
                    metadata = item.get('metadata', {})
                    all_subjects.add(metadata.get('subject', 'unknown'))
                    all_difficulties.add(metadata.get('difficulty_level', 'unknown'))
            
            metrics['coverage_metrics'] = {
                'subjects_covered': len(all_subjects),
                'difficulty_levels_covered': len(all_difficulties),
                'subject_distribution': {subject: 0 for subject in all_subjects},
                'difficulty_distribution': {difficulty: 0 for difficulty in all_difficulties}
            }
            
            # Calculate distributions
            for result in query_results:
                for item in result.get('results', []):
                    metadata = item.get('metadata', {})
                    subject = metadata.get('subject', 'unknown')
                    difficulty = metadata.get('difficulty_level', 'unknown')
                    
                    metrics['coverage_metrics']['subject_distribution'][subject] += 1
                    metrics['coverage_metrics']['difficulty_distribution'][difficulty] += 1
        
        self.metrics['retrieval'] = metrics
        return metrics
    
    def evaluate_learning_effectiveness(self, 
                                      learning_paths: List[Dict[str, Any]],
                                      student_progress: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate learning effectiveness.
        
        Args:
            learning_paths: Generated learning paths
            student_progress: Student progress data
            
        Returns:
            Dictionary containing learning effectiveness metrics
        """
        metrics = {
            'total_paths': len(learning_paths),
            'completion_rate': 0,
            'average_duration': 0,
            'subject_coverage': {},
            'difficulty_progression': {},
            'student_engagement': {}
        }
        
        if learning_paths:
            # Calculate completion rate
            completed_paths = sum(1 for path in learning_paths if path.get('status') == 'completed')
            metrics['completion_rate'] = completed_paths / len(learning_paths) if learning_paths else 0
            
            # Calculate average duration
            durations = [path.get('estimated_total_duration', 0) for path in learning_paths]
            metrics['average_duration'] = sum(durations) / len(durations) if durations else 0
            
            # Analyze subject coverage
            subject_counts = {}
            for path in learning_paths:
                subjects = path.get('subjects', [])
                for subject in subjects:
                    subject_counts[subject] = subject_counts.get(subject, 0) + 1
            
            metrics['subject_coverage'] = subject_counts
            
            # Analyze difficulty progression
            difficulty_counts = {}
            for path in learning_paths:
                progression = path.get('difficulty_progression', [])
                for difficulty in progression:
                    difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
            
            metrics['difficulty_progression'] = difficulty_counts
        
        if student_progress:
            # Analyze student engagement
            engagement_metrics = {
                'active_students': len(student_progress),
                'average_performance': 0,
                'learning_pace_distribution': {},
                'time_spent_distribution': {}
            }
            
            performances = [progress.get('average_performance', 0) for progress in student_progress]
            if performances:
                engagement_metrics['average_performance'] = sum(performances) / len(performances)
            
            # Analyze learning pace
            pace_counts = {}
            for progress in student_progress:
                pace = progress.get('learning_pace', 'normal')
                pace_counts[pace] = pace_counts.get(pace, 0) + 1
            
            engagement_metrics['learning_pace_distribution'] = pace_counts
            
            metrics['student_engagement'] = engagement_metrics
        
        self.metrics['learning'] = metrics
        return metrics
    
    def evaluate_system_performance(self, 
                                  performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate system performance.
        
        Args:
            performance_data: System performance data
            
        Returns:
            Dictionary containing system performance metrics
        """
        metrics = {
            'response_times': {},
            'throughput': {},
            'resource_usage': {},
            'error_rates': {}
        }
        
        # Analyze response times
        if 'response_times' in performance_data:
            times = performance_data['response_times']
            if times:
                metrics['response_times'] = {
                    'average': sum(times) / len(times),
                    'min': min(times),
                    'max': max(times),
                    'p95': sorted(times)[int(len(times) * 0.95)]
                }
        
        # Analyze throughput
        if 'requests_per_minute' in performance_data:
            metrics['throughput'] = {
                'requests_per_minute': performance_data['requests_per_minute'],
                'concurrent_users': performance_data.get('concurrent_users', 0)
            }
        
        # Analyze resource usage
        if 'cpu_usage' in performance_data:
            metrics['resource_usage'] = {
                'cpu_usage': performance_data['cpu_usage'],
                'memory_usage': performance_data.get('memory_usage', 0),
                'disk_usage': performance_data.get('disk_usage', 0)
            }
        
        # Analyze error rates
        if 'total_requests' in performance_data and 'error_requests' in performance_data:
            total = performance_data['total_requests']
            errors = performance_data['error_requests']
            metrics['error_rates'] = {
                'error_rate': errors / total if total > 0 else 0,
                'total_requests': total,
                'error_requests': errors
            }
        
        self.metrics['system'] = metrics
        return metrics
    
    def evaluate_content_quality(self, 
                               content_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate content quality.
        
        Args:
            content_data: Content quality data
            
        Returns:
            Dictionary containing content quality metrics
        """
        metrics = {
            'total_content': len(content_data),
            'quality_scores': {},
            'subject_distribution': {},
            'difficulty_distribution': {},
            'content_type_distribution': {},
            'metadata_completeness': {}
        }
        
        if content_data:
            # Calculate quality scores
            quality_scores = []
            for item in content_data:
                score = item.get('quality_score', 0)
                quality_scores.append(score)
            
            if quality_scores:
                metrics['quality_scores'] = {
                    'average': sum(quality_scores) / len(quality_scores),
                    'min': min(quality_scores),
                    'max': max(quality_scores),
                    'high_quality_count': sum(1 for score in quality_scores if score >= 0.8)
                }
            
            # Analyze distributions
            subject_counts = {}
            difficulty_counts = {}
            type_counts = {}
            
            for item in content_data:
                metadata = item.get('metadata', {})
                
                subject = metadata.get('subject', 'unknown')
                subject_counts[subject] = subject_counts.get(subject, 0) + 1
                
                difficulty = metadata.get('difficulty_level', 'unknown')
                difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
                
                content_type = metadata.get('content_type', 'unknown')
                type_counts[content_type] = type_counts.get(content_type, 0) + 1
            
            metrics['subject_distribution'] = subject_counts
            metrics['difficulty_distribution'] = difficulty_counts
            metrics['content_type_distribution'] = type_counts
            
            # Analyze metadata completeness
            completeness_scores = []
            for item in content_data:
                metadata = item.get('metadata', {})
                required_fields = ['subject', 'difficulty_level', 'content_type', 'title']
                present_fields = sum(1 for field in required_fields if field in metadata)
                completeness = present_fields / len(required_fields)
                completeness_scores.append(completeness)
            
            if completeness_scores:
                metrics['metadata_completeness'] = {
                    'average': sum(completeness_scores) / len(completeness_scores),
                    'complete_records': sum(1 for score in completeness_scores if score == 1.0)
                }
        
        self.metrics['quality'] = metrics
        return metrics
    
    def generate_evaluation_report(self, 
                                 report_name: Optional[str] = None) -> str:
        """
        Generate a comprehensive evaluation report.
        
        Args:
            report_name: Name for the report file
            
        Returns:
            Path to the generated report
        """
        if report_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"evaluation_report_{timestamp}.json"
        
        report_path = self.output_dir / report_name
        
        # Compile all metrics
        report = {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.metrics,
            'summary': self._generate_summary(),
            'recommendations': self._generate_recommendations()
        }
        
        # Save report
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Evaluation report generated: {report_path}")
        return str(report_path)
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of all metrics."""
        summary = {
            'overall_score': 0,
            'key_insights': [],
            'performance_indicators': {}
        }
        
        # Calculate overall score
        scores = []
        
        # Retrieval performance
        if self.metrics['retrieval']:
            retrieval = self.metrics['retrieval']
            if 'relevance_scores' in retrieval and 'average' in retrieval['relevance_scores']:
                scores.append(retrieval['relevance_scores']['average'])
        
        # Learning effectiveness
        if self.metrics['learning']:
            learning = self.metrics['learning']
            if 'completion_rate' in learning:
                scores.append(learning['completion_rate'])
        
        # System performance
        if self.metrics['system']:
            system = self.metrics['system']
            if 'error_rates' in system and 'error_rate' in system['error_rates']:
                error_rate = system['error_rates']['error_rate']
                scores.append(1 - error_rate)  # Convert error rate to success rate
        
        # Content quality
        if self.metrics['quality']:
            quality = self.metrics['quality']
            if 'quality_scores' in quality and 'average' in quality['quality_scores']:
                scores.append(quality['quality_scores']['average'])
        
        if scores:
            summary['overall_score'] = sum(scores) / len(scores)
        
        # Generate key insights
        insights = []
        
        if self.metrics['retrieval']:
            retrieval = self.metrics['retrieval']
            if 'relevance_scores' in retrieval:
                avg_relevance = retrieval['relevance_scores'].get('average', 0)
                insights.append(f"Average retrieval relevance: {avg_relevance:.3f}")
        
        if self.metrics['learning']:
            learning = self.metrics['learning']
            completion_rate = learning.get('completion_rate', 0)
            insights.append(f"Learning path completion rate: {completion_rate:.1%}")
        
        if self.metrics['system']:
            system = self.metrics['system']
            if 'error_rates' in system:
                error_rate = system['error_rates'].get('error_rate', 0)
                insights.append(f"System error rate: {error_rate:.1%}")
        
        summary['key_insights'] = insights
        
        return summary
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on metrics."""
        recommendations = []
        
        # Retrieval recommendations
        if self.metrics['retrieval']:
            retrieval = self.metrics['retrieval']
            if 'relevance_scores' in retrieval:
                avg_relevance = retrieval['relevance_scores'].get('average', 0)
                if avg_relevance < 0.7:
                    recommendations.append("Consider improving retrieval relevance by fine-tuning embedding models")
        
        # Learning recommendations
        if self.metrics['learning']:
            learning = self.metrics['learning']
            completion_rate = learning.get('completion_rate', 0)
            if completion_rate < 0.6:
                recommendations.append("Improve learning path completion by adjusting difficulty progression")
        
        # System recommendations
        if self.metrics['system']:
            system = self.metrics['system']
            if 'error_rates' in system:
                error_rate = system['error_rates'].get('error_rate', 0)
                if error_rate > 0.05:
                    recommendations.append("Address system errors to improve reliability")
        
        # Quality recommendations
        if self.metrics['quality']:
            quality = self.metrics['quality']
            if 'quality_scores' in quality:
                avg_quality = quality['quality_scores'].get('average', 0)
                if avg_quality < 0.8:
                    recommendations.append("Improve content quality through better curation and validation")
        
        return recommendations
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of all current metrics."""
        return {
            'retrieval': self.metrics['retrieval'],
            'learning': self.metrics['learning'],
            'system': self.metrics['system'],
            'quality': self.metrics['quality']
        } 