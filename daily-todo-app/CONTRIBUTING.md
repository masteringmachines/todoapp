# Contributing to Daily Todo App

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported in Issues
- Include detailed steps to reproduce
- Provide system information (OS, Python version)
- Include error messages and logs

### Suggesting Features

- Check existing feature requests first
- Clearly describe the feature and its use case
- Explain how it would benefit users

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Include type hints where appropriate
   - Add unit tests for new functionality

4. **Run tests**
   ```bash
   pytest tests/
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Ensure all tests pass

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/daily-todo-app.git
cd daily-todo-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8

# Run tests
pytest tests/ -v
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular
- Maximum line length: 88 characters

## Testing Guidelines

- Write tests for all new features
- Ensure existing tests pass
- Aim for good code coverage
- Test edge cases

## Feature Ideas

Some areas where contributions would be especially welcome:

- **Calendar Integration**: Sync with Google Calendar, Outlook
- **Cloud Sync**: Multi-device synchronization
- **Themes**: Additional color schemes and UI themes
- **Templates**: Pre-built task templates
- **Habit Tracking**: Daily habit monitoring
- **Team Features**: Collaboration and sharing
- **Voice Input**: Voice-to-text task creation
- **Weather Integration**: Real weather API integration
- **Mobile App**: Companion mobile application
- **AI Suggestions**: ML-based task recommendations

## Documentation

- Update README.md if adding new features
- Add docstrings to all public functions
- Include usage examples for new features

## Questions?

Feel free to open an issue for any questions or concerns.

## Code of Conduct

Be respectful and inclusive. We want this to be a welcoming community for everyone.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make Daily Todo App better! 🙏
