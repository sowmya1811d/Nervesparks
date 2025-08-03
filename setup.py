"""
Setup script for Educational RAG System

Initializes the system and creates sample data.
"""

import os
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_content():
    """Create sample educational content for testing."""
    sample_content = {
        "mathematics_basics.txt": """
# Mathematics Fundamentals

## Introduction to Algebra
Algebra is a branch of mathematics that deals with symbols and the rules for manipulating these symbols. In elementary algebra, those symbols (today written as Latin and Greek letters) represent quantities without fixed values, known as variables.

### Learning Objectives:
- Understand basic algebraic concepts
- Learn to solve simple equations
- Apply algebraic methods to real-world problems

### Key Concepts:
1. Variables and Constants
2. Linear Equations
3. Quadratic Equations
4. Functions and Graphs

### Example Problem:
Solve for x: 2x + 3 = 7
Solution: x = 2

This fundamental knowledge is essential for advanced mathematics and many scientific disciplines.
        """,
        
        "physics_mechanics.txt": """
# Physics: Classical Mechanics

## Newton's Laws of Motion
Classical mechanics is the study of the motion of objects and the forces that cause motion. Sir Isaac Newton formulated three fundamental laws that describe the relationship between forces acting on a body and the motion of that body.

### Learning Objectives:
- Understand Newton's three laws of motion
- Apply force and motion concepts
- Solve basic physics problems

### Newton's Laws:
1. First Law (Inertia): An object at rest stays at rest unless acted upon by an external force
2. Second Law (F = ma): Force equals mass times acceleration
3. Third Law (Action-Reaction): For every action, there is an equal and opposite reaction

### Example Application:
A car with mass 1000 kg accelerates at 2 m/s². What is the force?
F = ma = 1000 kg × 2 m/s² = 2000 N
        """,
        
        "computer_science_intro.txt": """
# Introduction to Computer Science

## Programming Fundamentals
Computer science is the study of computation, automation, and information. Programming is the process of creating a set of instructions that tell a computer how to perform a task.

### Learning Objectives:
- Understand basic programming concepts
- Learn to write simple programs
- Develop problem-solving skills

### Key Topics:
1. Variables and Data Types
2. Control Structures (if/else, loops)
3. Functions and Methods
4. Object-Oriented Programming

### Example Code:
```python
def calculate_area(length, width):
    return length * width

# Calculate area of a rectangle
area = calculate_area(5, 3)
print(f"Area: {area} square units")
```

Programming is essential in today's digital world and opens many career opportunities.
        """,
        
        "biology_cells.txt": """
# Biology: Cell Structure and Function

## The Cell: Basic Unit of Life
Cells are the basic structural and functional units of all living organisms. Understanding cell biology is fundamental to understanding life itself.

### Learning Objectives:
- Identify cell structures and their functions
- Understand cell processes
- Compare plant and animal cells

### Cell Components:
1. Cell Membrane: Controls what enters and exits
2. Nucleus: Contains genetic material
3. Mitochondria: Produces energy
4. Cytoplasm: Gel-like substance containing organelles

### Cell Types:
- Prokaryotic cells (bacteria)
- Eukaryotic cells (plants, animals, fungi)

### Example: Plant vs Animal Cells
Plant cells have cell walls and chloroplasts, while animal cells do not. Both contain nuclei and mitochondria.
        """,
        
        "history_ancient_civilizations.txt": """
# History: Ancient Civilizations

## The Rise of Early Civilizations
Ancient civilizations laid the foundation for modern society. Understanding these early cultures helps us appreciate human development and cultural evolution.

### Learning Objectives:
- Identify major ancient civilizations
- Understand their contributions to society
- Analyze historical patterns and developments

### Major Civilizations:
1. Mesopotamia (3500-2000 BCE)
2. Ancient Egypt (3100-30 BCE)
3. Ancient Greece (800-146 BCE)
4. Ancient Rome (753 BCE-476 CE)

### Key Contributions:
- Writing systems
- Architecture and engineering
- Legal systems
- Philosophy and science

### Example: Egyptian Pyramids
The Great Pyramid of Giza, built around 2560 BCE, demonstrates advanced engineering and mathematical knowledge of ancient Egyptians.
        """
    }
    
    # Create raw content directory
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Write sample content
    for filename, content in sample_content.items():
        file_path = raw_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Created sample content: {filename}")

def create_sample_students():
    """Create sample student data."""
    sample_students = [
        {
            "student_id": "STU001",
            "name": "Alice Johnson",
            "email": "alice.johnson@email.com",
            "age": 16,
            "current_level": "intermediate",
            "learning_pace": "normal",
            "time_availability": "medium",
            "content_preferences": {
                "videos": 3,
                "diagrams": 2,
                "reading": 1,
                "interactive": 2
            },
            "learning_behavior": {
                "time_on_videos": 45,
                "time_on_text": 30,
                "time_on_interactive": 25
            },
            "performance_patterns": {
                "visual_tasks": 0.85,
                "text_tasks": 0.70,
                "hands_on_tasks": 0.90
            }
        },
        {
            "student_id": "STU002",
            "name": "Bob Smith",
            "email": "bob.smith@email.com",
            "age": 18,
            "current_level": "advanced",
            "learning_pace": "fast",
            "time_availability": "high",
            "content_preferences": {
                "reading": 4,
                "note_taking": 3,
                "writing": 2,
                "discussions": 1
            },
            "learning_behavior": {
                "time_on_text": 60,
                "time_on_videos": 20,
                "time_on_interactive": 10
            },
            "performance_patterns": {
                "text_tasks": 0.95,
                "visual_tasks": 0.75,
                "hands_on_tasks": 0.80
            }
        },
        {
            "student_id": "STU003",
            "name": "Carol Davis",
            "email": "carol.davis@email.com",
            "age": 14,
            "current_level": "beginner",
            "learning_pace": "slow",
            "time_availability": "low",
            "content_preferences": {
                "experiments": 3,
                "hands_on": 4,
                "interactive": 3,
                "videos": 2
            },
            "learning_behavior": {
                "time_on_interactive": 50,
                "time_on_videos": 30,
                "time_on_text": 10
            },
            "performance_patterns": {
                "hands_on_tasks": 0.90,
                "visual_tasks": 0.80,
                "text_tasks": 0.60
            }
        }
    ]
    
    # Create student data directory
    student_dir = Path("data/student_data")
    student_dir.mkdir(parents=True, exist_ok=True)
    
    # Write sample students
    students_file = student_dir / "students.json"
    with open(students_file, 'w', encoding='utf-8') as f:
        json.dump(sample_students, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Created {len(sample_students)} sample students")

def initialize_directories():
    """Initialize all necessary directories."""
    directories = [
        "data/raw",
        "data/processed",
        "data/student_data",
        "data/vector_store",
        "src/content_processor",
        "src/vector_store",
        "src/learning_path",
        "src/student_management",
        "src/rag_engine",
        "src/evaluation",
        "notebooks",
        "tests",
        "docs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def main():
    """Main setup function."""
    logger.info("Starting Educational RAG System setup...")
    
    try:
        # Initialize directories
        initialize_directories()
        
        # Create sample content
        create_sample_content()
        
        # Create sample students
        create_sample_students()
        
        logger.info("Setup completed successfully!")
        logger.info("You can now run: streamlit run app.py")
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        raise

if __name__ == "__main__":
    main() 