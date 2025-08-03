# Educational RAG System - Deployment Guide

This guide provides step-by-step instructions for deploying the Educational Content RAG with Learning Path Generation system.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd educational-rag-system

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize the System

```bash
# Run the setup script to create sample data
python setup.py
```

### 3. Run the Application

```bash
# Start the Streamlit application
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📁 Project Structure

```
educational-rag-system/
├── app.py                          # Main Streamlit application
├── setup.py                        # System initialization
├── test_system.py                  # Component testing
├── requirements.txt                 # Python dependencies
├── README.md                       # Project documentation
├── DEPLOYMENT.md                   # This deployment guide
├── data/                           # Data storage
│   ├── raw/                        # Raw educational content
│   ├── processed/                  # Processed content
│   ├── student_data/               # Student profiles and progress
│   └── vector_store/               # Vector database
├── src/                            # Core system components
│   ├── content_processor/          # Content processing
│   ├── vector_store/               # Vector database operations
│   ├── learning_path/              # Learning path generation
│   ├── student_management/         # Student tracking
│   ├── rag_engine/                 # RAG implementation
│   └── evaluation/                 # System evaluation
├── notebooks/                      # Jupyter notebooks
├── tests/                          # Unit tests
└── docs/                           # Documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Vector Store Configuration
VECTOR_STORE_PATH=data/vector_store
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Content Processing
MAX_CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MIN_CHUNK_SIZE=100

# Learning Path Settings
MIN_OBJECTIVES_PER_PATH=3
MAX_OBJECTIVES_PER_PATH=10
MIN_DURATION_PER_OBJECTIVE=15
MAX_DURATION_PER_OBJECTIVE=60
```

### Customizing the System

1. **Content Processing**: Modify `src/content_processor/` for custom content types
2. **Vector Store**: Adjust `src/vector_store/` for different embedding models
3. **Learning Paths**: Customize `src/learning_path/` for specific educational domains
4. **Student Management**: Extend `src/student_management/` for additional features

## 🧪 Testing

Run the test suite to verify system components:

```bash
python test_system.py
```

This will test:
- Module imports
- Content processing
- Vector store operations
- Student management
- Learning path generation
- Setup functionality

## 📊 Monitoring and Analytics

### System Metrics

The application provides real-time metrics:
- Content processing statistics
- Student engagement analytics
- Learning path effectiveness
- System performance indicators

### Logging

System logs are available in:
- Application logs: Check Streamlit console output
- Error logs: Monitor for exceptions and warnings
- Performance logs: Track system response times

## 🔒 Security Considerations

### Data Protection

1. **Student Data**: Ensure compliance with educational data privacy regulations
2. **Content Security**: Implement access controls for sensitive educational materials
3. **API Security**: Use authentication for external API integrations

### Best Practices

- Regularly backup student data and learning paths
- Monitor system access and usage patterns
- Implement proper error handling and logging
- Keep dependencies updated for security patches

## 🚀 Production Deployment

### Option 1: Streamlit Cloud

1. Push code to GitHub repository
2. Connect repository to Streamlit Cloud
3. Deploy automatically on code changes

### Option 2: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t educational-rag .
docker run -p 8501:8501 educational-rag
```

### Option 3: Traditional Server

1. Set up a Linux server with Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Run with process manager (systemd, supervisor, etc.)
4. Configure reverse proxy (nginx, Apache) for HTTPS

## 📈 Scaling Considerations

### Performance Optimization

1. **Vector Store**: Consider cloud vector databases (Pinecone, Weaviate) for large datasets
2. **Content Processing**: Implement batch processing for large content libraries
3. **Caching**: Add Redis for session and content caching
4. **Load Balancing**: Use multiple Streamlit instances behind a load balancer

### Database Scaling

For production use:
- Replace file-based storage with PostgreSQL/MySQL
- Use Redis for session management
- Implement proper database migrations

## 🔄 Maintenance

### Regular Tasks

1. **Content Updates**: Refresh educational content regularly
2. **Model Updates**: Update embedding models for better performance
3. **Student Data**: Archive old student records periodically
4. **System Monitoring**: Check logs and performance metrics

### Backup Strategy

1. **Student Data**: Daily backups of student profiles and progress
2. **Learning Paths**: Backup generated learning paths
3. **Content**: Version control for educational content
4. **System Configuration**: Backup configuration files

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Vector Store Issues**: Check disk space and permissions
3. **Content Processing Failures**: Verify file formats and encoding
4. **Performance Issues**: Monitor system resources and optimize

### Getting Help

1. Check the logs for error messages
2. Run `python test_system.py` to identify component issues
3. Review the README.md for detailed documentation
4. Check GitHub issues for known problems

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Chroma Vector Database](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Educational RAG Best Practices](https://example.com)

---

**Note**: This deployment guide covers the basic setup. For production deployments, consider additional security, monitoring, and scaling requirements specific to your use case. 