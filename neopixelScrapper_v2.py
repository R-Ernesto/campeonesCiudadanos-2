import SCRAPPER
import CONTROL
import board # neopixel control
import neopixel # neopixel control
from PIL import Image # import images
import numpy as np # images to arrays to neopixels
import time # sleep between stations data
#import sys

webdriver_path = '/usr/bin/chromedriver'

datos_estaciones = SCRAPPER.seicaScrapper(webdriver_path)
''' datos_estaciones es una lista de 3x3,
    en donde cada renglon corresponde a una
    estación y cada columna a un dato de la estacion:
    nombre, color y calidad '''

for dato in datos_estaciones:
    print(dato[0]+", calidad de aire "+dato[2]+".")


# CONTROL

# usando matrices de 8x8 c/u
num_pantallas=4 
num_hileras=2 
#ancho = num_pantallas//num_hileras          

pixels = neopixel.NeoPixel(board.D18,64*num_pantallas,auto_write=True)

for i in range(len(datos_estaciones)): # range(len(datos_estaciones)) = range(3) por ahora

    pixels.fill((10,0,0))

    T = 5 #30 segundos

    # mostrando la imagen correspondiente cada cierto tiempo T

    img = Image.open('nubes/'+datos_estaciones[i][2]+'.png')

    img = CONTROL.escalarResolucionImg(img,num_hileras,num_pantallas)
    ''' convierte la imagen a la resolución 16x16'''

    img = img.convert('RGB') # convirtiendo la imagen a RGB (elimina canal alpha)
    img = np.asarray(img) # convirtiendo la imagen a numpy array
    img = 0.1*img #atenuar brillo    
    
    img = CONTROL.centrarImg8x8(img,num_hileras,num_pantallas)
    ''' cuando la imagen es convertida a 16x16 puede quedar con
        una resolucion menor, por ejemplo 16x10, en ese
        caso se centra para que quede en medio de el
        display'''

    CONTROL.putOnPixels8x8(pixels,img,num_hileras,num_pantallas)
    # CONTROL.putOnPixels8x8(img,num_hileras,num_pantallas,True) #dará error?

    pixels.show()

    time.sleep(T)
pixels.fill((0,10,0))
time.sleep(2)
pixels.fill((0,0,0))


