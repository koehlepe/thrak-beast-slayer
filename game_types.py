"""Type definitions and protocols for the game."""

from typing import NamedTuple


class EnemyStats(NamedTuple):
    """Statistics for an enemy type."""

    health: int
    attack: int
    defense: int
    points: int


class Vector2D(NamedTuple):
    """2D vector for position and direction."""

    x: int | float
    y: int | float
