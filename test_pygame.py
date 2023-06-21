import pygame
from config import *
from auto import Auto
import sys, random, math
from datetime import datetime
from button import *

pygame.init()

# Tamaño de pantalla
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

fondo = pygame.image.load(path_ruta).convert()
fondo = pygame.transform.scale(fondo, screen_size)
fondo_alto = fondo.get_height()
vidas = 100

auto = Auto(path_auto, SIZE_AUTO,(screen.get_width()//2, screen.get_height()-20))
clock = pygame.time.Clock()


menu_principal = pygame.image.load(image_folder + "menuCar.jpg").convert()

class Coin(pygame.sprite.Sprite):
    def __init__(self, image_path, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen.get_height():
            self.kill()

coins_group = pygame.sprite.Group()

def crear_coin():
    global coin_creation_timer
    global num_monedas_creadas

    # Código para crear y agregar monedas al grupo
    image_path = path_coin  # Ruta de la imagen de la moneda
    coin_size = (30, 30)  # Tamaño de la moneda (ancho y alto en píxeles)

    if num_monedas_creadas < num_monedas_total:
        current_time = pygame.time.get_ticks()
        if current_time - coin_creation_timer >= coin_intervalos:
            # Asignar una posición aleatoria a la moneda dentro del área permitida
            coin_position = (random.randint(160, screen.get_width() - coin_size[0] - 160),
                             random.randint(-500, -50))  # Posición inicial arriba de la pantalla

            # Crear una instancia de la clase Coin con la imagen cargada, tamaño y posición
            coin = Coin(image_path, coin_size, coin_position)

            # Agregar la moneda al grupo coins_group
            coins_group.add(coin)

            num_monedas_creadas += 1
            coin_creation_timer = current_time

def mostrar_puntaje():
    font = pygame.font.Font(path_fuente, 20)
    text = font.render("SCORE: " + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 40))

def mostrar_vidas():
    font = pygame.font.Font(path_fuente, 25)
    text = font.render("Vidas: " + str(vidas), True, (255, 255, 255))
    screen.blit(text, (10, 10))

def mostrar_game_over():
    game_over_image = pygame.image.load(image_folder + "gameover.png").convert_alpha()
    screen.blit(game_over_image, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)  # Pausa el juego durante 3 segundos
    start_game()

class ManchaAceite(pygame.sprite.Sprite):
    def __init__(self, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_folder + "/mancha.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = position

# Crear un grupo para almacenar las manchas de aceite
manchas_group = pygame.sprite.Group()


# def crear_mancha_aceite():
    
#     mancha_size = (30, 30)  # Tamaño de la mancha de aceite (ancho y alto en píxeles)
#     num_manchas = 5  # Número de manchas de aceite a crear

#     for _ in range(num_manchas):
#         x = random.randint(0, screen.get_width() - mancha_size[0])  # Posición X aleatoria en la pantalla
#         y = random.randint(0, screen.get_height() - mancha_size[1])  # Posición Y aleatoria en la pantalla

#         mancha_image = pygame.image.load(image_folder + "mancha.png").convert_alpha()
#         mancha_image = pygame.transform.scale(mancha_image, mancha_size)
#         mancha = ManchaAceite(mancha_size, position=(x, y))
#         manchas_group.add(mancha)

#         # Retraso de 2 segundos antes de crear la siguiente mancha de aceite
#         time.sleep(2)


# Define la clase Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, image_path, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = random.randint(2, 5)  # Velocidad aleatoria de movimiento vertical


    def update(self):
        self.rect.y += self.speed  # Mover el enemigo hacia abajo
        if self.rect.y > screen.get_height():  # Si el enemigo se sale de la pantalla
            self.kill()  # Eliminar el enemigo


enemigos_group = pygame.sprite.Group()

def crear_enemigo():
    global timer

    if len(enemigos_group) < MAX_ENEMIGOS:  # Verificar la cantidad actual de enemigos
        timer += 1  # Incrementar el temporizador en cada iteración

        if timer >= FRECUENCIA_ENEMIGO:  # Controlar la frecuencia de aparición de los enemigos
            x = random.randint(auto.rect.left, auto.rect.right)  # Posición X aleatoria dentro del área del auto
            y = random.randint(-200, -50)  # Posición Y aleatoria arriba de la pantalla

            # Crear un enemigo con una imagen aleatoria
            if random.random() < 0.5:
                enemigo = Enemigo(image_folder + "taxi.png", SIZE_ENEMIGO, (x, y))
            else:
                enemigo = Enemigo(image_folder + "policia.png", SIZE_ENEMIGO, (x, y))

            enemigos_group.add(enemigo)

            timer = 0  # Reiniciar el temporizador después de crear un nuevo enemigo

            # Establecer posición Y negativa para que aparezcan arriba
            enemigo.rect.y = y

# COLLISION_RADIUS = 30  # Radio de colisión entre el auto y los enemigos

def enemigo_colision():
    global vidas
    global score

    colisiones = pygame.sprite.spritecollide(auto, enemigos_group, True)
    colisiones_coins = pygame.sprite.spritecollide(auto, coins_group, True)

    if colisiones:
        vidas -= 10  # Descuenta un 10% de vida por colisión con un enemigo
        explosion_image = pygame.image.load(image_folder + "explosion.png").convert_alpha()
        explosion_rect = explosion_image.get_rect()
        explosion_rect.center = colisiones[0].rect.center  # Posición de la primera colisión
        screen.blit(explosion_image, explosion_rect)

    if colisiones_coins:
        score += 10


def start_game():
    global pos_fondo, timer, vidas, score
    pos_fondo = 0
    timer = 0
    vidas = 100
    score = 0
    velocidad_auto = 5
    direccion_auto = (0, 0)

    while True:

        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    auto.velocidad_x = -SPEED_AUTO
                    print(auto.velocidad_x)
                elif evento.key == pygame.K_RIGHT:
                    auto.velocidad_x = SPEED_AUTO
                    print(auto.velocidad_x)

                elif evento.key == pygame.K_UP:
                    auto.velocidad_y = -SPEED_AUTO
                    print(auto.velocidad_y)
                elif evento.key == pygame.K_DOWN:
                    auto.velocidad_y = SPEED_AUTO
                    print(auto.velocidad_y)

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    auto.velocidad_x = 0
                    print(auto.velocidad_x)
                elif evento.key == pygame.K_RIGHT:
                    auto.velocidad_x = 0
                    print(auto.velocidad_x)

                elif evento.key == pygame.K_UP:
                    auto.velocidad_y = 0
                    print(auto.velocidad_y)
                elif evento.key == pygame.K_DOWN:
                    auto.velocidad_y = 0
                    print(auto.velocidad_y)
        pos_fondo += 5

        if auto.rect.left <= 0:
            auto.rect.left = 0
        elif auto.rect.right > screen.get_width():
            auto.rect.right = screen.get_width()
        elif auto.rect.bottom > screen.get_height():
            auto.rect.bottom = screen.get_height()

        crear_enemigo()
        enemigos_group.update()

        crear_coin()
        coins_group.update

        # crear_mancha_aceite()
        # manchas_group.update

        screen.blit(fondo, (0, pos_fondo))
        screen.blit(fondo, (0, pos_fondo - fondo_alto))


        mostrar_vidas()
        mostrar_puntaje()

        screen.blit(auto.image, auto.rect)
        auto.update()

        for enemigo in enemigos_group:
            enemigo.update()

        enemigos_group.draw(screen)
        auto.update()

        enemigo_colision()


        # Verificar si se necesita reiniciar la posición del fondo
        if pos_fondo >= fondo_alto:
            pos_fondo = 0

        if vidas <= 0:
            # Acción a realizar cuando las vidas llegan a cero (por ejemplo, reiniciar el juego o mostrar "Game Over")
            # Reiniciar el juego
            pos_fondo = 0
            timer = 0
            mostrar_game_over()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:  # Si se presiona la tecla Enter
                main_menu()  # Regresar al menú principal

        colisiones_coins = pygame.sprite.spritecollide(auto, coins_group, True)

        if colisiones_coins:
            score += 10

        

        if pygame.sprite.spritecollide(auto, manchas_group, False):
        # Modificar la dirección del movimiento del auto para desviarlo
            for mancha in pygame.sprite.spritecollide(auto, manchas_group, False):
                dx = mancha.rect.centerx - auto.rect.centerx
                dy = mancha.rect.centery - auto.rect.centery
                magnitud = math.sqrt(dx**2 + dy**2)
                if magnitud > 0:
                    direccion_auto = (dx / magnitud, dy / magnitud)
                else:
                    direccion_auto = (0, 0)

                    # Actualizar la posición del auto en función de la dirección y velocidad
        auto.rect.x += velocidad_auto * direccion_auto[0]
        auto.rect.y += velocidad_auto * direccion_auto[1]

        coins_group.update()
        coins_group.draw(screen)

        manchas_group.update()
        manchas_group.draw(screen)
    

        pygame.display.flip()
        clock.tick(60)

def get_font(size):
    return pygame.font.Font(path_fuente, size)


def play():
    PLAY_BUTTON = Button(image=None, pos=(640, 250), text_input="PLAY", font=get_font(75), base_color="#f700ff",
                         hovering_color="Pink")

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    pygame.time.wait(500)
                    start_game()  # Llamar a la función "start_game()" para iniciar el juego

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(25).render("Para mover el auto tiene que utilizar las fechas del teclado.", True,
                                           "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(60), base_color="Black", hovering_color="Pink")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        screen.blit(menu_principal, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load(image_folder + "PlayRect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(30), base_color="#3b3b3b", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load(image_folder + "OptionsRect.png"), pos=(640, 320),
                                text_input="Instrucciones", font=get_font(30), base_color="#3b3b3b",
                                hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(image_folder + "QuitRect.png"), pos=(640, 390),
                             text_input="QUIT", font=get_font(30), base_color="#3b3b3b", hovering_color="White")

        PLAY_BUTTON.changeColor(MENU_MOUSE_POS)
        OPTIONS_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)

        PLAY_BUTTON.update(screen)
        OPTIONS_BUTTON.update(screen)
        QUIT_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.time.wait(500)
                    start_game()  # Llamar a la función "start_game()" para iniciar el juego
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()  # Llamar a la función "options()" para mostrar las instrucciones
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main_menu()


