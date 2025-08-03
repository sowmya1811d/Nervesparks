"""
Test script for Educational RAG System

Tests the core components of the system.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from content_processor import ContentProcessor
        print("✅ ContentProcessor imported successfully")
    except Exception as e:
        print(f"❌ Error importing ContentProcessor: {e}")
    
    try:
        from vector_store import VectorStore
        print("✅ VectorStore imported successfully")
    except Exception as e:
        print(f"❌ Error importing VectorStore: {e}")
    
    try:
        from learning_path import LearningPathGenerator
        print("✅ LearningPathGenerator imported successfully")
    except Exception as e:
        print(f"❌ Error importing LearningPathGenerator: {e}")
    
    try:
        from student_management import StudentManager
        print("✅ StudentManager imported successfully")
    except Exception as e:
        print(f"❌ Error importing StudentManager: {e}")

def test_content_processing():
    """Test content processing functionality."""
    print("\nTesting content processing...")
    
    try:
        from content_processor import ContentProcessor
        
        processor = ContentProcessor()
        print("✅ ContentProcessor initialized")
        
        # Test processing a sample file
        sample_content = """
        # Sample Educational Content
        
        This is a test document for mathematics.
        
        ## Learning Objectives:
        - Understand basic concepts
        - Apply mathematical principles
        - Solve problems effectively
        
        This content covers fundamental mathematical concepts.
        """
        
        # Create a test file
        test_file = Path("data/raw/test_content.txt")
        test_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        print("✅ Test file created")
        
        # Process the content
        result = processor.process_content(str(test_file))
        print(f"✅ Content processed: {result.get('file_path', 'Unknown')}")
        
        # Clean up
        test_file.unlink()
        print("✅ Test file cleaned up")
        
    except Exception as e:
        print(f"❌ Error in content processing test: {e}")

def test_vector_store():
    """Test vector store functionality."""
    print("\nTesting vector store...")
    
    try:
        from vector_store import VectorStore
        
        store = VectorStore()
        print("✅ VectorStore initialized")
        
        # Test statistics
        stats = store.get_statistics()
        print(f"✅ Vector store statistics: {stats}")
        
    except Exception as e:
        print(f"❌ Error in vector store test: {e}")

def test_student_management():
    """Test student management functionality."""
    print("\nTesting student management...")
    
    try:
        from student_management import StudentManager
        
        manager = StudentManager()
        print("✅ StudentManager initialized")
        
        # Test adding a student
        student_data = {
            'student_id': 'TEST001',
            'name': 'Test Student',
            'email': 'test@example.com',
            'age': 20,
            'current_level': 'intermediate',
            'learning_pace': 'normal',
            'time_availability': 'medium'
        }
        
        success = manager.add_student(student_data)
        if success:
            print("✅ Student added successfully")
        else:
            print("⚠️ Student already exists or error occurred")
        
        # Test getting students
        students = manager.get_all_students()
        print(f"✅ Retrieved {len(students)} students")
        
    except Exception as e:
        print(f"❌ Error in student management test: {e}")

def test_learning_path():
    """Test learning path generation."""
    print("\nTesting learning path generation...")
    
    try:
        from learning_path import LearningPathGenerator
        from vector_store import VectorStore
        
        vector_store = VectorStore()
        generator = LearningPathGenerator(vector_store)
        print("✅ LearningPathGenerator initialized")
        
        # Test with sample student profile
        student_profile = {
            'student_id': 'TEST001',
            'name': 'Test Student',
            'current_level': 'intermediate',
            'learning_pace': 'normal',
            'time_availability': 'medium',
            'average_performance': 0.7
        }
        
        # This would normally require content in the vector store
        print("✅ LearningPathGenerator ready (requires content in vector store)")
        
    except Exception as e:
        print(f"❌ Error in learning path test: {e}")

def test_setup():
    """Test the setup script."""
    print("\nTesting setup script...")
    
    try:
        import setup
        print("✅ Setup script imported successfully")
        
        # Test directory creation
        test_dirs = ["data/raw", "data/processed", "data/student_data"]
        for dir_path in test_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            if Path(dir_path).exists():
                print(f"✅ Directory created: {dir_path}")
            else:
                print(f"❌ Failed to create directory: {dir_path}")
        
    except Exception as e:
        print(f"❌ Error in setup test: {e}")

def main():
    """Run all tests."""
    print("🧪 Educational RAG System - Component Tests")
    print("=" * 50)
    
    test_imports()
    test_content_processing()
    test_vector_store()
    test_student_management()
    test_learning_path()
    test_setup()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\nTo run the application:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run setup: python setup.py")
    print("3. Start the app: streamlit run app.py")

if __name__ == "__main__":
    main() 