import pygame
##### PANTALLA ####
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
screen_size = (ANCHO_PANTALLA, ALTO_PANTALLA)


######## RUTAS ################
image_folder = "1. parcial_pygame/imagenes/"
path_ruta = "./1. parcial_pygame/imagenes/pista.jpg"
path_auto = "./1. parcial_pygame/imagenes/auto_rosa.png"
path_fuente = "1. parcial_pygame/font/NFS.ttf"
path_coin = "1. parcial_pygame/imagenes/coin.png"

########### TAMAÑO AUTOS Y ENEMIGO ################
SIZE_AUTO = (80,150)
SIZE_ENEMIGO = (80,150)
SIZE_COIN = (30,30)

### VELOCIDAD AUTO ######
SPEED_AUTO = 5

######## COORDENADAS ENEMIGO ##################

X_MIN = 50  # Valor mínimo de coordenada X
X_MAX = screen_size[0] - 50  # Valor máximo de coordenada X
Y_MIN = -700  # Valor mínimo de coordenada Y
Y_MAX = -50  # Valor máximo de coordenada Y
FRECUENCIA_ENEMIGO = 100  # Aparece un nuevo enemigo cada 60 ciclos de juego
FRECUENCIA_COIN = 100
MAX_ENEMIGOS = 3  # Máximo 3 enemigos en pantalla al mismo tiempo


#### RELOJ ######
clock = pygame.time.Clock()
FPS = 120

#### COLORES #####

RED = (255, 0, 0)


###### DISPLAY #####
MARGEN = 160
DISPLAY_TOP = 0  #arriba
DISPLAY_BOTTOM = ALTO_PANTALLA  #abajo
DISPLAY_LEFT = MARGEN   #izquierda
DISPLAY_RIGHT = ANCHO_PANTALLA-MARGEN #derecha
DISPLAY_CENTER_X = ANCHO_PANTALLA // 2   #mitad en eje x
DISPLAY_CENTER_Y = ALTO_PANTALLA // 2  #mitad en eje y
DISPLAY_MIDTOP = (DISPLAY_CENTER_X, DISPLAY_TOP)  #mitad arriba
DISPLAY_MIDBOTTOM = (DISPLAY_CENTER_X, ALTO_PANTALLA)  #mitad abajo
DISPLAY_MIDLEFT = (DISPLAY_LEFT, DISPLAY_CENTER_Y)  #mitad izquierda
DISPLAY_MIDRIGHT = (DISPLAY_RIGHT, DISPLAY_CENTER_Y)  #mitad derecha
DISPLAY_CENTER = (DISPLAY_CENTER_X, DISPLAY_CENTER_Y)  #centro

#### coins ### 

coin_creation_timer = pygame.time.get_ticks()  # Tiempo actual en milisegundos
coin_intervalos = 5000 # Intervalo de tiempo en milisegundos entre la creación de monedas
num_monedas_total = 20  # Número total de monedas a crear
num_monedas_creadas = 0  # Contador de monedas creadas

score = 0