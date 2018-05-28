#importar librerias
import pygame, sys, json
from pygame.locals import*
import time
#variables
WALLS = [] #lista de las paredes
MISILES = []#lista de misiles
PAUSA = False #variable para pausar el juego
CANTJUGADORES = None #variable global para la cantidad de jugadores
HIGHSCORES = 0 #variable global para el puntaje
NIVEL = 0 #variable global para el nivel
player1 = None
player2 = None
player3 = None
player4 = None
CARGADO = False
#incializacion
def juegoPrincipal(usuario1,usuario2):
    pygame.init()

    negro = (0,0,0) #color letra
    # dimensiones de la pantalla largo y ancho y el titulo de la ventana
    largo = 1280
    ancho = 720
    pantalla = pygame.display.set_mode([largo,ancho]) 
    pygame.display.set_caption("Death Race")

    #carga el sonido de las explosiones
    explosion_sonido = pygame.mixer.Sound("explosion.wav") 

    # se cargan las imagenes
    fondo = pygame.image.load ("pista1.png")
    fondo2 = pygame.image.load ("pista2.png")
    fondo3 = pygame.image.load ("pista3.png")
    puntajeFondo = pygame.image.load ("puntaje.png")

    menuFondo = pygame.image.load ("menu.png")
    menuReintentar = pygame.image.load ("menu2.png")

    explosion = pygame.image.load ("explosion.png")
    misil = pygame.image.load ("misil.png")
    misil_d = pygame.image.load ("misild.png")
    misil_a = pygame.image.load ("misila.png")
    misil_i = pygame.image.load ("misili.png")

    jugador_1 = pygame.image.load("jugador1.png")
    jugador_1d = pygame.image.load ("jugador1d.png")
    jugador_1a = pygame.image.load ("jugador1a.png")
    jugador_1i = pygame.image.load ("jugador1i.png")

    jugador_2 = pygame.image.load("jugador2.png")
    jugador_2d = pygame.image.load ("jugador2d.png")
    jugador_2a = pygame.image.load ("jugador2a.png")
    jugador_2i = pygame.image.load ("jugador2i.png")

    jugador_3 = pygame.image.load("jugador3.png")
    jugador_3d = pygame.image.load ("jugador3d.png")
    jugador_3a = pygame.image.load ("jugador3a.png")
    jugador_3i = pygame.image.load ("jugador3i.png")

    jugador_4 = pygame.image.load("jugador4.png")
    jugador_4d = pygame.image.load ("jugador4d.png")
    jugador_4a = pygame.image.load ("jugador4a.png")
    jugador_4i = pygame.image.load ("jugador4i.png")

    carro_azul = [jugador_1, jugador_1d, jugador_1a, jugador_1i,explosion]
    carro_amarillo = [jugador_2, jugador_2d, jugador_2a, jugador_2i,explosion]
    carro_rojo = [jugador_3, jugador_3d, jugador_3a, jugador_3i,explosion]
    carro_verde = [jugador_4, jugador_4d, jugador_4a, jugador_4i,explosion]
    imagenes_misil = [misil,misil_d,misil_a,misil_i]


    def leer():#funcion para leer
        global HIGHSCORE
        file = open("puntaje.txt","r+")
        texto = file.read()
        HIGHSCORE = texto.split(',')
        primero = HIGHSCORE[0]
        puntaje1 = HIGHSCORE[1]
        file.close()
            
    def escribir ():#funcion para escribir
        global HIGHSCORE
        file = open("puntaje.txt","r+")
        hilera = "" + str(HIGHSCORE[0])+","+ str(HIGHSCORE[1])+","+str(HIGHSCORE[2])+","+str(HIGHSCORE[3])+","+str(HIGHSCORE[4])+","+str(HIGHSCORE[5])
        file.write(hilera)
        file.close()
        
    def compararPuntaje(puntaje,nombre):#cambiar los nombres de posicion
        if puntaje > int(HIGHSCORE[1]):
            HIGHSCORE[1] = puntaje
            HIGHSCORE[0] = nombre
        elif puntaje > int(HIGHSCORE[3]):
            HIGHSCORE[3] = puntaje
            HIGHSCORE [2] = nombre
        elif puntaje > int(HIGHSCORE[5]):
            HIGHSCORE[5] = puntaje
            HIGHSCORE[4] = nombre
        if int(HIGHSCORE[1]) > int(HIGHSCORE[3]):
                HIGHSCORE[1] = int(HIGHSCORE [1])
        if int(HIGHSCORE[1]) < int(HIGHSCORE[3]):
            aux = int(HIGHSCORE[1])
            HIGHSCORE[1] = int(HIGHSCORE[3])
            HIGHSCORE[3] = aux
        if int(HIGHSCORE [3]) > int(HIGHSCORE [5]):
            HIGHSCORE[3] = int(HIGHSCORE [3])
        if int(HIGHSCORE[3]) < int(HIGHSCORE [5]):
            aux = int(HIGHSCORE [3])
            HIGHSCORE[3] = int(HIGHSCORE[5])
            HIGHSCORE [5] = aux              
    
    class Wall: #clase de la que se generan las paredes
        x = 0
        y = 0
        ancho = 0
        alto = 0
        def __init__(self, pos,ancho,alto):
            self.x = pos[0]
            self.y = pos [1]
            self.ancho = ancho
            self.alto = alto
            self.rect = pygame.Rect(pos[0], pos[1], ancho, alto)
            WALLS.append(self)

    class Carro: #clase de la que se generan los carros
        velocidad = 0
        velocidadLado = 0
        rotacion = 0 #0 arriba, 1 derecha, 2 abajo, 3 izquierda
        imagen = None
        x = 0
        y = 0
        choque = 0
        listaImagenes = []
        rect = None
        contadorMisil = 0
        controles = 0
        puntuacion = 0
        vuelta = False
        """
        listaImagenes[0] = arriba
        listaImagenes [1] = derecha
        listaImagenes [2] = abajo
        listaImagenes [3] = izquierda"""


        """
        1 == carro azul
        2 == carro amarillo
        3 == carro rojo
        4 == carro verde"""
        def __init__(self, velocidad,velocidadLado,rotacion,imagen,coordenadas,listaImagenes,controles,puntuacion,choque): #metodo
            self.velocidad = velocidad
            self.velocidadLado = velocidadLado
            self.rotacion = 0
            self.imagen = imagen
            self.x = int(coordenadas[0])
            self.y = int(coordenadas[1])
            self.listaImagenes = listaImagenes
            self.rect = pygame.Rect(self.x,self.y,40,55)
            self.controles = controles 
            self.puntuacion = puntuacion
            self.choque = choque
        def mover(self):
            global CANTJUGADORES
            global NIVEL
            keys = pygame.key.get_pressed()
            if self.choque == 0 and self.controles == 1: #Controles jugador 1
                if (keys[pygame.K_UP]):
                    self.y -= self.velocidad
                    self.rotacion = 0
                    self.rect = pygame.Rect(self.x,self.y,40,55)
                if (keys[pygame.K_DOWN]):
                    self.y += self.velocidad
                    self.rotacion = 2
                    self.rect = pygame.Rect(self.x,self.y,40,55)
                
                if keys[pygame.K_LEFT]:
                    self.x -= self.velocidadLado
                    self.rotacion = 3
                    self.rect = pygame.Rect(self.x,self.y,55,40)
                if keys[pygame.K_RIGHT]:
                    self.x += self.velocidadLado
                    self.rotacion = 1
                    self.rect = pygame.Rect(self.x,self.y,55,40)                
                    
                if keys[pygame.K_RCTRL]: #genera los misiles al disparar
                    if self.contadorMisil % 15 == 0: #contador para restringir cantidad de misiles
                        if self.rotacion == 0 : #misil cuando va para arriba
                            Misil(self.rotacion,self.x + 20,self.y - 30,self)
                        elif self.rotacion == 1 : #misil cuando va para la derecha
                            Misil(self.rotacion,self.x + 60,self.y + 20,self)
                        elif self.rotacion == 2 : #misil cuando va para abajo
                            Misil(self.rotacion,self.x + 20,self.y + 60,self)
                        else:                   #misil cuando va para la izquierda
                            Misil(self.rotacion,self.x - 31 ,self.y + 20,self)
                        self.contadorMisil = 0
                    self.contadorMisil += 1
                    
            if self.choque == 0 and self.controles == 2: #controles jugador 2
                if (keys[pygame.K_w]):
                    self.y -= self.velocidad
                    self.rotacion = 0
                    self.rect = pygame.Rect(self.x,self.y,40,55)
                if (keys[pygame.K_s]):
                    self.y += self.velocidad
                    self.rotacion = 2
                    self.rect = pygame.Rect(self.x,self.y,40,55)
                if keys[pygame.K_a]:
                    self.x -= self.velocidadLado
                    self.rotacion = 3
                    self.rect = pygame.Rect(self.x,self.y,55,40)
                if keys[pygame.K_d]:
                    self.x += self.velocidadLado
                    self.rotacion = 1
                    self.rect = pygame.Rect(self.x,self.y,55,40)
                if keys[pygame.K_q]: #genera los misiles al disparar
                    if self.contadorMisil % 15 == 0: #contador para restringir cantidad de misiles
                        if self.rotacion == 0 : #misil cuando va para arriba
                            Misil(self.rotacion,self.x + 20,self.y - 30,self)
                        elif self.rotacion == 1 : #misil cuando va para la derecha
                            Misil(self.rotacion,self.x + 60,self.y + 20,self)
                        elif self.rotacion == 2 : #misil cuando va para abajo
                            Misil(self.rotacion,self.x + 20,self.y + 60,self)
                        else:                   #misil cuando va para la izquierda
                            Misil(self.rotacion,self.x - 31 ,self.y + 20,self)
                        self.contadorMisil = 0
                    self.contadorMisil += 1
            # suma puntos cuando el jugador cruza la meta
            if NIVEL == 1:
                if self.x > 951 and self.vuelta == False:
                    self.vuelta = True
                if self.vuelta == True and self.x > 70 and self.x < 183 and self.y > 383 and self.y < 439:
                    self.vuelta = False
                    self.puntuacion += 1
            elif NIVEL == 2:
                if self.y > 400 and self.vuelta == False:
                    self.vuelta = True
                if self.vuelta == True and self.x > 405 and self.x < 475 and self.y > 10 and self.y < 110:
                    self.vuelta = False
                    self.puntuacion += 1
            elif NIVEL == 3:
                if self.x > 900 and self.vuelta == False:
                    self.vuelta = True
                if self.vuelta == True and self.x > 125 and self.x < 220 and self.y > 340 and self.y < 400:
                    self.vuelta = False
                    self.puntuacion += 1
                
                        
        def rotar (self):
            #movimiento PARA LOS BOTS
            #cambia la imagen que se muestra segun su direccion 
            #los lados del mapa empiezan en 1 al a izquierda y siguen aumento de acuerdo al reloj
            global NIVEL
            x = self.x
            y = self.y
            if NIVEL == 1: #para el nivel 1
                if x <= 555 and x >= 138 and y >= 583:#lado 6 carril externo hacia izquierda
                    self.rotacion = 3
                elif x <= 520 and x >= 130 and y >= 550 and y <= 580:#lado 6 carril interno hacia izquierda
                    self.rotacion = 3

                elif x <= 515 and x >= 505 and y >= 300 and y <= 552:#lado 5 carril interno hacia abajo
                    self.rotacion = 2
                elif x >= 550 and x <= 585 and y >=369 and y <= 650:#lado 5 carril externo hacia abajo
                    self.rotacion = 2
                    
                elif x >= 510 and x <= 1099 and y >= 315 and y <= 369:#lado 4 carril interno hacia izquierda
                    self.rotacion = 3
                elif x >= 550 and x <= 1142 and y >= 357 and y <=417:#lado 4 carril externo hacia izquierda
                    self.rotacion = 3

                elif x >= 1098 and x <= 1142 and y >= 100 and y <=390:#lado 3 carill carril interno hacia abajo
                    self.rotacion = 2
                elif x >= 1100 and x <= 1142 + 55 and y >= 40 and y <=335:#lado 3 carril externo hacia abajo
                    self.rotacion = 2

                elif x >= 117 and x <= 1100 and y <= 105:#lado 2 carril interno hacia derecha
                    self.rotacion = 1
                elif x >= 75 and x < 1142 and y <=54:#lado 2 carril externo hacia derecha
                    self.rotacion = 1        

                elif x <= 151 and x >= 118 and y <= 580:#lado 1 carril interno hacia arriba
                    self.rotacion = 0
                else:#lado 1 carril externo hacia arriba
                    self.rotacion = 0

            elif NIVEL == 2: #para el nivel 2
                if x >= 0 and x <= 60 and y >= 25 and y <= 720: #lado 1 carril externo hacia arriba
                    self.rotacion = 0
                elif x >= 50 and x <= 70 and y >= 85 and y <= 650: #lado 1 carril interno hacia arriba
                    self.rotacion = 0
                    
                elif x>= 0 and x <= 830 and y >= 0 and y <= 35: #lado 2 carril externo hacia derecha
                    self.rotacion = 1
                elif x >= 61 and x <= 780 and y >= 60 and y <= 90: #lado 2 carril interno hacia derecha
                    self.rotacion = 1

                elif x >= 820 and x <= 880 and y >= 0 and y <= 660: #lado 3 carril externo hacia abajo
                    self.rotacion = 2
                elif x >= 765 and x <= 825 and y >= 60 and y <=610: #lado 3 carril interno hacia abajo
                    self.rotacion = 2

                elif x >= 60 and x <= 810 and y >= 611 and y <= 660: #lado 4 carril interno hacia izquierda
                    self.rotacion = 3
                elif x >= 35 and x <= 870 and y >= 655 and y <= 720: #lado 4 carril externo hacia izquierda
                    self.rotacion = 3

            elif NIVEL == 3:
                if x >= 120 and x <= 130 and y >= 85 and y <= 645:#lado 1 carril externo hacia arriba
                    self.rotacion = 0
                elif x >=120 and x <= 440 and y <= 84:#lado 2 carril interno hacia derecha
                    self.rotacion = 1
                elif x >= 475 and x <= 535 and y >= 70 and y <= 320:#lado 3 carril externo hacia abajo
                    self.rotacion = 2
                elif x >= 440 and x <= 947 and y >= 321 and y <= 370:#lado 4 carril interno hacia derecha
                    self.rotacion = 1
                elif x >= 948 and x <= 1000 and y >= 200 and y <= 365:#lado 5 carril interno hacia arriba
                    self.rotacion = 0
                elif x >= 900 and x <= 1060 and y <= 200: #lado 6 carril externo hacia derecha
                    self.rotacion = 1
                elif x >= 1061 and x <= 1110 and y >= 145 and y <= 610:#lado 7 carril interno hacia abajo
                    self.rotacion = 2
                elif x >= 171 and x <= 1150 and y >= 611 and y <= 650:#lado 8 carril interno hacia izquierda
                    self.rotacion = 3


        def moverBot(self): #Funcion para mover a los bots segun su rotacion 
            if self.choque == 0:
                self.rotar()
                if self.rotacion == 0:
                    self.y -= self.velocidad
                    self.rect = pygame.Rect(self.x,self.y,40,55)
                elif self.rotacion == 1:
                    self.x += self.velocidad
                    self.rect = pygame.Rect(self.x,self.y,55,40)
                elif self.rotacion == 2:
                    self.y += self.velocidad
                    self.rect = pygame.Rect(self.x,self.y,40,55)
                else:
                    self.x -= self.velocidad
                    self.rect = pygame.Rect(self.x,self.y,55,40)
        
    class Misil:
        rotacion = 0
        velocidad = 15
        ancho = 0  
        alto = 0
        x = 0
        y = 0
        rect = pygame.Rect (0,0,20,30)
        imagen = 0
        carroDisparado = None

        def __init__ (self, rotacion, x, y,carroDisparado):
            self.rotacion = rotacion
            self.x = x
            self.y = y
            self.carroDisparado = carroDisparado
            if self.rotacion == 0:
                self.ancho = 20
                self.alto = 30
                self.rect = pygame.Rect (self.x, self.y, 20,30)
            elif self.rotacion == 2:
                self.ancho = 20
                self.alto = 30
                self.rect = pygame.Rect (self.x, self.y, 20,30)
            elif self.rotacion == 1:
                self.ancho = 30
                self.alto = 20
                self.rect = pygame.Rect (self.x, self.y, 30,20)
            else:
                self.ancho = 30
                self.alto = 20
                self.rect = pygame.Rect (self.x, self.y, 30,20)
            self.imagen = imagenes_misil [rotacion]

            MISILES.append (self)

        def moverMisil (self): #mueve la imagen del misil segun su orientacion
            if self.rotacion == 0:
                self.y -= self.velocidad
            elif self.rotacion == 1:
                self.x += self.velocidad
            elif self.rotacion == 2:
                self.y += self.velocidad
            else:
                self.x -= self.velocidad
            self.rect = pygame.Rect (self.x,self.y,self.ancho,self.alto)

            
    def detectarColision():# Funcion para detectar las colisiones
        global NIVEL
        global MISILES
        global player1,player2,player3,player4

        for wall in WALLS:
            if  wall.rect.colliderect(player1.rect) and player1.choque == 0: #choques del carro 1 con pared
                player1.velocidadLado = 0
                player1.velocidad = 0
                player1.rotacion = 4                
                player1.choque = 1
                pygame.mixer.Sound.play(explosion_sonido)
            if  wall.rect.colliderect(player2.rect) and player2.choque == 0: # choques del carro 2 con pared
                player2.velocidadLado = 0
                player2.velocidad = 0
                player2.rotacion = 4                
                player2.choque = 1
                pygame.mixer.Sound.play(explosion_sonido)

        for misil in MISILES:
            if CANTJUGADORES == True:
                if misil.rect.colliderect (player2.rect) and player2.choque == 0:
                    player2.velocidadLado = 0
                    player2.velocidad = 0
                    player2.rotacion = 4                
                    player2.choque = 1
                    pygame.mixer.Sound.play(explosion_sonido)
                    misil.carroDisparado.puntuacion += 1
                if misil.rect.colliderect (player3.rect) and player3.choque == 0:
                    player3.velocidadLado = 0
                    player3.velocidad = 0
                    player3.rotacion = 4                
                    player3.choque = 1
                    pygame.mixer.Sound.play(explosion_sonido)
                    misil.carroDisparado.puntuacion += 1
                if misil.rect.colliderect (player4.rect) and player4.choque == 0:
                    player4.velocidadLado = 0
                    player4.velocidad = 0
                    player4.rotacion = 4                
                    player4.choque = 1
                    pygame.mixer.Sound.play(explosion_sonido)
                    misil.carroDisparado.puntuacion += 1
                if player2.choque == 1 and player3.choque == 1 and player4.choque == 1:
                    NIVEL += 1
                    player1.vuelta = False
                    crearNivel()

            else:
                if misil.rect.colliderect (player3.rect) and player3.choque == 0:
                    player3.velocidadLado = 0
                    player3.velocidad = 0
                    player3.rotacion = 4                
                    player3.choque = 1
                    misil.carroDisparado.puntuacion += 1
                if misil.rect.colliderect (player4.rect) and player4.choque == 0:
                    player4.velocidadLado = 0
                    player4.velocidad = 0
                    player4.rotacion = 4                
                    player4.choque = 1
                    misil.carroDisparado.puntuacion += 1
                if player3.choque == 1 and player4.choque == 1:
                    NIVEL += 1
                    player1.vuelta = False
                    player2.vuelta = False
                    MISILES = [ ]
                    crearNivel()
        

    def crearNivel():
        global CANTJUGADORES
        global NIVEL
        global WALLS
        global MISILES
        global CARGADO
        global player1,player2,player3,player4
        ejecutando = True
        WALLS = []
        MISILES = []
        
        
        if NIVEL == 1:
            Wall((0,0),60,720)#pared izquierda (1)
            Wall((0,0),1280,40)#pared superior  (2)
            Wall((1190,0),94,720)#pared derecha (3)
            Wall((610,420),678,304)#paredes inferior derecha (4 y 5)
            Wall((0,655),1280,78)#pared inferior (6)
            Wall ((180,160),910,160) #pared interior derecha
            Wall ((170,295),320,235) #pared interior izquierda

            if CARGADO == False:
                if CANTJUGADORES == True:
                    player1 = Carro (8,9,0,jugador_1,(455,556),carro_azul,1,0,False)
                    player2 = Carro (8,9,0,jugador_2,(81,171),carro_amarillo,0,0,False)
                    player3 = Carro (8,9,0,jugador_3,(271,105),carro_rojo,0,0,False)
                    player4 = Carro (8,9,0,jugador_4,(118,543),carro_verde,0,0,False)

                else:
                    player1 = Carro (8,9,0,jugador_1,(118,483),carro_azul,1,0,False)
                    player2 = Carro (8,9,0,jugador_2,(75,483),carro_amarillo,2,0,False)
                    player3 = Carro (8,9,0,jugador_3,(75,300),carro_rojo,0,0,False)
                    player4 = Carro (8,9,0,jugador_4,(118,300),carro_verde,0,0,False)

            if CARGADO == True:
                    player1 = player1
                    player2 = player2
                    player3 = player3
                    player4 = player4
                    
        elif NIVEL == 2:
            Wall((880,0),400,720)#pared derecha
            Wall((120,120),640,480)#pared interior
            Wall((0,0),1280,5)#borde superior
            Wall((0,710),1280,10)#borde inferior
            Wall((0,0),5,720)#borde izquierdo

            if CARGADO == False:
                if CANTJUGADORES == True:
                    player1 = Carro (8,9,0,jugador_1,(68,331),carro_azul,1,0,False)
                    player2 = Carro (8,9,0,jugador_2,(556,615),carro_amarillo,0,0,False)
                    player3 = Carro (8,9,0,jugador_3,(839,359),carro_rojo,0,0,False)
                    player4 = Carro (8,9,0,jugador_4,(364,70),carro_verde,0,0,False)

                else:
                    player1 = Carro (8,9,0,jugador_1,(68,331),carro_azul,1,0,False)
                    player2 = Carro (8,9,0,jugador_2,(500,612),carro_amarillo,2,0,False)
                    player3 = Carro (8,9,0,jugador_3,(839,359),carro_rojo,0,0,False)
                    player4 = Carro (8,9,0,jugador_4,(506,619),carro_verde,0,0,False)

            if CARGADO == True:
                    player1 = player1
                    player2 = player2
                    player3 = player3
                    player4 = player4

                    
        elif NIVEL == 3:
            Wall((0,0),119,720)#pared izquierda
            Wall((0,0),540,20)#pared superior izq
            Wall((540,0),360,310)#pared superior medio
            Wall((900,0),380,135)#pared superior derecho
            Wall((1160,0),120,720)#pared derecha
            Wall((0,705),1280,15)#pared inferior
            Wall((230,130),200,470)#pared interior izquierda
            Wall((440,420),560,180)#pared interior medio
            Wall((1005,247),45,355)#pared interior derecha
            Wall((177,520),50,50)#snowman izquierda
            Wall((365,25),50,40)#snowman superior
            Wall((950,375),50,40)#snowball superior
            Wall((1120,670),55,45)#snowball inferior
            Wall((430,660),400,50) #icecicles

            if CARGADO == False:
                
                if CANTJUGADORES == True:
                    player1 = Carro (8,9,0,jugador_1,(128,421),carro_azul,1,0,False)
                    player2 = Carro (8,9,0,jugador_2,(526,617),carro_amarillo,0,0,False)
                    player3 = Carro (8,9,0,jugador_3,(550,321),carro_rojo,0,0,False)
                    player4 = Carro (8,9,0,jugador_4,(1062,377),carro_verde,0,0,False)

                else:
                    player1 = Carro (8,9,0,jugador_1,(128,421),carro_azul,1,0,False)
                    player2 = Carro (8,9,0,jugador_2,(175,421),carro_amarillo,2,0,False)
                    player3 = Carro (8,9,0,jugador_3,(550,321),carro_rojo,0,0,False)
                    player4 = Carro (8,9,0,jugador_4,(1062,377),carro_verde,0,0,False)

            if CARGADO == True:
                    player1 = player1
                    player2 = player2
                    player3 = player3
                    player4 = player4


        jugar(ejecutando,puntaje) #llama a ejecutar el juego

    def guardarNivel (NIVEL,player1,player2,player3,player4):#funcion para escribir
        file = open("partidaGuardada.txt","r+")
        hilera = str(NIVEL)+"@"+ str(player1.x)+"@"+str(player1.y)+"@"+str(player1.choque)+"@"+str(player1.puntuacion)+"@"+str(player2.x)+"@"+str(player2.y)+"@"+str(player2.choque)+"@"+str(player2.puntuacion)+"@"+str(player3.x)+"@"+str(player3.y)+"@"+str(player3.choque)+"@"+str(player4.x)+"@"+str(player4.y)+"@"+str(player4.choque)
        file.write(hilera)
        file.close()
    def cargarNivel (): 
        global NIVEL
        global player1,player2,player3,player4
        global CARGADO
        file = open("partidaGuardada.txt","r+")
        texto = file.read()
        lista = texto.split('@')
        NIVEL = lista[0]
        #listas con las coordenadas de los carros
        tupla1 = (int(lista[1]),int(lista[2]))
        tupla2 = (int(lista[5]),int(lista[6]))
        tupla3 = (int(lista[9]),int(lista[10]))
        tupla4 = (int(lista[12]),int(lista[13]))
        #Asigna los valores cargados a los jugadores
        player1 = Carro (8,9,0,jugador_1,tupla1,carro_azul,1,lista[4],lista[3])
        player2 = Carro (8,9,0,jugador_2,tupla2,carro_amarillo,2,lista[8],lista[7])
        player3 = Carro (8,9,0,jugador_3,tupla3,carro_rojo,0,0,lista[11])
        player4 = Carro (8,9,0,jugador_4,tupla4,carro_verde,0,0,lista[14])
        file.close()
        CARGADO == True
        crearNivel()
        

    def menu():
        ejecutando = True
        global CANTJUGADORES
        global PAUSA
        while ejecutando:
            global NIVEL
            pantalla.blit(menuFondo,(0,0))
            posMouse = pygame.mouse.get_pos()
            for event in pygame.event.get(): #Detecta los eventos que suceden
                if event.type == QUIT:#Si el evento es presionar la X, termina el programa
                    pygame.quit() 
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if posMouse[0]>265 and posMouse[0] < 669 and posMouse[1] > 245 and posMouse[1] < 445: # cuadro para 1 jugador
                        CANTJUGADORES = True
                        PAUSA = False
                        NIVEL = 1
                        crearNivel()                    
                    if posMouse[0]>265 and posMouse[0] < 669 and posMouse[1] > 470 and posMouse[1] < 675:# cuadro para 2 jugadores
                        CANTJUGADORES = False
                        PAUSA = False
                        NIVEL = 1
                        crearNivel()
                    if posMouse[0]>824 and posMouse[0] < 1179 and posMouse[1] > 495 and posMouse[1] < 664:# cuadro para ver puntuacion
                        puntaje()
                    if posMouse [0] > 138 and posMouse [0] < 273 and posMouse[1] > 653 and posMouse[1] < 708:# cuadro para cargar el nivel previamente guardado
                        cargarNivel()
                    if posMouse [0] > 21 and posMouse[0] < 126 and posMouse[1] > 650 and posMouse[1] < 710: # cuadro para salir del juego
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            
        

    def menu2(player1,player2):
        global CANTJUGADORES
        escribir()
        ejecutando = True
        while ejecutando:
            pantalla.blit(menuReintentar, (0,0))
            posMouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit() 
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if posMouse[0] > 477 and posMouse [0]< 574 and posMouse[1] > 512 and posMouse [1] < 561 and CANTJUGADORES == True: #continuar
                            CANTJUGADORES = True
                            crearNivel()
                        if posMouse[0] > 708 and posMouse [0]< 791 and posMouse[1] > 512 and posMouse [1] < 561: #salir
                            pygame.quit()
                            sys.exit()
                        if posMouse[0] > 477 and posMouse [0]< 574 and posMouse[1] > 512 and posMouse [1] < 561 and CANTJUGADORES == False: #continuar
                            CANTJUGADORES = False
                            crearNivel()
                        if posMouse[0] > 708 and posMouse [0]< 791 and posMouse[1] > 512 and posMouse [1] < 561 and CANTJUGADORES == False: #salir
                            pygame.quit()
                            sys.exit()
            pygame.display.update()
    def puntaje():#muestra el puntaje de los jugadores
        ejecutando = True
        fuente = pygame.font.SysFont('Arial',80)
        file = open("puntaje.txt","r+")
        texto = file.read()
        puntaje = texto.split(',')
        primero = puntaje[0]
        puntaje1 = puntaje[1]
        segundo = puntaje[2]
        puntaje2 = puntaje[3]
        tercero = puntaje[4]
        puntaje3 = puntaje[5]
        file.close()
        primerLugar = fuente.render(primero +".............."+puntaje1 ,0,negro)
        segundoLugar = fuente.render(segundo +".............."+puntaje2 ,0,negro)
        tercerLugar = fuente.render(tercero +".............."+puntaje3 ,0,negro)
        

        while ejecutando:
            pantalla.blit(puntajeFondo,(0,0))
            pantalla.blit(primerLugar,(550,250))
            pantalla.blit(segundoLugar,(550,350))
            pantalla.blit(tercerLugar,(550,450))
            posMouse = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit() 
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:#opcion para volver al menu principal por medio de un boton desde la pantalla de highscore
                        if posMouse[0] > 25 and posMouse [0]< 390 and posMouse[1] > 620 and posMouse [1] < 700:
                            menu()
            pygame.display.update()
    def jugar(ejecutando,puntaje):
        global player1,player2,player3,player4
        global PAUSA
        global NIVEL
        reloj = pygame.time.Clock()
        t0 = time.time()    
        Tiempo = 180
        fuente = pygame.font.SysFont('Arial',30)
        if NIVEL == 1: #pone musica para el primer nivel en loop
            soundtrack1 = pygame.mixer.music.load("soundtrack1.wav")
            pygame.mixer.music.play(-1)
        elif NIVEL == 2:
            soundtrack2 = pygame.mixer.music.load("soundtrack2.wav")
            pygame.mixer.music.play(-1)
        elif NIVEL == 3:
            soundtrack3 = pygame.mixer.music.load("soundtrack3.wav")
            pygame.mixer.music.play(-1)
        while ejecutando:
            if PAUSA == False:
                segundos = int (time.time()-t0)
                if (Tiempo - segundos) == 0:
                    puntaje()
                    
                if CANTJUGADORES == True: #Corre juego para 1 jugador
                    player1.mover()
                    player2.moverBot() 
                    player3.moverBot()
                    player4.moverBot()
                    print (pygame.mouse.get_pos())

                else:                   #Corre juego para 2 jugadores
                    player1.mover()
                    player2.mover() 
                    player3.moverBot()
                    player4.moverBot()
                detectarColision ()
                
                if player1.choque == 1 and CANTJUGADORES == True:
                    compararPuntaje(player1.puntuacion,usuario1)
                    compararPuntaje(player2.puntuacion,usuario2)
                    menu2(player1,player2)
                if player1.choque == 1 and player2.choque == 1 and CANTJUGADORES == False:
                    compararPuntaje(player1.puntuacion,usuario1)
                    compararPuntaje(player2.puntuacion,usuario2)
                    menu2(player1,player2)
                    
                for misil in MISILES:
                    misil.moverMisil()
            for event in pygame.event.get(): #Detecta los eventos que suceden
                if event.type == QUIT:#Si el evento es presionar la X, termina el programa
                    pygame.quit() 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_p:
                        PAUSA = not PAUSA
                    if event.key == K_g:
                        guardarNivel(NIVEL,player1,player2,player3,player4)
                        
                            
                
            #Fuente y mensajes a mostrar en pantalla
            jugador1 = fuente.render("Jugador 1: " + usuario1 ,0,negro)
            jugador2 = fuente.render("Jugador 2: " + usuario2,0,negro)
            puntaje1 = fuente.render("Puntaje: " + str(player1.puntuacion),0,negro)
            puntaje2 = fuente.render("Puntaje: " + str(player2.puntuacion),0,negro)
            tiempo = fuente.render("Tiempo: " + str(Tiempo - segundos),0,negro)

            #Carga el fondo
            if NIVEL == 1: #para el nivel 1
                pantalla.blit(fondo,(0,0))
                pantalla.blit (puntaje1,(709,512))
                pantalla.blit (puntaje2,(926,512))
                pantalla.blit (jugador1,(709,552))
                pantalla.blit (jugador2,(926,552))
                pantalla.blit (tiempo, (750,470))
            elif NIVEL == 2: #para el nivel 2
                pantalla.blit(fondo2,(0,0))
                pantalla.blit (puntaje1,(910,300))
                pantalla.blit (puntaje2,(910,470))
                pantalla.blit (jugador1,(910,250))
                pantalla.blit (jugador2,(910,420))
                pantalla.blit (tiempo, (950,190))
            elif NIVEL == 3: #para el nivel 3
                pantalla.blit(fondo3,(0,0))
                pantalla.blit (puntaje1,(565,125))
                pantalla.blit (puntaje2,(565,270))
                pantalla.blit (jugador1,(565,75))
                pantalla.blit (jugador2,(565,220))
                pantalla.blit (tiempo, (650,35))
            elif NIVEL ==4:
                compararPuntaje(player1.puntuacion,usuario1)
                compararPuntaje(player2.puntuacion,usuario2)
                puntaje()
            

            pantalla.blit (carro_azul[player1.rotacion],(player1.x,player1.y))
            pantalla.blit (carro_amarillo[player2.rotacion],(player2.x,player2.y))
            pantalla.blit (carro_rojo[player3.rotacion],(player3.x,player3.y))
            pantalla.blit (carro_verde[player4.rotacion],(player4.x,player4.y))
            
            for misil in MISILES:
                pantalla.blit (misil.imagen,(misil.x,misil.y))

            # actualizacion de pantalla
            pygame.display.update()
         
            # que el juego corra a 60 fps
            reloj.tick(60)


    """Para que corra si se define el ciclo como funcion"""
    leer()
    menu()
    pygame.quit()
    quit ()
