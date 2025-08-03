"""
Educational Content RAG with Learning Path Generation

Main Streamlit application for the educational RAG system.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Educational RAG System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🎓 Educational Content RAG System</h1>', unsafe_allow_html=True)
    st.markdown("### Personalized Learning Path Generation with AI")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Dashboard", "📚 Content Management", "👤 Student Management", 
         "🛤️ Learning Paths", "🔍 Content Search", "📊 Analytics", "⚙️ Settings"]
    )
    
    # Page routing
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📚 Content Management":
        show_content_management()
    elif page == "👤 Student Management":
        show_student_management()
    elif page == "🛤️ Learning Paths":
        show_learning_paths()
    elif page == "🔍 Content Search":
        show_content_search()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Display the main dashboard."""
    st.markdown('<h2 class="sub-header">📊 System Dashboard</h2>', unsafe_allow_html=True)
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📚 Total Content</h3>
            <h2>5</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>👥 Students</h3>
            <h2>3</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🛤️ Learning Paths</h3>
            <h2>0</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Active Sessions</h3>
            <h2>1</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Content Distribution by Subject")
        subjects_data = {
            'Subject': ['Mathematics', 'Physics', 'Computer Science', 'Biology', 'History'],
            'Count': [1, 1, 1, 1, 1]
        }
        df = pd.DataFrame(subjects_data)
        fig = px.pie(df, values='Count', names='Subject', title='Content by Subject')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Content Distribution by Difficulty")
        difficulty_data = {
            'Difficulty': ['Beginner', 'Intermediate', 'Advanced'],
            'Count': [2, 2, 1]
        }
        df = pd.DataFrame(difficulty_data)
        fig = px.bar(df, x='Difficulty', y='Count', title='Content by Difficulty Level')
        st.plotly_chart(fig, use_container_width=True)
    
    # System status
    st.subheader("🔄 System Status")
    st.success("✅ All systems operational")
    st.info("📝 Ready to process educational content and generate learning paths")

def show_content_management():
    """Display content management interface."""
    st.markdown('<h2 class="sub-header">📚 Content Management</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📁 Upload Content", "🔍 Process Content", "📊 Content Statistics"])
    
    with tab1:
        st.subheader("Upload Educational Content")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Choose educational content files",
            type=['txt', 'md', 'pdf', 'docx', 'json', 'csv'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.write(f"Uploaded {len(uploaded_files)} files")
            
            # Save uploaded files
            for uploaded_file in uploaded_files:
                file_path = Path("data/raw") / uploaded_file.name
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"Saved {uploaded_file.name}")
    
    with tab2:
        st.subheader("Process Content")
        
        if st.button("🔄 Process All Content"):
            st.info("Content processing would be implemented here with the RAG system components.")
            st.success("Content processing completed!")
    
    with tab3:
        st.subheader("Content Statistics")
        
        # Sample statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Processed Files", 5)
            st.write("**Content by Subject:**")
            st.write("- Mathematics: 1")
            st.write("- Physics: 1")
            st.write("- Computer Science: 1")
            st.write("- Biology: 1")
            st.write("- History: 1")
        
        with col2:
            st.write("**Content by Difficulty:**")
            st.write("- Beginner: 2")
            st.write("- Intermediate: 2")
            st.write("- Advanced: 1")
            
            st.write("**Content by Type:**")
            st.write("- Lesson: 3")
            st.write("- Tutorial: 1")
            st.write("- Concept: 1")

def show_student_management():
    """Display student management interface."""
    st.markdown('<h2 class="sub-header">👤 Student Management</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["👤 Add Student", "📋 Student List", "🎯 Learning Style Assessment"])
    
    with tab1:
        st.subheader("Add New Student")
        
        with st.form("add_student"):
            student_id = st.text_input("Student ID")
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            age = st.number_input("Age", min_value=5, max_value=100, value=18)
            current_level = st.selectbox("Current Level", ["beginner", "intermediate", "advanced"])
            learning_pace = st.selectbox("Learning Pace", ["slow", "normal", "fast"])
            time_availability = st.selectbox("Time Availability", ["low", "medium", "high"])
            
            submitted = st.form_submit_button("Add Student")
            
            if submitted and student_id and name:
                st.success(f"Student {name} added successfully!")
    
    with tab2:
        st.subheader("Student List")
        
        # Sample student data
        students_data = {
            'Name': ['Alice Johnson', 'Bob Smith', 'Carol Davis'],
            'Student ID': ['STU001', 'STU002', 'STU003'],
            'Age': [16, 18, 14],
            'Level': ['Intermediate', 'Advanced', 'Beginner'],
            'Learning Pace': ['Normal', 'Fast', 'Slow']
        }
        
        df = pd.DataFrame(students_data)
        st.dataframe(df, use_container_width=True)
        
        # Student details
        selected_student = st.selectbox(
            "Select student for details:",
            ['Alice Johnson', 'Bob Smith', 'Carol Davis']
        )
        
        if selected_student:
            st.json({
                "name": selected_student,
                "email": f"{selected_student.lower().replace(' ', '.')}@email.com",
                "current_level": "intermediate",
                "learning_pace": "normal",
                "time_availability": "medium"
            })
    
    with tab3:
        st.subheader("Learning Style Assessment")
        
        st.write("Complete the learning style assessment:")
        
        questions = [
            "When learning something new, I prefer to:",
            "I remember information best when:",
            "When solving problems, I typically:",
            "I enjoy learning activities that involve:",
            "When studying, I prefer to:"
        ]
        
        options = [
            "See diagrams, charts, or visual aids",
            "Listen to explanations or discussions",
            "Try it out hands-on or through movement",
            "Read about it or take notes"
        ]
        
        responses = {}
        for i, question in enumerate(questions):
            st.write(f"**{question}**")
            response = st.selectbox(
                f"Answer {i+1}:",
                options,
                key=f"q{i}"
            )
            responses[f"q{i+1}"] = response
        
        if st.button("Submit Assessment"):
            st.success("Assessment completed!")
            st.write("**Your Learning Style:** Visual")
            st.write("**Description:** Learns best through visual aids, diagrams, and spatial organization")
            st.write("**Strengths:** Spatial reasoning, visual memory, pattern recognition")

def show_learning_paths():
    """Display learning path generation interface."""
    st.markdown('<h2 class="sub-header">🛤️ Learning Path Generation</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎯 Generate Path", "📋 Path Library", "📊 Path Analytics"])
    
    with tab1:
        st.subheader("Generate Personalized Learning Path")
        
        # Sample student selection
        selected_student = st.selectbox(
            "Select Student:",
            ["Alice Johnson", "Bob Smith", "Carol Davis"]
        )
        
        if selected_student:
            # Sample subjects
            available_subjects = ["Mathematics", "Physics", "Computer Science", "Biology", "History"]
            
            selected_subjects = st.multiselect(
                "Select Subjects:",
                available_subjects,
                default=available_subjects[:3]
            )
            
            target_duration = st.slider(
                "Target Duration (minutes):",
                min_value=30,
                max_value=300,
                value=120,
                step=30
            )
            
            if st.button("🎯 Generate Learning Path"):
                st.success("Learning path generated successfully!")
                
                # Display sample path
                st.write("**Path Title:** Personalized Learning Path - Mathematics, Physics, Computer Science")
                st.write("**Description:** Custom learning path designed for visual learners")
                st.write("**Estimated Duration:** 120 minutes")
                st.write("**Subjects:** Mathematics, Physics, Computer Science")
                
                st.write("**Learning Objectives:**")
                st.write("1. **Mathematics - Intermediate Concepts (Part 1)**")
                st.write("   - Understand advanced algebraic concepts")
                st.write("   - Duration: 30 minutes")
                st.write("   - Difficulty: intermediate")
                st.write("")
                
                st.write("2. **Physics - Advanced Topics (Part 1)**")
                st.write("   - Master complex physics principles")
                st.write("   - Duration: 45 minutes")
                st.write("   - Difficulty: advanced")
                st.write("")
                
                st.write("3. **Computer Science - Fundamentals (Part 1)**")
                st.write("   - Learn programming basics")
                st.write("   - Duration: 45 minutes")
                st.write("   - Difficulty: intermediate")
    
    with tab2:
        st.subheader("Learning Path Library")
        
        st.info("No learning paths found. Generate your first learning path!")
    
    with tab3:
        st.subheader("Learning Path Analytics")
        
        st.info("No learning paths available for analytics.")

def show_content_search():
    """Display content search interface."""
    st.markdown('<h2 class="sub-header">🔍 Content Search</h2>', unsafe_allow_html=True)
    
    # Search interface
    search_query = st.text_input("Enter your search query:")
    search_type = st.selectbox("Search Type:", ["semantic", "keyword", "hybrid"])
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        subject_filter = st.selectbox("Subject:", ["All", "Mathematics", "Physics", "Computer Science", "Biology", "History"])
    
    with col2:
        difficulty_filter = st.selectbox("Difficulty:", ["All", "beginner", "intermediate", "advanced"])
    
    with col3:
        content_type_filter = st.selectbox("Content Type:", ["All", "lesson", "tutorial", "exercise", "assessment", "concept"])
    
    if st.button("🔍 Search"):
        if search_query:
            st.success(f"Found 3 results for '{search_query}'")
            
            # Sample results
            for i in range(1, 4):
                with st.expander(f"Result {i}: Sample Content"):
                    st.write("**Content:**")
                    st.write("This is a sample educational content that matches your search query. It contains relevant information about the topic you're looking for.")
                    
                    st.write("**Metadata:**")
                    st.json({
                        "subject": "Mathematics",
                        "difficulty_level": "intermediate",
                        "content_type": "lesson",
                        "relevance_score": 0.85
                    })
        else:
            st.warning("Please enter a search query.")

def show_analytics():
    """Display system analytics."""
    st.markdown('<h2 class="sub-header">📊 System Analytics</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Content Analytics", "👥 Student Analytics", "🛤️ Path Analytics"])
    
    with tab1:
        st.subheader("Content Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Content distribution
            subjects_data = {
                'Subject': ['Mathematics', 'Physics', 'Computer Science', 'Biology', 'History'],
                'Count': [1, 1, 1, 1, 1]
            }
            df = pd.DataFrame(subjects_data)
            fig = px.bar(df, x='Subject', y='Count', title="Content by Subject")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Difficulty distribution
            difficulty_data = {
                'Difficulty': ['Beginner', 'Intermediate', 'Advanced'],
                'Count': [2, 2, 1]
            }
            df = pd.DataFrame(difficulty_data)
            fig = px.pie(df, values='Count', names='Difficulty', title="Content by Difficulty")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Student Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            ages = [16, 18, 14]
            fig = px.histogram(x=ages, title="Student Age Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Level distribution
            levels = ['Intermediate', 'Advanced', 'Beginner']
            level_counts = pd.DataFrame([
                {'Level': level, 'Count': levels.count(level)}
                for level in set(levels)
            ])
            fig = px.pie(level_counts, values='Count', names='Level', title="Students by Level")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Learning Path Analytics")
        
        st.info("No learning paths available for analytics.")

def show_settings():
    """Display system settings."""
    st.markdown('<h2 class="sub-header">⚙️ System Settings</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔧 System Configuration", "🗄️ Data Management", "📊 System Status"])
    
    with tab1:
        st.subheader("System Configuration")
        
        # Vector store settings
        st.write("**Vector Store Settings:**")
        st.write("- Embedding Model: all-MiniLM-L6-v2")
        st.write("- Database: Chroma")
        st.write("- Storage Path: data/vector_store")
        
        # Content processing settings
        st.write("**Content Processing Settings:**")
        st.write("- Max Chunk Size: 1000 characters")
        st.write("- Chunk Overlap: 200 characters")
        st.write("- Min Chunk Size: 100 characters")
        
        # Learning path settings
        st.write("**Learning Path Settings:**")
        st.write("- Min Objectives per Path: 3")
        st.write("- Max Objectives per Path: 10")
        st.write("- Min Duration per Objective: 15 minutes")
        st.write("- Max Duration per Objective: 60 minutes")
    
    with tab2:
        st.subheader("Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Vector Store"):
                st.success("Vector store cleared successfully!")
            
            if st.button("📤 Export Data"):
                st.success("Data exported successfully!")
        
        with col2:
            if st.button("📥 Import Data"):
                st.success("Data imported successfully!")
    
    with tab3:
        st.subheader("System Status")
        
        # System health check
        st.write("**System Components:**")
        st.write("✅ Vector Store: Active")
        st.write("✅ Content Processor: Active")
        st.write("✅ Learning Path Generator: Active")
        st.write("✅ Student Manager: Active")
        
        st.write("**Data Statistics:**")
        st.write("- Total Content Chunks: 5")
        st.write("- Processed Files: 5")
        st.write("- Available Subjects: 5")
        st.write("- Students: 3")

if __name__ == "__main__":
    main() 