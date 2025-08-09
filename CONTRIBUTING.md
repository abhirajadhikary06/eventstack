# Contributing to EventStack

Thank you for your interest in contributing to EventStack! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Project Overview](#project-overview)
  - [Development Environment Setup](#development-environment-setup)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Workflow](#development-workflow)
  - [Branching Strategy](#branching-strategy)
  - [Commit Messages](#commit-messages)
  - [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Communication](#communication)

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Project Overview

EventStack is a platform for managing, organizing, and stacking events efficiently. It's built with Python using the Tornado web framework and SQLite for data storage. The application features:

- User authentication via GitHub
- Event creation and management
- Time slot voting system
- Real-time updates via WebSockets
- Responsive UI

### Development Environment Setup

1. **Fork and Clone the Repository**

   ```bash
   git clone https://github.com/abhirajadhikary06/eventstack.git
   cd eventstack
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**

   Create a `.env` file in the root directory with the following variables:

   ```
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   COOKIE_SECRET=your_secure_cookie_secret
   ```

5. **Run the Application**

   ```bash
   python main.py
   ```

   The application will be available at http://localhost:5000

## How to Contribute
There are many ways to contribute:

📃 Improve documentation

🐞 Report or fix bugs

✨ Add new features

🎨 Improve UI/UX


### Reporting Bugs

Before submitting a bug report:

1. Check the issue tracker to see if the bug has already been reported
2. If not, create a new issue with the "bug" label
3. Include detailed steps to reproduce the bug
4. Include screenshots if applicable
5. Describe the expected behavior and what actually happened
6. Include your environment details (OS, browser, etc.)

### Suggesting Enhancements

For feature requests:

1. Check the issue tracker to see if the enhancement has already been suggested
2. If not, create a new issue with the "enhancement" label
3. Clearly describe the feature and its benefits
4. If possible, outline how the feature might be implemented

### Pull Requests

1. Create a new branch from `main` for your changes
2. Make your changes following our [code style guidelines](#code-style)
3. Add or update tests as necessary
4. Update documentation as needed
5. Submit a pull request to the `main` branch
6. In your PR description, reference any related issues using keywords like "Fixes #123" or "Closes #456"

## Development Workflow

### Branching Strategy

- `main`: The primary branch containing stable code
- Feature branches: Create from `main` using the naming convention `feature/your-feature-name`
- Bug fix branches: Create from `main` using the naming convention `fix/issue-description`

### Commit Messages

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Example:
```
Add event filtering by date range

Implements the ability to filter events by start and end dates.
Closes #123
```

### Code Style

- Follow PEP 8 style guidelines for Python code
- Use 4 spaces for indentation (not tabs)
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused on a single task

## Testing

We encourage writing tests for new features and bug fixes. To run tests:

```bash
# Future test command will be added here
```

## Documentation

Please update documentation when adding or modifying features:

- Update README.md if necessary
- Add inline comments for complex code
- Update function docstrings
- If adding new API endpoints, document them appropriately

## Communication
If you have questions, suggestions, or need help:

Start a discussion in the GitHub Discussions (if enabled).

Open a new issue if you're facing a bug or want to propose an enhancement.

For urgent matters, mention maintainers directly in your issue or PR using @maintainer-username.

Stay respectful, constructive, and inclusive in all your interactions.
---

Thank you for contributing to EventStack! Your efforts help make this project better for everyone.