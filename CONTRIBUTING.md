# Contributing to Adminova

Thank you for your interest in contributing to Adminova! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect differing viewpoints

## How to Contribute

### Reporting Bugs

1. **Check existing issues** - Search to see if the bug has already been reported
2. **Create a new issue** - If the bug hasn't been reported, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, Django version)

### Suggesting Enhancements

1. **Check existing issues and pull requests** - Ensure the enhancement hasn't been suggested
2. **Create a new issue** with:
   - Clear description of the enhancement
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** - `git checkout -b feature/your-feature-name`
3. **Make your changes** - Follow the coding standards below
4. **Write/update tests** - Ensure your code is tested
5. **Update documentation** - Add/update relevant documentation
6. **Commit your changes** - Use clear, descriptive commit messages
7. **Push to your fork** - `git push origin feature/your-feature-name`
8. **Create a Pull Request** - Provide a clear description of your changes

## Development Setup

1. **Clone your fork**
```bash
git clone https://github.com/YOUR_USERNAME/adminova-django-dashboard.git
cd adminova-django-dashboard
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements/local.txt
```

4. **Set up environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Run tests**
```bash
pytest
```

## Coding Standards

### Python/Django

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Write docstrings for classes and functions
- Keep functions focused and small
- Use type hints where appropriate

### Code Formatting

Use Black for code formatting:
```bash
black .
```

Use isort for import sorting:
```bash
isort .
```

Check code with flake8:
```bash
flake8 .
```

### Testing

- Write tests for new features
- Maintain or improve test coverage
- Run tests before submitting PR
- Use pytest for testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific test file
pytest apps/payments/tests/test_mpesa.py
```

### Commit Messages

Write clear, concise commit messages:

```
Add M-Pesa payment retry mechanism

- Implement exponential backoff for failed payments
- Add retry count to payment model
- Update callback handler to process retries
- Add tests for retry logic
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description if needed
- Reference issues: `Fixes #123`, `Relates to #456`

## Project Structure

```
adminova-django-dashboard/
├── apps/                   # Django applications
│   ├── core/              # Core utilities
│   ├── users/             # User management
│   ├── subscriptions/     # Subscription system
│   ├── payments/          # Payment processing
│   └── dashboard/         # Dashboard views
├── adminova/              # Project configuration
├── docs/                  # Documentation
├── requirements/          # Dependencies
└── tests/                 # Test suite
```

## Testing Guidelines

### Unit Tests

- Test individual functions and methods
- Mock external dependencies
- Use fixtures for common setup

### Integration Tests

- Test API endpoints
- Test database interactions
- Test M-Pesa integration (sandbox)

### Test Coverage

Maintain minimum 80% coverage:
```bash
pytest --cov=apps --cov-report=html
```

## Documentation

- Update README.md for user-facing changes
- Update API documentation for API changes
- Add docstrings to new functions/classes
- Update relevant guides in `docs/`

## Review Process

1. Maintainers will review your PR
2. Address feedback and make requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited in the changelog

## Questions?

- Open an issue for questions
- Email: cavin.otieno012@gmail.com
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you for contributing to Adminova! Your efforts help make this project better for everyone.

---

Created by Cavin Otieno
