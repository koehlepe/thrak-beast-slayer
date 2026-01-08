"""THRAK: Beast Slayer - A multi-phase arcade game.

Features three distinct gameplay phases across historical eras:
- Stone Age: Wave-based top-down shooting
- Bronze Age: Side-scrolling platformer
- Iron Age: 2D RPG with turn-based battles
"""

import pygame
import random
import math
from typing import Optional, List, Tuple

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WAVE_DELAY,
    PHASE_STONE_AGE,
    PHASE_BRONZE_AGE,
    PHASE_IRON_AGE,
    MENU,
    PLAYING,
    GAME_OVER,
    DEV_MENU,
    STONE_AGE_WAVES,
    PLAYER_HEALTH_STONE,
    PLAYER_SPEED_STONE,
    SPEAR_SPEED,
    SPAWN_COOLDOWN,
    BRONZE_AGE_WAVES,
    BRONZE_LEVEL_WIDTH,
    PLAYER_HEALTH_BRONZE,
    PLAYER_SPEED_BRONZE,
    GRAVITY,
    JUMP_POWER,
    IRON_AGE_WAVES,
    IRON_MAP_WIDTH,
    IRON_MAP_HEIGHT,
    PLAYER_HEALTH_IRON,
    PLAYER_SPEED_IRON,
    BATTLE_COLLISION_DISTANCE,
    ENEMY_TYPES,
    INITIAL_ENEMY_COUNT,
    MAX_ENEMIES_PER_WAVE,
    IRON_ENEMY_TYPES,
    IRON_SPAWN_GROUPS,
    IRON_GROUP_SIZE_MIN,
    IRON_GROUP_SIZE_MAX,
)

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("THRAK: Beast Slayer")
clock: pygame.time.Clock = pygame.time.Clock()
font_large: pygame.font.Font = pygame.font.Font(None, 72)
font_medium: pygame.font.Font = pygame.font.Font(None, 36)
font_small: pygame.font.Font = pygame.font.Font(None, 24)


class Player(pygame.sprite.Sprite):
    """Stone Age player character - top-down warrior."""

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 60), pygame.SRCALPHA)
        # Head
        pygame.draw.circle(self.image, (200, 150, 100), (25, 12), 10)
        # Hair/wild mane
        pygame.draw.circle(self.image, (100, 50, 0), (25, 8), 12)
        pygame.draw.circle(self.image, (100, 50, 0), (18, 10), 8)
        pygame.draw.circle(self.image, (100, 50, 0), (32, 10), 8)
        # Body
        pygame.draw.rect(self.image, (139, 69, 19), (15, 22, 20, 18))
        # Arms
        pygame.draw.line(self.image, (200, 150, 100), (15, 25), (5, 35), 4)
        pygame.draw.line(self.image, (200, 150, 100), (35, 25), (45, 35), 4)
        # Legs
        pygame.draw.line(self.image, (80, 40, 20), (18, 40), (15, 55), 4)
        pygame.draw.line(self.image, (80, 40, 20), (32, 40), (35, 55), 4)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed = PLAYER_SPEED_STONE
        self.health = PLAYER_HEALTH_STONE
        self.score = 0

    def update(self) -> None:
        """Update player position based on keyboard input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += self.speed

    def shoot(self) -> None:
        """Fire a spear projectile from player position."""
        spear = Spear(self.rect.centerx, self.rect.top)
        all_sprites.add(spear)
        spears.add(spear)


class Spear(pygame.sprite.Sprite):
    """Projectile weapon fired by Stone Age player."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.image = pygame.Surface((12, 30), pygame.SRCALPHA)
        # Spear shaft
        pygame.draw.line(self.image, (139, 69, 19), (6, 0), (6, 25), 3)
        # Spear head
        pygame.draw.polygon(self.image, (200, 200, 200), [(6, 0), (2, 8), (6, 5), (10, 8)])
        # Feathers/fletching
        pygame.draw.polygon(self.image, (255, 200, 0), [(3, 20), (6, 28), (9, 20)])
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.speed = SPEAR_SPEED

    def update(self) -> None:
        """Move spear upward and remove if off-screen."""
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """Stone Age enemy - prehistoric beasts."""

    def __init__(self, x: float, y: float, enemy_type: str) -> None:
        super().__init__()
        self.enemy_type = enemy_type
        self.health = 1

        if enemy_type == "tiger":
            self.image = pygame.Surface((60, 50), pygame.SRCALPHA)
            # Body
            pygame.draw.ellipse(self.image, (255, 140, 0), (10, 15, 40, 20))
            # Head
            pygame.draw.circle(self.image, (255, 160, 20), (45, 20), 12)
            # Stripes
            pygame.draw.line(self.image, (200, 80, 0), (15, 18), (20, 28), 2)
            pygame.draw.line(self.image, (200, 80, 0), (25, 15), (30, 28), 2)
            pygame.draw.line(self.image, (200, 80, 0), (35, 15), (38, 28), 2)
            # Fangs
            pygame.draw.line(self.image, (255, 255, 255), (50, 28), (52, 35), 2)
            pygame.draw.line(self.image, (255, 255, 255), (56, 28), (58, 35), 2)
            # Tail
            pygame.draw.line(self.image, (200, 100, 0), (10, 22), (0, 15), 3)
            self.speed = 2.5
            self.points = 100

        elif enemy_type == "wolf":
            self.image = pygame.Surface((55, 45), pygame.SRCALPHA)
            # Body
            pygame.draw.ellipse(self.image, (80, 80, 90), (10, 15, 35, 18))
            # Head
            pygame.draw.circle(self.image, (100, 100, 110), (45, 18), 11)
            # Ears
            pygame.draw.polygon(self.image, (100, 100, 110), [(40, 5), (45, 0), (50, 5)])
            # Snout
            pygame.draw.circle(self.image, (120, 120, 130), (52, 20), 5)
            # Eyes
            pygame.draw.circle(self.image, (255, 200, 0), (48, 14), 2)
            # Tail
            pygame.draw.line(self.image, (80, 80, 90), (10, 18), (0, 10), 3)
            self.speed = 3.5
            self.points = 150

        elif enemy_type == "mammoth":
            self.image = pygame.Surface((80, 65), pygame.SRCALPHA)
            # Body
            pygame.draw.ellipse(self.image, (120, 80, 60), (15, 20, 50, 35))
            # Head
            pygame.draw.circle(self.image, (130, 90, 70), (20, 25), 13)
            # Large tusks
            pygame.draw.line(self.image, (240, 240, 200), (15, 35), (5, 45), 5)
            pygame.draw.line(self.image, (240, 240, 200), (25, 35), (0, 50), 5)
            # Trunk
            pygame.draw.arc(self.image, (100, 60, 40), (18, 30, 15, 20), 0, 3.14, 4)
            # Fur texture
            pygame.draw.line(self.image, (80, 50, 30), (25, 20), (28, 35), 2)
            pygame.draw.line(self.image, (80, 50, 30), (35, 18), (38, 35), 2)
            pygame.draw.line(self.image, (80, 50, 30), (45, 20), (48, 35), 2)
            self.health = 3
            self.speed = 1.5
            self.points = 300

        elif enemy_type == "scorpion":
            self.image = pygame.Surface((50, 55), pygame.SRCALPHA)
            # Body segments
            pygame.draw.circle(self.image, (139, 35, 69), (15, 25), 8)
            pygame.draw.circle(self.image, (139, 35, 69), (25, 32), 8)
            pygame.draw.ellipse(self.image, (139, 35, 69), (20, 35, 15, 12))
            # Head
            pygame.draw.circle(self.image, (180, 50, 100), (10, 15), 8)
            # Pincers
            pygame.draw.line(self.image, (180, 50, 100), (8, 10), (0, 5), 3)
            pygame.draw.line(self.image, (180, 50, 100), (12, 10), (5, 0), 3)
            # Stinger/tail
            pygame.draw.line(self.image, (200, 30, 80), (25, 30), (28, 10), 3)
            pygame.draw.line(self.image, (200, 30, 80), (28, 10), (32, 5), 3)
            pygame.draw.polygon(self.image, (255, 80, 150), [(28, 5), (26, 0), (32, 2), (30, 8)])
            self.speed = 4
            self.points = 120

        elif enemy_type == "pterodactyl":
            self.image = pygame.Surface((65, 45), pygame.SRCALPHA)
            # Wing
            pygame.draw.polygon(self.image, (100, 100, 120), [(10, 20), (0, 15), (5, 30), (25, 25)])
            pygame.draw.polygon(self.image, (120, 120, 140), [(10, 20), (0, 15), (3, 18)])
            # Body
            pygame.draw.circle(self.image, (110, 110, 130), (28, 22), 8)
            # Head
            pygame.draw.polygon(
                self.image, (130, 130, 150), [(35, 18), (60, 12), (62, 18), (55, 22)]
            )
            # Long beak
            pygame.draw.line(self.image, (150, 150, 170), (62, 15), (65, 15), 3)
            # Eye
            pygame.draw.circle(self.image, (255, 255, 0), (58, 14), 2)
            # Legs
            pygame.draw.line(self.image, (150, 150, 170), (28, 28), (25, 38), 2)
            pygame.draw.line(self.image, (150, 150, 170), (32, 28), (35, 38), 2)
            self.speed = 3
            self.points = 140

        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = random.choice([-1, 1])

    def update(self) -> None:
        """Update enemy position - move toward player and descend."""
        # Move toward player horizontally
        player_x = player.rect.centerx
        enemy_center = self.rect.centerx

        if enemy_center < player_x - 10:
            self.rect.x += self.speed
        elif enemy_center > player_x + 10:
            self.rect.x -= self.speed

        # Keep within bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Move down faster - attack pattern
        self.rect.y += 2.5

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self) -> bool:
        """Reduce health by 1 and return True if enemy defeated."""
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False


class BronzeWarrior(pygame.sprite.Sprite):
    """Bronze Age Warrior - enemy in platformer phase"""

    def __init__(self, x, y, warrior_type="standard", move_direction=-1):
        super().__init__()
        self.warrior_type = warrior_type
        self.health = 2 if warrior_type == "heavy" else 1
        self.speed = 1.0 if warrior_type == "heavy" else 1.8
        self.direction = move_direction  # Direction to move (-1 for left, 1 for right)

        if warrior_type == "heavy":
            self.image = pygame.Surface((50, 60), pygame.SRCALPHA)
            # Helmet with plume
            pygame.draw.rect(self.image, (180, 180, 150), (12, 5, 26, 18))
            pygame.draw.polygon(self.image, (255, 100, 0), [(12, 8), (15, 0), (18, 8)])
            pygame.draw.polygon(self.image, (255, 100, 0), [(35, 8), (38, 0), (41, 8)])
            # Bronze armor
            pygame.draw.rect(self.image, (205, 127, 50), (10, 22, 30, 22))
            pygame.draw.line(self.image, (150, 90, 30), (10, 30), (40, 30), 2)
            pygame.draw.line(self.image, (150, 90, 30), (10, 38), (40, 38), 2)
            # Shield
            pygame.draw.circle(self.image, (200, 120, 50), (7, 35), 8)
            pygame.draw.circle(self.image, (255, 160, 80), (7, 35), 5)
            # Legs
            pygame.draw.line(self.image, (100, 60, 30), (18, 44), (15, 58), 3)
            pygame.draw.line(self.image, (100, 60, 30), (32, 44), (35, 58), 3)
            self.points = 200
        else:
            self.image = pygame.Surface((45, 55), pygame.SRCALPHA)
            # Helmet
            pygame.draw.rect(self.image, (200, 180, 140), (10, 8, 25, 15))
            pygame.draw.polygon(self.image, (200, 180, 140), [(10, 8), (8, 15), (12, 18)])
            pygame.draw.polygon(self.image, (200, 180, 140), [(35, 8), (37, 15), (33, 18)])
            # Bronze armor
            pygame.draw.rect(self.image, (200, 120, 50), (8, 23, 29, 18))
            # Bronze sword
            pygame.draw.line(self.image, (200, 160, 100), (40, 25), (44, 5), 4)
            # Legs
            pygame.draw.line(self.image, (80, 50, 25), (16, 41), (13, 55), 3)
            pygame.draw.line(self.image, (80, 50, 25), (29, 41), (32, 55), 3)
            self.points = 150

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.gravity = GRAVITY
        self.on_ground = False
        self.direction = 1 if x < SCREEN_WIDTH // 2 else -1
        self.jump_timer = 0

    def update(self, platforms):
        # Horizontal movement (constant direction, no bouncing)
        self.rect.x += self.direction * self.speed

        # Remove if off left side of level
        if self.rect.right < 0:
            self.kill()
            return

        # Gravity and jumping
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Random jumping
        self.jump_timer -= 1
        if self.jump_timer <= 0 and self.on_ground and random.random() < 0.02:
            self.velocity_y = -10
            self.jump_timer = 30

        # Fall off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False


class Platform(pygame.sprite.Sprite):
    """Platforms for Bronze Age platformer phase"""

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((160, 100, 60))
        # Add texture
        pygame.draw.line(self.image, (120, 70, 40), (0, 0), (width, 0), 2)
        pygame.draw.line(self.image, (200, 140, 80), (0, height - 2), (width, height - 2), 2)
        self.rect = self.image.get_rect(topleft=(x, y))


class BronzePlayer(pygame.sprite.Sprite):
    """Bronze Age Warrior Player - platformer version"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 55), pygame.SRCALPHA)
        # Helmet
        pygame.draw.rect(self.image, (220, 200, 160), (10, 8, 25, 15))
        pygame.draw.circle(self.image, (220, 200, 160), (22, 8), 3)
        # Face
        pygame.draw.circle(self.image, (220, 180, 140), (22, 20), 4)
        # Armor - more detailed
        pygame.draw.rect(self.image, (210, 140, 60), (8, 23, 29, 20))
        pygame.draw.rect(self.image, (180, 110, 40), (8, 23, 29, 5))
        # Bronze sword
        pygame.draw.polygon(self.image, (210, 160, 100), [(40, 30), (43, 10), (45, 12), (42, 32)])
        # Legs
        pygame.draw.line(self.image, (100, 70, 35), (16, 43), (14, 55), 3)
        pygame.draw.line(self.image, (100, 70, 35), (29, 43), (31, 55), 3)

        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.velocity_y = 0
        self.velocity_x = 0
        self.gravity = GRAVITY
        self.on_ground = False
        self.speed = PLAYER_SPEED_BRONZE
        self.health = PLAYER_HEALTH_BRONZE
        self.score = 0
        self.sword_swing = False
        self.swing_timer = 0
        self.swing_duration = 8
        self.facing = 1  # 1 = right, -1 = left
        self.space_prev_pressed = False  # Track space key state to prevent continuous jumping

    def redraw_sprite(self):
        """Redraw the sprite based on facing direction"""
        self.image = pygame.Surface((45, 55), pygame.SRCALPHA)
        # Helmet
        pygame.draw.rect(self.image, (220, 200, 160), (10, 8, 25, 15))
        pygame.draw.circle(self.image, (220, 200, 160), (22, 8), 3)
        # Face
        pygame.draw.circle(self.image, (220, 180, 140), (22, 20), 4)
        # Armor - more detailed
        pygame.draw.rect(self.image, (210, 140, 60), (8, 23, 29, 20))
        pygame.draw.rect(self.image, (180, 110, 40), (8, 23, 29, 5))
        # Bronze sword - position based on facing direction
        if self.facing == 1:  # Facing right
            pygame.draw.polygon(
                self.image, (210, 160, 100), [(40, 30), (43, 10), (45, 12), (42, 32)]
            )
        else:  # Facing left
            pygame.draw.polygon(self.image, (210, 160, 100), [(5, 30), (2, 10), (0, 12), (3, 32)])
        # Legs
        pygame.draw.line(self.image, (100, 70, 35), (16, 43), (14, 55), 3)
        pygame.draw.line(self.image, (100, 70, 35), (29, 43), (31, 55), 3)

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        old_facing = self.facing
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing = -1
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing = 1

        # Redraw sprite if facing direction changed
        if self.facing != old_facing:
            self.redraw_sprite()

        self.rect.x += self.velocity_x

        # Gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Jump (only on key press, not while holding)
        space_pressed = keys[pygame.K_SPACE]
        if space_pressed and not self.space_prev_pressed and self.on_ground:
            self.velocity_y = -JUMP_POWER
            self.on_ground = False
        self.space_prev_pressed = space_pressed

        # Level bounds - allow player to move across entire level
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > bronze_level_width:
            self.rect.right = bronze_level_width

        # Fall off screen
        if self.rect.top > SCREEN_HEIGHT:
            return False  # Player died
        return True

    def swing_sword(self):
        """Start sword swing animation"""
        self.sword_swing = True
        self.swing_timer = self.swing_duration

    def get_sword_rect(self):
        """Get the hitbox of the swinging sword"""
        if self.sword_swing and self.swing_timer > 0:
            # Sword extends in the direction the player is facing
            if self.facing == 1:  # Facing right
                return pygame.Rect(self.rect.right - 5, self.rect.centery - 15, 30, 30)
            else:  # Facing left
                return pygame.Rect(self.rect.left - 25, self.rect.centery - 15, 30, 30)
        return pygame.Rect(0, 0, 0, 0)  # No collision when not swinging

    def get_feet_rect(self):
        """Get the hitbox for the player's feet (for stomp damage)"""
        # Bottom portion of the player for detecting stomps on enemies
        return pygame.Rect(self.rect.left, self.rect.bottom - 10, self.rect.width, 10)

    def draw_sword_swing(self, surface, camera_offset=0):
        """Draw the sword swing effect"""
        if self.sword_swing and self.swing_timer > 0:
            # Draw sword arc
            if self.facing == 1:  # Facing right
                center = (self.rect.right - camera_offset, self.rect.centery)
                radius = 25
                angle = (1 - self.swing_timer / self.swing_duration) * 1.57  # 90 degrees in radians
                end_x = int(center[0] + radius * math.sin(angle))
                end_y = int(center[1] - radius * math.cos(angle))
            else:  # Facing left
                center = (self.rect.left - camera_offset, self.rect.centery)
                radius = 25
                angle = (1 - self.swing_timer / self.swing_duration) * 1.57
                end_x = int(center[0] - radius * math.sin(angle))
                end_y = int(center[1] - radius * math.cos(angle))
            pygame.draw.line(surface, (210, 160, 100), center, (end_x, end_y), 5)


class IronPlayer(pygame.sprite.Sprite):
    """Iron Age Player - 2D top-down movement"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.draw_sprite()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = PLAYER_SPEED_IRON
        self.health = PLAYER_HEALTH_IRON
        self.max_health = PLAYER_HEALTH_IRON
        self.score = 0
        self.facing = (1, 0)  # (x, y) direction

    def draw_sprite(self):
        """Draw the Iron Age player sprite"""
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Helmet with better iron look
        pygame.draw.circle(self.image, (150, 150, 150), (20, 12), 10)
        pygame.draw.polygon(self.image, (120, 120, 120), [(12, 12), (10, 5), (14, 8)])
        pygame.draw.polygon(self.image, (120, 120, 120), [(28, 12), (30, 5), (26, 8)])
        # Body armor
        pygame.draw.rect(self.image, (180, 180, 180), (8, 22, 24, 14))
        pygame.draw.line(self.image, (100, 100, 100), (8, 28), (32, 28), 2)
        # Legs
        pygame.draw.line(self.image, (80, 80, 80), (15, 36), (12, 38), 2)
        pygame.draw.line(self.image, (80, 80, 80), (25, 36), (28, 38), 2)

    def update(self, obstacles):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.facing = (0, -1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.facing = (0, 1)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.facing = (-1, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.facing = (1, 0)

        # Diagonal movement
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.facing = (-1, -1)
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.facing = (1, -1)
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        ):
            self.facing = (-1, 1)
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (
            keys[pygame.K_RIGHT] or keys[pygame.K_d]
        ):
            self.facing = (1, 1)

        # Move with collision detection
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Boundary checking
        if 0 <= new_x <= iron_map_width - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= iron_map_height - self.rect.height:
            self.rect.y = new_y


class IronEnemy(pygame.sprite.Sprite):
    """Iron Age Enemy - involved in turn-based battles"""

    def __init__(self, x, y, enemy_type="warrior"):
        super().__init__()
        self.enemy_type = enemy_type
        self.health = IRON_ENEMY_TYPES[enemy_type]["health"]
        self.max_health = self.health
        self.attack_power = IRON_ENEMY_TYPES[enemy_type]["attack"]
        self.defense = IRON_ENEMY_TYPES[enemy_type]["defense"]
        self.points = IRON_ENEMY_TYPES[enemy_type]["points"]

        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.draw_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw_sprite(self):
        """Draw the enemy sprite based on type"""
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        if self.enemy_type == "warrior":
            # Iron warrior
            pygame.draw.circle(self.image, (150, 120, 80), (20, 12), 9)
            pygame.draw.rect(self.image, (180, 140, 60), (8, 22, 24, 14))
            pygame.draw.polygon(self.image, (200, 200, 200), [(15, 22), (12, 15), (18, 18)])
        elif self.enemy_type == "knight":
            # Iron knight with full armor
            pygame.draw.rect(self.image, (160, 160, 160), (10, 8, 20, 14))
            pygame.draw.circle(self.image, (160, 160, 160), (20, 10), 3)
            pygame.draw.rect(self.image, (140, 140, 140), (8, 22, 24, 14))
            pygame.draw.rect(self.image, (100, 100, 100), (8, 22, 24, 4))
        elif self.enemy_type == "warlord":
            # Iron warlord with crown
            pygame.draw.rect(self.image, (150, 150, 150), (10, 5, 20, 12))
            pygame.draw.polygon(self.image, (255, 200, 0), [(12, 5), (14, 0), (16, 5)])
            pygame.draw.polygon(self.image, (255, 200, 0), [(24, 5), (26, 0), (28, 5)])
            pygame.draw.rect(self.image, (130, 130, 130), (8, 17, 24, 20))
            pygame.draw.line(self.image, (100, 100, 100), (8, 25), (32, 25), 2)


class BattleState:
    """Manages a turn-based battle between player and enemy group"""

    def __init__(self, enemies_list):
        self.player_health = iron_player.health
        self.player_max_health = iron_player.max_health
        self.enemies = enemies_list.copy()
        self.current_turn = "player"  # "player" or "enemy"
        self.battle_log = ["Battle Started!", "Your turn!"]
        self.battle_over = False
        self.player_won = False
        self.selected_action = None  # "attack", "defend", "heal"
        self.defend_mode = False

    def player_attack(self):
        """Player attacks a random enemy"""
        if not self.enemies:
            return
        target = random.choice(self.enemies)
        damage = random.randint(3, 6)
        target.health -= damage
        self.battle_log.append(f"You attack for {damage} damage!")
        if target.health <= 0:
            self.battle_log.append(f"Enemy {target.enemy_type} defeated!")
            self.enemies.remove(target)
        self.end_player_turn()

    def player_defend(self):
        """Player defends (reduces damage next turn)"""
        self.battle_log.append("You take a defensive stance!")
        self.defend_mode = True
        self.end_player_turn()

    def player_heal(self):
        """Player heals some health"""
        heal_amount = random.randint(2, 7)
        self.player_health = min(self.player_health + heal_amount, self.player_max_health)
        self.battle_log.append(f"You heal for {heal_amount} health!")
        self.end_player_turn()

    def end_player_turn(self):
        """End player turn and start enemy turn"""
        if not self.enemies:
            self.battle_over = True
            self.player_won = True
            self.battle_log.append("Victory! All enemies defeated!")
            return
        self.current_turn = "enemy"
        self.enemy_attack()

    def enemy_attack(self):
        """All remaining enemies attack"""
        for enemy in self.enemies:
            damage = max(1, random.randint(1, enemy.attack_power + 2) - 1)
            self.player_health -= damage
            self.battle_log.append(f"Enemy {enemy.enemy_type} attacks for {damage} damage!")

        if self.player_health <= 0:
            self.battle_over = True
            self.player_won = False
            self.battle_log.append("You were defeated!")
        else:
            self.current_turn = "player"
            self.battle_log.append("Your turn!")


def spawn_iron_enemies():
    """Spawn enemy groups throughout the Iron Age map"""
    for i in range(IRON_SPAWN_GROUPS):
        x = random.randint(100, iron_map_width - 150)
        y = random.randint(100, iron_map_height - 150)

        group_size = random.randint(IRON_GROUP_SIZE_MIN, IRON_GROUP_SIZE_MAX)
        enemy_group = []
        for j in range(group_size):
            enemy_type = random.choice(list(IRON_ENEMY_TYPES.keys()))
            enemy = IronEnemy(x + j * 50, y, enemy_type)
            enemy_group.append(enemy)
            iron_enemies.add(enemy)

        iron_enemy_groups.append(enemy_group)


def draw_iron_game():
    """Draw the Iron Age game screen"""
    # Draw grass background
    screen.fill((60, 120, 60))

    # Draw simple grid pattern for terrain
    for x in range(0, iron_map_width, 50):
        pygame.draw.line(
            screen, (40, 100, 40), (x - iron_camera_x, 0), (x - iron_camera_x, SCREEN_HEIGHT), 1
        )
    for y in range(0, iron_map_height, 50):
        pygame.draw.line(
            screen, (40, 100, 40), (0, y - iron_camera_y), (SCREEN_WIDTH, y - iron_camera_y), 1
        )

    # Draw enemies
    for enemy in iron_enemies:
        enemy_screen_x = enemy.rect.x - iron_camera_x
        enemy_screen_y = enemy.rect.y - iron_camera_y
        if -50 < enemy_screen_x < SCREEN_WIDTH and -50 < enemy_screen_y < SCREEN_HEIGHT:
            screen.blit(enemy.image, (enemy_screen_x, enemy_screen_y))

    # Draw player at center
    player_screen_x = iron_player.rect.x - iron_camera_x
    player_screen_y = iron_player.rect.y - iron_camera_y
    screen.blit(iron_player.image, (player_screen_x, player_screen_y))

    # Draw UI
    health_text = font_small.render(
        f"Health: {iron_player.health}/{iron_player.max_health}", True, (255, 255, 255)
    )
    score_text = font_small.render(f"Score: {iron_player.score}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))


def draw_battle_screen(battle):
    """Draw the turn-based battle screen"""
    screen.fill((40, 40, 60))

    # Draw player info
    pygame.draw.rect(screen, (100, 150, 100), (10, 10, 300, 100))
    player_text = font_medium.render("Your Status", True, (255, 255, 255))
    health_text = font_small.render(
        f"Health: {battle.player_health}/{battle.player_max_health}", True, (255, 255, 255)
    )
    screen.blit(player_text, (20, 20))
    screen.blit(health_text, (20, 50))

    # Draw enemies info
    pygame.draw.rect(screen, (150, 100, 100), (10, 130, 300, 150))
    enemies_title = font_medium.render("Enemies", True, (255, 255, 255))
    screen.blit(enemies_title, (20, 140))
    for i, enemy in enumerate(battle.enemies):
        enemy_text = font_small.render(
            f"{enemy.enemy_type}: {enemy.health}/{enemy.max_health} HP", True, (255, 255, 255)
        )
        screen.blit(enemy_text, (20, 170 + i * 25))

    # Draw battle log
    pygame.draw.rect(screen, (80, 80, 80), (330, 10, 460, 270))
    log_title = font_medium.render("Battle Log", True, (255, 255, 255))
    screen.blit(log_title, (340, 20))

    # Show last few log messages
    for i, message in enumerate(battle.battle_log[-6:]):
        msg_text = font_small.render(message, True, (200, 200, 200))
        screen.blit(msg_text, (340, 50 + i * 30))

    # Draw action buttons
    pygame.draw.rect(screen, (100, 100, 150), (10, 300, 200, 50))
    attack_text = font_small.render("SPACE - Attack", True, (255, 255, 255))
    screen.blit(attack_text, (20, 310))

    pygame.draw.rect(screen, (100, 150, 100), (220, 300, 200, 50))
    heal_text = font_small.render("H - Heal", True, (255, 255, 255))
    screen.blit(heal_text, (230, 310))

    # Draw turn indicator
    if battle.current_turn == "player":
        turn_text = font_medium.render("YOUR TURN", True, (0, 255, 0))
    else:
        turn_text = font_medium.render("ENEMY TURN", True, (255, 0, 0))
    screen.blit(turn_text, (SCREEN_WIDTH - 250, 10))


def spawn_wave(wave_num):

    num_enemies = min(INITIAL_ENEMY_COUNT + wave_num, MAX_ENEMIES_PER_WAVE)

    for i in range(num_enemies):
        enemy_type = random.choice(ENEMY_TYPES)
        x = random.randint(50, SCREEN_WIDTH - 100)
        y = random.randint(-200, -50)
        enemy = Enemy(x, y, enemy_type)
        all_sprites.add(enemy)
        enemies.add(enemy)


def draw_game():
    # Draw cave background with gradient
    for y in range(SCREEN_HEIGHT):
        color_val = int(70 + (y / SCREEN_HEIGHT) * 40)
        pygame.draw.line(screen, (color_val, color_val // 2, 0), (0, y), (SCREEN_WIDTH, y))

    # Draw distant cave walls (perspective effect)
    pygame.draw.polygon(
        screen, (50, 35, 15), [(0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH - 150, 150), (150, 150)]
    )

    # Draw scattered rocks and boulders across the cave floor
    rock_positions = [
        (80, 120, 15),
        (200, 100, 20),
        (350, 140, 18),
        (500, 95, 22),
        (650, 130, 16),
        (120, 200, 12),
        (300, 220, 25),
        (550, 210, 14),
        (700, 240, 19),
        (180, 300, 18),
        (420, 320, 16),
        (600, 310, 21),
    ]
    for rock_x, rock_y, rock_size in rock_positions:
        pygame.draw.circle(screen, (50, 30, 15), (rock_x, rock_y), rock_size)
        pygame.draw.circle(screen, (60, 38, 18), (rock_x - 5, rock_y - 5), rock_size - 2)

    # Draw bushes/vegetation
    bush_positions = [(150, 180), (400, 200), (700, 160), (250, 320), (550, 280)]
    for bush_x, bush_y in bush_positions:
        # Bush base
        pygame.draw.ellipse(screen, (34, 80, 20), (bush_x - 20, bush_y - 15, 40, 30))
        # Bush highlights
        pygame.draw.circle(screen, (50, 120, 30), (bush_x - 10, bush_y - 10), 12)
        pygame.draw.circle(screen, (50, 120, 30), (bush_x + 10, bush_y - 8), 11)
        pygame.draw.circle(screen, (45, 110, 25), (bush_x, bush_y + 5), 10)

    # Draw cave cracks/crevices on ground
    pygame.draw.line(screen, (30, 15, 5), (100, 350), (180, 500), 2)
    pygame.draw.line(screen, (30, 15, 5), (400, 320), (420, 550), 2)
    pygame.draw.line(screen, (30, 15, 5), (700, 380), (650, 550), 2)

    # Draw ground/terrain at bottom (darker)
    pygame.draw.polygon(
        screen,
        (40, 25, 10),
        [
            (0, SCREEN_HEIGHT - 80),
            (SCREEN_WIDTH, SCREEN_HEIGHT - 80),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            (0, SCREEN_HEIGHT),
        ],
    )

    # Draw rocky terrain features at bottom
    rock_positions_bottom = [
        (100, SCREEN_HEIGHT - 60),
        (250, SCREEN_HEIGHT - 50),
        (400, SCREEN_HEIGHT - 70),
        (550, SCREEN_HEIGHT - 55),
        (700, SCREEN_HEIGHT - 65),
    ]
    for rock_x, rock_y in rock_positions_bottom:
        pygame.draw.circle(screen, (35, 20, 8), (rock_x, rock_y), 28)
        pygame.draw.circle(screen, (45, 28, 12), (rock_x, rock_y), 23)

    all_sprites.draw(screen)

    # Draw HUD
    health_text = font_small.render(f"Health: {player.health}", True, (255, 255, 255))
    score_text = font_small.render(f"Score: {player.score}", True, (255, 255, 255))
    wave_text = font_small.render(f"Wave: {wave_num}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(wave_text, (SCREEN_WIDTH - 150, 10))


def draw_menu():
    # Draw night sky background with stars
    screen.fill((20, 15, 40))

    # Draw stars
    for i in range(0, SCREEN_WIDTH, 60):
        for j in range(0, 150, 60):
            pygame.draw.circle(
                screen,
                (255, 255, 200),
                (i + random.randint(-20, 20), j + random.randint(-20, 20)),
                2,
            )

    # Draw moon
    pygame.draw.circle(screen, (240, 240, 180), (SCREEN_WIDTH - 80, 80), 60)
    pygame.draw.circle(screen, (20, 15, 40), (SCREEN_WIDTH - 70, 60), 50)

    # Draw mountains/cave entrance silhouette
    pygame.draw.polygon(
        screen,
        (30, 20, 10),
        [
            (0, SCREEN_HEIGHT),
            (150, 250),
            (SCREEN_WIDTH // 2, 200),
            (SCREEN_WIDTH - 150, 250),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
        ],
    )
    pygame.draw.polygon(
        screen, (40, 30, 15), [(150, 250), (SCREEN_WIDTH // 2, 200), (SCREEN_WIDTH - 150, 250)]
    )

    title = font_large.render("THRAK", True, (255, 100, 0))
    subtitle = font_medium.render("BEAST SLAYER OF THE STONE AGE", True, (255, 200, 0))

    # Backstory text
    backstory_font = pygame.font.Font(None, 18)
    story_line1 = backstory_font.render(
        "The ancient beasts have awakened. Darkness spreads across the land.", True, (200, 200, 200)
    )
    story_line2 = backstory_font.render(
        "Your tribe looks to you, THRAK, their greatest warrior.", True, (200, 200, 200)
    )
    story_line3 = backstory_font.render(
        "With spear in hand and fire in your heart, defend them or perish.", True, (200, 200, 200)
    )

    instructions = font_small.render(
        "Press SPACE to Hunt | Arrow Keys to Move | SPACE to Throw Spear", True, (200, 200, 200)
    )
    dev_text = font_small.render("Press D for Developer Mode", True, (100, 255, 100))

    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 160))
    screen.blit(story_line1, (SCREEN_WIDTH // 2 - story_line1.get_width() // 2, 240))
    screen.blit(story_line2, (SCREEN_WIDTH // 2 - story_line2.get_width() // 2, 270))
    screen.blit(story_line3, (SCREEN_WIDTH // 2 - story_line3.get_width() // 2, 300))
    screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 400))
    screen.blit(dev_text, (SCREEN_WIDTH // 2 - dev_text.get_width() // 2, 550))


def draw_game_over():
    # Draw cave background with gradient
    for y in range(SCREEN_HEIGHT):
        color_val = int(70 + (y / SCREEN_HEIGHT) * 40)
        pygame.draw.line(screen, (color_val, color_val // 2, 0), (0, y), (SCREEN_WIDTH, y))

    # Draw rocky terrain
    pygame.draw.polygon(
        screen,
        (60, 40, 20),
        [
            (0, SCREEN_HEIGHT),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            (SCREEN_WIDTH, SCREEN_HEIGHT - 80),
            (0, SCREEN_HEIGHT - 80),
        ],
    )

    game_over = font_large.render("GAME OVER", True, (255, 0, 0))
    score_text = font_medium.render(f"Final Score: {player.score}", True, (255, 255, 255))
    wave_text = font_medium.render(f"Wave Reached: {wave_num}", True, (255, 255, 255))
    restart = font_small.render("Press SPACE to return to menu", True, (200, 200, 200))
    screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, 320))
    screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 450))


# Sprite groups
all_sprites = pygame.sprite.Group()
spears = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
DEV_MENU = 3

game_state = MENU
game_phase = PHASE_STONE_AGE
wave_num = 1
wave_timer = 0
shoot_cooldown = 0
running = True

# Bronze age variables
bronze_platforms = pygame.sprite.Group()
bronze_warriors = pygame.sprite.Group()
bronze_player = None
bronze_wave = 1
bronze_level_width = BRONZE_LEVEL_WIDTH
bronze_camera_x = 0  # Camera position for scrolling

# Iron age variables
iron_player = None
iron_enemies = pygame.sprite.Group()
iron_enemy_groups = []
iron_map_width = IRON_MAP_WIDTH
iron_map_height = IRON_MAP_HEIGHT
iron_camera_x = 0
iron_camera_y = 0
iron_wave = 1
current_battle = None
battle_active = False


def draw_dev_menu():
    """Developer mode menu for testing phases"""
    screen.fill((30, 30, 40))

    title = font_large.render("DEVELOPER MODE", True, (0, 255, 0))
    subtitle = font_medium.render("Select Phase to Test", True, (100, 255, 100))

    option1 = font_medium.render("1 - Stone Age (Waves 1-5)", True, (255, 255, 255))
    option2 = font_medium.render("2 - Bronze Age (Platformer)", True, (255, 255, 255))
    option3 = font_medium.render("3 - Iron Age (2D RPG)", True, (255, 255, 255))
    option4 = font_small.render("0 - Back to Menu", True, (150, 150, 150))

    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 180))
    screen.blit(option1, (SCREEN_WIDTH // 2 - option1.get_width() // 2, 280))
    screen.blit(option2, (SCREEN_WIDTH // 2 - option2.get_width() // 2, 350))
    screen.blit(option3, (SCREEN_WIDTH // 2 - option3.get_width() // 2, 420))
    screen.blit(option4, (SCREEN_WIDTH // 2 - option4.get_width() // 2, 520))


def create_bronze_platforms():
    """Create platforms for Bronze Age side-scrolling level"""
    platforms = pygame.sprite.Group()
    # Create a long level with solid ground and strategic gaps
    platform_data = [
        # (x, y, width, height)
        # Main ground level - solid base with only a few gaps for jumping
        (0, SCREEN_HEIGHT - 50, 400, 50),  # Starting platform
        (500, SCREEN_HEIGHT - 50, 300, 50),  # Gap here, must jump (400-500)
        (850, SCREEN_HEIGHT - 50, 400, 50),  # Solid ground
        (1350, SCREEN_HEIGHT - 50, 150, 50),  # Small section
        (1600, SCREEN_HEIGHT - 50, 200, 50),  # Gap here, must jump (1500-1600)
        (1850, SCREEN_HEIGHT - 50, 500, 50),  # Solid ground
        (2450, SCREEN_HEIGHT - 50, 300, 50),  # Gap here, must jump (2350-2450)
        (2800, SCREEN_HEIGHT - 50, 200, 50),  # Final platform
        # Some elevated platforms for variety and challenge
        (600, SCREEN_HEIGHT - 150, 150, 20),  # Elevated platform
        (1200, SCREEN_HEIGHT - 120, 100, 20),  # Elevated platform
        (2200, SCREEN_HEIGHT - 140, 120, 20),  # Elevated platform
    ]
    for x, y, width, height in platform_data:
        platforms.add(Platform(x, y, width, height))
    return platforms


def spawn_bronze_warriors(wave):
    """Spawn Bronze Age warriors from the right side"""
    num_warriors = min(2 + wave, 5)
    for i in range(num_warriors):
        warrior_type = "heavy" if i % 3 == 0 else "standard"
        # Spawn from right side, spread across the level
        x = bronze_camera_x + SCREEN_WIDTH + random.randint(0, 300)
        y = 100
        warrior = BronzeWarrior(x, y, warrior_type, move_direction=-1)  # Moving left
        bronze_warriors.add(warrior)


def draw_bronze_game():
    """Draw Bronze Age side-scrolling platformer phase"""
    global bronze_camera_x

    # Sky background - gradient
    for y in range(SCREEN_HEIGHT):
        color_val = int(120 + (y / SCREEN_HEIGHT) * 40)
        pygame.draw.line(
            screen, (color_val, color_val - 40, color_val - 80), (0, y), (SCREEN_WIDTH, y)
        )

    # Draw sun
    sun_x = 600 - int(bronze_camera_x * 0.3)
    pygame.draw.circle(screen, (255, 220, 0), (sun_x, 80), 50)

    # Draw clouds parallax
    for i in range(5):
        cloud_x = (i * 300 - int(bronze_camera_x * 0.2)) % (SCREEN_WIDTH + 200) - 100
        pygame.draw.ellipse(screen, (200, 200, 200), (cloud_x, 60 + (i % 3) * 40, 100, 30))
        pygame.draw.ellipse(screen, (210, 210, 210), (cloud_x + 30, 50 + (i % 3) * 40, 80, 40))

    # Update camera to follow player
    target_camera = bronze_player.rect.centerx - SCREEN_WIDTH // 3
    bronze_camera_x = max(0, min(target_camera, bronze_level_width - SCREEN_WIDTH))

    # Draw platforms with camera offset
    for platform in bronze_platforms:
        screen_rect = platform.rect.copy()
        screen_rect.x -= int(bronze_camera_x)
        pygame.draw.rect(screen, (160, 100, 60), screen_rect)
        # Add platform detail
        pygame.draw.line(
            screen,
            (140, 80, 40),
            (screen_rect.x, screen_rect.y),
            (screen_rect.x + screen_rect.width, screen_rect.y),
            2,
        )

    # Draw level end flag
    flag_x = bronze_level_width - int(bronze_camera_x) - 50
    if flag_x > -50 and flag_x < SCREEN_WIDTH + 50:
        pygame.draw.rect(screen, (180, 100, 50), (flag_x, SCREEN_HEIGHT - 150, 40, 140))
        pygame.draw.polygon(
            screen,
            (255, 100, 0),
            [
                (flag_x + 40, SCREEN_HEIGHT - 150),
                (flag_x + 40, SCREEN_HEIGHT - 110),
                (flag_x + 100, SCREEN_HEIGHT - 130),
            ],
        )

    # Draw warriors with camera offset
    for warrior in bronze_warriors:
        warrior_screen_pos = warrior.rect.copy()
        warrior_screen_pos.x -= int(bronze_camera_x)
        if -50 < warrior_screen_pos.x < SCREEN_WIDTH + 50:
            screen.blit(warrior.image, warrior_screen_pos)

    # Draw player
    player_screen_rect = bronze_player.rect.copy()
    player_screen_rect.x -= int(bronze_camera_x)
    screen.blit(bronze_player.image, player_screen_rect)

    # Draw sword swing effect with camera offset
    if bronze_player.sword_swing and bronze_player.swing_timer > 0:
        bronze_player.draw_sword_swing(screen, int(bronze_camera_x))

    # Draw HUD
    health_text = font_small.render(f"Health: {bronze_player.health}", True, (255, 255, 255))
    score_text = font_small.render(f"Score: {bronze_player.score}", True, (255, 255, 255))
    progress = int((bronze_player.rect.x / bronze_level_width) * 100)
    progress_text = font_small.render(f"Progress: {progress}%", True, (100, 255, 100))
    wave_text = font_small.render(f"Wave: {bronze_wave}", True, (255, 200, 0))
    phase_text = font_small.render(
        "SIDE-SCROLLER | Reach the End! | ARROWS to Move | SPACE to Jump | S to Swing",
        True,
        (150, 200, 255),
    )
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(progress_text, (SCREEN_WIDTH - 250, 10))
    screen.blit(wave_text, (SCREEN_WIDTH - 250, 40))
    screen.blit(phase_text, (10, SCREEN_HEIGHT - 25))


while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                # Toggle developer mode
                if game_state == MENU:
                    game_state = DEV_MENU
            elif event.key == pygame.K_SPACE:
                if game_state == MENU:
                    game_state = PLAYING
                    game_phase = PHASE_STONE_AGE
                    wave_num = 1
                    all_sprites.empty()
                    player = Player()
                    all_sprites.add(player)
                    player.health = 3
                    player.score = 0
                    enemies.empty()
                    spears.empty()
                    wave_timer = pygame.time.get_ticks() - WAVE_DELAY
                    spawn_wave(wave_num)
                elif game_state == PLAYING and game_phase == PHASE_IRON_AGE and battle_active:
                    # Battle action: attack
                    if current_battle.current_turn == "player":
                        current_battle.player_attack()
                elif game_state == GAME_OVER:
                    game_state = MENU
            elif event.key == pygame.K_1 and game_state == DEV_MENU:
                # Stone Age testing
                game_state = PLAYING
                game_phase = PHASE_STONE_AGE
                wave_num = 1
                all_sprites.empty()
                player = Player()
                all_sprites.add(player)
                player.health = 3
                player.score = 0
                enemies.empty()
                spears.empty()
                wave_timer = pygame.time.get_ticks() - WAVE_DELAY
                spawn_wave(wave_num)
            elif event.key == pygame.K_2 and game_state == DEV_MENU:
                # Bronze Age testing
                game_state = PLAYING
                game_phase = PHASE_BRONZE_AGE
                bronze_player = BronzePlayer()
                bronze_player.health = 3
                bronze_player.score = 0
                bronze_platforms = create_bronze_platforms()
                bronze_warriors.empty()
                bronze_wave = 1
                spawn_bronze_warriors(bronze_wave)
            elif event.key == pygame.K_3 and game_state == DEV_MENU:
                # Iron Age testing
                game_state = PLAYING
                game_phase = PHASE_IRON_AGE
                iron_player = IronPlayer()
                iron_player.score = 0
                iron_enemies.empty()
                iron_enemy_groups.clear()
                current_battle = None
                battle_active = False
                spawn_iron_enemies()
            elif event.key == pygame.K_0 and game_state == DEV_MENU:
                # Back to menu
                game_state = MENU
            elif (
                event.key == pygame.K_s and game_state == PLAYING and game_phase == PHASE_BRONZE_AGE
            ):
                # Sword swing in bronze age
                bronze_player.swing_sword()
            elif (
                event.key == pygame.K_h
                and game_state == PLAYING
                and game_phase == PHASE_IRON_AGE
                and battle_active
            ):
                # Battle action: heal
                if current_battle.current_turn == "player":
                    current_battle.player_heal()

    if game_state == PLAYING:
        if game_phase == PHASE_STONE_AGE:
            # STONE AGE PHASE (original game)
            all_sprites.update()
            shoot_cooldown -= 1

            # Player attack (space key)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and shoot_cooldown <= 0:
                player.shoot()
                shoot_cooldown = 30

            # Collision detection: spears hitting enemies
            for spear in spears:
                hit_enemies = pygame.sprite.spritecollide(spear, enemies, False)
                for enemy in hit_enemies:
                    spear.kill()
                    if enemy.take_damage():
                        player.score += enemy.points

            # Collision detection: enemy touching player
            if pygame.sprite.spritecollide(player, enemies, False):
                player.health -= 1
                if player.health <= 0:
                    game_state = GAME_OVER

            # Check if wave is complete
            if len(enemies) == 0 and pygame.time.get_ticks() - wave_timer > WAVE_DELAY:
                wave_num += 1
                if wave_num > STONE_AGE_WAVES:
                    # Transition to Bronze Age
                    game_phase = PHASE_BRONZE_AGE
                    bronze_player = BronzePlayer()
                    bronze_player.score = player.score
                    bronze_player.health = player.health
                    bronze_platforms = create_bronze_platforms()
                    bronze_wave = 1
                    spawn_bronze_warriors(bronze_wave)
                else:
                    spawn_wave(wave_num)
                    wave_timer = pygame.time.get_ticks()

            draw_game()

        elif game_phase == PHASE_BRONZE_AGE:
            # BRONZE AGE PHASE (side-scrolling platformer)
            platform_list = list(bronze_platforms.sprites())
            alive = bronze_player.update(platform_list)
            if not alive:
                game_state = GAME_OVER

            # Check if reached level end
            if bronze_player.rect.x >= bronze_level_width - 100:
                # Level complete - move to next wave or Iron Age
                bronze_wave += 1
                if bronze_wave > BRONZE_AGE_WAVES:  # Bronze Age wave limit
                    # Transition to Iron Age
                    game_phase = PHASE_IRON_AGE
                    iron_player = IronPlayer()
                    iron_player.score = bronze_player.score  # Carry over score only
                    iron_enemies.empty()
                    iron_enemy_groups.clear()
                    iron_wave = 1
                    spawn_iron_enemies()
                else:
                    # Reset for next wave
                    bronze_player.rect.x = 0
                    bronze_camera_x = 0
                    bronze_warriors.empty()
                    spawn_bronze_warriors(bronze_wave)

            # Update sword swing timer
            if bronze_player.sword_swing:
                bronze_player.swing_timer -= 1
                if bronze_player.swing_timer <= 0:
                    bronze_player.sword_swing = False

            # Update warriors
            for warrior in bronze_warriors:
                warrior.update(platform_list)

            # Periodically spawn more warriors if cleared out
            if len(bronze_warriors) == 0:
                spawn_bronze_warriors(bronze_wave)

            # Check sword-warrior collisions (swing attacks)
            sword_rect = bronze_player.get_sword_rect()
            for warrior in bronze_warriors:
                if warrior.rect.colliderect(sword_rect):
                    if warrior.take_damage():
                        bronze_player.score += warrior.points

            # Check stomp collisions (jumping on enemy heads)
            feet_rect = bronze_player.get_feet_rect()
            for warrior in bronze_warriors:
                if feet_rect.colliderect(warrior.rect) and bronze_player.velocity_y > 0:
                    # Player is falling and hit enemy from above
                    warrior.take_damage()
                    bronze_player.score += warrior.points
                    bronze_player.velocity_y = -8  # Bounce the player up

            # Check warrior-player collision (damage)
            if pygame.sprite.spritecollide(bronze_player, bronze_warriors, False):
                bronze_player.health -= 1
                if bronze_player.health <= 0:
                    game_state = GAME_OVER

            draw_bronze_game()

        elif game_phase == PHASE_IRON_AGE:
            # IRON AGE PHASE (2D RPG with turn-based battles)
            if not battle_active:
                # Exploration mode
                iron_player.update([])

                # Update camera to follow player
                iron_camera_x = max(
                    0,
                    min(
                        iron_player.rect.centerx - SCREEN_WIDTH // 2, iron_map_width - SCREEN_WIDTH
                    ),
                )
                iron_camera_y = max(
                    0,
                    min(
                        iron_player.rect.centery - SCREEN_HEIGHT // 2,
                        iron_map_height - SCREEN_HEIGHT,
                    ),
                )

                # Check for collisions with enemy groups (start battle)
                for group in iron_enemy_groups:
                    # Check if player is adjacent/close to enemy group
                    for enemy in group:
                        dx = iron_player.rect.centerx - enemy.rect.centerx
                        dy = iron_player.rect.centery - enemy.rect.centery
                        distance = math.sqrt(dx * dx + dy * dy)
                        if distance < BATTLE_COLLISION_DISTANCE:  # Collision distance for battle start
                            # Start a battle
                            current_battle = BattleState(group)
                            battle_active = True
                            break
                    if battle_active:
                        break

                # Check if reached level end
                if iron_player.rect.x > iron_map_width - 100:
                    iron_wave += 1
                    if iron_wave > IRON_AGE_WAVES:  # Iron Age wave limit
                        game_state = GAME_OVER  # Victory state
                    else:
                        # Reset for next wave
                        iron_player.rect.x = 0
                        iron_player.rect.y = SCREEN_HEIGHT // 2
                        iron_enemies.empty()
                        iron_enemy_groups.clear()
                        spawn_iron_enemies()

                draw_iron_game()
            else:
                # Battle mode
                draw_battle_screen(current_battle)

                # Check if battle is over
                if current_battle.battle_over:
                    if current_battle.player_won:
                        iron_player.score += (
                            sum(enemy.points for enemy in current_battle.enemies) * 2
                        )
                        iron_player.health = min(iron_player.health + 1, iron_player.max_health)

                        # Remove the defeated enemy group from the map
                        for group in iron_enemy_groups:
                            if all(
                                enemy in current_battle.enemies or enemy.health <= 0
                                for enemy in group
                            ):
                                iron_enemy_groups.remove(group)
                                for enemy in group:
                                    enemy.kill()
                                break
                    else:
                        game_state = GAME_OVER

                    battle_active = False
                    current_battle = None

    elif game_state == MENU:
        draw_menu()

    elif game_state == DEV_MENU:
        draw_dev_menu()

    elif game_state == GAME_OVER:
        draw_game_over()

    pygame.display.flip()

pygame.quit()
