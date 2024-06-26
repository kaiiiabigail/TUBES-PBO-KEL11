import pygame
import os
import src.spritesheet as spritesheet
import src.settings as settings
import src.entities as entities
import src.ui as ui



class Win:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.font = pygame.font.Font(
            os.path.join('assets', 'Monocraft.ttf'), 32)

        self.title = pygame.image.load(
            os.path.join('assets', 'winner_title.png')).convert_alpha()
        self.title = pygame.transform.scale(
            self.title, (self.title.get_width() * 0.5, self.title.get_height() * 0.5))
        self.name = self.font.render(
            'Made by Kobs Corps', False, (255, 255, 255))
        self.using = self.font.render(
            'Press ENTER to Play Again', False, (255, 255, 255))
        
        self.background = pygame.Surface(
            self.screen.get_size()).convert_alpha()
        self.background.set_alpha(100)
        self.background.fill((63, 56, 81, 50))
        
        self.set_game_state = None  # We will set this later in the main Game class
        self.reset_game = None  # We will set this later in the main Game class
        
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            self.play_again()

    def play_again(self):
        if self.set_game_state and self.reset_game:
            self.reset_game()
            self.set_game_state('game')

    def update(self):
        self.input()
        self.render()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.name, (self.screen.get_width(
        ) / 2 - self.name.get_width() / 2, self.screen.get_height() / 2 + 100))
        self.screen.blit(self.using, (self.screen.get_width(
        ) / 2 - self.using.get_width() / 2, self.screen.get_height() / 2 + 150))
        self.screen.blit(self.title, (self.screen.get_width() /
                         2 - self.title.get_width() / 2, self.screen.get_height() / 1.5 - self.title.get_height() * 1.5))



class Lose:
    def __init__(self, screen, reset_level, set_state) -> None:
        self.screen = screen
        self.reset_level = reset_level
        self.set_game_state = set_state
        self.font = pygame.font.Font(
            os.path.join('assets', 'Monocraft.ttf'), 32)

        self.title = pygame.image.load(
            os.path.join('assets', 'lose_title.png')).convert_alpha()
        self.title = pygame.transform.scale(
            self.title, (self.title.get_width() * 0.5, self.title.get_height() * 0.5))
        self.hint = self.font.render(
            'press ENTER to retry', False, (255, 255, 255))

        self.background = pygame.Surface(
            self.screen.get_size()).convert_alpha()
        self.background.set_alpha(100)
        self.background.fill((63, 56, 81))

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            self.reset_level()
            self.set_game_state('game')

    def update(self):
        self.input()
        self.render()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.hint, (self.screen.get_width(
        ) / 2 - self.hint.get_width() / 2, self.screen.get_height() / 2 + 100))
        self.screen.blit(self.title, (self.screen.get_width() /
                         2 - self.title.get_width() / 2, self.screen.get_height() / 1.5 - self.title.get_height() * 1.5))


class Pause:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.font = pygame.font.Font(
            os.path.join('assets', 'Monocraft.ttf'), 32)

        self.title = pygame.image.load(
            os.path.join('assets', 'pause_title.png')).convert_alpha()
        self.title = pygame.transform.scale(
            self.title, (self.title.get_width() * 0.5, self.title.get_height() * 0.5))
        self.unpause_hint = self.font.render(
            'press ESC to unpause', False, (255, 255, 255))

        self.background = pygame.Surface(
            self.screen.get_size()).convert_alpha()
        self.background.set_alpha(100)
        self.background.fill((63, 56, 81, 50))

    def update(self):
        self.render()
   
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.unpause_hint, (self.screen.get_width(
        ) / 2 - self.unpause_hint.get_width() / 2, self.screen.get_height() / 2 + 100))
        self.screen.blit(self.title, (self.screen.get_width() /
                         2 - self.title.get_width() / 2, self.screen.get_height() / 1.5 - self.title.get_height() * 1.5))


class Level:
    def __init__(self, screen, swap_level, set_state, curr_level) -> None:
        self.layout = settings.Level_data()
        self.deco_layout = settings.Level_decor()
        self.entity_data = entities.Entity_data()

        self.screen = screen
        self.level_cleared = False
        self.swap_level = swap_level
        self.curr_level = curr_level

        self.entities = []
        self.player = entities.Player(screen, set_state)
        self.entities.append(self.player)
        self.scroll_speed = 0
        self.player_vel = self.player.velocity

        self.terrain_tiles = spritesheet.TerrainTiles()
        self.decoratione_tiles = spritesheet.DecorationTiles()
        self.map = []
        self.collidables = []

        self.enter_door = None
        self.exit_door = None

        self.ui = ui.Healthbar(self.screen)

        self.load()
        self.setup_level()
        if self.curr_level == 0:
            self.setup_tutorial()

        self.enter_door.close_sound.play()

    def load(self):
        for row_id, row in enumerate(self.layout.levels[self.curr_level]):
            for tile_id, tile in enumerate(row):
                if tile in self.terrain_tiles.background.keys():
                    position = (tile_id * settings.tile_size,
                                row_id * settings.tile_size)
                    t = spritesheet.Tile(
                        self.terrain_tiles.background[tile], position, (settings.tile_size, settings.tile_size))
                    self.map.append(t)
                elif tile in self.terrain_tiles.walls.keys():
                    position = (tile_id * settings.tile_size,
                                row_id * settings.tile_size)
                    t = spritesheet.Tile(
                        self.terrain_tiles.walls[tile], position, (settings.tile_size, settings.tile_size))
                    self.map.append(t)
                    self.collidables.append(t)

        for row_id, row in enumerate(self.deco_layout.levels[self.curr_level]):
            for tile_id, tile in enumerate(row):
                if tile in self.decoratione_tiles.decorations.keys():
                    position = (tile_id * settings.tile_size,
                                row_id * settings.tile_size)
                    t = spritesheet.Tile(
                        self.decoratione_tiles.decorations[tile], position, (settings.tile_size, settings.tile_size))
                    self.map.append(t)
                if tile in self.decoratione_tiles.platforms.keys():
                    position = (tile_id * settings.tile_size,
                                row_id * settings.tile_size)
                    t = spritesheet.Tile(
                        self.decoratione_tiles.platforms[tile], position, (settings.tile_size, settings.tile_size))
                    self.map.append(t)
                    self.collidables.append(t)

    def setup_tutorial(self):
        self.title = pygame.image.load(
            os.path.join('assets', 'king and pigs.png')).convert_alpha()
        self.title = pygame.transform.scale(
            self.title, (self.title.get_width() * 0.2, self.title.get_height() * 0.2))

        self.a_key = spritesheet.Tile(
            self.decoratione_tiles.hints['L'], (600, 400), self.decoratione_tiles.hints['L'].get_size())
        self.d_key = spritesheet.Tile(
            self.decoratione_tiles.hints['R'], (680, 400), self.decoratione_tiles.hints['R'].get_size())
        self.w_key = spritesheet.Tile(
            self.decoratione_tiles.hints['J'], (640, 350), self.decoratione_tiles.hints['J'].get_size())
        self.space_key = spritesheet.Tile(
            self.decoratione_tiles.hints['A'], (1500, 400), self.decoratione_tiles.hints['A'].get_size())
        self.enter_key = spritesheet.Tile(
            self.decoratione_tiles.hints['E'], (2000, 400), self.decoratione_tiles.hints['E'].get_size())

        self.map.append(self.a_key)
        self.map.append(self.d_key)
        self.map.append(self.w_key)
        self.map.append(self.space_key)
        self.map.append(self.enter_key)

    def setup_level(self):
        for item in self.entity_data.levels[self.curr_level]:
            item.screen = self.screen
            self.map.append(item)

            if isinstance(item, entities.Enemy):
                self.entities.append(item)
            elif isinstance(item, entities.Box):
                self.collidables.append(item)
            elif isinstance(item, entities.Door):
                if item.state == 'exit':
                    self.exit_door = item
                    item.change_scene = self.swap_level
                else:
                    self.enter_door = item

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.player.direction.x = -1
            self.player.flip_sprite = True
            self.player.animation_manager.set_state('run')
        elif keys[pygame.K_d]:
            self.player.direction.x = 1
            self.player.flip_sprite = False
            self.player.animation_manager.set_state('run')
        else:
            self.player.direction.x = 0
            self.player.animation_manager.set_state('idle')

        if keys[pygame.K_w]:
            if not self.player.is_in_air:
                self.player.jump()

        if keys[pygame.K_SPACE]:
            self.player.attack()

        if keys[pygame.K_RETURN] and self.player.rect.colliderect(self.exit_door.rect):
            if not self.level_cleared:
                self.exit_door.open_sound.play()
                self.player.animation_manager.set_state('enter_door')
                self.exit_door.animation_manager.set_state('open')
                self.level_cleared = not self.level_cleared

    def vertical_collision(self):
        for entity in self.entities:
            entity.gravity()

            for tile in self.collidables:
                if tile.rect.colliderect(entity.rect):
                    if entity.direction.y > 0:
                        entity.rect.bottom = tile.rect.top
                        entity.is_in_air = False
                    elif entity.direction.y < 0:
                        entity.rect.top = tile.rect.bottom
                    entity.direction.y = 0

    def horizontal_collision(self):
        for entity in self.entities:
            for tile in self.collidables:
                if tile.rect.colliderect(entity.rect):
                    if entity.direction.x > 0:
                        entity.rect.right = tile.rect.left
                    elif entity.direction.x < 0:
                        entity.rect.left = tile.rect.right
                    entity.direction.x = 0

    def move_map(self):
        for tile in self.map:
            tile.rect.x += self.scroll_speed
            if isinstance(tile, entities.Enemy):
                tile.walk_area[0] += self.scroll_speed
                tile.walk_area[1] += self.scroll_speed

    def scroll_map(self):
        if self.player.rect.x > self.screen.get_width()/2 + 100 and self.player.direction.x > 0:
            self.scroll_speed = -self.player_vel
            self.player.velocity = 0
            self.move_map()
        elif self.player.rect.x < self.screen.get_width()/2 - 200 and self.player.direction.x < 0:
            self.player.velocity = 0
            self.scroll_speed = self.player_vel
            self.move_map()
        else:
            self.scroll_speed = 0
            self.player.velocity = self.player_vel

    def show_tutorial(self):
        self.screen.blit(self.title, (self.screen.get_width() /
                                      2 - self.title.get_width()/2, 200))

    def update(self):
        self.render()
        self.scroll_map()
        self.horizontal_collision()
        self.vertical_collision()
        self.input()
        self.ui.update()

        self.enter_door.update()
        self.exit_door.update()

        # worse hitreg I've written lol
        for e in self.entities:
            e.update()
            if isinstance(e, entities.Enemy):
                if e.rect.colliderect(self.player.hurtbox) and self.player.can_deal_dmg:
                    e.take_damage()
                if e.rect.colliderect(self.player.rect) and self.player.can_take_damage and e.animation_manager.state != 'dead':
                    self.player.take_damage()
                    self.ui.took_damage()
                if e.is_dead():
                    self.entities.remove(e)
                    self.map.remove(e)

    def render(self):
        # render tiles
        for tile in self.map:
            if isinstance(tile, entities.Enemy):
                continue
            elif isinstance(tile, entities.Box):
                tile.render()
            tile.surface.set_colorkey((0, 0, 0))
            self.screen.blit(tile.surface, tile.rect)

        if self.curr_level == 0:
            self.show_tutorial()

        self.enter_door.render()
        self.exit_door.render()

        for e in self.entities:
            e.render()

        self.ui.render()