import pygame as pg

# define cores (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARKRED = (139, 0, 0)
YELLOW = (255, 255, 0)

# configurações do jogo
WIDTH = 1280
HEIGHT = 720
TITLESIZE = int(80 * WIDTH / 1920)
TEXTSIZE = int(50 * WIDTH / 1920)
INSTSIZE = int(36 * WIDTH / 1920)
FPS = 60
TITLE = "3030: Esqueci de Liberar"
BGCOLOR = DARKGREY

TILESIZE = 72
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# configurações do jogador
PLAYER_SPEED = 500
PLAYER_ROT_SPEED = 200
PLAYER_HIT_RECT = pg.Rect(0, 0, 40, 72)
MAX_TIME = 80

# configurações da PA
PA_BASE_SPEED = 300
PA_UP_SPEED = 30
PA_HIT_RECT = pg.Rect(0, 0, 50, 50)

# configurações dos sons
BG_MUSIC = 'jogo.mp3'
EFFECTS_SOUNDS = {'pick_pizza': 'pick_pizza.mp3',
                  'clock': 'ticking_clock.wav',
                  'game_over': 'game_over.mp3',
                  'menu': 'tela_inicial.mp3',
                  'moto': 'moto1.wav'
                  }
