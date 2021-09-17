# Bibliotecas importadas
import math
import pygame
import pandas as pd
df = pd.read_excel(r'C:\Users\rodri\Documents\GitHub\Taller-Python\Mapa.xlsx')

# Generador aleatorio de numeros
from random import seed
from random import randint
 
# Colores de rápido acceso
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Parámetros del juego
TEM = 200   # Número de ciclos por segundo (o inversa de tiempo por ciclo)
PUNT = 1000000  # Puntuación inicial
SUM = 1000      # Suma por éxito
RES = 10        # Resta por avance del tiempo

# Parámetros de velocidad/aceleración del jugador
VEL = 2.5/2
AC = 0.1/2

# Parámetro de velocidad de la pelota
VEL_P = 2.5/2.5
 
class Bloque(pygame.sprite.Sprite): # Clase derivada del sprite de pygame
 
    def __init__(self, color, x, y):

        # Llama al constructor de la clase padre (Sprite)
        super().__init__()
         
        # Imagen del bloque en pygame
        self.image = pygame.Surface([largo_bloque, alto_bloque])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
 
class Pelota(pygame.sprite.Sprite):
    
    # Atributos de Pelota
    x = 0.0
    y = 180.0
    rumbo = 200
    velocidad = VEL_P
 
    largo = 5
    alto = 5
    
    def __init__(self):

        super().__init__()
         
        # Imagen de Pelota en pygame
        self.image = pygame.Surface([self.largo, self.alto])
        self.rect = self.image.get_rect()
        self.image.fill(BLANCO)
         
        # Obtiene los atributos para alto/largo de la pantalla
        self.alto_pantalla = pygame.display.get_surface().get_height()
        self.largo_pantalla = pygame.display.get_surface().get_width()
     
    def botar_horizontal(self, diff):  #Solo para rebotes con superficies horizontales
         
        self.rumbo = (180 - self.rumbo) % 360
        self.rumbo -= diff

    def botar_vertical(self):   #Solo para rebotes con superficies verticales

        self.rumbo = (-self.rumbo) % 360
     
    def update(self):

        # Actualización de la posición
        rumbo_radianes = math.radians(self.rumbo)
        self.x += self.velocidad * math.sin(rumbo_radianes)
        self.y -= self.velocidad * math.cos(rumbo_radianes)
         
        # Actualización de la posición de la imagen
        self.rect.x = self.x
        self.rect.y = self.y
             
        # Rebotes 
        if self.x <= 0: # Rebote con la izda de la pantalla
            self.botar_vertical()
            self.x = 1
        elif self.x > self.largo_pantalla - self.largo:   # Rebote con la izda de la pantalla
            self.botar_vertical()
            self.x = self.largo_pantalla - self.largo - 1

        if self.y <= 0: # Rebote con la parte superior de la ventana
            self.botar_horizontal(0)
            self.y = 1
        elif self.y > 600:    # Rebote con la parte inferior de la pantalla
            self.botar_horizontal(0)
            return True      #Poner a false para MODO INMORTAL
        else:
            return False

    def upgrade(self):
        self.velocidad *= 5


class Bonus(pygame.sprite.Sprite):

    largo = 5
    alto = 10
    vy = 1
    tipo = 0

    def __init__(self, x, y):

        super().__init__()

        self.tipo = randint(1,2)
        if self.tipo == 1:
            COLOR = AZUL
        elif self.tipo == 2:
            COLOR = ROJO

        self.image = pygame.Surface([self.largo, self.alto])
        self.image.fill((COLOR))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.vy
        if (self.rect.y > 600) or (self.rect.y < 0):
            self.kill()

 
class Protagonista(pygame.sprite.Sprite):

    # Atributos del Protagonista
    x = 0.0
    y = 0.0
    vx = 0.0
    ax = 0.0

    largo = 75
    alto = 15
     
    def __init__(self):

        super().__init__()
        
        self.image = pygame.Surface([self.largo, self.alto])
        self.image.fill((BLANCO))
        self.rect = self.image.get_rect()

        self.alto_pantalla = pygame.display.get_surface().get_height()
        self.largo_pantalla = pygame.display.get_surface().get_width()
 
        self.rect.x = self.x = 0
        self.rect.y = self.y = self.alto_pantalla-self.alto
     

    def update(self):

        self.x += self.vx + 0.5 * self.ax * self.ax
        self.vx += self.ax
        self.rect.x = self.x

        if self.x < 0:
            self.rect.x = self.x = 0
            self.vx = -self.vx/2
        elif self.x > self.largo_pantalla - self.largo:
            self.rect.x = self.x = self.largo_pantalla - self.largo
            self.vx = -self.vx/2

        if self.vx > VEL:
            self.vx = VEL
        elif self.vx < -VEL:
            self.vx = -VEL


    def upgrade(self):
        self.largo *= 1.25

        self.image = pygame.Surface([self.largo, self.alto])
        self.image.fill((BLANCO))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y = self.alto_pantalla-self.alto


    def keydown(self, key):
        if key == pygame.K_d:
            self.ax += AC
        elif key == pygame.K_a:
            self.ax -= AC
            
    def keyup(self, key):
        if key == pygame.K_d:
            self.ax -= AC
        elif key == pygame.K_a:
            self.ax += AC

 
# Inicialización de pygame
pygame.init()
pantalla = pygame.display.set_mode([800, 600])          #Dimensiones de la ventana
pygame.display.set_caption('Arkanoid')                  #Título de la ventana
fuente = pygame.font.Font(None, 36)                     #Formato de texto
fondo_pantalla = pygame.Surface(pantalla.get_size())    #Superficie de proyección de la ventana
 
# Listas de los sprites involucrados en el juego
bloques = pygame.sprite.Group()
pelotas = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
todos_los_sprites = pygame.sprite.Group()
 
# Objeto plataforma
protagonista = Protagonista()
todos_los_sprites.add(protagonista)
 
# Objeto/s pelota/s
pelota = Pelota()
todos_los_sprites.add(pelota)
pelotas.add(pelota)

# Objetos bloques
largo_bloque = 23
alto_bloque = 15
top = 80
numero_de_filas = 5
numero_de_columnas = 32
 
for fila in range(0, numero_de_filas):
    # 32 columnas de bloques
    for columna in range(0, numero_de_columnas):
        # Crea un bloque (color,x,y)
        bloque = Bloque((int(df.iloc[fila,columna]), int(df.iloc[fila + 6,columna]), int(df.iloc[fila + 12,columna])), \
            columna * (largo_bloque + 2) + 1, top)
        if int(df.iloc[fila,columna]) != 0: #Añade el bloque si el valor de r es no nulo, si no, se descarta
            bloques.add(bloque)
            todos_los_sprites.add(bloque)
    # Mueve  hacia abajo el borde superior de la siguiente fila
    top += alto_bloque + 2
 
# Objeto reloj para regular el intervalo de refresco de la ventana
reloj = pygame.time.Clock()
 
# Condiciones del juego
inicio = False
pausa = False
game_over = False
salir_programa = False
contador = PUNT
temporizador = 0

# Pantalla de Inicio
while not (inicio or salir_programa):

    #Mensaje inicial
    pantalla.fill(NEGRO)
    texto = fuente.render("Bienvenido", True, BLANCO)
    textopos = texto.get_rect(centerx=fondo_pantalla.get_width()/2)
    textopos.top = 250
    pantalla.blit(texto, textopos) #Impresión de texto en pantalla
    texto = fuente.render("Para jugar pulse 'E', para salir pulse 'Esc'", True, BLANCO)
    textopos = texto.get_rect(centerx=fondo_pantalla.get_width()/2)
    textopos.top = 300
    pantalla.blit(texto, textopos)

    # Procesado de los eventos en el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salir_programa = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                inicio = True
            elif event.key == pygame.K_ESCAPE:
                salir_programa = True

    pygame.display.flip()

# Bucle principal
while not salir_programa:
 
    # Golpe de reloj ajustado a 30 ciclos/segundo
    reloj.tick(TEM)
    
    if not (game_over or pausa):
        temporizador += TEM/1000
        contador -= TEM/1000 * RES

    # Limpieza de la pantalla
    pantalla.fill(NEGRO)
     
    # Procesado de los eventos en el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salir_programa = True
        elif event.type == pygame.KEYDOWN:
            protagonista.keydown(event.key)
            if event.key == pygame.K_ESCAPE:
                salir_programa = True
            elif event.key == pygame.K_e:
                pausa = (pausa + 1) % 2  #Biestable botón pausa
        elif event.type == pygame.KEYUP:
            protagonista.keyup(event.key)
     
    # Evolución de los elementos del juego (si este está validado)
    if not (game_over or pausa):
        protagonista.update()
        game_over = pelota.update() #Mientras devuelva 'false' el juego prosigue
        for bonus in bonuses:
            bonus.update()

    texto = fuente.render("Puntuación: " + str(round(contador,2)), True, BLANCO)
    textopos = texto.get_rect(centerx = fondo_pantalla.get_width()* (1.3/8))
    textopos.top = 10
    textopos.left = 10
    pantalla.blit(texto, textopos)
    texto = fuente.render("Tiempo: " + str(round(temporizador,2)), True, BLANCO)
    textopos = texto.get_rect(centerx = fondo_pantalla.get_width() * (7/8))
    textopos.top = 10
    textopos.right = fondo_pantalla.get_width() - 10
    pantalla.blit(texto, textopos)
     
    # Al finalizar el juego se proyecta la pantalla de Game Over y sale del bucle del juego
    if game_over:
        texto = fuente.render("Game Over", True, BLANCO)
        textopos = texto.get_rect(centerx=fondo_pantalla.get_width()/2)
        textopos.top = 300 
        pantalla.blit(texto, textopos) #Impresión de texto en pantalla
    elif pausa:
        texto = fuente.render("Pausa - Pulse 'E' para proseguir", True, BLANCO)
        textopos = texto.get_rect(centerx=fondo_pantalla.get_width()/2)
        textopos.top = 300
        pantalla.blit(texto, textopos)
     
    # Condición de colisión de la pelota con el jugador
    if pygame.sprite.spritecollide(protagonista, pelotas, False):
        #Busca la posición de colisión de la pelota en la plataforma
        #OJO, la posición recibida por 'objeto.rect.x' es la esquina superior izda
        diff = (protagonista.rect.x + protagonista.largo/2) - (pelota.rect.x+pelota.largo/2)

        # En caso de colisión condiciona la altura de la pelota tras el cambio de dirección
        pelota.y = pantalla.get_height() - protagonista.alto - pelota.alto - 1
        pelota.botar_horizontal(diff)
     
    # Comprobación de colisiones (la lista queda vacía si no colisiona con nada)
    bloquesmuertos = pygame.sprite.spritecollide(pelota, bloques, True)
    bonusesmuertos = pygame.sprite.spritecollide(protagonista, bonuses, True)
    
    # Ante colisión (la lista de bloques "muertos" tiene contenido) se rebota
    if len(bloquesmuertos) > 0:

        contador += len(bloquesmuertos)*SUM

        for bloque in bloquesmuertos:

            if (pelota.rect.top <= bloque.rect.bottom) and (pelota.rect.top >= bloque.rect.top) and \
                (pelota.rect.right  >  bloque.rect.left) and(pelota.rect.left  <  bloque.rect.right): #Golpe por abajo:
                pelota.botar_horizontal(0)
            elif (pelota.rect.right >= bloque.rect.left) and (pelota.rect.left <= bloque.rect.left) and \
                (pelota.rect.top < bloque.rect.bottom) and (pelota.rect.bottom > bloque.rect.top):    #Golpe por la izda:
                pelota.botar_vertical()
            elif (pelota.rect.left <= bloque.rect.right) and (pelota.rect.right >= bloque.rect.right) and \
                (pelota.rect.top < bloque.rect.bottom) and (pelota.rect.bottom > bloque.rect.top):    #Golpe por la dcha:
                pelota.botar_vertical()
            elif (pelota.rect.bottom >= bloque.rect.top) and (pelota.rect.bottom <= bloque.rect.bottom) and \
                (pelota.rect.right  >  bloque.rect.left) and(pelota.rect.left  <  bloque.rect.right): #Golpe por arriba:
                pelota.botar_horizontal(0)

            if randint(0, int((numero_de_columnas * numero_de_filas - 1) / 10)) == 0: #Creará unos pocos bonuses por partida
                bonus = Bonus(bloque.rect.midbottom[0], bloque.rect.midbottom[1])
                bonuses.add(bonus)
                todos_los_sprites.add(bonus)

            break   #Solo un rebote por colisión (aunque sea múltiple)

            #if (pelota.rect.midtop[1] < bloque.rect.midtop[1]) and (pelota.rect.midright[0]  >  bloque.rect.midleft[0]) and(pelota.rect.midleft[0]  <  bloque.rect.midright[0]): #Golpe por abajo
            #    pelota.botar_horizontal(0)
            #elif (pelota.rect.midbottom[1] > bloque.rect.midbottom[1]) and (pelota.rect.midright[0]  >  bloque.rect.midleft[0]) and(pelota.rect.midleft[0]  <  bloque.rect.midright[0]): #Golpe por arriba:
            #    pelota.botar_horizontal(0)
            #elif (pelota.rect.midleft[0] <  bloque.rect.midleft[0]) and (pelota.rect.midtop[1] < bloque.rect.midbottom[1]) and (pelota.rect.midbottom[1] > bloque.rect.midtop[1]):    #Golpe por la izda
            #    pelota.botar_vertical()
            #elif (pelota.rect.midright[0] <  bloque.rect.midright[0]) and (pelota.rect.midtop[1] < bloque.rect.midbottom[1]) and (pelota.rect.midbottom[1] > bloque.rect.midtop[1]):
            #    pelota.botar_vertical()         
            #else:
            #    pelota.botar_vertical()

            # Evaluación del ángulo de colisión
            #x = (bloque.rect.x + 0.5 * largo_bloque) - (pelota.x + 0.5 * pelota.largo)
            #y = -((bloque.rect.y + 0.5* alto_bloque) - (pelota.y + 0.5 * pelota.alto))  #La coordenada "y" se mide desde arriba
            #a = math.atan2(y, x) #Ángulo que forma el vector que une los centros de la pelota con el rectángulo
            #if (a >= math.atan2((alto_bloque + pelota.alto), (largo_bloque + pelota.largo))) and \
            #(a <= math.atan2((alto_bloque + pelota.alto), -(largo_bloque + pelota.largo))):   #Reobote por abajo
            #    pelota.botar_horizontal(0)
            #elif (a >= math.atan2(-(alto_bloque + pelota.alto), (largo_bloque + pelota.largo))) and \
            #    (a <= math.atan2(-(alto_bloque + pelota.alto), -(largo_bloque + pelota.largo))):  #Reobote por arriba
            #    pelota.botar_horizontal(0)
            #else:   #Resto de rebotes
            #    pelota.botar_vertical()


    # Ante la colisión de bonus con el jugador, se otorga
    if len(bonusesmuertos) > 0:
        for bonus in bonusesmuertos:
            if bonus.tipo == 1:
                contador += len(bloquesmuertos) * SUM * 10
                protagonista.upgrade()
            elif bonus.tipo == 2:
                contador -= len(bloquesmuertos) * SUM * 10
                pelota.upgrade()
    
    # El juego se finaliza si todos los bloques desaparecen (la lista de bloques "vivos" queda vacía)
    if len(bloques) == 0:
        game_over = True
     
    # Proyección de los sprites tras los updates
    todos_los_sprites.draw(pantalla)
 
    # Actualización de la pantalla a la proyección más reciente
    pygame.display.flip()
 
pygame.quit()