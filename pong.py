import pygame
from pygame import *
from pygame.locals import *
import random
import sys

ANCHO = 800
ALTO = 555

FPS = 60
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
NARANJA = (237, 128, 19)

VELOCIDAD_PELOTA = 7
VELOCIDAD_RAQUETA_JUGADOR = 10
VELOCIDAD_RAQUETA_IA = VELOCIDAD_PELOTA - 1

PUNTUACION_GANADOR = 3

def imagen_random():
    img = []
    img.append(pygame.image.load("Assets/bola_amarilla.png"))
    img.append(pygame.image.load("Assets/bola_azul.png"))
    img.append(pygame.image.load("Assets/bola_roja.png"))
    img.append(pygame.image.load("Assets/bola_verde.png"))
    imagen = img[random.randint(0, len(img) - 1)]
    return imagen

class Pelota:
    def __init__(self):
        self.imagen = imagen_random()
        self.ancho, self.alto = self.imagen.get_size()

        # Coordenadas de posicion.
        #self.posicion = (ANCHO/2 - self.ancho/2, ALTO/2 - self.alto/2)
        self.x = ANCHO/2 - self.ancho/2
        self.y = ALTO/2 - self.alto/2
        # Direccion en la que mira.

        self.dir_x = random.choice([-VELOCIDAD_PELOTA, VELOCIDAD_PELOTA])
        self.dir_y = random.choice([-VELOCIDAD_PELOTA, VELOCIDAD_PELOTA])
        
        self.puntuacion = 0
        self.puntuacion_ia = 0
        
        self.jugando = True

    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def colision(self):
        if self.x <= 0:
            self.dir_x = -self.dir_x
        if self.x + self.ancho >= ANCHO:
            self.dir_x = -self.dir_x

        if self.y <= 0:
            self.dir_y = -self.dir_y
        if self.y + self.alto >= ALTO:
            self.dir_y = -self.dir_y
    
    def rebotar(self):
        if self.y <= 0:
            self.dir_y = -self.dir_y
        if self.y + self.alto >= ALTO:
            self.dir_y = -self.dir_y 

    def reiniciar(self):
        self.imagen = imagen_random()
        if self.x <= -self.ancho:
            self.puntuacion_ia += 1
        if self.x >= ANCHO:
            self.puntuacion += 1
        self.x = ANCHO / 2 - self.ancho / 2
        self.y = ALTO / 2 - self.alto / 2
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-VELOCIDAD_PELOTA, VELOCIDAD_PELOTA])
            
    
class Raqueta:
    def __init__(self):
        self.imagen = pygame.image.load("Assets/raqueta_blanca.png").convert_alpha()
        
        self.ancho, self.alto = self.imagen.get_size()
        
        self.x = 0
        self.y = ALTO/2 - self.alto/2
        
        self.dir_y = 0

    def mover(self):
        self.y += self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= ALTO:
            self.y = ALTO - self.alto
    
    def golpear(self, pelota):
        if (
            pelota.x < self.x + self.ancho
            and pelota.x > self.x
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
            ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho
    def mover_ia(self, pelota):
        if self.y > pelota.y:
            self.dir_y = -VELOCIDAD_RAQUETA_IA
        elif self.y < pelota.y:
            self.dir_y = VELOCIDAD_RAQUETA_IA
        else:
            self.dir_y = 0
        
        self.y += self.dir_y
        if self.y + self.alto >= ALTO:
            self.y = ALTO - self.alto
    def golpear_ia(self, pelota):
        if (
            pelota.x + pelota.ancho > self.x
            and pelota.x < self.x + self.ancho
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
            ):
            pelota.dir_x = -pelota.dir_x
            #pelota.x = self.x - self.ancho
            pelota.x = self.x - pelota.ancho
        

def main(modo_de_juego):
    pygame.init()

    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PONG")

    #Cambiamos el fondo de juego dependiendo del seleccionado por el usuario
    if (modo_de_juego == 1):
        fondo_juego = pygame.image.load("Assets/fondo_juego_1.png").convert()
    elif (modo_de_juego == 2):
        fondo_juego = pygame.image.load("Assets/fondo_juego_2.png").convert()
    else:
        fondo_juego = pygame.image.load("Assets/fondo_juego_3.png").convert()
        
    fuente = pygame.font.Font(None, 60)

    pelota = Pelota()
    
    raquetaJugador = Raqueta()
    raquetaJugador.x = 30
    
    raquetaIA = Raqueta()
    raquetaIA.x = ANCHO - (30 + raquetaIA.ancho)
    
    while(pelota.jugando):
        pelota.mover()
        pelota.rebotar()
        raquetaJugador.mover()
        raquetaJugador.golpear(pelota)
        raquetaIA.mover_ia(pelota)
        raquetaIA.golpear_ia(pelota)

        #ventana.fill(BLANCO)
        ventana.blit(fondo_juego, [0, 0])
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))
        ventana.blit(raquetaJugador.imagen, (raquetaJugador.x, raquetaJugador.y))
        ventana.blit(raquetaIA.imagen, (raquetaIA.x, raquetaIA.y))
        
        texto = f"{pelota.puntuacion}  {pelota.puntuacion_ia}"
        letrero = fuente.render(texto, False, BLANCO)
        ventana.blit(letrero, (ANCHO / 2 - fuente.size(texto)[0] / 2, 50))
        
        if pelota.x <= 0 or pelota.x + pelota.ancho >= ANCHO:
            texto_reiniciar = f"Pulse espacio para jugar"
            letrero_reiniciar = fuente.render(texto_reiniciar, False, NEGRO)
            ventana.blit(letrero_reiniciar, (ANCHO / 2 - fuente.size(texto_reiniciar)[0] / 2, ALTO / 2))
            
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

        if pelota.puntuacion >= PUNTUACION_GANADOR or pelota.puntuacion_ia >= PUNTUACION_GANADOR:
            pantalla_final(pelota, 1, modo_de_juego)
            pelota.jugando = False

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pelota.jugando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    raquetaJugador.dir_y = -VELOCIDAD_RAQUETA_JUGADOR
                if evento.key == pygame.K_s:
                    raquetaJugador.dir_y = VELOCIDAD_RAQUETA_JUGADOR
                if evento.key == pygame.K_UP:
                    raquetaJugador.dir_y = -VELOCIDAD_RAQUETA_JUGADOR
                if evento.key == pygame.K_DOWN:
                    raquetaJugador.dir_y = VELOCIDAD_RAQUETA_JUGADOR
                    
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_w:
                    raquetaJugador.dir_y = 0
                if evento.key == pygame.K_s:
                    raquetaJugador.dir_y = 0
                if evento.key == pygame.K_UP:
                    raquetaJugador.dir_y = 0
                if evento.key == pygame.K_DOWN:
                    raquetaJugador.dir_y = 0
                if evento.key == pygame.K_SPACE:
                    if pelota.x <= 0 or pelota.x + pelota.ancho >= ANCHO:
                        pelota.reiniciar()    

    pygame.quit()
    
def main2(modo_de_juego):
    pygame.init()

    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PONG")

    #Cambiamos el fondo de juego dependiendo del seleccionado por el usuario
    if (modo_de_juego == 1):
        fondo_juego = pygame.image.load("Assets/fondo_juego_1.png").convert()
    elif (modo_de_juego == 2):
        fondo_juego = pygame.image.load("Assets/fondo_juego_2.png").convert()
    else:
        fondo_juego = pygame.image.load("Assets/fondo_juego_3.png").convert()
    
    fuente = pygame.font.Font(None, 60)

    pelota = Pelota()
    
    raquetaJugador = Raqueta()
    raquetaJugador.x = 30
    
    raquetaJugador2 = Raqueta()
    raquetaJugador2.x = ANCHO - (30 + raquetaJugador2.ancho)

    jugando = True
    while(jugando):
        pelota.mover()
        pelota.rebotar()
        raquetaJugador.mover()
        raquetaJugador.golpear(pelota)
        raquetaJugador2.mover()
        raquetaJugador2.golpear_ia(pelota)

        #ventana.fill(BLANCO)
        ventana.blit(fondo_juego, [0, 0])
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))
        ventana.blit(raquetaJugador.imagen, (raquetaJugador.x, raquetaJugador.y))
        ventana.blit(raquetaJugador2.imagen, (raquetaJugador2.x, raquetaJugador2.y))
        
        texto = f"{pelota.puntuacion}  {pelota.puntuacion_ia}"
        letrero = fuente.render(texto, False, BLANCO)
        ventana.blit(letrero, (ANCHO / 2 - fuente.size(texto)[0] / 2, 50))
        
        if pelota.x <= 0 or pelota.x + pelota.ancho >= ANCHO:
            texto_reiniciar = f"Pulse espacio para jugar"
            letrero_reiniciar = fuente.render(texto_reiniciar, False, NEGRO)
            ventana.blit(letrero_reiniciar, (ANCHO / 2 - fuente.size(texto_reiniciar)[0] / 2, ALTO / 2))
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
        
        if pelota.puntuacion >= PUNTUACION_GANADOR or pelota.puntuacion_ia >= PUNTUACION_GANADOR:
            pantalla_final(pelota, 2, modo_de_juego)
            pelota.jugando = False

        for evento in pygame.event.get():
            if evento.type == QUIT:
                jugando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    raquetaJugador.dir_y = -VELOCIDAD_RAQUETA_JUGADOR
                if evento.key == pygame.K_s:
                    raquetaJugador.dir_y = VELOCIDAD_RAQUETA_JUGADOR
                if evento.key == pygame.K_UP:
                    raquetaJugador2.dir_y = -VELOCIDAD_RAQUETA_JUGADOR
                if evento.key == pygame.K_DOWN:
                    raquetaJugador2.dir_y = VELOCIDAD_RAQUETA_JUGADOR
                    
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_w:
                    raquetaJugador.dir_y = 0
                if evento.key == pygame.K_s:
                    raquetaJugador.dir_y = 0
                if evento.key == pygame.K_UP:
                    raquetaJugador2.dir_y = 0
                if evento.key == pygame.K_DOWN:
                    raquetaJugador2.dir_y = 0
                if evento.key == pygame.K_SPACE:
                    if pelota.x <= 0 or pelota.x + pelota.ancho >= ANCHO:
                        pelota.reiniciar()  

    pygame.quit()
    
def pintar_boton(ventana_final, boton, palabra):
    fuente_botones = font.SysFont("Calibri", 30)
    
    if boton.collidepoint(mouse.get_pos()):
        draw.rect(ventana_final, NARANJA, boton, 0)
    else:
        draw.rect(ventana_final, ROJO, boton, 0)
    texto = fuente_botones.render(palabra, True, BLANCO)
    ventana_final.blit(texto, (boton.x + (boton.width - texto.get_width())/2, boton.y + (boton.height - texto.get_height())/2))

def dibujar_botones(pantalla, lista_botones):
    for boton in lista_botones:
        if boton['on_click']:
            pantalla.blit(boton['imagen_pressed'], boton['rect'])
        else:
            pantalla.blit(boton['imagen'], boton['rect'])
 
    
def pantalla_inicial(): 
    pygame.init()
       
    activa = True
    
    ventana_inicial = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PONG")
    fondo_pantalla = pygame.image.load("Assets/fondo_pantalla_inicial.png").convert()
    
    fuente = pygame.font.Font(None, 120)   

    modo_de_juego = 1 
    
    un_jugador = Rect(200, 250, 150, 50)
    dos_jugadores = Rect(400, 250, 200, 50)

    imagen_boton = pygame.image.load("Assets/modo_juego_1.png")
    imagen_boton_pressed = pygame.image.load("Assets/modo_juego_1_pressed.png")
    imagen_boton_2 = pygame.image.load("Assets/modo_juego_2.png")
    imagen_boton_pressed_2 = pygame.image.load("Assets/modo_juego_2_pressed.png")
    imagen_boton_3 = pygame.image.load("Assets/modo_juego_3.png")
    imagen_boton_pressed_3 = pygame.image.load("Assets/modo_juego_3_pressed.png")
    rect_boton_1 = imagen_boton.get_rect()
    rect_boton_2 = imagen_boton.get_rect()
    rect_boton_3 = imagen_boton.get_rect()
    botones = []
    rect_boton_1.topleft = [50, 350]
    rect_boton_2.topleft = [300, 350]
    rect_boton_3.topleft = [550, 350]
    botones.append(
        {'numero': 1, 'imagen': imagen_boton, 'imagen_pressed': imagen_boton_pressed, 'rect': rect_boton_1,
        'on_click': True})
    botones.append(
        {'numero': 2, 'imagen': imagen_boton_2, 'imagen_pressed': imagen_boton_pressed_2, 'rect': rect_boton_2,
        'on_click': False})
    botones.append(
        {'numero': 3, 'imagen': imagen_boton_3, 'imagen_pressed': imagen_boton_pressed_3, 'rect': rect_boton_3,
        'on_click': False})
    
    while(activa):
        ventana_inicial.blit(fondo_pantalla, [0, 0])
        
        texto = f"Ping Pong"
        letrero = fuente.render(texto, False, BLANCO)
        ventana_inicial.blit(letrero, (ANCHO / 2 - fuente.size(texto)[0] / 2, 100))
        
        pintar_boton(ventana_inicial, un_jugador, "1 jugador")
        pintar_boton(ventana_inicial, dos_jugadores, "2 jugadores")
        
        dibujar_botones(ventana_inicial, botones)
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                activa = False
            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if un_jugador.collidepoint(mouse.get_pos()):
                    print('click boton un jugador modo de juego ', modo_de_juego)
                    main(modo_de_juego)
                    activa = False
                elif dos_jugadores.collidepoint(mouse.get_pos()):
                    print('click boton dos jugadores modo de juego ', modo_de_juego)
                    main2(modo_de_juego)
                    activa = False
                else:
                    for boton in botones:
                        collidepoint = boton['rect'].collidepoint(mouse.get_pos())
                        if(collidepoint):
                            for boton in botones:
                                collidepoint = boton['rect'].collidepoint(mouse.get_pos())
                                boton['on_click'] = collidepoint
                                if(collidepoint):
                                    modo_de_juego = boton['numero']
                
    pygame.quit()
    
def pantalla_final(pelota, num_jugadores, modo_de_juego):   
    pygame.init()
     
    activa = True
    
    ventana_final = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("PONG")
    
    fuente = pygame.font.Font(None, 60)       
    
    salir = Rect(200, 400, 150, 50)
    reiniciar = Rect(400, 400, 200, 50)
    
    while(activa):
        ventana_final.fill(BLANCO)
        
        if pelota.puntuacion > pelota.puntuacion_ia:
            texto = f"Felicidades!! Has ganado"
        else:
            texto = f"Has perdido"    
        
        letrero = fuente.render(texto, False, NEGRO)
        ventana_final.blit(letrero, (ANCHO / 2 - fuente.size(texto)[0] / 2, 200))
        
        pintar_boton(ventana_final, salir, "Salir")
        pintar_boton(ventana_final, reiniciar, "Volver a jugar")
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                activa = False
            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if salir.collidepoint(mouse.get_pos()):
                    print('click boton salir')
                    activa = False
                if reiniciar.collidepoint(mouse.get_pos()):
                    print('click boton reiniciar')
                    if num_jugadores == 1:
                        main(modo_de_juego)
                    if num_jugadores == 2:
                        main2(modo_de_juego)
    pygame.quit()

if __name__ == "__main__":
    #main()
    pantalla_inicial()