# Contributing to Multi-Program Launcher

Thank you for your interest in contributing to Multi-Program Launcher! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Windows OS (for testing)
- Git

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/multi-program-launcher.git
   cd multi-program-launcher
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the launcher**
   ```bash
   python launcher_main.py
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and concise

### Project Structure

```
multi-program-launcher/
├── launcher_main.py          # Main entry point
├── config_manager.py         # Configuration management
├── program_manager.py        # Program execution and management
├── ui_manager.py            # User interface management
├── monitor_manager.py       # Process monitoring
├── logger.py                # Logging functionality
├── config.yml               # Configuration file
├── requirements.txt         # Python dependencies
├── build_exe.py            # Build script for executable
└── README.md               # Documentation
```

### Testing

Before submitting changes:

1. **Test functionality**
   - Run the launcher and test basic operations
   - Test program execution with different file types
   - Test position adjustment functionality
   - Test error handling

2. **Test building**
   ```bash
   python build_exe.py
   ```
   - Verify the executable builds successfully
   - Test the built executable

3. **Code review**
   - Review your changes for potential issues
   - Ensure error handling is appropriate
   - Check for memory leaks or performance issues

## Submitting Changes

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Implement the feature or fix
   - Add tests if applicable
   - Update documentation if needed

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template

### Commit Message Guidelines

Use clear, descriptive commit messages:

- **Format**: `type: brief description`
- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- **Examples**:
  - `feat: add support for custom window sizes`
  - `fix: resolve PowerShell execution policy issue`
  - `docs: update installation instructions`

### Pull Request Template

When creating a PR, include:

- **Description**: What the change does
- **Type of change**: Bug fix, feature, documentation, etc.
- **Testing**: How you tested the changes
- **Screenshots**: If UI changes are involved
- **Breaking changes**: Any breaking changes

## Areas for Contribution

### High Priority

- **Bug fixes**: Any issues reported in the Issues section
- **Performance improvements**: Optimize program execution or UI responsiveness
- **Error handling**: Improve error messages and recovery

### Medium Priority

- **New features**: Additional functionality that fits the project scope
- **UI improvements**: Better user experience and interface design
- **Documentation**: Improve README, add examples, create tutorials

### Low Priority

- **Code refactoring**: Improve code structure and maintainability
- **Testing**: Add unit tests or integration tests
- **CI/CD**: Set up automated testing and deployment

## Reporting Issues

### Bug Reports

When reporting bugs, include:

1. **System information**
   - Windows version
   - Python version
   - Launcher version

2. **Steps to reproduce**
   - Detailed steps to reproduce the issue
   - Expected vs actual behavior

3. **Error messages**
   - Full error messages or logs
   - Screenshots if applicable

4. **Additional context**
   - Programs being launched
   - Configuration settings
   - Recent changes

### Feature Requests

When requesting features:

1. **Clear description** of the desired functionality
2. **Use case** explaining why it's needed
3. **Implementation suggestions** if you have ideas
4. **Priority level** (high/medium/low)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and constructive
- Focus on what is best for the community

### Enforcement

- Unacceptable behavior will not be tolerated
- Maintainers will remove, edit, or reject comments and commits
- Violations may result in temporary or permanent ban

## Getting Help

If you need help:

1. **Check existing issues** for similar problems
2. **Search documentation** for relevant information
3. **Ask questions** in the Issues section
4. **Join discussions** in the community

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Multi-Program Launcher! 