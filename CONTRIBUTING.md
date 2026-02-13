# Contributing to Supply Chain Analytics Dashboard

Thank you for contributing to our Supply Chain Analytics Dashboard! This interactive platform empowers supply chain managers in the fashion and beauty industry to make data-driven decisions through comprehensive visualization and analysis tools.

> **Note**: This contributing guide is adapted from the [GitHub Docs Contributing Guide](https://github.com/github/docs/blob/main/.github/CONTRIBUTING.md) and [Atom Contributing Guide](https://github.com/atom/atom/blob/master/CONTRIBUTING.md).

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branching Strategy](#branching-strategy)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Getting Help](#getting-help)

## Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms. We are committed to fostering an open, respectful, and inclusive environment for all contributors.

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Git** installed and configured
2. **Conda** or **Miniconda** installed
3. **Python 3.10+** (managed through conda)
4. Access to the team repository

### Setting Up Your Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/UBC-MDS/DSCI-532_2026_27_TBD.git
   cd DSCI-532_2026_27_TBD
   ```

2. **Create and activate the conda environment**:
   ```bash
   conda env create -f environment.yml
   conda activate supply-chain-dashboard
   ```

3. **Verify installation**:
   ```bash
   conda list  # Check installed packages
   ```

4. **Run the dashboard locally**:
   ```bash
   cd src
   python app.py
   ```
   The dashboard will be available at `http://localhost:8000`

## Development Workflow

We follow a collaborative workflow based on Git best practices:

1. **Create an issue** for the feature/bug you're working on (if not already exists)
2. **Assign yourself** to the issue
3. **Create a feature branch** from `main`
4. **Make your changes** following our code style guidelines
5. **Test your changes** thoroughly
6. **Submit a pull request** for review
7. **Address review feedback** if any
8. **Merge** after approval from at least one team member

## Branching Strategy

### Branch Naming Convention

Use descriptive branch names following this pattern:

```
<type>/<short-description>
```

**Types**:
- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests
- `style/` - Code style/formatting changes

**Examples**:
```
feature/add-interactive-filter
fix/data-loading-error
docs/update-readme
refactor/improve-plot-performance
```

### Protected Branches

- `main` - Production-ready code (protected)
- `dev` - Development integration branch (if used)

## Commit Message Guidelines

Write clear, concise commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semi-colons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(visualization): add shipping cost comparison by transportation mode

- Implement interactive bar chart using Plotly Express
- Add hover tooltips showing cost breakdown details
- Include filtering by route and supplier
- Color code by transportation mode (air, sea, rail, road)

Closes #12
```

```
fix(data): resolve missing value handling in supply chain dataset

The data loader was failing on rows with null supplier_quality values.
Implemented fillna() strategy using column median for numeric fields
and 'Unknown' for categorical fields.

Fixes #23
```

```
docs(proposal): complete Section 3 & 4 of M1 proposal

- Add dataset description and exploratory data analysis
- Include shipping cost analysis visualizations
- Document data cleaning and preprocessing steps

Closes #5
```

## Pull Request Process

### Before Submitting

- [ ] Code follows the project style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code sections
- [ ] Documentation updated (if applicable)
- [ ] No new warnings or errors introduced
- [ ] Tests added/updated (if applicable)
- [ ] Local testing performed

### Submitting a PR

1. **Push your branch** to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** with:
   - **Clear title** describing the change
   - **Description** explaining what and why
   - **Link to related issue** (e.g., "Closes #15")
   - **Screenshots/GIFs** for UI changes

3. **Request review** from at least one team member

4. **Address feedback** promptly and professionally

### PR Review Guidelines

When reviewing PRs:

- Be constructive and respectful
- Test the changes locally
- Check for code quality and consistency
- Verify documentation is updated
- Approve only when satisfied with the changes

## Code Style Guidelines

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Maximum line length: 88 characters (Black formatter default)
- Use docstrings for functions and classes

**Example**:
```python
def load_supply_chain_data(file_path: str) -> pd.DataFrame:
    """
    Load and preprocess supply chain data from CSV file.

    Performs data cleaning including handling missing values,
    standardizing column names, and validating data types.

    Parameters
    ----------
    file_path : str
        Path to the CSV file containing supply chain data
        (e.g., 'data/supply_chain_data.csv')

    Returns
    -------
    pd.DataFrame
        Preprocessed dataframe with columns:
        - shipping_cost: float
        - transportation_mode: str
        - route: str
        - supplier_quality: float
        - inventory_level: int

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist
    ValueError
        If required columns are missing
    """
    # Implementation
    pass
```

### Data Visualization

- **Color Schemes**: Use consistent, professional color palettes across all plots
  - Apply color-blind friendly palettes (e.g., viridis, plasma)
  - Use semantic colors (red for high costs, green for optimal performance)
- **Labels & Titles**: Ensure all plots have:
  - Clear, descriptive titles
  - Labeled axes with units (e.g., "Shipping Cost (USD)", "Quantity (units)")
  - Legends when multiple categories are shown
- **Interactivity**: Implement hover tooltips, zoom, and pan capabilities
- **Performance**: Optimize for large datasets (use aggregation, sampling where appropriate)
- **Supply Chain Specifics**:
  - Use appropriate chart types (bar charts for comparisons, heatmaps for route analysis)
  - Include trend lines where relevant
  - Show confidence intervals or error bars for predictions

### Dashboard Layout

- Maintain consistent spacing and alignment throughout the interface
- Use responsive design principles for different screen sizes
- Organize visualizations logically (group related metrics)
- Include clear filters and controls for user interaction
- Provide loading indicators for data-heavy operations
- Follow the design patterns established in the M1 proposal sketch

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_data_processing.py

# Run with coverage
pytest --cov=src tests/
```

### Writing Tests

- Write tests for new features
- Ensure tests are independent and reproducible
- Use descriptive test names
- Aim for meaningful test coverage

**Example**:
```python
def test_load_data_handles_missing_values():
    """Test that data loader correctly handles missing values in supply chain data."""
    # Arrange
    test_file = "tests/data/sample_with_nulls.csv"

    # Act
    df = load_supply_chain_data(test_file)

    # Assert
    assert df.isnull().sum().sum() == 0, "Missing values not properly handled"
    assert 'shipping_cost' in df.columns, "Missing required column"
    assert df['shipping_cost'].dtype in ['float64', 'int64'], "Invalid data type"

def test_shipping_cost_calculation():
    """Test shipping cost calculation for different transportation modes."""
    # Arrange
    test_data = pd.DataFrame({
        'transportation_mode': ['Air', 'Sea', 'Rail'],
        'distance': [1000, 5000, 2000],
        'weight': [100, 500, 300]
    })

    # Act
    result = calculate_shipping_cost(test_data)

    # Assert
    assert len(result) == 3, "Should return cost for all modes"
    assert result['Air'].iloc[0] > result['Sea'].iloc[0], "Air should be more expensive than sea"
```

## Documentation

### Code Comments

- Comment complex logic and algorithms
- Explain "why" not "what" (code shows what)
- Keep comments up-to-date with code changes
- Use TODO comments for future improvements

### README Updates

When adding features that affect usage:

- Update installation instructions
- Add usage examples
- Update dependencies list
- Revise troubleshooting section if needed

## Getting Help

### Team Communication

- **Slack/Discord**: For quick questions and discussions
- **GitHub Issues**: For bug reports and feature requests
- **Team Meetings**: For major decisions and planning

### Resources

**Project Documentation:**
- [Project README](README.md) - Setup and overview
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community standards
- [Branch Structure](BRANCH_STRUCTURE.md) - Branching strategy
- [M1 Proposal](reports/m1_proposal.md) - Project proposal and design

**Learning Resources:**
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Plotly Documentation](https://plotly.com/python/)
- [Dash Documentation](https://dash.plotly.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

**Course Materials:**
- [DSCI 532 Course Repository](https://github.com/UBC-MDS/DSCI_532_viz-2)
- [DSCI 524 Collaborative Software Development](https://github.com/UBC-MDS/DSCI_524_collab-sw-dev)

## Project Team

This project is maintained by:
- [@roccolee18](https://github.com/roccolee18)
- [@amanbinepal](https://github.com/amanbinepal)
- [@junliliu1](https://github.com/junliliu1)

## Attribution

This contributing guide is adapted from:
- [GitHub Docs Contributing Guide](https://github.com/github/docs/blob/main/.github/CONTRIBUTING.md)
- [Atom Contributing Guide](https://github.com/atom/atom/blob/master/CONTRIBUTING.md)

---

## Questions or Suggestions?

Thank you for contributing to the Supply Chain Analytics Dashboard.

If you have questions or suggestions about this contributing guide, please:
- Open an issue on GitHub
- Contact the team members
- Bring it up during team meetings

We appreciate your contributions to making supply chain management more data-driven and efficient.
