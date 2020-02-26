import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from random import choice, gauss
import random
import time
np.random.seed(920204)
random.seed(920204)

class Visualizador():
    def __init__(self, figsize = (5,5)):
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize = figsize)

    def show(self, img, title = ''):
        self.vis = self.ax.imshow(img, vmax = 3)
        self.ax.set_title(title)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update(self, img, title = ''):
        self.vis.set_data(img)
        self.ax.set_title(title)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def visualizar(ax, terreno, iteracion = 0, texto = ''):
    ax.imshow(terreno)
    ax.set_title(f'iteración {iteracion} '+ texto)
    plt.draw()


def obtenerVecindad(terreno, y, x, r):
    ## vecindad de Moore con r=1
    inix, finx = x-r, x+r+1
    iniy, finy = y-r, y+r+1
    if inix < 0:
        inix = 0
    elif finx > terreno.shape[1]:
        finx = terreno.shape[1]
    if iniy < 0:
        iniy = 0
    elif finy > terreno.shape[0]:
        finy = terreno.shape[0]
    print(f'De {iniy} a {finy} y de {inix} a {finx}')
    return terreno[iniy:finy, inix:finx]

def obtenerSalida(yi, xi, salidas):
    coordSal = (None, None)
    dist_min = np.inf

    for salida in salidas:
        y, x = salida
        distancia = sqrt((y-yi)**2 + (x-xi)**2)
        if distancia < dist_min:
            coordSal = (y,x)
            dist_min = distancia
    
    return coordSal

def signo(a):
    return(int(a/abs(a)))

def calcularSiguiente(p1, p2, tipo = ''):
    reloj = [[0,1], [1,1], [1,0], [1,-1],
                 [0,-1], [-1,-1], [-1,0], [-1,1]]
    # Se calcula la dirección para seguir el camino más corto
    # de p1 a p2
    despx, despy = 0,0 ##Se queda en el mismo lugar
    ## Se calcula el movimiento óptimo
    yvec, xvec = p2[0]-p1[0], p2[1]-p1[1]
    if xvec == 0 and yvec!=0:
        despy = signo(yvec)
    elif yvec == 0 and xvec!=0:
        despx = signo(xvec)
    else:#if xvec != 0 and yvec!= 0:
        despy = signo(yvec)
        despx = signo(xvec)

    if tipo == 'suboptima':
        
        _disp = 3
        _mejor = [despy, despx]
        _indicemejor = reloj.index(_mejor)
        _posibles = [reloj[(_indicemejor+i)%len(reloj)] \
                for i in range(-_disp//2-1,_disp//2+2,1)]
        _indice =int(gauss(_disp, 1.5))
        if _indice<0: _indice = 0
        elif _indice>=len(_posibles): _indice = len(_posibles)-1
        despy, despx = _posibles[_indice]
    
    elif tipo == 'aleatoria':
        despy, despx = choice(reloj)
        
    return (p1[0]+despy, p1[1]+despx) 

def ajustarATerreno(pos, terreno):
    maxy, maxx = terreno.shape
    posy, posx = pos
    if posy < 0: posy = 0
    elif posy >=maxy: posy = maxy-1
    if posx < 0: posx = 0
    elif posx >= maxx: posx = maxx-1

    return(posy, posx)

def conteo(terreno, TIPO):
    unique, counts = np.unique(terreno, return_counts = True)
    d = dict(zip(unique, counts))
    return d.get(TIPO, 0)

def colocar(terreno, regiones, paraguardar, TIPO):
    for y1,x1,y2,x2 in regiones:
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                terreno[y,x] = TIPO
                paraguardar.append((y,x))



vis = Visualizador()

SALIDA = 1
PEATON = 2
OBSTACULO = 3
ADAPTATIVO = False

ancho = 100
to_print = False
dimensiones = (ancho, ancho)
regiones_de_salidas = [(0,ancho//2-2, 0, ancho//2+3), #Salida norte
                       (ancho//2-2, ancho-1, ancho//2+3, ancho-1) #Salida este
                       ]
                       
regiones_de_obstaculos = [(0, 0, 0, ancho-1), #Pared norte
                          (0, ancho-1, ancho-1, ancho-1), #Pared este
                          (0, 0, ancho-1, 0), #Pared oeste
                          (ancho-1, 0, ancho-1, ancho-1), #Pared sur
                          (ancho//2-1, ancho//3, ancho//2+1, ancho//3*2) #bloqueo intermedio
                          ]
obstaculos = []
salidas = []
terreno = np.zeros(dimensiones, dtype = np.uint)

peats = (50,50)
terreno[-peats[0]-1:-1, 1:peats[1]+1] = np.random.choice([0,PEATON], peats) #se agregan peatones

colocar(terreno, regiones_de_obstaculos, obstaculos, OBSTACULO)
colocar(terreno, regiones_de_salidas, salidas, SALIDA)


##Condiciones de la simulacion
maxiter = 1000
contador = 0
max_estancamiento = 0
relacion_estancamiento = 0
umbral_est_bajo = 0.6
umbral_est_alto = 0.9
umbral_adaptativo = 0.2

npeatones = conteo(terreno, PEATON)
vis.show(terreno)
while npeatones>0 and contador<maxiter:
    terreno_temp = np.zeros_like(terreno, dtype = np.uint)
    peatones_sacados = 0
    peatones_estaticos = 0
    tipo_adapt = 'ajuste'
    if to_print: print(f'Iter = {contador}')
    if contador == maxiter*4:
        salidas.append((ancho//2, ancho-1))
    #terreno[-1:,:] = PEATON
    for y in range(dimensiones[0]):
        for x in range(dimensiones[1]):
            posicion = y, x
            celda = terreno[posicion]
            if celda == OBSTACULO:
                terreno_temp[posicion] = OBSTACULO
            elif celda == SALIDA:
                terreno_temp[posicion] = SALIDA
            elif celda == PEATON:
                movido = False
                if to_print: print(f'Peaton en {posicion}')
                #vecindad = obtenerDisponibles(terreno, *posicion) La función canmbió
                pos_salida = obtenerSalida(y, x, salidas)
                if to_print: print(f'Salida en {pos_salida}')
                siguiente = calcularSiguiente(posicion, pos_salida)#, tipo='aleatoria')
                siguiente = ajustarATerreno(siguiente, terreno)
                if to_print: print(f'Siguiente celda {siguiente}, estado: {terreno[siguiente]}, estado_temp: {terreno_temp[siguiente]}')
                if terreno[siguiente] == SALIDA: #Se saca al peatón
                    terreno[posicion] = 0
                    movido = True
                    peatones_sacados += 1
                elif terreno[siguiente] == 0 and terreno_temp[siguiente] == 0: #Si está y estará disponible la celda, se mueve
                    movido = True
                    if to_print: print('Se mueve')
                    terreno_temp[siguiente] = PEATON
                    terreno[posicion] = 0 ##Se quita del tablero anterior
                elif (terreno[siguiente] >= PEATON or \
                    terreno_temp[siguiente] >= PEATON) and ADAPTATIVO: # Si ya está ocupado se busca otra celda
                    
                    if relacion_estancamiento > umbral_est_alto: tipo_adapt = 'aleatoria'
                    elif relacion_estancamiento > umbral_est_bajo: tipo_adapt = 'suboptima'
                    
                    siguiente = calcularSiguiente(posicion, pos_salida, tipo = tipo_adapt)
                    siguiente = ajustarATerreno(siguiente, terreno)

                    if to_print: print(f'Ajuste de siguiente a {siguiente}')
                    if to_print: print(f'Siguiente celda {siguiente}, estado: {terreno[siguiente]}, estado_temp: {terreno_temp[siguiente]}')
                    if terreno[siguiente] == 0 and terreno_temp[siguiente]==0: #Si está disponible la celda, se mueve
                        movido = True
                        if to_print: print('Se mueve')
                        terreno_temp[siguiente] = PEATON
                        terreno[posicion] = 0 ##Se quita del tablero anterior

                if not movido:
                    terreno_temp[posicion] = PEATON
                    peatones_estaticos += 1
                        
                

    npeatones = conteo(terreno_temp, PEATON)
    if npeatones > 0: 
        relacion_estancamiento = peatones_estaticos/npeatones
    max_estancamiento = max(relacion_estancamiento, max_estancamiento)
    
    titulo = f'Iter {contador +1}, #peatones = {npeatones} - {peatones_sacados}\n rel_estaticos = {relacion_estancamiento:.2f}'
    if ADAPTATIVO : titulo+= ' ADAPTATIVO '+tipo_adapt
    if relacion_estancamiento > umbral_adaptativo: ADAPTATIVO = True
    else: 
        ADAPTATIVO = False
        tipo_adapt = 'ajuste'
    
    terreno = terreno_temp.copy()
    vis.update(terreno, titulo) 
    contador+=1
    time.sleep(0)

print(f'Terminado en {contador} ciclos con un maximo de estancamiento de {max_estancamiento:.2f}')
