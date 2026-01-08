# Quick Start Guide

## 🚀 Getting Started

### First Time Setup
```bash
# Install development tools
pip install -r requirements-dev.txt

# Verify everything works
python -c "from config import *; from game_types import *; print('✓ Setup complete!')"
```

### Run the Game
```bash
make run
# OR
python main.py
```

## 📋 Daily Development Workflow

### 1. Before Starting Work
```bash
# Ensure all dependencies are installed
pip install -r requirements-dev.txt
```

### 2. After Making Changes
```bash
# Format your code
make format

# Check for issues
make lint

# Check types
make type-check
```

### 3. Before Committing
```bash
# Run all quality checks
make lint && make type-check && make format

# Run tests (when available)
make test
```

## 🛠️ Useful Commands

| Command | Purpose |
|---------|---------|
| `make run` | Play the game |
| `make format` | Auto-format code with Black |
| `make lint` | Check code quality |
| `make type-check` | Find type errors |
| `make test` | Run unit tests |
| `make clean` | Remove build artifacts |
| `make help` | Show all commands |

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Game features & how to play |
| `DEVELOPMENT.md` | Coding standards & best practices |
| `MODERNIZATION.md` | What was improved & why |
| `CHECKLIST.md` | Tasks to complete |
| `SUMMARY.md` | Overview of changes |
| `config.py` | Game constants & settings |

## 🎮 Playing the Game

### Main Menu
- Press **SPACE** to start
- Press **D** to access Developer Mode

### Game Phases
1. **Stone Age** - Defend against beasts (top-down)
   - Includes looping background music and short SFX. Generated WAVs are placed in `assets/sounds/` on first run.
2. **Bronze Age** - Platformer with warriors
3. **Iron Age** - RPG with turn-based battles

See `README.md` for detailed game instructions.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'pygame'"
```bash
pip install pygame==2.5.2
```

### "ModuleNotFoundError: No module named 'config'"
Make sure you're running from the project root:
```bash
cd C:\Users\koehl\Development\thrak-beast-slayer
python main.py
```

### "Black/flake8 not found"
Install dev dependencies:
```bash
pip install -r requirements-dev.txt
```

## 📝 Coding Standards

### Adding New Constants
✅ **DO:** Add to `config.py`
```python
NEW_SETTING: int = 100
```

✅ **DO:** Import from config
```python
from config import NEW_SETTING
```

❌ **DON'T:** Hardcode values in functions
```python
enemy_health = 100  # Bad! Use config instead
```

### Writing Functions
✅ **DO:** Add type hints and docstrings
```python
def take_damage(self) -> bool:
    """Reduce health by 1 and return True if defeated."""
    self.health -= 1
    return self.health <= 0
```

❌ **DON'T:** Skip type hints
```python
def take_damage(self):
    self.health -= 1
```

## 🎯 Next Steps

1. **Read** `DEVELOPMENT.md` for detailed guidelines
2. **Review** `CHECKLIST.md` for what to work on next
3. **Code** following the standards
4. **Test** with `make test` when tests are available
5. **Commit** after running quality checks

## 📊 Project Status

**Current Phase**: Infrastructure Complete ✅  
**Type Hints**: 30% complete 🔄  
**Docstrings**: 40% complete 🔄  
**Tests**: Not started 📋  

See `CHECKLIST.md` for detailed progress tracking.

## 🎓 Learning Resources

- [Python PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Black Formatter](https://black.readthedocs.io/)
- [Pygame Docs](https://www.pygame.org/docs/)

## 💡 Tips

1. **Use `make` commands** - They handle formatting and checking
2. **Read docstrings** - They explain what code does
3. **Follow config.py pattern** - Add constants there
4. **Use type hints** - Help catch bugs early
5. **Format before committing** - Keeps code clean

## 🚦 Quick Command Reference

```bash
# Setup
pip install -r requirements-dev.txt

# Development
make format  # Format code
make lint    # Check code
make run     # Play game

# Quality
make type-check  # Type checking
make test        # Run tests (when available)

# Cleanup
make clean   # Remove artifacts
```

---

**Ready to code?** Start with `make run` to play, then read `DEVELOPMENT.md` for standards!
