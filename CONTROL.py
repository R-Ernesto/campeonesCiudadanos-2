import board # neopixel control
import neopixel # neopixel control
from PIL import Image # import images
import numpy as np # images to arrays to neopixels
#import time # sleep between stations data
import sys

def putOnPixels8x8(pixels,img,num_hileras,num_pantallas):
    ''' imprime una imagen con resolución (num_hileras*8)x(num_pantallas//numero_hileras*8)
        si no esta en esa resolución se reescala a ella
    '''        
    if num_pantallas%num_hileras!=0:            
        sys.exit("al llamar printOnNeopixel de CONTROL.py: error, el número de pantallas debe ser divisible entre el número de hileras")
    ancho = num_pantallas//num_hileras      

    #partimos la imagen en hileras
    hileras = []
    for i in range(num_hileras):
        hileras.append([])
    hileras = np.vsplit(img,np.arange(8,8*num_hileras,8))    

    # impresion de hileras en led-displays  

    for k in range(num_hileras): # hileras de pantallas
        for i in range(8): # renglones i
            for j in range(img.shape[1]): # número de columnas j            
                if (64*ancho*k+j*8+7-i)<256 and (64*ancho*k+j*8+7-i)>191:
                    pixels[64*ancho*k+j*8+7-i] = hileras[k][i][j]*1.5                    
                else:
                    pixels[64*ancho*k+j*8+7-i] = hileras[k][i][j]                           
    print("Ready!")

def centrarImg8x8(img,num_hileras,num_pantallas):
    '''centrado de imagen
        vamos a suponer que el ancho siempre es correcto, y la altura no
        hay que centrar la imagen a lo alto
        si la imagen tiene n renglones, y n<8*num_hileras entonces
        n + (8*num_hileras)%n = 8*num_hileras = número de renglones
        agregar (n%(8*num_hileras))/2 renglones arriba y abajo de la imagen para centrarla '''    

    n = img.shape[0] # número de renglones de la imagen = altura

    if n<8*num_hileras:
        n_comp = (8*num_hileras)%n # n complemento, 'n' + 'n complemento' = '8*num_hileras'
        # print('n_comp=%d'%n_comp)
        if n_comp%2 == 0: # si el complemento de n es divisible por 2 entonces agregamos el mismo número de renglones arriba y abao de la imagen
            n_sup = n_comp//2 # numero de renglones a agregar arriba
            n_inf = n_comp//2 #                               abajo
            # print('n_sup=%d'%n_sup)
            # print('n_inf=%d'%n_inf)
        else:
            n_sup = n_comp//2 
            n_inf = n_comp//2+1
            # print('n_sup=%d'%n_sup)
            # print('n_inf=%d'%n_inf)

    img_ancho = img.shape[1]
    reng_sup = np.zeros((n_sup,img_ancho*3),dtype='int').reshape((n_sup,img_ancho,3))
    reng_inf = np.zeros((n_inf,img_ancho*3),dtype='int').reshape((n_inf,img_ancho,3))

    img = np.vstack([reng_sup,img,reng_inf])

    return img

def escalarResolucionImg(img,num_hileras,num_pantallas):
    ancho = num_pantallas//num_hileras          
    maxsize = (num_hileras*8, ancho*8) # resolución
    img.thumbnail(maxsize, Image.ANTIALIAS)        
    
    return img