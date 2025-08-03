# Educational Content RAG with Learning Path Generation

A comprehensive Retrieval-Augmented Generation (RAG) system that creates personalized learning paths by retrieving and organizing educational content based on student level, learning style, and progress tracking.

## 🎯 Features

- **Educational Content Processing**: Intelligent categorization and chunking of educational materials
- **Personalized Learning Paths**: Dynamic generation based on student profile and progress
- **Student Progress Tracking**: Real-time monitoring and adaptation of learning paths
- **Learning Style Identification**: Accommodation of different learning preferences (visual, auditory, kinesthetic)
- **Competency-Based Sequencing**: Intelligent content ordering based on skill progression
- **Multi-modal Resource Integration**: Support for text, images, and interactive content
- **Knowledge Gap Analysis**: Identification and remediation of learning gaps

## 🏗️ Architecture

### Core Components

1. **Content Processing Pipeline**
   - Educational content ingestion and preprocessing
   - Intelligent chunking strategies for different content types
   - Metadata extraction and categorization

2. **Vector Database & Embeddings**
   - Chroma vector database for efficient retrieval
   - Sentence Transformers for semantic embeddings
   - Multi-modal embedding support

3. **Learning Path Generator**
   - Student profile analysis and learning style identification
   - Competency mapping and skill progression tracking
   - Adaptive difficulty adjustment

4. **RAG Engine**
   - Context-aware retrieval with relevance scoring
   - Personalized response generation
   - Progress-aware content recommendations

5. **Student Management System**
   - Progress tracking and analytics
   - Learning style assessment
   - Performance prediction modeling

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the System**
   ```bash
   python setup.py
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Access the Application**
   - Open your browser and go to `http://localhost:8501`
   - Start creating personalized learning paths!

## 📁 Project Structure

```
educational-rag/
├── app.py                          # Main Streamlit application
├── setup.py                        # System initialization
├── requirements.txt                 # Python dependencies
├── README.md                       # Project documentation
├── data/                           # Educational content and datasets
│   ├── raw/                        # Raw educational materials
│   ├── processed/                  # Processed and chunked content
│   └── student_data/               # Student profiles and progress
├── src/                            # Core system components
│   ├── content_processor/          # Content processing pipeline
│   ├── vector_store/               # Vector database management
│   ├── learning_path/              # Learning path generation
│   ├── student_management/         # Student tracking system
│   ├── rag_engine/                 # RAG implementation
│   └── evaluation/                 # System evaluation metrics
├── notebooks/                      # Jupyter notebooks for analysis
├── tests/                          # Unit and integration tests
└── docs/                           # Additional documentation
```

## 🎓 Learning Path Features

### Student Profile Analysis
- **Learning Style Assessment**: Identifies visual, auditory, or kinesthetic preferences
- **Skill Level Evaluation**: Determines current competency across subjects
- **Progress Tracking**: Monitors learning milestones and achievements

### Adaptive Content Sequencing
- **Prerequisite Mapping**: Ensures logical learning progression
- **Difficulty Adjustment**: Dynamically adjusts content complexity
- **Knowledge Gap Remediation**: Identifies and fills learning gaps

### Personalized Recommendations
- **Context-Aware Retrieval**: Finds relevant content based on current progress
- **Learning Style Accommodation**: Tailors content presentation to preferences
- **Performance Prediction**: Anticipates learning needs and challenges

## 🔧 Technical Implementation

### Embedding Models
- **Text Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Multi-modal Support**: CLIP for image-text embeddings
- **Domain-Specific**: Fine-tuned models for educational content

### Vector Database
- **Chroma**: Local vector database for efficient retrieval
- **Metadata Filtering**: Content type, difficulty, subject filtering
- **Hybrid Search**: Semantic + keyword-based retrieval

### RAG Pipeline
- **Chunking Strategy**: Semantic-aware content splitting
- **Retrieval**: Top-k retrieval with relevance scoring
- **Generation**: Context-aware response generation with citations

## 📊 Evaluation Metrics

### Retrieval Performance
- **Precision@K**: Accuracy of top-k retrieved documents
- **Recall@K**: Coverage of relevant content
- **NDCG**: Normalized Discounted Cumulative Gain

### Learning Effectiveness
- **Knowledge Retention**: Post-assessment scores
- **Learning Progression**: Skill advancement tracking
- **Engagement Metrics**: Time spent, completion rates

### System Performance
- **Latency**: Response time for queries
- **Throughput**: Concurrent user handling
- **Scalability**: System performance under load

## 🎨 User Interface

The application provides an intuitive interface for:
- **Student Registration**: Profile creation and learning style assessment
- **Learning Path Visualization**: Interactive progress tracking
- **Content Exploration**: Browse and search educational materials
- **Progress Analytics**: Detailed performance insights
- **Adaptive Recommendations**: Personalized content suggestions

## 🔬 Research & Development

### Current Capabilities
- ✅ Educational content processing and categorization
- ✅ Personalized learning path generation
- ✅ Student progress tracking and adaptation
- ✅ Learning style identification and accommodation
- ✅ Competency-based content sequencing
- ✅ Multi-modal learning resource integration
- ✅ Knowledge gap identification and remediation

### Future Enhancements
- 🔄 Advanced learning analytics and insights
- 🔄 Collaborative learning features
- 🔄 Real-time assessment integration
- 🔄 Mobile application development
- 🔄 AI-powered tutoring assistance

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Educational content providers and datasets
- Open-source RAG and NLP communities
- Research institutions for learning science insights

---

**Built with ❤️ for personalized education** 