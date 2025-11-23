# Galaga Spear

A simple Galaga-like arcade game built with Python and Pygame.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python main.py
```

## Game Instructions

### Menu
- Press **SPACE** to start the game

### Gameplay
- **LEFT/RIGHT Arrow Keys** - Move your spaceship left and right
- **SPACE** - Shoot at enemies
- Destroy all enemies to advance to the next wave
- Avoid enemy fire and collisions with enemies
- Each enemy destroyed is worth 100 points

### Game Over
- Press **SPACE** to return to the menu

## Features

- **Progressive Waves**: Each wave spawns more enemies and becomes increasingly challenging
- **Health System**: You start with 3 health points; lose them all and it's game over
- **Scoring System**: Earn 100 points for each enemy destroyed
- **Enemy AI**: Enemies move horizontally while descending and fire randomly
- **Collision Detection**: Full collision detection between bullets, enemies, and the player
- **Wave Progression**: Complete each wave by destroying all spawned enemies

## Game Mechanics

- Player ship spawns at the bottom center of the screen
- Enemies spawn at the top and move downward diagonally
- You can shoot one bullet at a time (with cooldown)
- Enemies also shoot back at random intervals
- Touching an enemy or getting hit by enemy fire damages your health
- The game ends when your health reaches 0

## Controls Summary

| Control | Action |
|---------|--------|
| SPACE (Menu) | Start Game |
| LEFT ARROW | Move Left |
| RIGHT ARROW | Move Right |
| SPACE (Playing) | Shoot |
| SPACE (Game Over) | Return to Menu |

Enjoy the game!
