from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def seicaScrapper(webdriver_path='/usr/bin/chromedriver'):
    ''' webdriver_path default /usr/bin/chromedriver
        webdriver_path for windows 10 is (e.g.) executable_path=r'C:/chromedriver.exe' not implemented
    '''

    # descargando datos

    op = webdriver.ChromeOptions() 
        # opciones del webdriver
    op.add_argument('headless') 
        # para que no se abra el navegador en gui
    op.add_argument('--no-sandbox') 
        # para que corra con sudo
    browser = webdriver.Chrome(webdriver_path,options=op)
        # creando objeto browser
    browser.get("https://smaot.guanajuato.gob.mx/sitio/seica/monitoreo/leon")
        # cargando pagina seica

    # extrayendo datos

    ciudad_estaciones = browser.find_elements_by_class_name("ciudad_estaciones") 
    ''' ciudad_estaciones es un lista, en donde se 
        repite 4 veces la misma entrada, por eso 
        en tabla solo tomamos una de ellas '''

    tabla = ciudad_estaciones[0].find_elements_by_tag_name('td')    
    ''' Solo tomamos una entrada de la lista ciudad_estaciones.
        tabla tiene 6 elementos, son los nombres y colores de 
        las 3 estaciones en León '''
    
    calidades_dicc = {'buena'               : '#00e400', 
                      'aceptable'           : '#ffff00',
                      'mala'                : '#ff7e00',
                      'muy mala'            : '#ff0000',
                      'extremadamente mala' : '#8f3f97'}
        # diccionario calidad-color, se usa más adelante

    calidades_lista = ['buena','aceptable','mala','muy mala','extremadamente mala']
        # también se usa más adelante

    datos_estaciones = []
        # lista donde se almacenarán los datos

    for i in range(0,6,2): # i de 0 a 6 de 2 en 2: 0,2,4                 
        estacion_nombre = tabla[i].get_attribute('innerHTML') 
        ''' los nombres de estaciones son los elementos 
            con indices 0,2,4 en tabla '''

        estacion_color = tabla[i+1].find_element_by_class_name("est_inf").get_attribute('style') 
        ''' los colores de cada estacion son los 
            elementos con indices 1,3,5 en la tabla'''   
        
        estacion_color = str(estacion_color)[22:-2] 
        ''' filtrando el dato rgb de estacion_color'''      

        estacion_color = estacion_color.split(',')       
        estacion_color = list(map(int,estacion_color))
            # casteando rgb string a lista
        
        r,g,b = estacion_color[0],estacion_color[1],estacion_color[2] 
        color_hex = '#%02x%02x%02x' % (r, g, b)
            #casteando rgb a hex

        for calidad in calidades_lista:
            # eligiendo calidad
            if color_hex == calidades_dicc[calidad]:
                estacion_calidad = calidad
              
        datos_estaciones.append([estacion_nombre,estacion_color,estacion_calidad])
            # generando lista de datos de cada estacion

    browser.quit()

    return datos_estaciones