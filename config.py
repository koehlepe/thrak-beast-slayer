"""Game configuration constants."""

# Screen dimensions
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60

# Timing (milliseconds)
WAVE_DELAY: int = 3000

# Game phases
PHASE_STONE_AGE: int = 0
PHASE_BRONZE_AGE: int = 1
PHASE_IRON_AGE: int = 2

# Game states
MENU: int = 0
PLAYING: int = 1
GAME_OVER: int = 2
DEV_MENU: int = 3

# Stone Age configuration
STONE_AGE_WAVES: int = 5
PLAYER_HEALTH_STONE: int = 3
PLAYER_SPEED_STONE: int = 5
SPEAR_SPEED: int = 7
SPAWN_COOLDOWN: int = 10

# Bronze Age configuration
BRONZE_AGE_WAVES: int = 3
BRONZE_LEVEL_WIDTH: int = 3000
PLAYER_HEALTH_BRONZE: int = 3
PLAYER_SPEED_BRONZE: int = 4
GRAVITY: float = 0.5
JUMP_POWER: int = 12

# Iron Age configuration
IRON_AGE_WAVES: int = 3
IRON_MAP_WIDTH: int = 2000
IRON_MAP_HEIGHT: int = 1500
PLAYER_HEALTH_IRON: int = 5
PLAYER_SPEED_IRON: int = 4
BATTLE_COLLISION_DISTANCE: int = 80

# Enemy configuration
ENEMY_TYPES: list[str] = ["tiger", "wolf", "mammoth", "scorpion", "pterodactyl"]
INITIAL_ENEMY_COUNT: int = 3
MAX_ENEMIES_PER_WAVE: int = 8

# Iron Age enemy configuration
IRON_ENEMY_TYPES: dict[str, dict] = {
    "warrior": {"health": 10, "attack": 2, "defense": 1, "points": 50},
    "knight": {"health": 15, "attack": 3, "defense": 2, "points": 100},
    "warlord": {"health": 20, "attack": 4, "defense": 3, "points": 200},
}
IRON_SPAWN_GROUPS: int = 5
IRON_GROUP_SIZE_MIN: int = 1
IRON_GROUP_SIZE_MAX: int = 3
