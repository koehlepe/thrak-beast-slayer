# Development Guide

## Code Quality Standards

This project adheres to modern Python development standards:

### 1. **Type Hints (PEP 484)**
- All function signatures should include type hints
- Use `Optional[T]` for nullable types
- Use `List[T]`, `Dict[K, V]`, etc. from typing module

Example:
```python
def take_damage(self) -> bool:
    """Reduce health by 1 and return True if enemy defeated."""
    self.health -= 1
    if self.health <= 0:
        self.kill()
        return True
    return False
```

### 2. **Docstrings**
- All classes should have module-level docstrings
- All public methods should have docstring descriptions
- Use single-line docstrings for simple methods

Example:
```python
class Player(pygame.sprite.Sprite):
    """Stone Age player character - top-down warrior."""
    
    def shoot(self) -> None:
        """Fire a spear projectile from player position."""
```

### 3. **Code Style (PEP 8 + Black)**
- Maximum line length: 100 characters
- Use `make format` to auto-format code with Black
- No trailing whitespace
- Blank lines between class/function definitions

### 4. **Configuration Management**
- Use `config.py` for all magic numbers and constants
- Never hardcode values in function bodies
- Update `config.py` when adding new configurable parameters

Example:
```python
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
```

### 5. **Testing**
- Unit tests in `tests/` directory
- Use pytest for testing
- Run `make test` before committing

Example:
```bash
def test_player_takes_damage():
    player = Player()
    assert player.health == 3
    player.take_damage()
    assert player.health == 2
```

### 6. **Linting**
- Run `make lint` to check code quality
- Fix all lint errors before committing
- Tools: flake8 (style), pylint (issues)

### 7. **Type Checking**
- Run `make type-check` with mypy
- Resolve type warnings for better code reliability

## Refactoring Progress

### ✅ Complete
- [x] Project metadata (pyproject.toml)
- [x] Configuration module (config.py)
- [x] Type definitions (types.py)
- [x] Development tools setup (Makefile, requirements-dev.txt)
- [x] Initial type hints in main.py

### 📋 In Progress
- [ ] Add docstrings to all classes and methods
- [ ] Complete type hint migration
- [ ] Add error handling and validation
- [ ] Create test suite

### 🔄 Future Improvements
- [ ] Split main.py into multiple modules (sprites/, game_logic/, ui/)
- [ ] Create sprite factory for easier enemy creation
- [ ] Implement logging system
- [ ] Add game state manager
- [ ] Configuration file format (JSON/YAML)
- [ ] Performance profiling

## Common Development Tasks

### Format code:
```bash
make format
```

### Run linting:
```bash
make lint
```

### Type check:
```bash
make type-check
```

### Run all checks:
```bash
make lint && make type-check && make format
```

### Run game:
```bash
make run
```

## Best Practices

1. **Use type hints** for all new code
2. **Write docstrings** for public methods
3. **Follow PEP 8** style guidelines
4. **Test your changes** before committing
5. **Use configuration** for adjustable values
6. **Keep functions small** and focused
7. **Comment complex logic** but not obvious code
8. **Use meaningful variable names**

## Useful Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [PEP 484 Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Pygame Documentation](https://www.pygame.org/docs/)

## Git Workflow

1. Create feature branch: `git checkout -b feature/description`
2. Make changes and test
3. Format and lint: `make format && make lint`
4. Commit with clear message: `git commit -m "description"`
5. Push and create pull request

## Performance Tips

- Minimize sprite group iterations
- Cache frequently used calculations
- Use sprite groups efficiently
- Profile with: `python -m cProfile main.py`
