# Contributing to AI-Self-Healing-Validation-System

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git
- GitHub account
- Basic understanding of FastAPI, Streamlit, and LangGraph

### Setup Development Environment

1. **Fork the Repository**
   ```bash
   # Fork the repository on GitHub
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/AI-Self-Healing-Validation-System.git
   cd AI-Self-Healing-Validation-System
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configurations
   ```

5. **Run Locally**
   ```bash
   python run_all.py
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add type hints where appropriate
- Include docstrings for functions and classes

### Project Structure

```
AI-Self-Healing-Validation-System/
├── app.py                 # FastAPI backend
├── ui.py                  # Streamlit frontend
├── agents.py              # AI agent implementations
├── tools.py               # Utility tools
├── graph.py              # LangGraph workflow
├── main.py               # Main workflow execution
├── config.py             # Configuration management
├── state.py              # State management
├── run_all.py            # Local development runner
├── requirements.txt      # Python dependencies
├── Dockerfile           # Frontend container
├── Dockerfile.backend   # Backend container
├── render.yaml           # Render deployment config
└── README.md            # Project documentation
```

## Types of Contributions

### 🐛 Bug Reports

1. **Search existing issues** before creating a new one
2. **Use descriptive title** for the issue
3. **Provide detailed information**:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
   - Screenshots if applicable

### ✨ Feature Requests

1. **Explain the problem** you're trying to solve
2. **Describe the proposed solution**
3. **Consider alternative approaches**
4. **Explain why this feature is valuable**

### 📝 Documentation

- Improve README.md
- Add inline code comments
- Create tutorials or guides
- Fix typos and grammatical errors

### 🔧 Code Contributions

#### Before You Start

1. **Create an issue** to discuss your changes
2. **Fork the repository** and create a new branch
3. **Follow the coding guidelines** mentioned above

#### Making Changes

1. **Make small, focused commits**
2. **Write clear commit messages**:
   ```
   type(scope): description
   
   examples:
   feat(ui): add new dashboard component
   fix(backend): resolve memory leak issue
   docs(docs): update API documentation
   ```

3. **Test your changes**:
   - Run the application locally
   - Test all affected features
   - Ensure no regressions

#### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Create pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes
   - Testing instructions

## Development Workflow

### 1. Setup
```bash
git checkout -b feature/your-feature-name
# Make your changes
```

### 2. Test
```bash
# Run backend
python app.py

# Run frontend (in separate terminal)
streamlit run ui.py

# Run both together
python run_all.py
```

### 3. Commit
```bash
git add .
git commit -m "feat(scope): add your feature description"
```

### 4. Push and Create PR
```bash
git push origin feature/your-feature-name
# Create pull request on GitHub
```

## Testing

### Manual Testing
- Test all API endpoints
- Verify Streamlit UI functionality
- Test self-healing workflow
- Check deployment configuration

### Automated Testing
Currently, the project uses simulated testing. Future improvements:
```bash
# Add unit tests
pytest tests/

# Add integration tests
pytest tests/integration/

# Add end-to-end tests
pytest tests/e2e/
```

## Code Review Guidelines

### For Reviewers
- Check code follows project standards
- Verify functionality works as expected
- Ensure documentation is updated
- Test the changes if possible

### For Contributors
- Respond to feedback promptly
- Make requested changes
- Explain your design decisions
- Be open to suggestions

## Deployment

### Local Development
```bash
# Development mode
python run_all.py

# Production mode
docker-compose up
```

### Render Deployment
- Changes to `render.yaml` require careful review
- Environment variables must be set in Render dashboard
- Test deployment in staging first

## Release Process

1. **Update version numbers** in relevant files
2. **Update CHANGELOG.md** with release notes
3. **Create release tag** on GitHub
4. **Deploy to production**
5. **Monitor for issues**

## Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Avoid personal attacks or criticism

### Communication
- Use GitHub issues for bug reports and feature requests
- Use discussions for general questions
- Be patient with response times
- Help others when you can

## Recognition

### Contributors
All contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributor statistics

### Ways to Contribute
- Code contributions
- Bug reports and feature requests
- Documentation improvements
- Community support
- Testing and feedback

## Getting Help

### Resources
- [Project Documentation](README.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [GitHub Issues](https://github.com/Adityakg05/AI-Self-Healing-Validation-System/issues)

### Contact
- Create GitHub issue for bugs or questions
- Join discussions for general conversation
- Mention maintainers for urgent issues

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

## Thank You!

Thank you for contributing to AI-Self-Healing-Validation-System! Your contributions help make this project better for everyone.

---

Remember: Every contribution matters, no matter how small. Whether it's fixing a typo, reporting a bug, or suggesting a new feature, we appreciate your help!
