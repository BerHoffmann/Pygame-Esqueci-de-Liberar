import pygame as pg
import pytmx

from settings import *


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


class Camera:
    def __init__(self, width, height):
        '''construtor da camera'''
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        '''atualiza a camera'''
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limita para os lados do mapa
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)


class TiledMap:
    def __init__(self, filename):
        '''construtor do mapa'''
        tmap = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tmap.width * tmap.tilewidth
        self.height = tmap.height * tmap.tileheight
        self.tmxdata = tmap

    def render(self, surface):
        '''renderiza mapa'''
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        '''faz o mapa'''
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
