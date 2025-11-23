import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WAVE_DELAY = 3000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("THRAK: Beast Slayer")
clock = pygame.time.Clock()
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Game phases
PHASE_STONE_AGE = 0
PHASE_BRONZE_AGE = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
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
        self.speed = 5
        self.health = 3
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += self.speed

    def shoot(self):
        spear = Spear(self.rect.centerx, self.rect.top)
        all_sprites.add(spear)
        spears.add(spear)

class Spear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12, 30), pygame.SRCALPHA)
        # Spear shaft
        pygame.draw.line(self.image, (139, 69, 19), (6, 0), (6, 25), 3)
        # Spear head
        pygame.draw.polygon(self.image, (200, 200, 200), [(6, 0), (2, 8), (6, 5), (10, 8)])
        # Feathers/fletching
        pygame.draw.polygon(self.image, (255, 200, 0), [(3, 20), (6, 28), (9, 20)])
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
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
            pygame.draw.polygon(self.image, (130, 130, 150), [(35, 18), (60, 12), (62, 18), (55, 22)])
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

    def update(self):
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

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False

class BronzeWarrior(pygame.sprite.Sprite):
    """Bronze Age Warrior - enemy in platformer phase"""
    def __init__(self, x, y, warrior_type="standard"):
        super().__init__()
        self.warrior_type = warrior_type
        self.health = 2 if warrior_type == "heavy" else 1
        self.speed = 1.5 if warrior_type == "heavy" else 2.5
        
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
        self.gravity = 0.5
        self.on_ground = False
        self.direction = 1 if x < SCREEN_WIDTH // 2 else -1
        self.jump_timer = 0

    def update(self, platforms):
        # Horizontal movement (patrol with direction)
        self.rect.x += self.direction * self.speed
        
        # Bounce off screen edges
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
        
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
        self.gravity = 0.5
        self.on_ground = False
        self.speed = 4
        self.health = 3
        self.score = 0
        self.sword_swing = False
        self.swing_timer = 0
        self.swing_duration = 8
        self.facing = 1  # 1 = right, -1 = left

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
            pygame.draw.polygon(self.image, (210, 160, 100), [(40, 30), (43, 10), (45, 12), (42, 32)])
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
        
        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -12
            self.on_ground = False
        
        # Screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
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
    
    def draw_sword_swing(self, surface):
        """Draw the sword swing effect"""
        if self.sword_swing and self.swing_timer > 0:
            # Draw sword arc
            if self.facing == 1:  # Facing right
                center = (self.rect.right, self.rect.centery)
                radius = 25
                angle = (1 - self.swing_timer / self.swing_duration) * 1.57  # 90 degrees in radians
                end_x = int(center[0] + radius * math.sin(angle))
                end_y = int(center[1] - radius * math.cos(angle))
            else:  # Facing left
                center = (self.rect.left, self.rect.centery)
                radius = 25
                angle = (1 - self.swing_timer / self.swing_duration) * 1.57
                end_x = int(center[0] - radius * math.sin(angle))
                end_y = int(center[1] - radius * math.cos(angle))
            pygame.draw.line(surface, (210, 160, 100), center, (end_x, end_y), 5)

def spawn_wave(wave_num):
    enemy_types = ["tiger", "wolf", "mammoth", "scorpion", "pterodactyl"]
    num_enemies = min(3 + wave_num, 8)
    
    for i in range(num_enemies):
        enemy_type = random.choice(enemy_types)
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
    pygame.draw.polygon(screen, (50, 35, 15), [(0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH - 150, 150), (150, 150)])
    
    # Draw scattered rocks and boulders across the cave floor
    rock_positions = [
        (80, 120, 15), (200, 100, 20), (350, 140, 18), (500, 95, 22), (650, 130, 16),
        (120, 200, 12), (300, 220, 25), (550, 210, 14), (700, 240, 19),
        (180, 300, 18), (420, 320, 16), (600, 310, 21),
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
    pygame.draw.polygon(screen, (40, 25, 10), [(0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
    
    # Draw rocky terrain features at bottom
    rock_positions_bottom = [(100, SCREEN_HEIGHT - 60), (250, SCREEN_HEIGHT - 50), (400, SCREEN_HEIGHT - 70), (550, SCREEN_HEIGHT - 55), (700, SCREEN_HEIGHT - 65)]
    for rock_x, rock_y in rock_positions_bottom:
        pygame.draw.circle(screen, (35, 20, 8), (rock_x, rock_y), 28)
        pygame.draw.circle(screen, (45, 28, 12), (rock_x, rock_y), 23)
    
    all_sprites.draw(screen)
    
    # Draw HUD with top-down view indicator
    health_text = font_small.render(f"Health: {player.health}", True, (255, 255, 255))
    score_text = font_small.render(f"Score: {player.score}", True, (255, 255, 255))
    wave_text = font_small.render(f"Wave: {wave_num}", True, (255, 255, 255))
    view_text = font_small.render("TOP-DOWN VIEW", True, (150, 200, 255))
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(wave_text, (SCREEN_WIDTH - 150, 10))
    screen.blit(view_text, (SCREEN_WIDTH // 2 - 70, 10))

def draw_menu():
    # Draw night sky background with stars
    screen.fill((20, 15, 40))
    
    # Draw stars
    for i in range(0, SCREEN_WIDTH, 60):
        for j in range(0, 150, 60):
            pygame.draw.circle(screen, (255, 255, 200), (i + random.randint(-20, 20), j + random.randint(-20, 20)), 2)
    
    # Draw moon
    pygame.draw.circle(screen, (240, 240, 180), (SCREEN_WIDTH - 80, 80), 60)
    pygame.draw.circle(screen, (20, 15, 40), (SCREEN_WIDTH - 70, 60), 50)
    
    # Draw mountains/cave entrance silhouette
    pygame.draw.polygon(screen, (30, 20, 10), [(0, SCREEN_HEIGHT), (150, 250), (SCREEN_WIDTH // 2, 200), (SCREEN_WIDTH - 150, 250), (SCREEN_WIDTH, SCREEN_HEIGHT)])
    pygame.draw.polygon(screen, (40, 30, 15), [(150, 250), (SCREEN_WIDTH // 2, 200), (SCREEN_WIDTH - 150, 250)])
    
    title = font_large.render("THRAK", True, (255, 100, 0))
    subtitle = font_medium.render("BEAST SLAYER OF THE STONE AGE", True, (255, 200, 0))
    
    # Backstory text
    backstory_font = pygame.font.Font(None, 18)
    story_line1 = backstory_font.render("The ancient beasts have awakened. Darkness spreads across the land.", True, (200, 200, 200))
    story_line2 = backstory_font.render("Your tribe looks to you, THRAK, their greatest warrior.", True, (200, 200, 200))
    story_line3 = backstory_font.render("With spear in hand and fire in your heart, defend them or perish.", True, (200, 200, 200))
    
    instructions = font_small.render("Press SPACE to Hunt | Arrow Keys to Move | SPACE to Throw Spear", True, (200, 200, 200))
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
    pygame.draw.polygon(screen, (60, 40, 20), [(0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), (0, SCREEN_HEIGHT - 80)])
    
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

def draw_dev_menu():
    """Developer mode menu for testing phases"""
    screen.fill((30, 30, 40))
    
    title = font_large.render("DEVELOPER MODE", True, (0, 255, 0))
    subtitle = font_medium.render("Select Phase to Test", True, (100, 255, 100))
    
    option1 = font_medium.render("1 - Stone Age (Waves 1-5)", True, (255, 255, 255))
    option2 = font_medium.render("2 - Bronze Age (Platformer)", True, (255, 255, 255))
    option3 = font_small.render("0 - Back to Menu", True, (150, 150, 150))
    
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 180))
    screen.blit(option1, (SCREEN_WIDTH // 2 - option1.get_width() // 2, 280))
    screen.blit(option2, (SCREEN_WIDTH // 2 - option2.get_width() // 2, 350))
    screen.blit(option3, (SCREEN_WIDTH // 2 - option3.get_width() // 2, 450))

def create_bronze_platforms():
    """Create platforms for Bronze Age platformer"""
    platforms = pygame.sprite.Group()
    # Bottom platform
    platforms.add(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    # Staircase pattern
    platforms.add(Platform(100, SCREEN_HEIGHT - 120, 150, 20))
    platforms.add(Platform(300, SCREEN_HEIGHT - 180, 150, 20))
    platforms.add(Platform(500, SCREEN_HEIGHT - 240, 150, 20))
    platforms.add(Platform(650, SCREEN_HEIGHT - 160, 120, 20))
    # Floating platforms
    platforms.add(Platform(150, 300, 120, 20))
    platforms.add(Platform(500, 250, 120, 20))
    return platforms

def spawn_bronze_warriors(wave):
    """Spawn Bronze Age warriors"""
    num_warriors = min(2 + wave, 5)
    for i in range(num_warriors):
        warrior_type = "heavy" if i % 3 == 0 else "standard"
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = 100
        warrior = BronzeWarrior(x, y, warrior_type)
        bronze_warriors.add(warrior)

def draw_bronze_game():
    """Draw Bronze Age side-scrolling platformer phase"""
    # Sky background - gradient
    for y in range(SCREEN_HEIGHT):
        color_val = int(120 + (y / SCREEN_HEIGHT) * 40)
        pygame.draw.line(screen, (color_val, color_val - 40, color_val - 80), (0, y), (SCREEN_WIDTH, y))
    
    # Draw sun
    pygame.draw.circle(screen, (255, 220, 0), (SCREEN_WIDTH - 100, 80), 50)
    
    # Draw clouds
    for i in range(3):
        cloud_x = (i * 300) % SCREEN_WIDTH
        pygame.draw.ellipse(screen, (200, 200, 200), (cloud_x, 60 + i * 40, 100, 30))
        pygame.draw.ellipse(screen, (210, 210, 210), (cloud_x + 30, 50 + i * 40, 80, 40))
    
    # Draw platforms
    bronze_platforms.draw(screen)
    
    # Draw warriors
    bronze_warriors.draw(screen)
    
    # Draw player
    screen.blit(bronze_player.image, bronze_player.rect)
    
    # Draw sword swing effect
    bronze_player.draw_sword_swing(screen)
    
    # Draw HUD
    health_text = font_small.render(f"Health: {bronze_player.health}", True, (255, 255, 255))
    score_text = font_small.render(f"Score: {bronze_player.score}", True, (255, 255, 255))
    wave_text = font_small.render(f"Bronze Age - Wave: {bronze_wave}", True, (255, 200, 0))
    phase_text = font_small.render("PLATFORMER | ARROWS to Move | SPACE to Jump | S to Swing Sword", True, (150, 200, 255))
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(wave_text, (SCREEN_WIDTH - 300, 10))
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
                    player = Player()
                    all_sprites.add(player)
                    player.health = 3
                    player.score = 0
                    enemies.empty()
                    spears.empty()
                    wave_timer = pygame.time.get_ticks() - WAVE_DELAY
                    spawn_wave(wave_num)
                elif game_state == GAME_OVER:
                    game_state = MENU
            elif event.key == pygame.K_1 and game_state == DEV_MENU:
                # Stone Age testing
                game_state = PLAYING
                game_phase = PHASE_STONE_AGE
                wave_num = 1
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
            elif event.key == pygame.K_0 and game_state == DEV_MENU:
                # Back to menu
                game_state = MENU
            elif event.key == pygame.K_s and game_state == PLAYING and game_phase == PHASE_BRONZE_AGE:
                # Sword swing in bronze age
                bronze_player.swing_sword()

    if game_state == PLAYING:
        if game_phase == PHASE_STONE_AGE:
            # STONE AGE PHASE (original game)
            all_sprites.update()
            shoot_cooldown -= 1

            # Player attack (space key)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and shoot_cooldown <= 0:
                player.shoot()
                shoot_cooldown = 10

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
                if wave_num > 5:
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
            # BRONZE AGE PHASE (platformer)
            platform_list = list(bronze_platforms.sprites())
            alive = bronze_player.update(platform_list)
            if not alive:
                game_state = GAME_OVER
            
            # Update sword swing timer
            if bronze_player.sword_swing:
                bronze_player.swing_timer -= 1
                if bronze_player.swing_timer <= 0:
                    bronze_player.sword_swing = False
            
            # Update warriors
            for warrior in bronze_warriors:
                warrior.update(platform_list)
            
            # Check sword-warrior collisions (swing attacks)
            sword_rect = bronze_player.get_sword_rect()
            for warrior in bronze_warriors:
                if warrior.rect.colliderect(sword_rect):
                    if warrior.take_damage():
                        bronze_player.score += warrior.points
            
            # Check warrior-player collision (damage)
            if pygame.sprite.spritecollide(bronze_player, bronze_warriors, False):
                bronze_player.health -= 1
                if bronze_player.health <= 0:
                    game_state = GAME_OVER
            
            # Wave complete
            if len(bronze_warriors) == 0:
                bronze_wave += 1
                spawn_bronze_warriors(bronze_wave)
            
            draw_bronze_game()

    elif game_state == MENU:
        draw_menu()
    
    elif game_state == DEV_MENU:
        draw_dev_menu()

    elif game_state == GAME_OVER:
        draw_game_over()

    pygame.display.flip()

pygame.quit()