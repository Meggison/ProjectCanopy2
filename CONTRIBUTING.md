# Contributing to Project Canopy 2

Thank you for your interest in contributing to Project Canopy 2! This document provides guidelines for contributing to our forest monitoring project.

## 🌟 Ways to Contribute

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Submit improvements and new features
- **Documentation**: Improve project documentation
- **Data Contributions**: Share relevant datasets or ground truth data

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Google Earth Engine account (for satellite data access)
- Basic knowledge of machine learning and geospatial data

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork the repo on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/ProjectCanopy2.git
   cd ProjectCanopy2
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Google Earth Engine**
   ```bash
   earthengine authenticate
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maximum line length: 88 characters (Black formatter standard)

### Example Function Documentation
```python
def process_satellite_data(image_path: str, mask_path: str) -> np.ndarray:
    """
    Process satellite imagery and corresponding masks.
    
    Args:
        image_path (str): Path to the satellite image file
        mask_path (str): Path to the corresponding mask file
    
    Returns:
        np.ndarray: Processed image array
    
    Raises:
        FileNotFoundError: If input files don't exist
    """
    # Function implementation here
    pass
```

### Jupyter Notebooks
- Clear markdown documentation between code cells
- Remove output before committing (use `jupyter nbconvert --clear-output`)
- Include cell execution order and dependencies
- Add summary comments for complex operations

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_preprocessing.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Writing Tests
- Write unit tests for all new functions
- Use descriptive test names
- Include edge cases and error conditions
- Mock external dependencies (GEE, file I/O)

## 📊 Data Guidelines

### Dataset Contributions
- Ensure data has proper licensing for open source use
- Include metadata and documentation
- Use standard geospatial formats (GeoTIFF, GeoJSON)
- Provide clear geographic and temporal context

### Ground Truth Data
- Include accuracy assessment information
- Document collection methodology
- Specify coordinate reference system
- Provide data quality metrics

## 🔄 Pull Request Process

### Before Submitting
1. **Test your changes** thoroughly
2. **Update documentation** if needed
3. **Add/update tests** for new functionality
4. **Run code formatting**:
   ```bash
   black src/ tests/
   isort src/ tests/
   ```

### Pull Request Checklist
- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with main branch

### Commit Message Format
```
type(scope): short description

Longer description if needed

- Bullet point for specific changes
- Another bullet point

Closes #123
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Examples**:
- `feat(preprocessing): add Sentinel-3 data support`
- `fix(models): resolve memory leak in training loop`
- `docs(readme): update installation instructions`

## 🐛 Issue Reporting

### Bug Reports
Please include:
- **Environment details** (OS, Python version, package versions)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and stack traces
- **Sample data** if relevant (ensure no sensitive information)

### Feature Requests
Please include:
- **Clear description** of the proposed feature
- **Use case** and motivation
- **Possible implementation** approach
- **Alternative solutions** considered

## 📋 Project Areas

### High Priority Areas
- **Model Performance**: Improving segmentation accuracy
- **Scalability**: Processing larger geographic areas
- **Real-time Processing**: Reducing latency for time-sensitive applications
- **Documentation**: User guides and API documentation

### Specialized Contributions
- **GIS Expertise**: Geospatial processing optimization
- **Remote Sensing**: Satellite data analysis improvements
- **ML Engineering**: Model deployment and serving
- **UI/UX**: Visualization and user interface development

## 🤝 Code of Conduct

### Our Standards
- **Respectful**: Treat all community members with respect
- **Inclusive**: Welcome contributors from all backgrounds
- **Collaborative**: Work together towards common goals
- **Professional**: Maintain professional communication

### Unacceptable Behavior
- Harassment or discrimination of any kind
- Offensive comments or personal attacks
- Sharing others' private information
- Inappropriate use of project resources

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Technical questions and bug reports
- **GitHub Discussions**: General questions and ideas
- **Project Website**: [www.projectcanopy.org](https://www.projectcanopy.org)

### Mentorship
New contributors are welcome! We're happy to help you get started:
- Look for issues labeled `good first issue`
- Ask questions in GitHub Discussions
- Request code review and feedback

## 🏆 Recognition

Contributors will be recognized through:
- **Contributors list** in README
- **Release notes** for significant contributions
- **Project credits** on website and publications

Thank you for contributing to forest conservation through technology! 🌲

---

*For additional questions, please open an issue or visit our project website.*