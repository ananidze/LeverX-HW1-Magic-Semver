# LeverX-HW1-Magic-Semver
Implements a `Version` class for comparing semantic versions (per [semver.org](https://semver.org)).

## Examples

```python
>>> Version('1.1.3') < Version('2.2.3')
True
>>> Version('1.0.1b') < Version('1.0.10-alpha.beta')
True
```

## Usage

Run tests:

```bash
uv run main.py
```
