# THRAK: Beast Slayer

A multi-phase arcade game built with Python and Pygame featuring three distinct game phases across the ages of human civilization.

## Quick Start

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the game:**
```bash
python main.py
```

## Game Features

### Three Distinct Phases

1. **Stone Age** - Top-down wave-based shooting
   - Defend against prehistoric beasts
   - Survive 5 waves of increasingly difficult enemies
   - Earn points to progress

2. **Bronze Age** - Side-scrolling platformer
   - Navigate treacherous terrain
   - Defeat armored warriors
   - Complete 3 levels to advance

3. **Iron Age** - 2D RPG with turn-based battles
   - Explore a vast map
   - Encounter enemy groups for strategic turn-based combat
   - Manage health and resources

### Game Instructions

#### Menu
- Press **SPACE** to start the game
- Press **D** to access Developer Mode

#### Stone Age (Wave Combat)
- **LEFT/RIGHT Arrow Keys** - Move left and right
- **SPACE** - Throw spear at enemies
- Destroy all enemies to advance to the next wave

#### Bronze Age (Platformer)
- **LEFT/RIGHT Arrow Keys** - Move horizontally
- **SPACE** - Jump
- **S** - Swing sword
- Reach the level end to progress

#### Iron Age (RPG)
- **Arrow Keys or WASD** - Move around the map
- **SPACE** - Attack in battle
- **H** - Heal in battle
- Encounter and defeat enemy groups

#### Developer Mode
- Press **1** - Test Stone Age
- Press **2** - Test Bronze Age
- Press **3** - Test Iron Age
- Press **0** - Return to main menu

## Development

### Prerequisites
- Python 3.9+
- pip

### Setting Up Development Environment

1. **Install development dependencies:**
```bash
pip install -r requirements-dev.txt
```

2. **Format code with Black:**
```bash
make format
```

3. **Run linting checks:**
```bash
make lint
```

4. **Type checking:**
```bash
make type-check
```

5. **Run tests:**
```bash
make test
```

### Code Style

This project follows:
- **PEP 8** - Python style guide
- **Black** - Code formatter (100 char line length)
- **Type Hints** - PEP 484 type annotations (where practical)

### Development Workflow

1. Make your changes
2. Run `make format` to format code
3. Run `make lint` to check for issues
4. Run `make test` to verify functionality
5. Commit your changes

### Project Structure

```
thrak-beast-slayer/
├── main.py              # Main game entry point
├── config.py            # Configuration constants
├── types.py             # Type definitions
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── pyproject.toml       # Project metadata and tool config
├── pytest.ini           # Pytest configuration
├── .flake8              # Flake8 configuration
├── Makefile             # Development tasks
└── README.md            # This file
```

## Features

- **Progressive Difficulty** - Enemies become stronger across phases
- **Health System** - Manage limited health resources
- **Scoring System** - Earn points for defeating enemies
- **Wave Progression** - Advance through increasingly challenging content
- **Collision Detection** - Accurate hit detection for all game mechanics
- **Multiple Game Modes** - Unique gameplay in each age
- **Developer Mode** - Test individual game phases

## Controls Summary

| Control | Action |
|---------|--------|
| **SPACE** (Menu) | Start Game |
| **D** (Menu) | Developer Mode |
| **Arrow Keys** | Move |
| **SPACE** (Game) | Interact/Shoot/Jump |
| **S** (Bronze Age) | Swing Sword |
| **H** (Iron Age Battle) | Heal |
| **SPACE** (Game Over) | Return to Menu |

## Game Mechanics

### Combat System
- Different attack types for each phase
- Enemy variety with unique behavior patterns
- Damage calculation and health management
- Victory and defeat conditions

### Progression System
- Complete waves/levels to advance phases
- Carry over health and score between phases
- Increasingly challenging enemy waves
- Final victory after all phases complete

## Troubleshooting

**Game won't start:**
- Ensure pygame is installed: `pip install pygame`
- Check Python version: `python --version` (3.9+)

**Performance issues:**
- Lower screen resolution in config.py
- Reduce enemy spawn rate in wave functions

## License

MIT License

## Enjoy the game!

Become THRAK, the legendary beast slayer!

