import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


def draw_time_bar(surf, x, y, pct):
    '''desenha a barra de tempo'''
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        '''construtor da classe Game'''
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        '''desenha texto na tela, recebendo qual esse texto, posição, fonte, cor e alinhamento'''
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def load_data(self):
        '''carrega os dados para o jogo'''

        # pastas
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        img_folder = path.join(game_folder, 'img')
        sounds_folder = path.join(game_folder, 'sounds')

        # fontes
        self.hud_font = path.join(img_folder, 'Cabin.ttf')
        self.title_font = path.join(img_folder, 'lazer84.ttf')

        # mapa
        self.map = TiledMap(path.join(map_folder, 'mapav2.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # imagens
        self.bg_img = pg.image.load(
            path.join(img_folder, 'background.png'))
        self.bg_img = pg.transform.scale(self.bg_img, ((WIDTH, HEIGHT)))
        self.player_img = pg.image.load(
            path.join(img_folder, 'moto_V2.png')).convert_alpha()
        self.PA_img = pg.image.load(
            path.join(img_folder, 'PA.png')).convert_alpha()
        self.flecha_img = pg.image.load(
            path.join(img_folder, 'flecha.png')).convert_alpha()
        self.pizza_img = pg.image.load(
            path.join(img_folder, 'pizza.png')).convert_alpha()

        # tela
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        # sons
        pg.mixer.music.load(path.join(sounds_folder, BG_MUSIC))
        pg.mixer.music.set_volume(0.5)
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(
                path.join(sounds_folder, EFFECTS_SOUNDS[type]))
        self.effects_sounds['moto'].set_volume(0.05)

    def new(self):
        '''inicializa variáveis para um novo jogo'''
        self.effects_sounds['menu'].stop()
        self.time = 0
        self.go_message = ''
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grass = pg.sprite.Group()
        self.pizza = pg.sprite.Group()
        self.PA = pg.sprite.Group()
        self.agua = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:

            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)

            if tile_object.name == 'PA':
                PA(self, tile_object.x, tile_object.y,
                   PA_BASE_SPEED - 50 + 8*len(self.PA))

            if tile_object.name == 'obs':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)

            if tile_object.name == 'rua':
                Grama(self, tile_object.x, tile_object.y,
                      tile_object.width, tile_object.height)

            if tile_object.name == 'agua':
                Agua(self, tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height)

            if tile_object.name == 'pizza':
                Pizza.pizza_places.append((tile_object.x, tile_object.y))

        Pizza(self)
        self.flecha = Flecha(self)
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False

    def run(self):
        '''define o loop para rodar o jogo'''
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.time > MAX_TIME:
                self.go_message = 'Você demorou muito para entregar a pizza'
                self.playing = False
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        '''sai do jogo'''
        pg.quit()
        sys.exit()

    def update(self):
        '''atualiza o jogo'''
        self.all_sprites.update()
        self.time += 1/60
        if round(self.time, 2) == MAX_TIME - 8:
            self.effects_sounds['clock'].play()
        self.camera.update(self.player)

    def draw_grid(self):
        '''desenha grid do mapa'''
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        '''desenha mapa, hub e sprites'''
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            if not sprite == self.player or not self.flecha:
                self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.screen.blit(self.player.image, self.camera.apply(self.player))
        self.screen.blit(self.flecha.image, self.flecha.rect)

        # Hub
        draw_time_bar(self.screen, 10, 10, (MAX_TIME - self.time) / MAX_TIME)

        self.draw_text('Pizzas entregues: {}'.format(self.player.qtepizzas), self.hud_font, 30, RED,
                       WIDTH - 10, 10, align="topright")
        self.draw_text("PA's: {}".format(len(self.PA)), self.hud_font, 30, RED,
                       WIDTH - 10, 50, align="topright")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Pausado", self.title_font, 105, RED,
                           WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        '''capta os eventos'''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    if self.paused == False:
                        self.paused = True
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                        self.paused = False

    def show_start_screen(self):
        '''mostra a tela de início'''
        self.effects_sounds['menu'].play()
        self.screen.fill(BLACK)
        self.screen.blit(self.bg_img, (0, 0))
        self.draw_text("3030: Esqueci de", self.title_font, TITLESIZE, DARKRED,
                       25*WIDTH / 96, 5 * HEIGHT / 36, align="center")
        self.draw_text("Liberar", self.title_font, TITLESIZE, DARKRED,
                       25*WIDTH / 96, 25 * HEIGHT / 108, align="center")

        start = self.draw_text("Iniciar", self.hud_font, TEXTSIZE, DARKRED,
                               5 * WIDTH / 16, 85 * HEIGHT / 108, align="center")

        instructions = self.draw_text("Instruções", self.hud_font, TEXTSIZE, DARKRED,
                                      5 * WIDTH / 16, 95 * HEIGHT / 108, align="center")
        pg.display.flip()
        self.wait_for_click(start, instructions)

    def como_jogar_screen(self):
        '''mostra a tela de instruções'''
        self.screen.fill(BLACK)
        d = 55
        h = 70
        self.draw_text("~", self.hud_font, 100, DARKRED,
                       55/96 * WIDTH, 13 * HEIGHT / 108, align="center")
        self.draw_text("Instruçoes", self.title_font, TITLESIZE, DARKRED,
                       WIDTH / 2, HEIGHT / 6, align="center")
        self.draw_text("Você é um entregador de pizza que entrou na portaria sem ser liberado! A polícia está atrás de você!", self.hud_font, INSTSIZE, WHITE,
                       WIDTH / 2, HEIGHT / 6 + d + h, align="center")
        self.draw_text("Ande pelo mapa usando as teclas WASD ou setas (direita e esquerda rotacionam a moto).", self.hud_font, INSTSIZE, WHITE,
                       WIDTH / 2, HEIGHT / 6 + 2*d + h, align="center")
        self.draw_text("Andar pela grama diminui sua velocidade e há blocos intransponíveis no mapa. Não ande através do lago!", self.hud_font, INSTSIZE, WHITE,
                       WIDTH / 2, HEIGHT / 6 + 3*d + h, align="center")
        self.draw_text("Para entregar as pizzas, siga a seta do canto superior esquerdo para encontrá-las.", self.hud_font, INSTSIZE, WHITE,
                       WIDTH / 2, HEIGHT / 6 + 4*d + h, align="center")
        self.draw_text("É preciso pressionar a barra de espaço para efetuar a entrega.", self.hud_font, INSTSIZE, WHITE,
                       WIDTH / 2, HEIGHT / 6 + 5*d + h, align="center")
        self.draw_text("Cuidado. Há um tempo limite para realizar a entrega!", self.hud_font, INSTSIZE, WHITE,
                       WIDTH / 2, HEIGHT / 6 + 6*d + h, align="center")
        self.draw_text("Evite que a polícia o encontre!", self.hud_font, INSTSIZE, WHITE,
                       WIDTH / 2, HEIGHT / 6 + 7*d + h, align="center")

        start = self.draw_text("Iniciar", self.hud_font, TEXTSIZE, DARKRED,
                               WIDTH / 2, HEIGHT * 7 / 8, align="center")
        pg.display.flip()
        self.wait_for_click(start)

    def show_go_screen(self):
        '''mostra a tela de game over'''
        pg.mixer.music.stop()
        self.effects_sounds['moto'].stop()
        self.effects_sounds['clock'].stop()
        self.effects_sounds['game_over'].play()
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, DARKRED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text(self.go_message, self.hud_font, TEXTSIZE + 10, WHITE,
                       WIDTH / 2, HEIGHT * 2/3, align="center")
        self.draw_text("Pressione ESPAÇO para tentar novamente", self.hud_font, TEXTSIZE - 10, WHITE,
                       WIDTH / 2, HEIGHT * 4 / 5, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        '''espera por tecla para executar função'''
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        self.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        self.effects_sounds['game_over'].stop()
                        waiting = False

    def wait_for_click(self, button1, button2=False):
        '''espera por clique nos botoes passados por parâmetro para executar função'''
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed()[0] and button1.collidepoint(pg.mouse.get_pos()):
                        waiting = False
                    if button2 and pg.mouse.get_pressed()[0]:
                        if button2.collidepoint(pg.mouse.get_pos()):
                            waiting = False
                            self.como_jogar_screen()


# cria o jogo
g = Game()

# mostra a tela de inicio
g.show_start_screen()

# inicia o loop do jogo
while True:
    g.new()
    g.run()
    g.show_go_screen()
