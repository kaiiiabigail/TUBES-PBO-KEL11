import pygame
import src.settings as settings
import os


class Spritesheet:
    def __init__(self, image, size) -> None:
        self.sheet = image
        self.frame = pygame.Surface(size)
        self.width, self.height = size
        self.length = (self.sheet.get_width() / self.width) - 1

    def get_length(self):
        return self.length

    def fetch_frame(self, current_frame, row=0, scale=2):
        self.frame = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.frame.blit(self.sheet, (0, 0),
                        (self.width * current_frame, self.height * row, self.width, self.height))
        self.frame = pygame.transform.scale(
            self.frame, (self.width * scale, self.height * scale))

        return self.frame


class Tile():
    def __init__(self, sprite, pos, size):
        self.surface = sprite
        self.rect = pygame.Rect(pos, size)

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y


# generating levels from a list of strings
# might change this to images if it seems worth it
# or find something that's way better...
class TerrainTiles:
    def __init__(self) -> None:
        self.background_tileset = Spritesheet(pygame.image.load(
            os.path.join('assets', 'environment', 'terrain.png')).convert_alpha(), (32, 32))

        self.background = {
            'A': self.background_tileset.fetch_frame(1, 7),
            'B': self.background_tileset.fetch_frame(2, 7),
            'C': self.background_tileset.fetch_frame(3, 7),
            'D': self.background_tileset.fetch_frame(1, 8),
            'E': self.background_tileset.fetch_frame(2, 8),
            'F': self.background_tileset.fetch_frame(3, 8),
            'G': self.background_tileset.fetch_frame(1, 9),
            'H': self.background_tileset.fetch_frame(2, 9),
            'I': self.background_tileset.fetch_frame(3, 9),
        }

        self.walls = {
            'J': self.background_tileset.fetch_frame(1, 1),
            'K': self.background_tileset.fetch_frame(2, 1),
            'L': self.background_tileset.fetch_frame(3, 1),
            'M': self.background_tileset.fetch_frame(1, 2),
            'N': self.background_tileset.fetch_frame(3, 2),
            'O': self.background_tileset.fetch_frame(1, 3),
            'P': self.background_tileset.fetch_frame(2, 3),
            'Q': self.background_tileset.fetch_frame(3, 3),

            'R': self.background_tileset.fetch_frame(7, 1),
            'S': self.background_tileset.fetch_frame(8, 1),
            'T': self.background_tileset.fetch_frame(7, 2),
            'U': self.background_tileset.fetch_frame(8, 2),

            'V': self.background_tileset.fetch_frame(5, 1),
            'W': self.background_tileset.fetch_frame(5, 2),
            'X': self.background_tileset.fetch_frame(5, 3),

            'Y': self.background_tileset.fetch_frame(11, 1),
            'Z': self.background_tileset.fetch_frame(10, 2)
        }


class DecorationTiles:
    def __init__(self) -> None:
        self.decorations_tileset = Spritesheet(pygame.image.load(
            os.path.join('assets', 'environment', 'decorations.png')).convert_alpha(), (32, 32))

        self.decorations = {
            'W': self.decorations_tileset.fetch_frame(2, 3),
            'I': self.decorations_tileset.fetch_frame(3, 3),
            'N': self.decorations_tileset.fetch_frame(2, 4),
            'D': self.decorations_tileset.fetch_frame(3, 4),

            'F': self.decorations_tileset.fetch_frame(1, 1),
            'G': self.decorations_tileset.fetch_frame(1, 2),
            'S': self.decorations_tileset.fetch_frame(1, 3),
        }

        self.platforms = {
            'P': self.decorations_tileset.fetch_frame(2, 2),
            'L': self.decorations_tileset.fetch_frame(3, 2),
            'A': self.decorations_tileset.fetch_frame(4, 2),
            'T': self.decorations_tileset.fetch_frame(5, 2),
        }

        self.hints = {
            'L': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'buttons', 'a_key.png')).convert_alpha(), (settings.tile_size, settings.tile_size)),
            'R': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'buttons', 'd_key.png')).convert_alpha(), (settings.tile_size, settings.tile_size)),
            'J': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'buttons', 'w_key.png')).convert_alpha(), (settings.tile_size, settings.tile_size)),
            'A': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'buttons', 'space_key.png')).convert_alpha(), (settings.tile_size, settings.tile_size)),
            'E': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'buttons', 'enter_key.png')).convert_alpha(), (settings.tile_size, settings.tile_size)),
        }


